# pylint: disable=[line-too-long, missing-module-docstring, useless-object-inheritance, too-many-instance-attributes]
# pylint: disable=[too-many-arguments, self-assigning-variable, too-few-public-methods, import-error]
# pylint: disable=[too-many-positional-arguments, broad-exception-caught, import-outside-toplevel]
import datetime
import logging
import logging.handlers
import os
import sys
import threading
from datetime import timezone
import colorlog
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_PATH = os.path.join(ROOT_PATH, "output", "logs")
sys.path.append(LOG_PATH)
# ---------------------------------------------------------------------------
# Thread-local context storage
# ---------------------------------------------------------------------------
# pytest-xdist spawns one *process* per worker (not just threads), so
# threading.local() gives each parallel process its own independent copy of
# worker_id / test_name - no cross-process bleed.
# ---------------------------------------------------------------------------
_local = threading.local()
_handler_lock = threading.Lock()
# One file-handler per process (keyed by worker-id so the cache key is stable)
_file_handlers: dict = {}
class _ContextFilter(logging.Filter):
    """Injects worker_id and test_name into every LogRecord from thread-local."""
    def filter(self, record: logging.LogRecord) -> bool:
        record.worker_id = getattr(_local, "worker_id", "main")
        record.test_name = getattr(_local, "test_name", "-")
        return True
def set_log_context(worker_id: str = "main", test_name: str = "-") -> None:
    """
    Stamp the current process/thread with worker_id + test_name.
    Call this at fixture setup time before each test.
    """
    _local.worker_id = worker_id
    _local.test_name = test_name
def clear_log_context() -> None:
    """Reset context after a test (fixture teardown)."""
    _local.worker_id = "main"
    _local.test_name = "-"
# ---------------------------------------------------------------------------
# Log format
# ---------------------------------------------------------------------------
_FMT = (
    "%(asctime)s  [%(worker_id)-6s]  [%(test_name)s]"
    "  %(levelname)-8s  %(name)s:%(funcName)s:%(lineno)d  %(message)s"
)
_DATE_FMT = "%Y-%m-%d %H:%M:%S"
def _get_file_handler(worker_id):
    """
    Return (and cache) a RotatingFileHandler that writes to a worker-specific
    log file: output/logs/test_execution_<worker_id>.log
    Using one file per worker process eliminates all cross-process write
    contention / garbled lines when running pytest -n <N>. The files are
    merged in chronological order at session end by merge_worker_logs()
    which is called from tests/conftest.py.
    The file handler is set to INFO so verbose Selenium event-listener
    DEBUG output (before_find / after_find / before_click / ...) does not
    pollute test_execution.log. Developers who want to see those events
    can run with --log-cli-level=DEBUG to view them on the console.
    """
    with _handler_lock:
        if worker_id not in _file_handlers:
            os.makedirs(LOG_PATH, exist_ok=True)
            log_file = os.path.join(LOG_PATH, f"test_execution_{worker_id}.log")
            formatter = logging.Formatter(fmt=_FMT, datefmt=_DATE_FMT)
            handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,
                backupCount=5,
                delay=False,
                encoding="utf-8",
            )
            handler.setLevel(logging.INFO)
            handler.setFormatter(formatter)
            handler.addFilter(_ContextFilter())
            _file_handlers[worker_id] = handler
        return _file_handlers[worker_id]
def merge_worker_logs():
    """
    Merge all per-worker log files (test_execution_gw*.log /
    test_execution_main.log) into a single test_execution.log, ordered by
    worker (main first, then gw0, gw1, gw2, ...). Within each worker block
    the original file order (= chronological) is preserved.
    Called once at the end of the test session from tests/conftest.py.
    """
    import glob
    pattern = os.path.join(LOG_PATH, "test_execution_*.log")
    # Sort: "main" first, then gw0, gw1, gw2 numerically
    def _worker_sort_key(path):
        name = os.path.splitext(os.path.basename(path))[0].replace("test_execution_", "")
        if name == "main":
            return (0, 0)
        # "gw3" -> (1, 3)
        num = int(name[2:]) if name.startswith("gw") and name[2:].isdigit() else 999
        return (1, num)
    worker_files = sorted(glob.glob(pattern), key=_worker_sort_key)
    if not worker_files:
        return
    all_lines = []
    for wf in worker_files:
        try:
            with open(wf, encoding="utf-8") as fh:
                lines = fh.readlines()
            if lines:
                # Derive a display label from the filename, e.g. "gw0" / "main"
                worker_label = os.path.splitext(os.path.basename(wf))[0]
                worker_label = worker_label.replace("test_execution_", "")
                separator = f"\n{'=' * 80}\n  Worker: {worker_label}\n{'=' * 80}\n"
                all_lines.append(separator)
                all_lines.extend(lines)
        except Exception:
            pass
    merged_path = os.path.join(LOG_PATH, "test_execution.log")
    with open(merged_path, "w", encoding="utf-8") as out:
        for line in all_lines:
            out.write(line)
    # Remove the worker shards after a successful merge
    for wf in worker_files:
        try:
            os.remove(wf)
        except Exception:
            pass
class Logger(object):
    """
    Parallel-safe logger for pytest-xdist runs.
    Each xdist worker process writes to its own shard file
    (output/logs/test_execution_gw0.log, ..._gw1.log, ..._main.log).
    At session end the shards are merged into
    output/logs/test_execution.log.
    Logger level hierarchy:
      - logger        : DEBUG (lets every record through)
      - file handler  : INFO  (test_execution.log stays clean)
      - console       : INFO  (stdout shows STEP messages, not event noise)
    DEBUG records (e.g. Selenium EventListener traces) are still emitted
    by the logger but are filtered out by both handlers' levels - they
    can be revealed with --log-cli-level=DEBUG.
    Typical usage - via the `log` fixture (preferred):
        def test_foo(log):
            log.info("tagged with [gw0] [test_foo]")
    Module-level usage (still works; context shown as [main] [-] until
    set_log_context() is called by the fixture):
        log = Logger(file_id=__name__)
    """
    def __init__(self, file_id=None, date_tag=None, **_ignored):
        if date_tag is None:
            date_tag = datetime.datetime.now(tz=timezone.utc).strftime("%Y-%m-%d-%H-%M")
        logger_name = file_id or __name__
        logger = logging.getLogger(logger_name)
        # Only attach handlers once per logger name per process
        if not logger.handlers:
            # Determine which worker shard file to write to
            worker_id = os.environ.get("PYTEST_XDIST_WORKER", "main")
            logger.addHandler(_get_file_handler(worker_id))
            # Coloured console handler - INFO so STEP messages are visible
            # but Selenium EventListener DEBUG noise stays out of stdout.
            console_handler = colorlog.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(colorlog.ColoredFormatter(
                fmt="%(log_color)s" + _FMT,
                datefmt=_DATE_FMT,
            ))
            console_handler.addFilter(_ContextFilter())
            logger.addHandler(console_handler)
            logger.setLevel(logging.DEBUG)
            logger.propagate = False
        self.logger = logger
        self.date_tag = date_tag
        self.file_id = file_id
        self.info = logger.info
        self.error = logger.error
        self.debug = logger.debug
        self.warning = logger.warning
        self.exception = logger.exception
