# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository. See also `AGENTS.md` and `README.md`.

## Commands

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Tests
The right app/service config is selected automatically by the per-app `conftest.py` for the path being collected, so `APP_NAME` / `SERVICE_NAME` / `MOBILE_APP_NAME` are no longer required. `REGION` defaults to `QA`, `BROWSER` defaults to `CHROME`, `HEADLESS` defaults to `N`.

```bash
# UI - Heroku
pytest -vvv -m "heroku" tests/

# UI - PTA
pytest -vvv -m "pta" tests/

# API - JSONPlaceholder
pytest -vvv -m "jsonplaceholder" tests/

# Mobile - KWA
pytest -vvv -m "kwa" tests/

# Data quality - REST Countries (raw `requests`, no WebDriver / BasePage)
pytest -vvv -m "restcountries_data" tests/data/

# Run a single test file
pytest -vvv tests/ui/heroku/test_heroku.py

# Run a single test by name
pytest -vvv tests/ui/heroku/test_heroku.py::TestHerokuApp::test_ab_test_page

# Parallel execution with retries and HTML report
BROWSER=CHROME pytest -vvv -m "pta" -n 4 --reruns 3 \
  --html=output/reports/report.html --self-contained-html \
  --alluredir=output/allure-results tests/
```

### Performance (Locust, not pytest)
JSONPlaceholder load test with 9 tasks:
```bash
locust -f tests/performance/locustfile.py --headless \
  --host=https://jsonplaceholder.typicode.com -u 10 -r 2 --run-time 60s
```

### Locator Auto-Healer
Parses `output/logs/test_execution.log`, asks Claude for fixes, patches page objects, and opens a PR. See `tutorial/locator_auto_healer.md`.
```bash
python -m scripts.healer.run_healer --dry-run
```

### Lint
Pylint must score **10.0/10** (enforced by CI):
```bash
pylint framework/ tests/ config/
```

### Docker
```bash
docker build -t selenium-python-automation .
docker run -e BROWSER=CHROME -e HEADLESS=Y selenium-python-automation pytest -m "pta" tests/
```

## Architecture

The framework uses a layered **Page Object Model (POM)** with **per-app config auto-discovery**. There is no central `if APP_NAME == ...` switch — each app/service folder under `tests/` owns a `conftest.py` that loads its own config via `config/config_parser.py`. Tests are routed entirely by **pytest markers**.

```
config/              ← YAML/JSON/Excel configs at config/<type>/<app>/, region-keyed
framework/
  interfaces/        ← APIClient (GET/POST/PUT/DELETE with OAuth2 support)
  listeners/         ← Selenium EventListener (EventFiringWebDriver) for nav/click/exception logging
  pages/ui/          ← BasePage with all shared WebDriver interactions
  utilities/         ← Logger, screenshots, screen recording (ffmpeg), Faker helpers, loaders
scripts/
  healer/            ← Locator Auto-Healer pipeline (parse_failures → heal → patcher → open_pr)
tests/
  conftest.py        ← Session-level: cleans output/, creates dirs, writes environment.properties, exposes `log` fixture
  ui/
    conftest.py      ← Function-level: WebDriver init/teardown, browser options, video recording, screenshot on failure
    <app>/
      pages/         ← App-specific page objects (inherit BasePage)
      test_<app>.py  ← Test classes (use page objects, fixtures)
      features/      ← (PTA only) pytest-bdd .feature files
      steps/         ← (PTA only) pytest-bdd step definitions
  api/
    conftest.py      ← Session-level: APIClient fixture with OAuth token
    <service>/
      test_<service>.py
  mobile/
    conftest.py      ← Autouse: Appium server, local/cloud device config
    <app>/
      test_<app>.py
  data/
    restcountries/   ← Raw `requests` data quality tests (no BasePage / WebDriver)
  performance/
    locustfile.py    ← Locust tasks (no marker, no BasePage)
  snippet/           ← Demos for excel / param / retry markers
output/              ← Auto-generated: logs/, reports/, screenshots/, videos/, allure-results/, healer/
```

### Configuration Loading

`config/config_parser.py` is the central config loader. It resolves YAML/JSON/Excel files under `config/<type>/<app>/` by name (e.g. `ui_test_data_config`, `ui_test_excel_data_config`). Each per-app `tests/.../<app>/conftest.py` declares its own `testdata` (and other) fixtures by calling `ConfigParser.load_config(...)` with the right config name — so `APP_NAME` / `SERVICE_NAME` / `MOBILE_APP_NAME` env vars are no longer needed. `REGION` is still read at the test level to pick the right region-keyed block (`DEV`, `QA`, `STAGE`, `PROD`).

