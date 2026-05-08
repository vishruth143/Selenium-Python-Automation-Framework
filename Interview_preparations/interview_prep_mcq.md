# 🎯 Interview Preparation: MCQ — Selenium Python Automation Framework

> **Based on the actual codebase.** Each question tests your real understanding of this framework's architecture, design decisions, and implementation details. Answers with explanations are at the bottom of each section.

---

## 📦 SECTION 1: Framework Architecture & Design Patterns

---

**Q1.** What design pattern is the primary structural backbone of this automation framework?

- A) Singleton Pattern
- B) Page Object Model (POM)
- C) Factory Pattern
- D) Facade Pattern

---

**Q2.** How does the framework select the right app/service configuration for tests? (No central `if APP_NAME == ...` switch exists.)

- A) By reading the `APP_NAME` environment variable in a central `conftest.py`
- B) Each app/service folder under `tests/` owns its own `conftest.py` that loads its config via `ConfigParser`
- C) A global config dictionary in `config_parser.py` auto-selects based on test file path
- D) pytest markers directly inject config values into test functions

---

**Q3.** In which order does the fixture chain execute in this framework?

- A) Per-app conftest → UI/API/Mobile conftest → tests/conftest.py
- B) tests/conftest.py (session) → tests/ui/conftest.py (layer) → tests/ui/\<app\>/conftest.py (per-app)
- C) tests/ui/\<app\>/conftest.py → tests/conftest.py → tests/ui/conftest.py
- D) All conftest.py files are loaded simultaneously

---

**Q4.** How are tests in this framework routed to the correct app or service?

- A) A global `APP_NAME` environment variable
- B) The file path of the test file
- C) Pytest markers defined in `pytest.ini`
- D) The `SERVICE_NAME` environment variable

---

**Q5.** What is the correct way to add a NEW application to this framework?

- A) Add an `if APP_NAME == "newapp"` branch to `tests/conftest.py`
- B) Create `tests/<layer>/<app>/{__init__.py, conftest.py, pages/, test_<app>.py}`, a `config/<layer>/<app>/` folder, and register a marker in `pytest.ini`
- C) Simply add test files anywhere under `tests/` and update `common_config.yml`
- D) Only update `config/config_parser.py` with the new app's config path

---

### ✅ Section 1 Answers

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | **B** | The framework uses a layered Page Object Model — each app has page classes inheriting `BasePage`. |
| 2 | **B** | Per-app `conftest.py` calls `ConfigParser.load_config(name)` — no central APP_NAME branching. |
| 3 | **B** | session → layer → per-app. This is explicitly documented in CLAUDE.md Fixture Chain. |
| 4 | **C** | `pytest.ini` declares markers (`pta`, `heroku`, `kwa`, `jsonplaceholder`, `restcountries_data`) that route tests. |
| 5 | **B** | This is the exact "new app" rule from AGENTS.md and CLAUDE.md. |

---

## 🏗️ SECTION 2: BasePage & Page Object Implementation

---

**Q6.** Where does `BasePage` live and what is its primary responsibility?

- A) `tests/ui/base_page.py` — stores all test assertions
- B) `framework/pages/ui/base_page.py` — owns ALL WebDriver primitives (waits, clicks, scroll, JS)
- C) `config/base_page.py` — manages configuration loading
- D) `framework/interfaces/base_page.py` — handles API calls

---

**Q7.** Which of the following is the correct way to define a locator in a Page Object class?

- A) `self.username = driver.find_element(By.ID, "username")`
- B) `USERNAME = (By.ID, "username")` (class-level tuple)
- C) `username_locator = {"by": By.ID, "value": "username"}`
- D) `USERNAME = driver.By.ID + "#username"`

---

**Q8.** How does `BasePage.find_element()` differ from raw `driver.find_element()`?

- A) They are identical; `BasePage.find_element()` is just an alias
- B) `BasePage.find_element()` uses `WebDriverWait` with an explicit timeout and accepts an `expected_conditions` condition
- C) `BasePage.find_element()` uses `ImplicitWait` instead of explicit waits
- D) `BasePage.find_element()` automatically retries 3 times on `NoSuchElementException`

---

**Q9.** What is the default `expected_condition` used by `BasePage.find_element()` when no condition is specified?

- A) `EC.element_to_be_clickable`
- B) `EC.visibility_of_element_located`
- C) `EC.presence_of_element_located`
- D) `EC.text_to_be_present_in_element`

---

**Q10.** In `LandingPage`, elements are exposed as Python `@property` methods. What is the **benefit** of this approach?

- A) Elements are found at class import time, making tests faster
- B) Elements are re-fetched lazily on each access, avoiding `StaleElementReferenceException`
- C) Properties bypass WebDriverWait and directly use `driver.find_element`
- D) Properties cache the element permanently for the lifetime of the test

---

**Q11.** What is the **forbidden pattern** for interacting with elements, according to project rules?

- A) Using `@property` in page classes
- B) Using class-level tuple locators
- C) Calling raw `driver.find_element()` directly inside test methods or page classes
- D) Inheriting from `BasePage`

---

