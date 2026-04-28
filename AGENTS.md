# AGENTS.md

Guidance for AI coding agents working in this Selenium + Pytest + Appium framework. See `CLAUDE.md` and `README.md` for full detail.

## Big Picture

Layered **Page Object Model** with **per-app config auto-discovery**. There is no central `if APP_NAME == ...` switch — each app/service folder under `tests/` owns a `conftest.py` that loads its own config via `config/config_parser.py` (`ConfigParser.load_config(name)`). Tests are selected and routed entirely by **pytest markers** (`-m pta`, `-m heroku`, `-m jsonplaceholder`, `-m kwa`, `-m restcountries_data`).

Fixture chain (read in order to understand any test):
1. `tests/conftest.py` — session: cleans `output/`, writes Allure `environment.properties`, exposes `log` fixture.
2. `tests/{ui,api,mobile}/conftest.py` — layer: WebDriver / APIClient / Appium lifecycle, screenshot + ffmpeg video on UI failure (kept only on fail).
3. `tests/{ui,api,mobile}/<app>/conftest.py` — app: declares `testdata` (and `api_client` / `driver` for mobile) by loading the matching config file. Region-keyed blocks (`DEV`/`QA`/`STAGE`/`PROD`) selected by `REGION` env var (default `QA`).

Config files live at `config/<type>/<app>/` as YAML / JSON / XLSX (e.g. `config/ui/pta/ui_test_data_config.yml`, `config/ui/pta/ui_test_excel_data_config.xlsx`).

## Page Object Convention

Every page inherits `framework/pages/ui/base_page.py` (`BasePage` owns ALL WebDriver primitives: waits, clicks, typing, scroll, JS). Pages MUST follow this shape — see `tests/ui/heroku/pages/landing_page.py` and `tests/ui/pta/pages/login_page.py`:

- **Locators**: class-level tuples — `USERNAME = (By.ID, "username")`
- **Properties**: lazy `self.find_element(by, locator, condition)` with explicit waits
- **Actions**: composite methods like `type_username(...)`, `click_submit()` that call BasePage primitives — never raw `driver.find_element` in tests or pages.

Selenium events are auto-logged via `framework/listeners/event_listeners.py` (EventFiringWebDriver).

## Logging & Artifacts

Use `framework/utilities/custom_logger.py`. Tests log steps as literal `STEP 01`, `STEP 02`, ... for grep-ability across the rotating `output/logs/test_execution.log` (10 MB × 5). On UI failure, `screenshot_utils.py` + `screen_recording_utils.py` (ffmpeg) drop artifacts under `output/screenshots/` and `output/videos/`; passing tests' videos are deleted.

## Commands

```bash
pip install -r requirements.txt

# Run by marker (REGION/BROWSER/HEADLESS optional; defaults: QA / CHROME / N)
pytest -vvv -m "pta" tests/
pytest -vvv -m "heroku" tests/
pytest -vvv -m "jsonplaceholder" tests/
pytest -vvv -m "kwa" tests/
pytest -vvv -m "restcountries_data" tests/data/

# Performance (Locust, not pytest) — JSONPlaceholder, 9 tasks
locust -f tests/performance/locustfile.py --headless \
  --host=https://jsonplaceholder.typicode.com -u 10 -r 2 --run-time 60s

# Locator Auto-Healer pipeline (parses output/logs, asks Claude, patches page objects, opens PR)
python -m scripts.healer.run_healer --dry-run

# Full CI-style run
pytest -vvv -m "pta" -n 4 --reruns 3 --html=output/reports/report.html \
  --self-contained-html --alluredir=output/allure-results tests/

# Lint MUST score 10.0/10 (CI-enforced)
pylint framework/ tests/ config/
```

Markers are declared in `pytest.ini` and map 1:1 to app/service names (`pta, heroku, kwa, jsonplaceholder, restcountries_data`) plus cross-cutting `excel, param, retry` used by `tests/snippet/` demos. Add new ones there.

## Project-Specific Rules

- **Do NOT** add `APP_NAME` / `SERVICE_NAME` / `MOBILE_APP_NAME` env-var branching — that pattern was removed; route via per-app `conftest.py` instead.
- **Do NOT** put WebDriver calls in tests — extend `BasePage` if a primitive is missing.
- New app? Create `tests/<layer>/<app>/{__init__.py, conftest.py, pages/, test_<app>.py}`, a matching `config/<layer>/<app>/` folder, and a marker in `pytest.ini`.
- Two PTA test variants exist intentionally: `test_pta_clean_version.py` (terse) and `test_pta_tutorial_version.py` (heavily commented for onboarding) — keep both in sync when changing flows.
- BDD lives at `tests/ui/pta/features/*.feature` with steps in `tests/ui/pta/steps/test_pta_app.py` (pytest-bdd).
- Performance tests are **Locust**, not pytest — `tests/performance/locustfile.py` (no marker, no `BasePage`).
- Data quality tests live at `tests/data/restcountries/` and use raw `requests` against the REST Countries API (no `BasePage`, no WebDriver) — marker `restcountries_data`.
- Locator Auto-Healer (`scripts/healer/`) consumes `output/logs/test_execution.log`, writes `output/healer/{failures,suggestions,patch_report}.json` + `pr_body.md`, then patches page objects and opens a PR. See `tutorial/locator_auto_healer.md`. Do NOT hand-edit files under `output/healer/`.

## Commits

Conventional Commits enforced. Allowed scopes: `deps, conftest, logger, common, config, pta, hirokuapp, jsonplaceholder, performance, data, kwa, ci, readme`. Example: `feat(hirokuapp): add broken_images_page page object`. See skill at `.claude/skills/commit-message/SKILL.md`.