### Fixture Chain

1. **Session** (`tests/conftest.py`): Cleans `output/`, creates dirs, writes Allure `environment.properties`, registers the autouse `_stamp_log_context` fixture and exposes the `log` fixture.
2. **Layer** (`tests/ui/conftest.py`, `tests/api/conftest.py`, `tests/mobile/conftest.py`): Cross-app concerns only — WebDriver / APIClient / Appium server lifecycle. UI layer also handles screenshot + ffmpeg video on failure (passing tests' videos are deleted).
3. **Per-app** (`tests/ui/<app>/conftest.py`, `tests/api/<service>/conftest.py`, `tests/mobile/<app>/conftest.py`): Declares the app-specific `testdata` (and `api_client` / `driver` for mobile) by loading the matching config file directly — no central if/elif on env vars.

### Page Object Pattern

Every page class inherits `framework/pages/ui/base_page.py` (`BasePage` owns ALL WebDriver primitives: waits, clicks, typing, scroll, URL checks, JS execution). Reference implementations: `tests/ui/heroku/pages/landing_page.py` and `tests/ui/pta/pages/login_page.py`.

- **Locators** — class-level tuples `USERNAME = (By.ID, "username")`
- **Properties** — lazy elements using `self.find_element(by, locator, condition)` with explicit waits
- **Action methods** — composite operations (e.g., `type_username`, `click_submit`) that call `BasePage` primitives — never raw `driver.find_element` in tests or pages

Selenium events are auto-logged via `framework/listeners/event_listeners.py` (EventFiringWebDriver).

### Logging & Artifacts

`framework/utilities/custom_logger.py` creates a rotating file logger (`output/logs/test_execution.log`, 10 MB × 5) with colored console output. Tests log steps as literal `STEP 01`, `STEP 02`, … for grep-ability. On UI failure, `screenshot_utils.py` + `screen_recording_utils.py` (ffmpeg) drop artifacts under `output/screenshots/` and `output/videos/`.

## Markers and Scopes

Pytest markers (declared in `pytest.ini`) map 1-to-1 to app/service names, plus cross-cutting markers used by `tests/snippet/` demos:

- App/service: `pta`, `heroku`, `kwa`, `jsonplaceholder`, `restcountries_data`
- Cross-cutting: `excel`, `param`, `retry`

Add new markers to `pytest.ini`.

## Project-Specific Rules

- **Do NOT** add `APP_NAME` / `SERVICE_NAME` / `MOBILE_APP_NAME` env-var branching — that pattern was removed; route via per-app `conftest.py` instead.
- **Do NOT** put WebDriver calls in tests — extend `BasePage` if a primitive is missing.
- New app? Create `tests/<layer>/<app>/{__init__.py, conftest.py, pages/, test_<app>.py}`, a matching `config/<layer>/<app>/` folder, and a marker in `pytest.ini`.
- Two PTA test variants exist intentionally: `test_pta_clean_version.py` (terse) and `test_pta_tutorial_version.py` (heavily commented for onboarding) — keep both in sync when changing flows.
- BDD lives at `tests/ui/pta/features/*.feature` with steps in `tests/ui/pta/steps/test_pta_app.py` (pytest-bdd).
- Performance tests are **Locust**, not pytest — `tests/performance/locustfile.py` (no marker, no `BasePage`).
- Data quality tests live at `tests/data/restcountries/` and use raw `requests` against the REST Countries API (no `BasePage`, no WebDriver) — marker `restcountries_data`.
- Locator Auto-Healer (`scripts/healer/`) consumes `output/logs/test_execution.log`, writes `output/healer/{failures,suggestions,patch_report}.json` + `pr_body.md`, then patches page objects and opens a PR. Do NOT hand-edit files under `output/healer/`.

## Commit Style

This project enforces [Conventional Commits](https://www.conventionalcommits.org/). Allowed scopes: `deps`, `conftest`, `logger`, `common`, `config`, `pta`, `hirokuapp`, `jsonplaceholder`, `performance`, `data`, `kwa`, `ci`, `readme`.

Example: `feat(hirokuapp): add broken_images_page page object`

See the commit-message skill at `.claude/skills/commit-message/SKILL.md`.
