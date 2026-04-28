"""
Locator Auto-Healer — orchestrator.

Runs the full pipeline:
    parse_failures -> heal -> patcher -> open_pr
Each step is independently scriptable; this just chains them.
"""
from __future__ import annotations

import argparse

from scripts.healer import heal, open_pr, parse_failures, patcher


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Run the full Locator Auto-Healer pipeline.")
    parser.add_argument("--dry-run", action="store_true", help="Patch + PR steps run in dry-run mode.")
    parser.add_argument("--include-low", action="store_true", help="Apply low-confidence suggestions too.")
    parser.add_argument("--allow-dirty", action="store_true", help="Allow unrelated unstaged changes.")
    parser.add_argument("--base", default="main", help="Base branch for the PR (default: main).")
    parser.add_argument("--no-pr", action="store_true", help="Stop after patching; do not open a PR.")
    args = parser.parse_args()

    print("=" * 72)
    print("[1/4] Parsing failures from log")
    print("=" * 72)
    parse_failures.main()

    print("\n" + "=" * 72)
    print("[2/4] Asking Claude for fixes")
    print("=" * 72)
    heal.main()

    print("\n" + "=" * 72)
    print("[3/4] Patching page objects")
    print("=" * 72)
    results = patcher.apply_suggestions(include_low=args.include_low, dry_run=args.dry_run)
    patcher.write_report(results)
    patched = sum(1 for r in results if r.status == "patched")
    print(f"\nPatched {patched} / {len(results)} suggestion(s).")

    if args.no_pr or patched == 0:
        print("\nSkipping PR step.")
        return

    print("\n" + "=" * 72)
    print("[4/4] Opening PR")
    print("=" * 72)
    open_pr.open_pr(dry_run=args.dry_run, allow_dirty=args.allow_dirty, base_branch=args.base)


if __name__ == "__main__":
    main()