**Q12.** Look at `LandingPage.click_ab_testing_lnk()`. How does it click the element?

```python
def click_ab_testing_lnk(self):
    self.click(*self._ab_testing_lnk)
```

What does `*self._ab_testing_lnk` do here?

- A) It calls the `click` method on the locator tuple itself
- B) It unpacks the tuple `(By.XPATH, "//a[...]")` into two positional arguments: `by` and `locator`
- C) It dereferences a pointer to the element
- D) It converts the locator to a CSS selector automatically

---

### ✅ Section 2 Answers

| Q | Answer | Explanation |
|---|--------|-------------|
| 6 | **B** | `framework/pages/ui/base_page.py` owns ALL WebDriver primitives — the single source for all page interactions. |
| 7 | **B** | Class-level tuples like `USERNAME = (By.ID, "username")` is the standard locator pattern. |
| 8 | **B** | `find_element` uses `WebDriverWait(driver, timeout).until(condition((by, locator)))`. |
| 9 | **C** | Default is `EC.presence_of_element_located` — the element just needs to exist in the DOM. |
| 10 | **B** | Lazy `@property` re-fetches elements on each access, which is critical for dynamic pages. |
| 11 | **C** | "Do NOT put WebDriver calls in tests" is an explicit rule in both CLAUDE.md and AGENTS.md. |
| 12 | **B** | `*self._ab_testing_lnk` unpacks `(By.XPATH, "//a[...]")` into `by=By.XPATH, locator="//a[...]"`. |

---

## ⚙️ SECTION 3: Configuration Management

---

**Q13.** What class is responsible for loading all configuration files in this framework?

- A) `YamlLoader` in `framework/utilities/loaders.py`
- B) `ConfigParser` in `config/config_parser.py`
- C) `TestConfig` in `tests/conftest.py`
- D) `EnvironmentConfig` in `config/common_config.yml`

---

**Q14.** Which file formats does `ConfigParser.load_config()` support?

- A) Only YAML (`.yml`)
- B) JSON and YAML only
- C) YAML, JSON, and XLSX (via separate methods)
- D) XML, YAML, and JSON

---

**Q15.** What does the `REGION` environment variable control in this framework?

- A) Which country's API endpoint to target
- B) Which browser to launch for testing
- C) Which region-keyed block (`DEV`, `QA`, `STAGE`, `PROD`) is selected from YAML/JSON configs
- D) Which test suite (UI/API/Mobile) to run

---

**Q16.** What is the **default** value of `REGION` if the environment variable is not set?

- A) `DEV`
- B) `PROD`
- C) `STAGE`
- D) `QA`

---

**Q17.** How does a per-app `conftest.py` (e.g., `tests/ui/heroku/conftest.py`) load its test data?

- A) `import yaml; yaml.safe_load(open("config/ui/heroku/..."))`
- B) `ConfigParser.load_config("heroku_ui_test_data_config")`
- C) Reading `os.environ["TEST_DATA_PATH"]`
- D) Directly instantiating `ConfigParser(app="heroku")`

---

**Q18.** How does a test function access region-specific data from the `testdata` fixture?

- A) `testdata.get_region("QA")`
- B) `testdata[region]["base_url"]` — treating the loaded config as a nested dict keyed by region
- C) `testdata.region.base_url`
- D) `testdata["base_url"]` — region is auto-resolved inside the fixture

---

### ✅ Section 3 Answers

| Q | Answer | Explanation |
|---|--------|-------------|
| 13 | **B** | `config/config_parser.py` is "the central config loader" per CLAUDE.md. |
| 14 | **C** | `load_config()` handles `.json` and `.yml`/`.yaml`. `load_xlsx()` is a separate method for Excel. |
| 15 | **C** | `REGION` selects the block from YAML/JSON; default is `QA`. |
| 16 | **D** | `os.environ.get("REGION", "QA")` — default is `QA`. |
| 17 | **B** | `ConfigParser.load_config("heroku_ui_test_data_config")` — exact pattern in `tests/ui/heroku/conftest.py`. |
| 18 | **B** | `testdata[region]["ab_test_url"]` — region is passed as a separate fixture from `tests/ui/conftest.py`. |

---

## 🌐 SECTION 4: WebDriver & Browser Management

---

**Q19.** Which class wraps the raw WebDriver to enable automatic event logging?

- A) `LoggingWebDriver`
- B) `EventFiringWebDriver` from `selenium.webdriver.support.events`
- C) `DebugWebDriver` from `framework/interfaces/`
- D) `TracingWebDriver` in `framework/listeners/`

---

**Q20.** What is the `MyEventListener` class and where does it live?

- A) A pytest plugin in `tests/conftest.py` that hooks into test lifecycle
- B) A subclass of `AbstractEventListener` in `framework/listeners/event_listeners.py` that logs WebDriver events
- C) A Selenium Grid listener in `framework/interfaces/api_client.py`
- D) A logging handler in `framework/utilities/custom_logger.py`

---

**Q21.** At what log level do routine WebDriver events (navigate, find, click) get logged by `MyEventListener`?

- A) `INFO`
- B) `WARNING`
- C) `DEBUG`
- D) `ERROR`

