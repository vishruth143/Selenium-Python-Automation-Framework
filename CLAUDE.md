# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Tests
Tests require environment variables to select the app, region, and browser. The `REGION` defaults to `QA`, `BROWSER` defaults to `CHROME`, `HEADLESS` defaults to `N`.

```bash
# UI - Herokuapp
APP_NAME=HIROKUAPP REGION=QA BROWSER=CHROME pytest -vvv -m "hirokuapp" tests/

# UI - PTA
APP_NAME=PTA REGION=QA BROWSER=CHROME pytest -vvv -m "pta" tests/

# API - Reqres
SERVICE_NAME=REQRES REGION=QA pytest -vvv -m "reqres" tests/

# API - Commerce Tools
SERVICE_NAME=COMMERCE_TOOLS REGION=QA pytest -vvv -m "commerce_tools" tests/

# Mobile - KWA
MOBILE_APP_NAME=KWA pytest -vvv -m "kwa" tests/

# Run a single test file
APP_NAME=HIROKUAPP pytest -vvv tests/ui/heroku/test_heroku.py

# Run a single test by name
APP_NAME=HIROKUAPP pytest -vvv tests/ui/heroku/test_heroku.py::TestHirokuApp::test_ab_test_page

# Parallel execution with retries and HTML report
APP_NAME=PTA BROWSER=CHROME pytest -vvv -m "pta" -n 4 --reruns 3 \
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
docker run -e APP_NAME=PTA -e BROWSER=CHROME -e HEADLESS=Y selenium-python-automation pytest tests/
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

`config/config_parser.py` is the central config loader. It reads the env vars (`APP_NAME`, `SERVICE_NAME`, `MOBILE_APP_NAME`, `REGION`) and resolves the correct YAML/JSON/Excel file under `config/<type>/<app>/`. Each YAML config has region-keyed blocks (`DEV`, `QA`, `STAGE`, `PROD`).

### Fixture Chain

1. **Session** (`tests/conftest.py`): Cleans and recreates `output/` subdirectories; writes Allure `environment.properties`.
2. **Function - UI** (`tests/ui/conftest.py`): Reads config → builds WebDriver (Chrome/Firefox/Edge, local or Grid) → yields driver → tears down; captures screenshot and video on failure.
3. **Function - API** (`tests/api/conftest.py`): Instantiates `APIClient` with base URL and optional OAuth2 token.
4. **Session - Mobile** (`tests/mobile/conftest.py`): Starts Appium server; builds desired capabilities from config.

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