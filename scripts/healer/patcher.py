"""
Locator Auto-Healer — Step 5

Read suggestions.json and rewrite each broken locator tuple in its page-object
file in place. Produces patch_report.json for the PR-creation step (Step 6).
"""
from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

from scripts.healer.config import (
    HEALER_OUTPUT_DIR,
    REPO_ROOT,
    SUGGESTIONS_JSON,
    UI_TESTS_DIR,
)

PATCH_REPORT_JSON = HEALER_OUTPUT_DIR / "patch_report.json"

# Confidence levels we accept by default. Anything else is skipped unless
# --include-low is passed.
DEFAULT_ACCEPTED_CONFIDENCE = {"high", "medium"}

# Regex used to locate the *exact* tuple inside the original line so we can
# rebuild it preserving leading whitespace and trailing comments.
_TUPLE_RE = re.compile(
    r"""
    ^(?P<indent>\s*)
    (?P<var>_[A-Za-z0-9_]+)
    \s*=\s*
    \(\s*By\.[A-Z_]+\s*,\s*[\"'].*?[\"']\s*\)
    (?P<trailing>.*)$
    """,
    re.VERBOSE,
)


@dataclass
class PatchResult:
    """One row of the patch_report.json file."""
    file_path: str            # absolute, posix-style
    relative_path: str        # repo-relative, posix-style
    app: str                  # tests/ui/<app>/...
    var_name: str
    line_no: int
    old_line: str
    new_line: str
    confidence: str
    reason: str
    status: str               # "patched" | "skipped" | "drift" | "no-match"


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _infer_app(path: Path) -> str:
    """tests/ui/<app>/pages/foo.py -> '<app>'. Falls back to '' if not found."""
    try:
        rel = path.relative_to(UI_TESTS_DIR)
    except ValueError:
        return ""
    return rel.parts[0] if rel.parts else ""


def _build_new_line(old_line: str, new_by: str, new_selector: str) -> str | None:
    """
    Rebuild the tuple line, preserving indentation and any trailing comment.
    Returns None if the line shape is unexpected.
    """
    m = _TUPLE_RE.match(old_line)
    if not m:
        return None
    # Use double quotes; escape any embedded double quotes in the selector.
    safe_sel = new_selector.replace("\\", "\\\\").replace('"', '\\"')
    return f'{m["indent"]}{m["var"]} = ({new_by}, "{safe_sel}"){m["trailing"]}'


def _atomic_write(path: Path, content: str) -> None:
    """Write to <path>.tmp then os.replace - crash-safe."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8", newline="\n")
    os.replace(tmp, path)


# --------------------------------------------------------------------------- #
# Core
# --------------------------------------------------------------------------- #
def apply_suggestions(include_low: bool = False, dry_run: bool = False) -> List[PatchResult]:
    """Apply every suggestion in suggestions.json and return per-suggestion results."""
    if not SUGGESTIONS_JSON.exists():
        raise SystemExit(f"Run heal first - missing {SUGGESTIONS_JSON}")

    suggestions = json.loads(SUGGESTIONS_JSON.read_text(encoding="utf-8"))
    accepted = DEFAULT_ACCEPTED_CONFIDENCE | ({"low"} if include_low else set())

    results: List[PatchResult] = []
    # Group by file so we read/write each file at most once
    by_file: dict[Path, list[dict]] = {}
    for s in suggestions:
        by_file.setdefault(Path(s["file_path"]), []).append(s)

    for file_path, items in by_file.items():
        try:
            lines = file_path.read_text(encoding="utf-8").splitlines(keepends=False)
        except OSError as exc:
            print(f"  ! Cannot read {file_path}: {exc}")
            continue

        modified = False
        for s in items:
            res = _apply_one(file_path, lines, s, accepted)
            results.append(res)
            if res.status == "patched":
                modified = True

        if modified and not dry_run:
            _atomic_write(file_path, "\n".join(lines) + "\n")

    return results


def _apply_one(
    file_path: Path,
    lines: list[str],
    suggestion: dict,
    accepted_confidence: set[str],
) -> PatchResult:
    """Patch a single suggestion against the in-memory `lines` buffer."""
    rel = file_path.relative_to(REPO_ROOT).as_posix()
    base = PatchResult(
        file_path=file_path.as_posix(),
        relative_path=rel,
        app=_infer_app(file_path),
        var_name=suggestion["var_name"],
        line_no=suggestion["line_no"],
        old_line=suggestion["original_line"],
        new_line="",
        confidence=suggestion.get("confidence", "unknown"),
        reason=suggestion.get("reason", ""),
        status="skipped",
    )

    if base.confidence not in accepted_confidence:
        print(f"  - {rel}:{base.line_no} {base.var_name}  skipped (confidence={base.confidence})")
        return base

    # 1-based line_no -> 0-based index
    idx = suggestion["line_no"] - 1
    if not 0 <= idx < len(lines):
        base.status = "no-match"
        print(f"  ! {rel}:{base.line_no} line out of range")
        return base

    current = lines[idx]
    if current.rstrip() != suggestion["original_line"].rstrip():
        base.status = "drift"
        print(f"  ! {rel}:{base.line_no} drift - file changed since heal; skipping")
        return base

    new_line = _build_new_line(current, suggestion["new_by"], suggestion["new_selector"])
    if new_line is None:
        base.status = "no-match"
        print(f"  ! {rel}:{base.line_no} unexpected line shape; skipping")
        return base

    if new_line == current:
        base.status = "skipped"
        base.new_line = new_line
        print(f"  = {rel}:{base.line_no} {base.var_name}  already correct")
        return base

    lines[idx] = new_line
    base.new_line = new_line
    base.status = "patched"
    print(f"  + {rel}:{base.line_no} {base.var_name}")
    print(f"      - {current.strip()}")
    print(f"      + {new_line.strip()}")
    return base


def write_report(results: List[PatchResult]) -> None:
    """Persist patch_report.json for Step 6 (open_pr)."""
    HEALER_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PATCH_REPORT_JSON.write_text(
        json.dumps([asdict(r) for r in results], indent=2),
        encoding="utf-8",
    )


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Apply Claude locator suggestions in place.")
    parser.add_argument(
        "--include-low",
        action="store_true",
        help="Also apply suggestions with confidence=low (default: skip).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would change but do not write files.",
    )
    args = parser.parse_args()

    print(f"Patching from {SUGGESTIONS_JSON} (dry_run={args.dry_run})...")
    results = apply_suggestions(include_low=args.include_low, dry_run=args.dry_run)
    write_report(results)

    patched = sum(1 for r in results if r.status == "patched")
    print(
        f"\nDone. {patched} patched / {len(results)} total "
        f"-> report: {PATCH_REPORT_JSON}"
    )


if __name__ == "__main__":
    main()