---

**Q22.** What three browsers are supported by the `driver` fixture in `tests/ui/conftest.py`?

- A) Chrome, Safari, Internet Explorer
- B) Chrome, Firefox, Edge
- C) Chrome, Firefox, Opera
- D) Chrome, Brave, Edge

---

**Q23.** Which Chrome flag is required when running in headless mode inside a Docker container?

- A) `--disable-gpu`
- B) `--headless=legacy`
- C) `--no-sandbox` and `--disable-dev-shm-usage`
- D) `--remote-debugging-port=9222`

---

**Q24.** When is the browser window **maximized** and when is it **NOT** maximized in the `driver` fixture?

- A) Always maximized regardless of headless setting
- B) Maximized only when `HEADLESS=Y`
- C) Maximized only when `HEADLESS` is not `Y` (i.e., headed/visible mode)
- D) Never maximized; a fixed `--window-size=1920,1080` is always used

---

**Q25.** How is the WebDriver's teardown handled in the `driver` fixture?

- A) Using a pytest `yield` boundary — `driver.quit()` is called after `yield`
- B) Via `request.addfinalizer(teardown)` — registers a teardown function that calls `driver.close()` then `driver.quit()`
- C) In a `try/finally` block within the test function itself
- D) pytest automatically calls `driver.quit()` at the end of every function

---

### ✅ Section 4 Answers

| Q | Answer | Explanation |
|---|--------|-------------|
| 19 | **B** | `EventFiringWebDriver(driver_instance, MyEventListener())` wraps the driver. |
| 20 | **B** | `MyEventListener(AbstractEventListener)` in `framework/listeners/event_listeners.py`. |
| 21 | **C** | `log.debug(...)` is used for `before_navigate_to`, `before_find`, `before_click` etc. Only `on_exception` uses `log.error`. |
| 22 | **B** | Chrome, Firefox, Edge — controlled via `BROWSER` env var. |
| 23 | **C** | `--no-sandbox` and `--disable-dev-shm-usage` are added for Docker. |
| 24 | **C** | `if not headless: driver_instance.maximize_window()` — headless uses `--window-size=1920,1080` flag instead. |
| 25 | **B** | `request.addfinalizer(teardown)` — the teardown function calls `close()` then `quit()` then stops video. |

---

## 📝 SECTION 5: Logging & Artifacts

---

**Q26.** What is the name of the main log file and where is it stored?

- A) `framework.log` in the project root
- B) `test_execution.log` in `output/logs/`
- C) `pytest.log` in `output/reports/`
- D) `automation.log` in `output/allure-results/`

---

**Q27.** What type of file handler is used for the log file, and what are its rotation settings?

- A) `FileHandler` with no rotation
- B) `TimedRotatingFileHandler` rotating daily
- C) `RotatingFileHandler` with `maxBytes=10 MB` and `backupCount=5`
- D) `StreamHandler` writing to stdout only

---

**Q28.** How does the logger handle parallel test execution with `pytest-xdist`?

- A) All workers write to a single `test_execution.log` with a threading lock
- B) Each xdist worker writes to its own shard file (`test_execution_gw0.log`, `_gw1.log`, etc.); shards are merged at session end
- C) Workers write to separate folders and logs are never merged
- D) Parallel logging is disabled; `-n` flag forces sequential test execution

---

**Q29.** What pytest convention does this framework adopt for logging test steps?

- A) Using `print()` statements with `[STEP]` prefix
- B) Logging steps as `STEP 01`, `STEP 02`, etc. for grep-ability across the log file
- C) Using `allure.step()` decorators on all action methods
- D) Writing steps to a separate `steps.txt` file

---

**Q30.** What happens to video recordings of **PASSED** tests?

- A) They are kept permanently in `output/videos/`
- B) They are uploaded to Allure results
- C) They are deleted after the test passes to save disk space
- D) They are compressed and moved to `output/reports/`

---

**Q31.** What tool is used to record desktop videos during test execution?

- A) OpenCV
- B) Selenium's built-in screen recording
- C) ffmpeg
- D) OBS Studio CLI

---

**Q32.** On test **failure**, what artifact is captured and where is it saved?

- A) A HAR file saved to `output/reports/`
- B) A PNG screenshot saved to `output/screenshots/`
- C) A JSON dump of the page source to `output/logs/`
- D) A browser console log to `output/allure-results/`

---

### ✅ Section 5 Answers

| Q | Answer | Explanation |
|---|--------|-------------|
| 26 | **B** | `output/logs/test_execution.log` — per CLAUDE.md and `custom_logger.py`. |
| 27 | **C** | `RotatingFileHandler(maxBytes=10*1024*1024, backupCount=5)` — code in `custom_logger.py` line 69–76. |
| 28 | **B** | Each worker writes to `test_execution_{worker_id}.log`; `merge_worker_logs()` merges at session end in `pytest_sessionfinish`. |
| 29 | **B** | "Tests log steps as literal `STEP 01`, `STEP 02`, … for grep-ability" — CLAUDE.md. |
| 30 | **C** | `os.remove(video_path)` for passed tests in `pytest_runtest_makereport` — retried up to 10 times. |
| 31 | **C** | `screen_recording_utils.py` uses ffmpeg. |
| 32 | **B** | `driver.save_screenshot(screenshot_path)` → PNG file in `output/screenshots/` with timestamp. |

