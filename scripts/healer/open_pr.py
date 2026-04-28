"""
Locator Auto-Healer — Step 6

Read patch_report.json, create a branch, commit only the patched files, push,
and open a PR via the GitHub CLI.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import shutil
import subprocess
from pathlib import Path
from typing import List

from scripts.healer.config import (
    APP_TO_SCOPE,
    BRANCH_PREFIX,
    COMMIT_MESSAGE_TEMPLATE,
    FALLBACK_SCOPE,
    PR_BODY,
    PR_TITLE_TEMPLATE,
    REPO_ROOT,
)
from scripts.healer.patcher import PATCH_REPORT_JSON


# --------------------------------------------------------------------------- #
# Shell helpers
# --------------------------------------------------------------------------- #
def _run(cmd: list[str], dry_run: bool = False, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command from the repo root, streaming output."""
    printable = " ".join(cmd)
    print(f"  $ {printable}")
    if dry_run:
        return subprocess.CompletedProcess(cmd, 0, "", "")
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip())
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed (exit {result.returncode}): {printable}")
    return result


def _require_executable(name: str) -> str:
    exe = shutil.which(name) or shutil.which(f"{name}.cmd") or shutil.which(f"{name}.exe")
    if not exe:
        raise RuntimeError(f"{name!r} not found on PATH.")
    return exe


# --------------------------------------------------------------------------- #
# Report loading
# --------------------------------------------------------------------------- #
def _load_patched_rows() -> List[dict]:
    if not PATCH_REPORT_JSON.exists():
        raise SystemExit(f"Run patcher first - missing {PATCH_REPORT_JSON}")
    rows = json.loads(PATCH_REPORT_JSON.read_text(encoding="utf-8"))
    return [r for r in rows if r["status"] == "patched"]


def _derive_scope(rows: List[dict]) -> str:
    apps = {r["app"] for r in rows if r["app"]}
    scopes = {APP_TO_SCOPE.get(a, a) for a in apps}
    if len(scopes) == 1:
        return scopes.pop()
    return FALLBACK_SCOPE


def _patched_files(rows: List[dict]) -> List[str]:
    """Repo-relative posix paths of unique files to add."""
    seen: set[str] = set()
    out: list[str] = []
    for r in rows:
        if r["relative_path"] not in seen:
            seen.add(r["relative_path"])
            out.append(r["relative_path"])
    return out


def _build_pr_body(rows: List[dict]) -> str:
    lines = [PR_BODY, "", "### Changes", ""]
    for r in rows:
        lines.append(
            f"- `{r['relative_path']}` line {r['line_no']} "
            f"(`{r['var_name']}`, confidence: **{r['confidence']}**)"
        )
        lines.append(f"  - reason: {r['reason']}")
        lines.append(f"  - before: `{r['old_line'].strip()}`")
        lines.append(f"  - after:  `{r['new_line'].strip()}`")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Git workflow
# --------------------------------------------------------------------------- #
def _ensure_clean_working_tree(allow_dirty: bool, files_to_change: List[str]) -> None:
    """
    Refuse to run if there are unstaged changes outside the files we plan to commit,
    unless --allow-dirty is passed.
    """
    result = _run(["git", "status", "--porcelain"], check=True)
    dirty = [
        line[3:].strip()
        for line in result.stdout.splitlines()
        if line and line[3:].strip() not in files_to_change
    ]
    if dirty and not allow_dirty:
        joined = "\n   ".join(dirty)
        raise SystemExit(
            "Working tree has unrelated changes:\n   "
            f"{joined}\n"
            "Commit/stash them, or re-run with --allow-dirty."
        )


def _current_branch() -> str:
    return _run(["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()


def _new_branch_name() -> str:
    stamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{BRANCH_PREFIX}-{stamp}"


def open_pr(dry_run: bool = False, allow_dirty: bool = False, base_branch: str = "main") -> None:
    """End-to-end: branch -> add -> commit -> push -> gh pr create."""
    _require_executable("git")
    _require_executable("gh")

    rows = _load_patched_rows()
    if not rows:
        print("No patched files in report - nothing to commit.")
        return

    files = _patched_files(rows)
    scope = _derive_scope(rows)
    branch = _new_branch_name()
    commit_msg = COMMIT_MESSAGE_TEMPLATE.format(scope=scope)
    pr_title = PR_TITLE_TEMPLATE.format(scope=scope)
    pr_body = _build_pr_body(rows)

    print(f"Scope:   {scope}")
    print(f"Branch:  {branch}")
    print(f"Files:   {files}")
    print(f"Commit:  {commit_msg}")
    print()

    _ensure_clean_working_tree(allow_dirty, files)

    starting_branch = _current_branch()
    print(f"Starting from branch: {starting_branch}")

    _run(["git", "checkout", "-b", branch], dry_run=dry_run)
    _run(["git", "add", *files], dry_run=dry_run)
    _run(["git", "commit", "-m", commit_msg], dry_run=dry_run)
    _run(["git", "push", "-u", "origin", branch], dry_run=dry_run)

    # Pass body via a temp file so newlines survive Windows quoting.
    body_file = REPO_ROOT / "output" / "healer" / "pr_body.md"
    if not dry_run:
        body_file.write_text(pr_body, encoding="utf-8")

    _run(
        [
            "gh", "pr", "create",
            "--base", base_branch,
            "--head", branch,
            "--title", pr_title,
            "--body-file", str(body_file),
        ],
        dry_run=dry_run,
    )

    print(f"\nDone. Branch '{branch}' pushed and PR opened against '{base_branch}'.")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Open a PR with the auto-healed locator fixes.")
    parser.add_argument("--dry-run", action="store_true", help="Print git/gh commands without running.")
    parser.add_argument("--allow-dirty", action="store_true", help="Allow unrelated unstaged changes.")
    parser.add_argument("--base", default="main", help="Base branch for the PR (default: main).")
    args = parser.parse_args()

    open_pr(dry_run=args.dry_run, allow_dirty=args.allow_dirty, base_branch=args.base)


if __name__ == "__main__":
    main()