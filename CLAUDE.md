# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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

# Run a single test file
pytest -vvv tests/ui/heroku/test_heroku.py

# Run a single test by name
pytest -vvv tests/ui/heroku/test_heroku.py::TestHerokuApp::test_ab_test_page

# Parallel execution with retries and HTML report
BROWSER=CHROME pytest -vvv -m "pta" -n 4 --reruns 3 \
  --html=output/reports/report.html --self-contained-html \
  --alluredir=output/allure-results tests/
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

The framework uses a layered **Page Object Model (POM)** with configuration-driven test execution.

```
config/              ← YAML/JSON/Excel configs, organized by app and region
framework/
  interfaces/        ← APIClient (GET/POST/PUT/DELETE with OAuth2 support)
  listeners/         ← Selenium EventListener for navigation/click/exception logging
  pages/ui/          ← BasePage with all shared WebDriver interactions
  utilities/         ← Logger, screenshots, screen recording, Faker helpers, loaders
tests/
  conftest.py        ← Session-level: cleans output/, creates dirs, writes environment.properties
  ui/
    conftest.py      ← Function-level: WebDriver init/teardown, browser options, video recording, screenshot on failure
    <app>/
      pages/         ← App-specific page objects (inherit BasePage)
      test_<app>.py  ← Test classes (use page objects, fixtures)
  api/
    conftest.py      ← Session-level: APIClient fixture with OAuth token
    <service>/
      test_<service>.py
  mobile/
    conftest.py      ← Autouse: Appium server, local/cloud device config
    <app>/
      test_<app>.py
output/              ← Auto-generated: logs/, reports/, screenshots/, videos/, allure-results/
```

### Configuration Loading

`config/config_parser.py` is the central config loader. It resolves YAML/JSON/Excel files under `config/<type>/<app>/` by name (e.g. `pta_ui_test_data_config`). Each per-app `tests/.../<app>/conftest.py` declares its own `testdata` (and other) fixtures by calling `ConfigParser.load_config(...)` with the right config name - so `APP_NAME` / `SERVICE_NAME` / `MOBILE_APP_NAME` env vars are no longer needed. `REGION` is still read at the test level to pick the right region-keyed block (`DEV`, `QA`, `STAGE`, `PROD`).

### Fixture Chain

1. **Session** (`tests/conftest.py`): Cleans `output/`, creates dirs, writes Allure `environment.properties`, registers the autouse `_stamp_log_context` fixture and exposes the `log` fixture.
2. **Layer** (`tests/ui/conftest.py`, `tests/mobile/conftest.py`): Cross-app concerns only - WebDriver lifecycle / Appium server lifecycle.
3. **Per-app** (`tests/ui/<app>/conftest.py`, `tests/api/<service>/conftest.py`, `tests/mobile/<app>/conftest.py`): Declares the app-specific `testdata` (and `api_client` / `driver` for mobile) by loading the matching config file directly - no central if/elif on env vars.

### Page Object Pattern

Each page class inherits `BasePage` and follows this structure:
- **Locators** — class-level tuples `(By.X, "selector")`
- **Properties** — lazy elements using `self.find_element(by, locator, condition)` with explicit waits
- **Action methods** — composite operations (e.g., `type_username`, `click_submit`) that call `BasePage` primitives

`BasePage` (`framework/pages/ui/base_page.py`) owns all WebDriver interaction: waits, clicks, typing, scroll, URL checks, and JS execution.

### Logging

`framework/utilities/custom_logger.py` creates a rotating file logger (`output/logs/test_execution.log`, 10 MB / 5 backups) with colored console output. Tests log steps as `STEP 01`, `STEP 02`, etc. for easy tracing.

## Markers and Scopes

Pytest markers (defined in `pytest.ini`) map 1-to-1 to app/service names:
`pta`, `hirokuapp`, `kwa`, `reqres`, `commerce_tools`, `excel`, `param`, `retry`

## Commit Style

This project enforces [Conventional Commits](https://www.conventionalcommits.org/). Known scopes: `deps`, `conftest`, `logger`, `common`, `config`, `pta`, `hirokuapp`, `reqres`, `kwa`, `ci`, `readme`.

Example: `feat(hirokuapp): add broken_images_page page object`