---

## 🧪 SECTION 6: Pytest Fixtures & Hooks

---

**Q33.** What is the scope of the `region` fixture?

- A) `function` — recreated for every test
- B) `class` — shared across a test class
- C) `session` — created once and shared across all tests in a session
- D) `module` — shared within a single test module

---

**Q34.** What is the scope of the `driver` fixture?

- A) `session`
- B) `module`
- C) `class`
- D) `function` (default) — a fresh browser is created for each test

---

**Q35.** What does the `@pytest.fixture(autouse=True)` decorator do in `_stamp_log_context`?

- A) Makes the fixture available only to tests in the same class
- B) Automatically applies the fixture to EVERY test without needing to explicitly request it
- C) Runs the fixture only when a specific marker is present
- D) Restricts the fixture to session scope

---

**Q36.** Which pytest hook is used to capture screenshots on test failure in `tests/ui/conftest.py`?

- A) `pytest_test_failed`
- B) `pytest_exception_interact`
- C) `pytest_runtest_makereport`
- D) `pytest_report_teststatus`

---

**Q37.** Why is `@pytest.hookimpl(tryfirst=True, hookwrapper=True)` used on `pytest_runtest_makereport`?

- A) `tryfirst` makes it run last; `hookwrapper` disables default reporting
- B) `tryfirst` ensures this hook runs before other plugins (e.g., HTML reporter) so screenshots are available when the report is generated; `hookwrapper` lets the default pytest reporting run first via `yield`, then inspects the result
- C) Both flags together skip the test if the setup fails
- D) `hookwrapper` replaces `yield` with a synchronous callback

---

**Q38.** What is `pytest_sessionstart` used for in `tests/conftest.py`?

- A) To run before each individual test
- B) To initialize the WebDriver
- C) To clean the `output/` directory, recreate subdirectories, and write Allure `environment.properties`, `executor.json`
- D) To register new pytest markers

---

**Q39.** What does `pytest_sessionfinish` do in `tests/conftest.py`?

- A) Teardown the WebDriver after all tests
- B) Merge per-worker log shards into the final `test_execution.log` (only on the controller process)
- C) Generate the HTML report
- D) Archive screenshots and videos to the allure results folder

---

### ✅ Section 6 Answers

| Q | Answer | Explanation |
|---|--------|-------------|
| 33 | **C** | `@pytest.fixture(scope="session")` — `region` reads `REGION` env var once. |
| 34 | **D** | `@pytest.fixture()` with no scope argument defaults to `function` — fresh browser for every test. |
| 35 | **B** | `autouse=True` applies the fixture to every test in scope automatically. |
| 36 | **C** | `pytest_runtest_makereport` is the hook for post-result processing. |
| 37 | **B** | This is the exact explanation in the conftest comments (lines 209–213). |
| 38 | **C** | `pytest_sessionstart` cleans `output/`, creates dirs, writes `environment.properties`, `executor.json`, `categories.json`. |
| 39 | **B** | `pytest_sessionfinish` calls `merge_worker_logs()` only when `PYTEST_XDIST_WORKER` env var is NOT set (controller only). |

---

## 🔌 SECTION 7: API Testing

---

**Q40.** What class is used for all API interactions and where does it live?

- A) `RequestsHelper` in `tests/api/conftest.py`
- B) `APIClient` in `framework/interfaces/api_client.py`
- C) `HTTPClient` in `framework/utilities/common.py`
- D) `RestClient` in `config/api/`

---

**Q41.** What underlying Python library does `APIClient` use for HTTP requests?

- A) `urllib3`
- B) `httpx`
- C) `requests` (with `requests.Session()`)
- D) `aiohttp`

---

**Q42.** What OAuth2 grant type does `APIClient.get_oauth_token()` use?

- A) `authorization_code`
- B) `password`
- C) `implicit`
- D) `client_credentials`

---

**Q43.** After obtaining an OAuth token, what TWO properties does `APIClient.get_oauth_token()` assert about the token response?

- A) `token_type == "Bearer"` and `expires_in > 0` and `access_token` is not empty
- B) `status_code == 200` and `token` length > 10
- C) `grant_type == "client_credentials"` and `token_type == "Bearer"`
- D) `expires_in == 3600` and `scope == "read"`

---

**Q44.** How is a test marked as an API test for JSONPlaceholder?

- A) `@pytest.mark.api`
- B) `@pytest.mark.jsonplaceholder`
- C) `@pytest.mark.restapi`
- D) By placing the test in `tests/api/` folder — no marker needed

---

### ✅ Section 7 Answers

