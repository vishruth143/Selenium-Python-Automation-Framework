# pylint: disable=[unused-argument, missing-module-docstring, missing-module-docstring, unspecified-encoding]
# pylint: disable=[missing-function-docstring, line-too-long, import-outside-toplevel, deprecated-argument]
# pylint: disable=[broad-exception-caught, unused-variable]

import os
import shutil
import stat
import logging
import json
import platform

import pytest

from framework.utilities.custom_logger import (
    Logger,
    merge_worker_logs,
    set_log_context,
    clear_log_context,
)


def _on_rm_error(func, path, exc_info):
    # Try to remove read-only or locked files
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        print(f"Could not delete locked file: {path}")

def _release_log_handlers():
    """
    Close and remove every file handler attached to every active logger.
    This releases the OS-level lock on test_execution.log (and any other
    log files) so that shutil.rmtree can delete the output folder cleanly.
    The handlers are opened fresh once the output directories are recreated.
    """
    for name, logger in list(logging.Logger.manager.loggerDict.items()):
        if isinstance(logger, logging.Logger):
            for handler in list(logger.handlers):
                try:
                    handler.flush()
                    handler.close()
                except Exception:
                    pass
                logger.removeHandler(handler)

# Clean up output folder before any tests run
def pytest_sessionstart(session):
    # When running under pytest-xdist, this hook fires once per worker
    # process as well as on the master/controller. Only the master should
    # clean and recreate the output/ directory - otherwise workers will
    # delete files (logs, screenshots, videos) being written by sibling
    # workers, which is another major source of "jumbled" / lost output.
    if os.environ.get("PYTEST_XDIST_WORKER"):
        return

    # Release all open log file handles BEFORE attempting to delete the folder.
    # Logger instances created at module level (e.g. in test files) open
    # test_execution.log immediately on import, which locks the file on Windows.
    # Closing every handler here lets shutil.rmtree proceed without errors.
    _release_log_handlers()

    output_dir = os.path.join(os.getcwd(), 'output')
    if os.path.exists(output_dir):
        try:
            shutil.rmtree(output_dir, onerror=_on_rm_error)
            print(f"Cleaned up output directory: {output_dir}")
        except Exception as e:
            print(f"Failed to clean output directory {output_dir}: {e}")
    else:
        print(f"Output directory does not exist, no cleanup needed: {output_dir}")

    # Create all required output subdirectories
    os.makedirs(os.path.join(output_dir, 'allure-results'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'logs'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'reports'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'screenshots'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'videos'), exist_ok=True)

    env_file_path = os.path.join(output_dir, 'allure-results', 'environment.properties')
    with open(env_file_path, 'w') as f:
        f.write(f"REGION={os.getenv('REGION', 'QA')}")
        f.write(f"\nBROWSER={os.getenv('BROWSER', 'CHROME')}")
        f.write(f"\nHEADLESS={os.getenv('HEADLESS', 'N')}")

    # Copy categories.json into allure-results so the Allure "Categories" tab
    # groups failures into meaningful buckets (Product Defects, Test Defects, etc.)
    categories_src = os.path.join(os.getcwd(), 'config', 'categories.json')
    categories_dst = os.path.join(output_dir, 'allure-results', 'categories.json')
    if os.path.exists(categories_src):
        shutil.copy2(categories_src, categories_dst)
        print(f"Copied categories.json to: {categories_dst}")

    # Generate executor.json so the Allure "Executors" widget shows
    # who/what ran the tests (CI server or local machine).
    executor_data = _build_executor_info()
    executor_path = os.path.join(output_dir, 'allure-results', 'executor.json')
    with open(executor_path, 'w') as f:
        json.dump(executor_data, f, indent=2)
    print(f"Generated executor.json: {executor_data.get('name')}")

    # Initialise the framework Logger on the main / controller process so
    # the main shard file (test_execution_main.log) is created and a session
    # header row is written. The shard files for every worker (and main)
    # are merged into a single test_execution.log in pytest_sessionfinish.
    main_log = Logger(file_id="session").logger
    set_log_context(worker_id="main", test_name="session")
    main_log.info("=" * 80)
    main_log.info("Pytest session started - executor=%s, region=%s, browser=%s, headless=%s",
                  executor_data.get("name"),
                  os.getenv("REGION", "QA"),
                  os.getenv("BROWSER", "CHROME"),
                  os.getenv("HEADLESS", "N"))
    main_log.info("=" * 80)
    clear_log_context()


