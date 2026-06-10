# GitHub Copilot Instructions

Use these project-specific instructions when generating or modifying code in this repository.

## Architecture and Routing

- This framework uses a layered **Page Object Model (POM)** with **per-app config auto-discovery**.
- Do **not** introduce central `APP_NAME`, `SERVICE_NAME`, or `MOBILE_APP_NAME` branching.
- Tests are routed by **pytest markers** declared in `pytest.ini`: `pta`, `heroku`, `kwa`, `wdio`, `jsonplaceholder`, and `restcountries_data`.
- Each app or service under `tests/` owns its own `conftest.py` and loads its own config with `config/config_parser.py` via `ConfigParser.load_config(...)`.
- Region-specific values come from `DEV` / `QA` / `STAGE` / `PROD` config blocks selected by the `REGION` environment variable.

## Page Object Rules

- UI page objects must inherit `framework/pages/ui/base_page.py` (`BasePage`).
- Keep locators as class-level tuples, for example `USERNAME = (By.ID, "username")`.
- Expose elements through lazy properties using `self.find_element(...)` with explicit waits.
- Implement user actions as page methods such as `type_username(...)` and `click_submit()`.
- Do **not** use raw `driver.find_element(...)` calls in tests.
- If a shared Selenium interaction is missing, extend `BasePage` instead of duplicating WebDriver logic in page objects or tests.

## Test Layer Conventions

- `tests/conftest.py` owns session-level output cleanup, Allure environment metadata, and logging fixtures.
- `tests/ui/conftest.py`, `tests/api/conftest.py`, and `tests/mobile/conftest.py` own only cross-app lifecycle concerns.
- App-specific fixtures belong in `tests/<layer>/<app>/conftest.py`.
- New apps should follow this pattern:
  - `tests/<layer>/<app>/{__init__.py, conftest.py, pages/, test_<app>.py}`
  - matching config folder under `config/<layer>/<app>/`
  - marker added to `pytest.ini`

## Project-Specific Rules

- Keep the two PTA variants in sync when changing PTA flows:
  - `tests/ui/pta/test_pta_clean_version.py`
  - `tests/ui/pta/test_pta_tutorial_version.py`
- PTA BDD assets live under:
  - `tests/ui/pta/features/`
  - `tests/ui/pta/steps/`
- Performance tests are **Locust** in `tests/performance/locustfile.py`, not pytest tests.
- Data quality tests are in `tests/data/restcountries/` and use raw `requests`, not Selenium `BasePage`.
- Do **not** hand-edit generated healer artifacts under `output/healer/`.

## Logging and Artifacts

- Use `framework/utilities/custom_logger.py` for framework logging.
- Test steps should log as literal `STEP 01`, `STEP 02`, and so on for log grep-ability.
- UI failures produce screenshots and ffmpeg videos under `output/screenshots/` and `output/videos/`.

## Validation Commands

Use the smallest relevant command for the area you changed.

```powershell
pip install -r requirements.txt
pytest -vvv -m "pta" tests/
pytest -vvv -m "heroku" tests/
pytest -vvv -m "jsonplaceholder" tests/
pytest -vvv -m "kwa" tests/
pytest -vvv -m "wdio" tests/
pytest -vvv -m "restcountries_data" tests/data/
pylint framework/ tests/ config/
```

## Commit Guidance

- Follow Conventional Commits.
- Allowed scopes: `deps`, `conftest`, `logger`, `common`, `config`, `pta`, `hirokuapp`, `jsonplaceholder`, `performance`, `data`, `kwa`, `ci`, `readme`.

## Related Docs

- `AGENTS.md` - concise repo guidance for coding agents
- `CLAUDE.md` - expanded commands, architecture, and project rules
- `README.md` - setup, execution, reporting, and MCP usage instructions
