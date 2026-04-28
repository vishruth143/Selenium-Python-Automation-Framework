"""
Parse output/logs/test_execution.log and extract UI locator failures.

Detection rule
--------------
The framework's BasePage raises:
    Exception(f"Element not found: ({by}, {locator}) | Exception: {str(e)}")
which appears in the log as:
    ... ERROR ... Error: Element not found: (id, username1) | Exception: ...

We rely on that canonical string instead of trying to parse Selenium stack
traces, which are noisy and driver-version dependent.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from typing import List

from scripts.healer.config import LOG_FILE, FAILURES_JSON, HEALER_OUTPUT_DIR

# --- Regexes ---------------------------------------------------------------

# Example matched line:
# 2026-04-28 14:09:05  [main  ]  [test_pta_login]  ERROR  test_pta_clean_version:test_pta_login:80  Error: Element not found: (id, username1) | Exception: Message:
_LINE_RE = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})"   # timestamp
    r".*?\[(?P<test_name>[^\]]+)\]"                            # [test_xxx]
    r"\s+ERROR\s+"
    r"(?P<module>[\w_]+):(?P<function>[\w_]+):(?P<line>\d+)"   # module:func:line
    r"\s+Error:\s+Element not found:\s+"
    r"\((?P<by>[^,]+),\s*(?P<selector>.+?)\)"                  # (by, selector)
    r"\s*\|\s*Exception:"
)


@dataclass
class LocatorFailure:
    timestamp: str
    test_name: str
    module: str
    function: str
    line: int
    by: str          # e.g. "id", "xpath", "css selector"
    selector: str    # e.g. "username1"
    raw_line: str


def parse_log(log_path=LOG_FILE) -> List[LocatorFailure]:
    """Read the log file and return one LocatorFailure per matching ERROR line."""
    if not log_path.exists():
        raise FileNotFoundError(f"Log file not found: {log_path}")

    failures: List[LocatorFailure] = []
    with log_path.open(encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            m = _LINE_RE.search(raw)
            if not m:
                continue
            failures.append(
                LocatorFailure(
                    timestamp=m["timestamp"],
                    test_name=m["test_name"].strip(),
                    module=m["module"],
                    function=m["function"],
                    line=int(m["line"]),
                    by=m["by"].strip().lower(),
                    selector=m["selector"].strip().strip('"').strip("'"),
                    raw_line=raw.strip(),
                )
            )
    return _dedupe(failures)


def _dedupe(items: List[LocatorFailure]) -> List[LocatorFailure]:
    """Same (by, selector) reported multiple times → keep only the first."""
    seen = set()
    unique = []
    for f in items:
        key = (f.by, f.selector)
        if key in seen:
            continue
        seen.add(key)
        unique.append(f)
    return unique


def write_failures_json(failures: List[LocatorFailure], out_path=FAILURES_JSON) -> None:
    HEALER_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = [asdict(f) for f in failures]
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    failures = parse_log()
    write_failures_json(failures)
    print(f"Parsed {len(failures)} unique locator failure(s) → {FAILURES_JSON}")
    for f in failures:
        print(f"  - {f.test_name}: ({f.by}, {f.selector})")


if __name__ == "__main__":
    main()