def pytest_sessionfinish(session, exitstatus):
    """
    Merge per-worker log shards into a single test_execution.log.

    pytest-xdist workers each write to their own shard file
    (test_execution_gw0.log, test_execution_gw1.log, ...) to avoid
    cross-process write contention. This hook runs on the *controller*
    process after all workers have finished, so all shards are fully
    flushed and safe to read and merge.
    """
    # Only the controller process (no PYTEST_XDIST_WORKER env var) merges.
    if os.environ.get("PYTEST_XDIST_WORKER"):
        return
    # Release file handles so Windows lets us read & delete the shard files.
    _release_log_handlers()
    try:
        merge_worker_logs()
        print("Merged worker log shards into test_execution.log")
    except Exception as e:
        print(f"Warning: could not merge worker logs: {e}")


# ---------------------------------------------------------------------------
# Global fixtures - available to UI, API, mobile and data tests alike.
# ---------------------------------------------------------------------------
@pytest.fixture()
def log(request):
    """
    Return a Logger pre-stamped with worker-id and test-name.

    Usage:
        def test_foo(log):
            log.info("hello")  # -> [gw0]  [test_foo]  INFO  ...
    """
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "main")
    test_name = request.node.name
    set_log_context(worker_id=worker_id, test_name=test_name)
    logger = Logger(file_id=request.node.module.__name__.rsplit(".", 1)[-1])
    yield logger
    clear_log_context()


@pytest.fixture(autouse=True)
def _stamp_log_context(request):
    """
    Autouse fixture - stamps thread-local log context for EVERY test so that
    module-level Logger instances (the existing pattern in this framework)
    pick up the running test's worker_id + test_name without needing to
    explicitly request the `log` fixture.

    Also writes a clear START / END banner around each test so that when
    several tests run sequentially on the same xdist worker (e.g. 4 tests
    on `-n 2`), each test's log lines are visually separated inside the
    worker's shard file.
    """
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "main")
    test_name = request.node.name
    set_log_context(worker_id=worker_id, test_name=test_name)

    banner_logger = Logger(file_id="test.lifecycle")
    banner_logger.info("-" * 80)
    banner_logger.info("TEST START: %s", test_name)
    banner_logger.info("-" * 80)

    yield

    banner_logger.info("-" * 80)
    banner_logger.info("TEST END:   %s", test_name)
    banner_logger.info("-" * 80)
    clear_log_context()


def _build_executor_info():
    """
    Return an executor dict for Allure.
    Detects GitHub Actions, Jenkins, or falls back to local machine info.
    """
    # --- GitHub Actions ---
    if os.getenv('GITHUB_ACTIONS') == 'true':
        server_url = os.getenv('GITHUB_SERVER_URL', 'https://github.com')
        repo = os.getenv('GITHUB_REPOSITORY', '')
        run_id = os.getenv('GITHUB_RUN_ID', '')
        run_number = os.getenv('GITHUB_RUN_NUMBER', '0')
        build_url = f"{server_url}/{repo}/actions/runs/{run_id}"
        return {
            "name": "GitHub Actions",
            "type": "github",
            "buildName": f"Run #{run_number}",
            "buildUrl": build_url,
            "buildOrder": int(run_number),
            "reportUrl": build_url,
        }

    # --- Jenkins ---
    if os.getenv('JENKINS_URL'):
        return {
            "name": "Jenkins",
            "type": "jenkins",
            "buildName": os.getenv('BUILD_DISPLAY_NAME', os.getenv('BUILD_NUMBER', 'N/A')),
            "buildUrl": os.getenv('BUILD_URL', ''),
            "buildOrder": int(os.getenv('BUILD_NUMBER', '0')),
            "reportUrl": os.getenv('BUILD_URL', ''),
        }

    # --- Local machine ---
    return {
        "name": f"Local ({platform.node()})",
        "type": "local",
        "buildName": f"{platform.system()} {platform.release()}",
    }