| Q | Answer | Explanation |
|---|--------|-------------|
| 40 | **B** | `framework/interfaces/api_client.py` contains the `APIClient` class. |
| 41 | **C** | `self.session = requests.Session()` — uses the `requests` library with session. |
| 42 | **D** | `data={"grant_type": "client_credentials"}` — code line 33 in `api_client.py`. |
| 43 | **A** | All three assertions exist: `token_type == "Bearer"`, `expires_in > 0`, `access_token` not empty (lines 45–57). |
| 44 | **B** | `@pytest.mark.jsonplaceholder` is declared in `pytest.ini`. |

---

## 📊 SECTION 8: Performance Testing (Locust)

---

**Q45.** Which tool is used for performance testing in this framework?

- A) pytest-benchmark
- B) JMeter
- C) Locust
- D) k6

---

**Q46.** Where does the performance test file live and is it a pytest file?

- A) `tests/performance/test_performance.py` — yes, it's a pytest file
- B) `tests/performance/locustfile.py` — NO, it is NOT a pytest file (no markers, no `BasePage`)
- C) `config/performance/locustfile.py` — it's a config file
- D) `framework/interfaces/locustfile.py` — part of the framework interfaces

---

**Q47.** How many tasks does the `JsonPlaceholderUser` Locust user class define?

- A) 5 tasks
- B) 7 tasks
- C) 9 tasks
- D) 12 tasks

---

**Q48.** In the Locust task weight distribution, which operation has the **highest** weight?

- A) `POST /posts` (weight 3)
- B) `DELETE /posts/{id}` (weight 1)
- C) `GET /posts` (weight 10)
- D) `GET /users` (weight 6)

---

**Q49.** What is the Locust command to run a headless load test against JSONPlaceholder with 10 users, spawn rate 2, for 60 seconds?

- A) `locust -f locustfile.py -u 10 -r 2 -t 60`
- B) `locust -f tests/performance/locustfile.py --headless --host=https://jsonplaceholder.typicode.com -u 10 -r 2 --run-time 60s`
- C) `pytest -m performance tests/performance/ -u 10`
- D) `python tests/performance/locustfile.py --users=10`

---

### ✅ Section 8 Answers

| Q | Answer | Explanation |
|---|--------|-------------|
| 45 | **C** | Locust — per CLAUDE.md "Performance (Locust, not pytest)". |
| 46 | **B** | `tests/performance/locustfile.py` — "no marker, no `BasePage`" — explicitly stated in CLAUDE.md. |
| 47 | **C** | 9 tasks: 5 GET reads + POST + PUT + PATCH + DELETE — listed in the locustfile docstring. |
| 48 | **C** | `@task(10)` for `GET /posts` — heaviest task weight simulating the most common read. |
| 49 | **B** | This is the exact command from CLAUDE.md's Performance section. |

---

## 🤖 SECTION 9: Locator Auto-Healer

---

**Q50.** What is the Locator Auto-Healer and what problem does it solve?

- A) A tool that automatically generates all page object locators from screenshots
- B) A pipeline that parses test failures from logs, asks an AI (Claude) for locator fixes, patches page objects, and opens a GitHub PR
- C) A Selenium extension that self-heals broken tests during execution in real time
- D) A script that generates Allure reports from test logs

---

**Q51.** What are the 4 steps of the Locator Auto-Healer pipeline in order?

- A) `scan → fix → commit → deploy`
- B) `parse_failures → heal → patcher → open_pr`
- C) `detect → suggest → review → merge`
- D) `log → analyze → report → alert`

---

**Q52.** What is the input consumed by the Locator Auto-Healer and where does it write its output?

- A) Input: `pytest.ini`; Output: `output/reports/`
- B) Input: `output/logs/test_execution.log`; Output: `output/healer/{failures,suggestions,patch_report}.json` + `pr_body.md`
- C) Input: page object files; Output: `output/allure-results/`
- D) Input: `config/` YAML files; Output: `scripts/healer/patches/`

---

**Q53.** What does the `--dry-run` flag do when running the healer?

- A) Runs only the `parse_failures` step and exits
- B) Skips the `heal` step (no AI calls)
- C) Runs the patch and PR steps in dry-run mode — no actual file changes or PR is opened
- D) Generates a report without any side effects

---

**Q54.** Which files should you **NEVER** manually edit in this framework?

- A) Files under `config/`
- B) Files under `output/healer/`
- C) Files under `tests/ui/`
- D) Files under `framework/pages/`

---

### ✅ Section 9 Answers

| Q | Answer | Explanation |
|---|--------|-------------|
| 50 | **B** | "Parses `output/logs/test_execution.log`, asks Claude for fixes, patches page objects, and opens a PR." — CLAUDE.md |
| 51 | **B** | `parse_failures → heal → patcher → open_pr` — in `run_healer.py` comments and `[1/4]...[4/4]` print steps. |
| 52 | **B** | Input: `test_execution.log`; Output: `output/healer/` — from CLAUDE.md Locator Auto-Healer section. |
| 53 | **C** | `--dry-run` is passed to both `patcher.apply_suggestions(dry_run=args.dry_run)` and `open_pr.open_pr(dry_run=...)`. |
| 54 | **B** | "Do NOT hand-edit files under `output/healer/`" — explicit rule in CLAUDE.md. |

---

## 🐳 SECTION 10: CI/CD, Docker & Reporting

---

