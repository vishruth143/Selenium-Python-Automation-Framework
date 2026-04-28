"""
Locator Auto-Healer — Step 4

For each failure in failures.json:
  1. Find the page-object file + variable name owning the broken locator.
  2. Build a prompt with the page source and the failure context.
  3. Call the Claude CLI (`claude -p --bare --output-format json`) and capture
     the suggestion. The prompt is piped via STDIN so we don't hit Windows'
     command-line length limit.
  4. Write all suggestions to suggestions.json for the patcher (Step 5).
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

from scripts.healer.config import (
    FAILURES_JSON,
    HEALER_OUTPUT_DIR,
    PROMPT_FILE,
    REPO_ROOT,
    SUGGESTIONS_JSON,
    UI_TESTS_DIR,
)

# Map the framework's lowercase log strings to the By.* constants used in code.
BY_LOG_TO_CONST = {
    "id": "By.ID",
    "name": "By.NAME",
    "xpath": "By.XPATH",
    "css selector": "By.CSS_SELECTOR",
    "class name": "By.CLASS_NAME",
    "link text": "By.LINK_TEXT",
    "partial link text": "By.PARTIAL_LINK_TEXT",
    "tag name": "By.TAG_NAME",
}


@dataclass
class LocatorMatch:
    """Where in the codebase a broken locator lives."""
    file_path: Path
    var_name: str
    line_no: int
    original_line: str


@dataclass
class Suggestion:
    """A Claude-suggested replacement for a broken locator tuple."""
    file_path: str
    var_name: str
    line_no: int
    original_line: str
    old_by: str
    old_selector: str
    new_by: str
    new_selector: str
    confidence: str
    reason: str


# --------------------------------------------------------------------------- #
# 1. Locate the broken tuple in tests/ui/**/pages/*.py
# --------------------------------------------------------------------------- #
def find_locator_in_page_objects(by_const: str, selector: str) -> Optional[LocatorMatch]:
    """Return the first page-object line that defines (by_const, selector)."""
    pattern = re.compile(
        r"^\s*(?P<var>_[A-Za-z0-9_]+)\s*=\s*\(\s*"
        + re.escape(by_const)
        + r"\s*,\s*[\"']"
        + re.escape(selector)
        + r"[\"']\s*\)"
    )

    for py_file in UI_TESTS_DIR.rglob("pages/*.py"):
        try:
            lines = py_file.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, start=1):
            m = pattern.match(line)
            if m:
                return LocatorMatch(
                    file_path=py_file,
                    var_name=m["var"],
                    line_no=i,
                    original_line=line,
                )
    return None


# --------------------------------------------------------------------------- #
# 2. Build the prompt
# --------------------------------------------------------------------------- #
def build_prompt(match: LocatorMatch, by_const: str, selector: str, log_excerpt: str) -> str:
    """Render the prompt template with all runtime context."""
    template = PROMPT_FILE.read_text(encoding="utf-8")
    page_source = match.file_path.read_text(encoding="utf-8")
    return template.format(
        file_path=match.file_path.as_posix(),
        var_name=match.var_name,
        by_const=by_const,
        selector=selector,
        page_source=page_source,
        log_excerpt=log_excerpt,
    )


# --------------------------------------------------------------------------- #
# 3. Call Claude CLI
# --------------------------------------------------------------------------- #
def _resolve_claude_executable() -> str:
    """Find the claude CLI on PATH (Windows uses claude.cmd)."""
    exe = shutil.which("claude") or shutil.which("claude.cmd")
    if not exe:
        raise RuntimeError(
            "claude CLI not found on PATH. Install with `npm i -g @anthropic-ai/claude-code` "
            "and run `claude login`."
        )
    return exe


def call_claude(prompt: str) -> str:
    """
    Run Claude in print mode and return raw stdout.

    Flags:
      --bare              skip CLAUDE.md auto-discovery, hooks and plugin sync
                          so project context cannot bias the model into prose.
      --output-format json wrap the assistant reply in a stable envelope.

    The prompt is fed via STDIN (not as an argv string) for two reasons:
      * Windows' command-line length limit (~32 KB).
      * Avoids quoting hell with embedded quotes in page-object source.
    """
    exe = _resolve_claude_executable()
    cmd = [exe, "-p", "--bare", "--output-format", "json"]
    result = subprocess.run(
        cmd,
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=180,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"claude CLI failed (exit {result.returncode})\nSTDERR:\n{result.stderr}"
        )
    return result.stdout.strip()


def _extract_first_json_object(text: str) -> str:
    """Return the first balanced {...} block in `text`, ignoring braces in strings."""
    depth = 0
    start = -1
    in_str = False
    str_ch = ""
    escape = False
    for i, ch in enumerate(text):
        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == str_ch:
                in_str = False
            continue
        if ch in ('"', "'"):
            in_str = True
            str_ch = ch
            continue
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start != -1:
                return text[start : i + 1]
    raise ValueError("No balanced JSON object found")


def parse_claude_response(text: str) -> dict:
    """
    With --output-format json, stdout looks like:
        {"type":"result","subtype":"success","result":"<assistant text>", ...}
    Extract `result`, then pull the first balanced JSON object out of it.
    """
    inner = text
    try:
        envelope = json.loads(text)
        if isinstance(envelope, dict) and "result" in envelope:
            inner = envelope["result"]
    except json.JSONDecodeError:
        pass  # CLI version may not wrap; fall through with raw text

    try:
        json_blob = _extract_first_json_object(inner)
    except ValueError as exc:
        raise ValueError(f"No JSON object found in Claude response:\n{inner}") from exc
    return json.loads(json_blob)


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #
def heal_all() -> List[Suggestion]:
    """Iterate over failures.json and produce a Suggestion for each healable one."""
    failures = json.loads(FAILURES_JSON.read_text(encoding="utf-8"))
    suggestions: List[Suggestion] = []

    for failure in failures:
        by_log = failure["by"].lower()
        by_const = BY_LOG_TO_CONST.get(by_log)
        if not by_const:
            print(f"  ! Unknown By strategy in log: {failure['by']!r} - skipping")
            continue

        match = find_locator_in_page_objects(by_const, failure["selector"])
        if not match:
            print(
                f"  ! Could not locate ({by_const}, {failure['selector']!r}) "
                f"in any page object - skipping"
            )
            continue

        rel = match.file_path.relative_to(REPO_ROOT)
        print(f"  -> {rel} :{match.line_no} {match.var_name}")

        prompt = build_prompt(match, by_const, failure["selector"], failure["raw_line"])
        try:
            raw = call_claude(prompt)
            parsed = parse_claude_response(raw)
        except (RuntimeError, ValueError, json.JSONDecodeError) as exc:
            print(f"    ! Claude call failed: {exc}")
            continue

        suggestions.append(
            Suggestion(
                file_path=match.file_path.as_posix(),
                var_name=match.var_name,
                line_no=match.line_no,
                original_line=match.original_line,
                old_by=by_const,
                old_selector=failure["selector"],
                new_by=parsed["by"],
                new_selector=parsed["selector"],
                confidence=parsed.get("confidence", "unknown"),
                reason=parsed.get("reason", ""),
            )
        )
        print(
            f"    + suggested: ({parsed['by']}, {parsed['selector']!r})  "
            f"[{parsed.get('confidence')}]"
        )

    return suggestions


def write_suggestions(items: List[Suggestion]) -> None:
    """Persist suggestions for the patcher (Step 5) to consume."""
    HEALER_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SUGGESTIONS_JSON.write_text(
        json.dumps([asdict(s) for s in items], indent=2),
        encoding="utf-8",
    )


def main() -> None:
    """CLI entry point."""
    if not FAILURES_JSON.exists():
        raise SystemExit(f"Run parse_failures first - missing {FAILURES_JSON}")
    print(f"Healing {FAILURES_JSON} ...")
    items = heal_all()
    write_suggestions(items)
    print(f"\nWrote {len(items)} suggestion(s) -> {SUGGESTIONS_JSON}")


if __name__ == "__main__":
    main()

