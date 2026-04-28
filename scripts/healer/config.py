"""Central configuration for the Locator Auto-Healer agent."""
from pathlib import Path

# Repo root = two levels up from this file (scripts/healer/config.py)
REPO_ROOT = Path(__file__).resolve().parents[2]

# Inputs
LOG_FILE = REPO_ROOT / "output" / "logs" / "test_execution.log"

# Where page objects live (per-app, as per CLAUDE.md architecture)
UI_TESTS_DIR = REPO_ROOT / "tests" / "ui"

# Where the healer writes its own artifacts
HEALER_OUTPUT_DIR = REPO_ROOT / "output" / "healer"
FAILURES_JSON = HEALER_OUTPUT_DIR / "failures.json"
SUGGESTIONS_JSON = HEALER_OUTPUT_DIR / "suggestions.json"

# Prompt template
PROMPT_FILE = Path(__file__).parent / "prompts" / "heal_locator.md"

# Git / PR settings
BRANCH_PREFIX = "fix/heal-locators"

# Conventional-commit templates. `{scope}` is filled in at runtime
# from the apps whose page objects were patched.
COMMIT_MESSAGE_TEMPLATE = "fix({scope}): auto-heal broken UI locators"
PR_TITLE_TEMPLATE = "fix({scope}): auto-heal broken UI locators"
PR_BODY = (
    "This PR was generated automatically by the Locator Auto-Healer agent.\n\n"
    "It updates page-object locators that failed during the most recent UI test run.\n"
    "Please review each change carefully before merging."
)

# Map folder name under tests/ui/ → conventional-commit scope.
# Folder name and scope happen to be identical for current apps,
# but we keep the mapping so future apps can rename freely.
APP_TO_SCOPE = {
    "heroku": "heroku",
    "pta": "pta",
}

# Used when more than one app is patched in the same run,
# or when no app can be inferred.
FALLBACK_SCOPE = "common"

# Selenium exception names we treat as "locator failures"
LOCATOR_EXCEPTIONS = (
    "NoSuchElementException",
    "TimeoutException",
    "ElementNotInteractableException",
    "StaleElementReferenceException",
)