**Q55.** What is the required Pylint score enforced by CI?

- A) 8.0/10
- B) 9.0/10
- C) 9.5/10
- D) 10.0/10

---

**Q56.** What three modules/packages must pass Pylint to meet CI requirements?

- A) `tests/`, `config/`, `scripts/`
- B) `framework/`, `tests/`, `config/`
- C) `framework/`, `tests/`, `scripts/`
- D) All Python files recursively from the root

---

**Q57.** What does the `environment.properties` file written at session start contain and how is it used?

- A) Browser driver paths used by `driver` fixture
- B) `REGION`, `BROWSER`, `HEADLESS` values written to `output/allure-results/` for Allure's Environment widget
- C) Test data values read by all fixtures
- D) Docker environment variables for container startup

---

**Q58.** What is the purpose of `categories.json` in `config/`?

- A) To configure pytest markers and test categories
- B) To define Allure "Categories" that group test failures into buckets like "Product Defects" and "Test Defects"
- C) To store test data categories for parametrized tests
- D) To configure Locust task categories

---

**Q59.** The `executor.json` generated at session start supports which CI environments automatically?

- A) Only Jenkins
- B) Only GitHub Actions
- C) GitHub Actions, Jenkins, and local machine (auto-detected via env vars)
- D) GitHub Actions, CircleCI, and Azure DevOps

---

**Q60.** What is the correct Docker command to run PTA tests headlessly?

- A) `docker run selenium-python-automation pytest -m "pta"`
- B) `docker run -e BROWSER=CHROME -e HEADLESS=Y selenium-python-automation pytest -m "pta" tests/`
- C) `docker run -v ./tests:/app/tests selenium-python-automation pytest`
- D) `docker exec -it selenium-python-automation pytest -m pta`

---

### ✅ Section 10 Answers

| Q | Answer | Explanation |
|---|--------|-------------|
| 55 | **D** | "Pylint must score **10.0/10** (enforced by CI)" — CLAUDE.md Commands section. |
| 56 | **B** | `pylint framework/ tests/ config/` — exact command in CLAUDE.md. |
| 57 | **B** | Written to `output/allure-results/environment.properties` with `REGION`, `BROWSER`, `HEADLESS`. |
| 58 | **B** | `config/categories.json` is copied to `allure-results/` to populate Allure's Categories tab. |
| 59 | **C** | `_build_executor_info()` checks `GITHUB_ACTIONS`, `JENKINS_URL`, then falls back to local machine. |
| 60 | **B** | `docker run -e BROWSER=CHROME -e HEADLESS=Y selenium-python-automation pytest -m "pta" tests/` — from CLAUDE.md Docker section. |

---

## 🔀 SECTION 11: Parallel Execution & pytest-xdist

---

**Q61.** What flag enables parallel test execution in pytest?

- A) `--parallel=4`
- B) `-n 4` (via `pytest-xdist`)
- C) `--workers=4`
- D) `-j 4`

---

**Q62.** Why does `pytest_sessionstart` return early when `PYTEST_XDIST_WORKER` env var is set?

- A) Workers don't need to run tests
- B) To prevent each worker process from deleting the `output/` directory that sibling workers are actively writing to
- C) Workers don't support Allure reporting
- D) To skip video recording on worker processes

---

**Q63.** What is `threading.local()` used for in `custom_logger.py`?

- A) To share logger instances between threads
- B) As a thread/process-local context storage for `worker_id` and `test_name` so each xdist worker process has its own independent copy
- C) To lock the log file against concurrent writes
- D) To cache logger objects for performance

---

**Q64.** How are per-worker log shards ordered when merged into `test_execution.log`?

- A) Alphabetically by filename
- B) Chronologically by the first log timestamp in each file
- C) `main` first, then `gw0`, `gw1`, `gw2`, … numerically
- D) Randomly — order is not guaranteed

---

### ✅ Section 11 Answers

| Q | Answer | Explanation |
|---|--------|-------------|
| 61 | **B** | `-n 4` via `pytest-xdist` — used in the parallel execution example in CLAUDE.md. |
| 62 | **B** | "Only the master should clean … otherwise workers will delete files being written by sibling workers" — `tests/conftest.py` comment lines 53–55. |
| 63 | **B** | `_local = threading.local()` prevents cross-process bleed of `worker_id`/`test_name` context. |
| 64 | **C** | `_worker_sort_key` returns `(0,0)` for `main` and `(1, num)` for `gwN` — `main` always first. |

---

## 📱 SECTION 12: Mobile Testing

---

**Q65.** What marker is used for mobile (KWA app) tests?

- A) `@pytest.mark.mobile`
- B) `@pytest.mark.appium`
- C) `@pytest.mark.kwa`
- D) `@pytest.mark.android`

---

**Q66.** Where is the Android APK for mobile testing stored?

- A) `tests/mobile/kwa/Android_Demo_App.apk`
- B) `framework/app_apk/Android_Demo_App.apk`
- C) `config/mobile/kwa/Android_Demo_App.apk`
- D) `output/apk/Android_Demo_App.apk`

---

**Q67.** Which conftest.py handles the Appium server setup for mobile tests?

- A) `tests/conftest.py` (session level)
- B) `tests/mobile/kwa/conftest.py` (per-app)
- C) `tests/mobile/conftest.py` (layer level, autouse)
- D) `framework/pages/mobile/conftest.py`

---

### ✅ Section 12 Answers

| Q | Answer | Explanation |
|---|--------|-------------|
| 65 | **C** | `@pytest.mark.kwa` — declared in `pytest.ini`. |
| 66 | **B** | `framework/app_apk/Android_Demo_App.apk` — visible in the workspace structure. |
| 67 | **C** | `tests/mobile/conftest.py` — "Autouse: Appium server, local/cloud device config" per CLAUDE.md Architecture. |

---

## 🌍 SECTION 13: Data Quality Testing

---

**Q68.** What test marker is used for REST Countries data quality tests?

- A) `@pytest.mark.data`
- B) `@pytest.mark.restcountries`
- C) `@pytest.mark.restcountries_data`
- D) `@pytest.mark.dataquality`

---

**Q69.** What makes REST Countries tests different from UI tests in this framework?

- A) They use a different assertion library
- B) They use raw `requests` against the REST Countries API — NO `BasePage`, NO WebDriver
- C) They run in a separate Docker container
- D) They use `APIClient` instead of raw requests

---

**Q70.** Where do data quality tests live?

- A) `tests/api/restcountries/`
- B) `tests/data/restcountries/`
- C) `config/data/restcountries/`
- D) `tests/ui/restcountries/`

---

### ✅ Section 13 Answers

| Q | Answer | Explanation |
|---|--------|-------------|
| 68 | **C** | `@pytest.mark.restcountries_data` — declared in `pytest.ini`. |
| 69 | **B** | "raw `requests` against the REST Countries API (no `BasePage`, no WebDriver)" — CLAUDE.md. |
| 70 | **B** | `tests/data/restcountries/` — per CLAUDE.md Architecture section. |

---

## 🎨 SECTION 14: BDD Testing

---

**Q71.** Which pytest plugin enables BDD (Gherkin) testing in this framework?

- A) `pytest-cucumber`
- B) `pytest-behave`
- C) `pytest-bdd`
- D) `pytest-gherkin`

---

**Q72.** For which application does BDD testing exist in this framework?

- A) Heroku (heroku app)
- B) JSONPlaceholder (API)
- C) PTA (pta app)
- D) KWA (mobile app)

---

**Q73.** Where do the BDD `.feature` files and step definitions live?

- A) Feature files: `tests/ui/pta/features/*.feature` | Step definitions: `tests/ui/pta/steps/test_pta_app.py`
- B) Feature files: `tests/bdd/features/*.feature` | Step definitions: `tests/bdd/steps/`
- C) Both feature files and steps in `tests/ui/pta/test_pta_bdd.py`
- D) Feature files: `config/features/` | Step definitions: `tests/ui/pta/`

---

**Q74.** Which pytest hook captures screenshots for failed BDD scenarios?

- A) `pytest_runtest_makereport`
- B) `pytest_bdd_step_error`
- C) `pytest_bdd_after_scenario`
- D) `pytest_bdd_scenario_fail`

---

### ✅ Section 14 Answers

| Q | Answer | Explanation |
|---|--------|-------------|
| 71 | **C** | `pytest-bdd` — mentioned in `requirements.txt` and CLAUDE.md BDD section. |
| 72 | **C** | "BDD lives at `tests/ui/pta/features/*.feature`" — CLAUDE.md. |
| 73 | **A** | "BDD lives at `tests/ui/pta/features/*.feature` with steps in `tests/ui/pta/steps/test_pta_app.py`" — CLAUDE.md. |
| 74 | **C** | `pytest_bdd_after_scenario` — implemented in `tests/ui/conftest.py` lines 289–313. |

---

## 💬 SECTION 15: Commit Conventions & Naming

---

**Q75.** What commit message convention is enforced in this project?

- A) GitHub Flow commits
- B) Conventional Commits (`feat(scope): description`)
- C) Angular commit style with Jira ticket numbers
- D) Free-form commit messages

---

**Q76.** Which of the following is a **VALID** commit message scope for this project?

- A) `selenium`
- B) `webdriver`
- C) `hirokuapp`
- D) `restapi`

---

**Q77.** Which of these is a correctly formatted commit message for this framework?

- A) `fix: fixed the login test`
- B) `feat(hirokuapp): add broken_images_page page object`
- C) `update(pta): login page locators updated`
- D) `FEAT[pta]: new login test added`

---

### ✅ Section 15 Answers

| Q | Answer | Explanation |
|---|--------|-------------|
| 75 | **B** | "This project enforces Conventional Commits" — CLAUDE.md Commit Style section. |
| 76 | **C** | `hirokuapp` is in the allowed scopes list: `deps, conftest, logger, common, config, pta, hirokuapp, jsonplaceholder, performance, data, kwa, ci, readme`. |
| 77 | **B** | "Example: `feat(hirokuapp): add broken_images_page page object`" — exact example from CLAUDE.md. |

---

## 🧩 SECTION 16: Output Structure & File Organization

---

**Q78.** Which directories are auto-created at **session start** under `output/`?

- A) `logs/`, `screenshots/`, `reports/`, `videos/`, `allure-results/`
- B) `logs/`, `allure/`, `html_reports/`, `artifacts/`
- C) `output/`, `results/`, `debug/`, `tmp/`
- D) Only `allure-results/` and `logs/`

---

**Q79.** What happens to the entire `output/` directory at the **start** of each test session?

- A) It is archived to a zip file
- B) It is left untouched
- C) It is deleted (`shutil.rmtree`) and recreated fresh
- D) Only log files are cleared; screenshots and videos are kept

---

**Q80.** Screenshot filenames follow which naming convention?

- A) `screenshot_<random_uuid>.png`
- B) `<safe_test_name>_<YYYYMMDD_HHMMSS>.png`
- C) `test_<test_class>_<method>.png`
- D) `<browser>_<timestamp>.png`

---

### ✅ Section 16 Answers

| Q | Answer | Explanation |
|---|--------|-------------|
| 78 | **A** | `os.makedirs` for `allure-results`, `logs`, `reports`, `screenshots`, `videos` — `tests/conftest.py` lines 74–78. |
| 79 | **C** | `shutil.rmtree(output_dir, onerror=_on_rm_error)` then recreated — `pytest_sessionstart` in `tests/conftest.py`. |
| 80 | **B** | `f"{safe_name}_{timestamp}.png"` where `safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', test_name)` and `timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")` — `screenshot_utils.py`. |

---

## 🏆 BONUS SECTION: Tricky/Advanced Questions

---

**Q81.** Why does `tests/conftest.py` call `_release_log_handlers()` BEFORE `shutil.rmtree()` on Windows?

- A) To flush pending log writes before deletion
- B) On Windows, file handles are held by the OS as exclusive locks; open `FileHandler`s prevent `shutil.rmtree` from deleting `test_execution.log`
- C) To prevent logger from capturing the cleanup operation
- D) Because `shutil.rmtree` requires exclusive access to the Python GIL

---

**Q82.** What would happen if you used `ImplicitWait` instead of `ExplicitWait` in `BasePage`?

- A) Tests would run faster since implicit waits have lower overhead
- B) It would work identically to explicit waits
- C) Mixing implicit and explicit waits can cause unpredictable timeouts and flaky tests — explicit waits are safer and more precise
- D) Implicit waits only work with Firefox

---

**Q83.** The `find_element` method signature is `find_element(self, by, locator, condition=EC.presence_of_element_located)`. Why is `condition` a **function reference** rather than a result?

- A) Python requires all default arguments to be callable
- B) The condition is passed to `WebDriverWait.until()` which calls it repeatedly with the driver until it returns truthy — so it must be the condition factory, not its result
- C) It's a design mistake; it should be the evaluated result
- D) `EC.presence_of_element_located` is a constant, not a function

---

**Q84.** The two PTA test files `test_pta_clean_version.py` and `test_pta_tutorial_version.py` exist intentionally. What is the **rule** about them?

- A) They test different features; no sync is needed
- B) `test_pta_tutorial_version.py` will be deleted once onboarding is complete
- C) Both must be kept in sync when changing flows — the tutorial version is heavily commented for onboarding
- D) Only `test_pta_clean_version.py` is run in CI; the tutorial version is skipped

---

**Q85.** In the `driver` fixture, why is `driver_instance.close()` called **before** `driver_instance.quit()`?

- A) `close()` saves the current state before quitting
- B) `close()` closes the current browser tab; `quit()` shuts down the entire browser process — calling both ensures a clean teardown
- C) `close()` is required on Windows; `quit()` works only on Linux
- D) They are interchangeable; order doesn't matter

---

### ✅ Bonus Answers

| Q | Answer | Explanation |
|---|--------|-------------|
| 81 | **B** | "Logger instances created at module level … open `test_execution.log` immediately on import, which locks the file on Windows." — `tests/conftest.py` comment lines 57–61. |
| 82 | **C** | Mixing implicit + explicit waits causes flakiness — a well-known Selenium anti-pattern. Explicit waits give precise, testable conditions. |
| 83 | **B** | `WebDriverWait.until(condition((by, locator)))` — `condition` is the factory (e.g., `EC.presence_of_element_located`) that gets called with the locator tuple to create the actual callable. |
| 84 | **C** | "keep both in sync when changing flows" — explicit rule in CLAUDE.md. |
| 85 | **B** | `close()` closes the current window; `quit()` kills the entire WebDriver session. Calling both is the safe Selenium pattern in the framework's teardown. |

---

## 📊 Score Card

| Score | Level |
|-------|-------|
| 75–85 | ✅ **Expert** — You can architect and extend this framework confidently |
| 60–74 | 🟡 **Advanced** — Strong grasp; review missed questions |
| 45–59 | 🟠 **Intermediate** — Re-read CLAUDE.md + key source files |
| Below 45 | 🔴 **Beginner** — Study the fixture chain, BasePage, and conftest hierarchy |

---

*Good luck with your interviews! 🚀*

