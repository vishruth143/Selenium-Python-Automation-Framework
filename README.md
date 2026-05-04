<!-- markdownlint-disable MD033 MD041 -->
<div align="center">

# 🧪 Selenium-Python-Automation-Framework

**A scalable, maintainable test automation framework for UI, API, Mobile, Performance & Data testing.**

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.43.0-43B02A?logo=selenium&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-9.0.3-blue?logo=pytest&logoColor=white)
![Appium](https://img.shields.io/badge/Appium-5.3.1-purple?logo=appium&logoColor=white)
![Locust](https://img.shields.io/badge/Locust-2.43.4-orange)
![License](https://img.shields.io/badge/License-MIT-green)

Built with Python · Selenium · Pytest · Pytest-BDD · Appium · Locust · Requests

Containerized with Docker · CI/CD via GitHub Actions & Jenkins · Notifications via MS Teams

![Architecture](automation_architecture.png)
![Coverage](automation_coverage.png)

</div>

---

## 📑 Table of Contents

1. [Features](#-features)
2. [Prerequisites](#-prerequisites)
3. [Quick Start](#-quick-start)
4. [Project Structure](#-project-structure)
5. [Locator Naming Conventions](#-locator-naming-conventions)
6. [Environment Variables](#-environment-variables)
7. [Pytest Flag Reference](#-pytest-flag-reference)
8. [Running Tests](#-running-tests)
   - [UI · PTA](#ui--pta)
   - [UI · Heroku](#ui--heroku)
   - [API · JSONPlaceholder](#api--jsonplaceholder)
   - [Mobile · KWA](#mobile--kwa)
   - [Performance · Locust](#performance--locust)
   - [Data Quality · REST Countries](#data-quality--rest-countries)
9. [Reports](#-reports)
   - [HTML Report](#html-report)
   - [Allure Report](#allure-report)
   - [One-Click Executor Scripts](#-one-click-executor-scripts-windows)
10. [Docker](#-docker)
11. [CI/CD Integration](#-cicd-integration)
    - [GitHub Actions](#-github-actions)
    - [Jenkins](#-jenkins)
12. [MS Teams Notifications](#-ms-teams-notifications)
13. [Screen Recording (ffmpeg)](#-screen-recording-ffmpeg)
14. [Inspecting Environment Variables](#-inspecting-environment-variables)
15. [Conventional Commits](#-conventional-commits)
16. [MCP Servers](#-mcp-servers)
17. [Claude · GitHub Integration](#-claude--github-integration)

---

## ✨ Features

| #  | Feature                                                            | Status |
|----|--------------------------------------------------------------------|:------:|
| 1  | 🎭 Selenium · Python · Pytest test automation framework            | ✅     |
| 2  | 🔧 Python programming support                                       | ✅     |
| 3  | 🌐 Cross-browser UI testing (Chrome, Firefox, Edge)                 | ✅     |
| 4  | 🧪 API testing with the `requests` library                          | ✅     |
| 5  | 📊 HTML and Allure reports                                          | ✅     |
| 6  | 🎯 Auto-waits, parallel execution and retry mechanisms              | ✅     |
| 7  | 🔧 CI/CD with Jenkins and GitHub Actions                            | ✅     |
| 8  | 📥 Docker containerization                                          | ✅     |
| 9  | 📢 Microsoft Teams notifications                                    | ✅     |
| 10 | 🧩 BDD support with Pytest-BDD                                      | ✅     |
| 11 | 📂 Data-driven testing with JSON and Excel                          | ✅     |
| 12 | 🗂️ Page Object Model (POM) design pattern                          | ✅     |
| 13 | 🧑‍💻 Custom logging and screenshot capture on failures               | ✅     |
| 14 | ⚙️ Environment-driven configuration management                      | ✅     |
| 15 | 🎥 Screen capture and video recording of failed UI tests            | ✅     |
| 16 | 📱 Mobile testing support with Appium                               | ✅     |
| 17 | 🦗 Performance testing with Locust                                  | ✅     |
| 18 | 🗄️ Data quality testing with REST Countries API                    | ✅     |

---

## 🛠 Prerequisites

Ensure the following tools are installed before setting up the project:

| Tool          | Version | Purpose                                          | Install                                                      |
|---------------|---------|--------------------------------------------------|--------------------------------------------------------------|
| Python        | 3.10+   | Runtime for Pytest, Selenium and all dependencies | [python.org](https://www.python.org/downloads/)              |
| Google Chrome | Latest  | Default browser for test execution               | [chrome](https://www.google.com/chrome/)                     |
| ChromeDriver  | Auto    | Selenium WebDriver for Chrome                    | Auto-managed by Selenium Manager                             |
| Node.js       | 18+     | Required for MCP server tools (optional)         | [nodejs.org](https://nodejs.org/)                            |
| ffmpeg        | Any     | Screen recording for failed UI tests             | [ffmpeg.org](https://ffmpeg.org/download.html)               |
| Git           | Any     | Source control                                   | [git-scm.com](https://git-scm.com/)                          |

> **Note:** Firefox and Edge are also supported. Their respective WebDrivers are managed automatically by Selenium Manager (bundled with Selenium 4.6+).

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/vishruth143/Selenium-Python-Automation-Framework.git
cd Selenium-Python-Automation-Framework
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables (optional)

```powershell
$env:REGION   = "QA"      # default: QA
$env:BROWSER  = "CHROME"  # default: CHROME
$env:HEADLESS = "N"       # default: N
```

### 5. Run tests

```powershell
pytest -vvv -m "pta" -n 4 --reruns 3 `
  --html=output/reports/pta_report.html --self-contained-html `
  --alluredir=output/allure-results `
  --capture=tee-sys --durations=10 tests
```

### 6. Generate the Allure report

```bash
allure generate output/allure-results --clean -o output/allure-report
```

### 7. View the report

- Open `output/reports/pta_report.html` in a browser, **or**
- Serve the Allure report locally:

  ```bash
  python -m http.server 8000
  # Visit http://localhost:8000/output/allure-report
  ```

---

## 🚀 Project Structure

```text
Selenium-Python-Automation-Framework/
├── .claude/
│   └── skills/
│       └── commit-message/
│           └── SKILL.md                                   # AI skill: generate conventional commit messages
│
├── .github/
│   └── workflows/
│       ├── ci.yml                                         # GitHub Actions CI workflow
│       ├── claude-code-review.yml                         # Claude AI automated code review workflow
│       └── claude.yml                                     # Claude AI GitHub integration workflow
│
├── config/                                                # Configuration files
│   ├── api/
│   │   └── jsonplaceholder/
│   │       ├── api_test_data_config.json                  # JSONPlaceholder API test data
│   │       └── api_test_env_config.yml                    # JSONPlaceholder API environment config
│   │
│   ├── data/
│   │   └── restcountries/
│   │       └── data_validation_config.yml                 # Data validation rules (ranges, expected counts, regions)
│   │
│   ├── mobile/
│   │   └── kwa/
│   │       ├── mobile_test_data_config.yml                # Mobile test data
│   │       └── mobile_test_env_config.yml                 # Mobile environment config
│   │
│   ├── performance/
│   │   └── jsonplaceholder/
│   │       └── perf_test_config.yml                       # Locust performance test config
│   │
│   ├── ui/
│   │   ├── heroku/
│   │   │   ├── ui_test_data_config.yml                    # Heroku UI test data
│   │   │   └── ui_test_env_config.yml                     # Heroku UI environment config
│   │   │
│   │   └── pta/
│   │       ├── ui_test_data_config.yml                    # PTA UI test data
│   │       ├── ui_test_env_config.yml                     # PTA UI environment config
│   │       └── ui_test_excel_data_config.xlsx             # Excel-driven test data
│   │
│   ├── categories.json                                    # Allure report failure categories
│   ├── common_config.yml                                  # Shared config
│   └── config_parser.py                                   # Centralized config parser
│
├── executor/                                              # One-click test + report executor scripts
│   ├── heroku_ui_tests_executor.bat
│   ├── jsonplaceholder_api_tests_executor.bat
│   └── pta_ui_tests_executor.bat
│
├── framework/                                             # Core framework
│   ├── app_apk/
│   │   └── Android_Demo_App.apk                           # Android APK for mobile testing
│   ├── interfaces/
│   │   └── api_client.py                                  # HTTP client wrapper (GET/POST/PUT/PATCH/DELETE + OAuth2)
│   ├── listeners/
│   │   └── event_listeners.py                             # Selenium EventFiringWebDriver hooks for auto-logging
│   ├── pages/
│   │   ├── mobile/                                        # Mobile base page objects
│   │   └── ui/
│   │       └── base_page.py                               # BasePage — all shared WebDriver interactions & waits
│   └── utilities/
│       ├── common.py                                      # General helpers (Faker, data utils)
│       ├── custom_logger.py                               # Rotating file logger with colored console output
│       ├── emulator_launcher.py                           # Android emulator auto-start helper
│       ├── loaders.py                                     # YAML / JSON / Excel config loaders
│       ├── screen_recording_utils.py                      # ffmpeg screen recording (start/stop/delete on pass)
│       └── screenshot_utils.py                            # Screenshot capture on test failure
│
├── output/                                                # Auto-generated test artifacts (cleaned each session)
│   ├── allure-report/                                     # Generated Allure HTML report
│   ├── allure-results/                                    # Raw Allure result files (JSON + attachments)
│   ├── healer/                                            # Locator Auto-Healer artifacts (do NOT hand-edit)
│   │   ├── failures.json
│   │   ├── suggestions.json
│   │   ├── patch_report.json
│   │   └── pr_body.md
│   ├── logs/
│   │   └── test_execution.log                             # Merged execution log (per-worker shards merged at session end; 10 MB / 5 backups)
│   ├── reports/                                           # pytest-html self-contained HTML reports
│   ├── screenshots/                                       # PNG screenshots captured on test failure
│   └── videos/                                            # MP4 screen recordings (kept only on failure)
│
├── scripts/                                               # Standalone tooling (not part of the test suite)
│   └── healer/                                            # Locator Auto-Healer — fixes broken locators via Claude
│       ├── prompts/
│       │   └── heal_locator.md                            # Prompt template sent to Claude per failure
│       ├── config.py                                      # Healer constants (paths, thresholds, model name)
│       ├── parse_failures.py                              # Step 1 — parse logs → failures.json
│       ├── heal.py                                        # Step 2 — ask Claude → suggestions.json
│       ├── patcher.py                                     # Step 3 — apply suggestions → patch_report.json
│       ├── open_pr.py                                     # Step 4 — branch + commit + push + open PR
│       └── run_healer.py                                  # Orchestrator: parse → heal → patch → PR
│
├── tests/                                                 # Test suite
│   ├── api/
│   │   ├── jsonplaceholder/
│   │   │   ├── conftest.py                                # JSONPlaceholder fixtures: api_client + testdata
│   │   │   └── test_jsonplaceholder.py                    # JSONPlaceholder API tests
│   │   └── conftest.py                                    # APIClient with base URL + optional OAuth2
│   │
│   ├── data/
│   │   ├── restcountries/
│   │   │   └── test_data_restcountries.py                 # 25 data quality tests (REST Countries API)
│   │   └── conftest.py                                    # Session-scoped API fetch + DataFrame merge
│   │
│   ├── mobile/
│   │   ├── kwa/
│   │   │   ├── pages/
│   │   │   │   ├── contact_us_form_page.py
│   │   │   │   ├── enter_some_value_page.py
│   │   │   │   └── home_page.py
│   │   │   └── test_kwa.py                                # KWA mobile functional tests
│   │   └── conftest.py                                    # Appium server + desired capabilities
│   │
│   ├── performance/
│   │   └── locustfile.py                                  # Locust performance tests — JSONPlaceholder (9 tasks)
│   │
│   ├── snippet/                                           # Reusable code snippets and examples
│   │   ├── test_excel.py
│   │   ├── test_parametrize_mechanism.py
│   │   └── test_retry_mechanism.py
│   │
│   ├── ui/
│   │   ├── heroku/
│   │   │   ├── pages/
│   │   │   │   ├── ab_test_page.py
│   │   │   │   ├── add_remove_elements_page.py
│   │   │   │   ├── basic_auth_page.py
│   │   │   │   ├── broken_images_page.py
│   │   │   │   ├── challenging_dom_page.py
│   │   │   │   ├── digest_auth_page.py
│   │   │   │   ├── disappearing_elements_page.py
│   │   │   │   └── landing_page.py
│   │   │   ├── conftest.py
│   │   │   └── test_heroku.py
│   │   │
│   │   ├── pta/
│   │   │   ├── features/
│   │   │   │   └── pta_app.feature                        # Gherkin feature file for PTA BDD tests
│   │   │   ├── pages/
│   │   │   │   ├── contact_page.py
│   │   │   │   ├── home_page.py
│   │   │   │   └── login_page.py
│   │   │   ├── steps/
│   │   │   │   └── test_pta_app.py                        # pytest-bdd step definitions
│   │   │   ├── test_pta_clean_version.py                  # Minimal-comment variant
│   │   │   └── test_pta_tutorial_version.py               # Tutorial-style commented variant
│   │   │
│   │   └── conftest.py                                    # WebDriver init/teardown, screenshot & video on failure
│   │
│   └── conftest.py                                        # Session fixtures — clean output/, write Allure env props, executor.json, autouse log-context stamping
│
├── tutorial/
│   ├── locator_auto_healer.md                             # Locator Auto-Healer pipeline guide
│   └── tutorial.docx                                      # Framework tutorial document
│
├── resume/
│   └── Vishvambruth_JavagalThimmegowda_QEM_Resume_2026.docx
│
├── .gitignore
├── AGENTS.md                                              # AI coding-agent guidance (concise)
├── CLAUDE.md                                              # AI assistant guidance (commands, architecture, patterns)
├── automation_architecture.drawio                         # Editable architecture diagram (draw.io source)
├── automation_architecture.png                            # Framework architecture diagram
├── automation_coverage.png                                # Test coverage diagram
├── Dockerfile
├── Jenkinsfile
├── pytest.ini
├── README.md
└── requirements.txt
```

---

## 🏷 Locator Naming Conventions

All locators defined in page object classes under `tests/**/pages/` follow a consistent suffix convention so the element type is immediately clear from the variable name alone.

| Element Type       | Suffix      | Example                                                  |
|--------------------|-------------|----------------------------------------------------------|
| Button             | `_btn`      | `_submit_btn = (By.ID, "submit")`                        |
| Text field / Input | `_txt`      | `_page_heading_txt = (By.XPATH, "//h1[...]")`            |
| Input field        | `_input`    | `_username_input = (By.ID, "username")`                  |
| Password field     | `_pwd`      | `_password_pwd = (By.ID, "password")`                    |
| Link / Anchor      | `_lnk`      | `_logout_lnk = (By.XPATH, "//a[...]")`                   |
| Dropdown / Select  | `_ddl`      | `_region_ddl = (By.ID, "region")`                        |
| Checkbox           | `_chk`      | `_remember_me_chk = (By.ID, "remember")`                 |
| Radio button       | `_rdo`      | `_gender_male_rdo = (By.ID, "male")`                     |
| Label / Text span  | `_lbl`      | `_error_message_lbl = (By.ID, "error")`                  |
| Header             | `_hdr`      | `_page_title_hdr = (By.TAG_NAME, "h2")`                  |
| Image              | `_img`      | `_logo_img = (By.CSS_SELECTOR, "img.logo")`              |
| Table              | `_tbl`      | `_results_tbl = (By.ID, "results")`                      |
| List / `<ul>`      | `_lst`      | `_nav_menu_lst = (By.CSS_SELECTOR, "ul.nav")`            |
| List item / `<li>` | `_itm`      | `_cart_item_itm = (By.CSS_SELECTOR, "li.cart-item")`     |
| Form               | `_frm`      | `_login_frm = (By.ID, "login-form")`                     |
| Container / `<div>`| `_ctr`      | `_modal_ctr = (By.ID, "modal")`                          |
| Icon               | `_ico`      | `_search_ico = (By.CSS_SELECTOR, "i.search")`            |
| Textarea           | `_area`     | `_comments_area = (By.ID, "comments")`                   |
| Alert / Toast      | `_alert`    | `_success_alert = (By.CSS_SELECTOR, ".alert")`           |

### Naming Pattern

```python
# Class-level tuple (private by convention): _<descriptive_name>_<suffix>
_username_input    = (By.ID, "username")
_password_input    = (By.ID, "password")
_submit_btn        = (By.ID, "submit")
_error_message_lbl = (By.ID, "error")
```

**Examples from this project:**

```python
# tests/ui/pta/pages/login_page.py
_username_input             = (By.ID, "username")
_password_input             = (By.ID, "password")
_submit_btn                 = (By.ID, "submit")
_logout_btn                 = (By.XPATH, "//a[normalize-space()='Log out']")
_logged_in_successfully_txt = (By.XPATH, "//h1[normalize-space()='Logged In Successfully']")

# tests/ui/heroku/pages/landing_page.py
_ab_testing_lnk          = (By.XPATH, "//a[normalize-space()='A/B Testing']")
_add_remove_elements_lnk = (By.XPATH, "//a[normalize-space()='Add/Remove Elements']")
_broken_images_lnk       = (By.XPATH, "//a[normalize-space()='Broken Images']")
```

> 💡 This convention makes locators self-documenting — no need to inspect the HTML to know what type of element a variable represents.

---

## 🌱 Environment Variables

> **Note:** `APP_NAME`, `SERVICE_NAME`, and `MOBILE_APP_NAME` were previously required to select which app/service/mobile-app to run. They are **no longer needed** — each app folder under `tests/` has its own `conftest.py` that loads the right config automatically based on the test path being collected.

### UI Testing

| Variable   | Description                                                 | Default  | Accepted Values                    | Required |
|------------|-------------------------------------------------------------|----------|------------------------------------|:--------:|
| `REGION`   | Target region/environment                                   | `QA`     | `DEV`, `QA`, `STAGE`, `PROD`       | Optional |
| `BROWSER`  | Browser to run tests on                                     | `CHROME` | `CHROME`, `FIREFOX`, `EDGE`        | Optional |
| `HEADLESS` | Run in headless mode                                        | `N`      | `Y`, `N`                           | Optional |

### API Testing

| Variable | Description               | Default | Accepted Values              | Required |
|----------|---------------------------|---------|------------------------------|:--------:|
| `REGION` | Target region/environment | `QA`    | `DEV`, `QA`, `STAGE`, `PROD` | Optional |

### Mobile Testing

| Variable | Description               | Default | Accepted Values              | Required |
|----------|---------------------------|---------|------------------------------|:--------:|
| `REGION` | Target region/environment | `QA`    | `DEV`, `QA`, `STAGE`, `PROD` | Optional |

---

## 🚩 Pytest Flag Reference

| Flag                    | Description                                                                  |
|-------------------------|------------------------------------------------------------------------------|
| `-v`                    | Verbose output (test names and status)                                       |
| `-vv`                   | More verbose (captured output, fixture info)                                 |
| `-vvv`                  | Most verbose (internal debug logs, detailed fixture steps)                   |
| `-m <expression>`       | Run tests matching marker expression (e.g. `pta or jsonplaceholder`)         |
| `--html=<path>`         | Save HTML report to specified path                                           |
| `--self-contained-html` | Embed CSS/JS into the report (no external files)                             |
| `--capture=tee-sys`     | Show `print()` and log output in both terminal and HTML report               |
| `--durations=10`        | Show top 10 slowest tests                                                    |
| `--maxfail=1`           | Stop after first failure                                                     |
| `--disable-warnings`    | Disable warning output                                                       |
| `--log-cli-level=INFO`  | Console log level (`DEBUG`, `INFO`, `WARNING`, `ERROR`)                      |
| `-n 4`                  | Run tests in parallel using 4 CPU cores (pytest-xdist)                       |
| `--reruns 3`            | Rerun failed tests up to 3 times (pytest-rerunfailures)                      |
| `-s`                    | Disable output capturing — print directly to terminal                        |
| `tests`                 | Path to test suite root                                                      |

---

## 🧪 Running Tests

### UI · PTA

```powershell
$env:REGION="QA"; $env:BROWSER="CHROME"; $env:HEADLESS="N"
pytest -vvv -m "pta" -n 4 --maxfail=1 --log-cli-level=INFO --reruns 3 `
  --html=output/reports/report.html --self-contained-html `
  --alluredir=output/allure-results --capture=tee-sys --durations=10 tests
```

### UI · Heroku

```powershell
$env:REGION="QA"; $env:BROWSER="CHROME"; $env:HEADLESS="N"
pytest -vvv -m "heroku" --maxfail=1 --log-cli-level=INFO --reruns 3 `
  --html=output/reports/hirokuapp_report.html --self-contained-html `
  --alluredir=output/allure-results --capture=tee-sys --durations=10 tests
```

### API · JSONPlaceholder

```powershell
$env:REGION="QA"
pytest -vvv -m "jsonplaceholder" -n 4 --maxfail=1 --log-cli-level=INFO --reruns 3 `
  --html=output/reports/report.html --self-contained-html `
  --alluredir=output/allure-results --capture=tee-sys --durations=10 tests
```

### Mobile · KWA

```powershell
pytest -vvv -m "kwa" --maxfail=1 --log-cli-level=INFO --reruns 3 `
  --html=output/reports/report.html --self-contained-html `
  --alluredir=output/allure-results --capture=tee-sys --durations=10 tests
```

### Performance · Locust

```powershell
# With web UI — open http://localhost:8089 to start/monitor the test
$env:REGION="QA"
locust -f tests/performance/locustfile.py

# Headless (CI/CD)
$env:REGION="QA"
locust -f tests/performance/locustfile.py --headless `
  --host=https://jsonplaceholder.typicode.com -u 10 -r 2 --run-time 60s `
  --html=output/reports/performance_report.html
```

### Data Quality · REST Countries

```powershell
$env:REGION="QA"
pytest -vvv -m "restcountries_data" tests/data/ `
  --html=output/reports/data_report.html --self-contained-html `
  --alluredir=output/allure-results tests
```

---

## 📊 Reports

### HTML Report

Generated automatically when you pass `--html=...` to `pytest`. Open the file in any browser:

```text
output/reports/report.html
```

### Allure Report

#### Step 1 — Install the Allure CLI (one-time)

```powershell
Set-ExecutionPolicy RemoteSigned -scope CurrentUser
iwr -useb get.scoop.sh | iex
scoop install allure
```

#### Step 2 — Run tests and collect results

```powershell
pytest --alluredir=output/allure-results tests
```

#### Step 3 — Generate the report

```powershell
allure generate output/allure-results --clean -o output/allure-report
```

#### Step 4 — Serve and view

```powershell
python -m http.server 8000
# Visit http://localhost:8000/output/allure-report
```

> Press **Ctrl+C** to stop the server when done.

### ⚡ One-Click Executor Scripts (Windows)

The `executor/` folder contains Windows batch scripts that run the full test suite **and** generate + serve the Allure report in a single step.

| Script                                            | Test Suite                | Marker                   | Browser           |
|---------------------------------------------------|---------------------------|--------------------------|-------------------|
| `executor/heroku_ui_tests_executor.bat`           | Heroku UI tests           | `-m "heroku"`            | Chrome (headless) |
| `executor/pta_ui_tests_executor.bat`              | PTA UI tests              | `-m "pta"`               | Chrome (headless) |
| `executor/jsonplaceholder_api_tests_executor.bat` | JSONPlaceholder API tests | `-m "jsonplaceholder"`   | N/A               |

**How to run**

- **Option A — Double-click** the `.bat` file in Windows Explorer.
- **Option B — PowerShell** from the project root:

  ```powershell
  cmd /c executor\heroku_ui_tests_executor.bat
  cmd /c executor\pta_ui_tests_executor.bat
  cmd /c executor\jsonplaceholder_api_tests_executor.bat
  ```

**What each script does**

1. Sets optional env vars (`REGION`, `BROWSER`, `HEADLESS` where applicable)
2. Runs pytest with `-n 4` parallel workers + Allure results + HTML report
3. Validates that `output/allure-results/` exists and is non-empty
4. Generates the Allure report via `allure generate output/allure-results --clean -o output/allure-report`
5. Starts a local HTTP server and opens `http://localhost:8000/output/allure-report` in your default browser

> Press **Ctrl+C** in the terminal to stop the HTTP server.

**Prerequisites**

- Python virtual environment must be activated (`.venv\Scripts\activate`)
- Allure CLI on `PATH` (see [Allure Report](#allure-report))
- Google Chrome installed (for UI executors)

---

## 🐳 Docker

```powershell
# Build the image
docker build -t selenium-python-automation .

# Chrome
docker run -e REGION=qa -e BROWSER=CHROME -e HEADLESS=Y selenium-python-automation `
  pytest -vvv -m "pta or jsonplaceholder" -n 4 --maxfail=1 --log-cli-level=INFO --reruns 3 `
  --html=output/reports/report.html --self-contained-html `
  --alluredir=output/allure-results --capture=tee-sys --durations=10 tests

# Firefox
docker run -e REGION=qa -e BROWSER=FIREFOX -e HEADLESS=Y selenium-python-automation `
  pytest -vvv -m "pta or jsonplaceholder" -n 4 --maxfail=1 --log-cli-level=INFO --reruns 3 `
  --html=output/reports/report.html --self-contained-html `
  --alluredir=output/allure-results --capture=tee-sys --durations=10 tests

# Edge
docker run -e REGION=qa -e BROWSER=EDGE -e HEADLESS=Y selenium-python-automation `
  pytest -vvv -m "pta or jsonplaceholder" -n 4 --maxfail=1 --log-cli-level=INFO --reruns 3 `
  --html=output/reports/report.html --self-contained-html `
  --alluredir=output/allure-results --capture=tee-sys --durations=10 tests
```

---

## 🔁 CI/CD Integration

### 🐙 GitHub Actions

The pipeline triggers automatically when changes are pushed or merged to `main` for any of the following:

- **Folders:** `.github/`, `config/`, `framework/`, `tests/`
- **Files:** `Dockerfile`, `pytest.ini`

**Viewing results**

1. Go to the **Actions** tab in GitHub → select the latest workflow run
2. Download `allure-report.zip` from the **Artifacts** section
3. Extract the zip, open a terminal in the extracted folder and run:

   ```powershell
   python -m http.server 8000
   # Visit http://localhost:8000
   ```

### 🔧 Jenkins

#### Prerequisites

- Jenkins installed and running (default: `http://localhost:8080`)
- Docker installed and accessible to Jenkins
- This repo connected to Jenkins via SCM (Git)

#### One-time setup — create the pipeline job

1. Open Jenkins → **New Item**
2. Enter a name (e.g. `Selenium-Python-Automation-Framework`) → select **Pipeline** → click **OK**
3. Under the **Pipeline** section:
   - Set **Definition** to `Pipeline script from SCM`
   - Set **SCM** to `Git`
   - Enter repo URL: `https://github.com/vishruth143/Selenium-Python-Automation-Framework.git`
   - Set **Script Path** to `Jenkinsfile`
4. Click **Save**

#### Running the pipeline

1. Open the job → click **Build with Parameters**
2. Select **BROWSER**: `CHROME`, `FIREFOX`, or `EDGE`
3. Click **Build**

#### What the pipeline does

| Stage                   | Action                                                                              |
|-------------------------|-------------------------------------------------------------------------------------|
| **Checkout**            | Pulls latest code from Git                                                          |
| **Build Docker Image**  | `docker build -t selenium-python-automation .`                                      |
| **Run Tests**           | Runs `pytest -m "pta or jsonplaceholder"` inside the container with `HEADLESS=Y`   |
| **Copy Results**        | Copies `output/` (reports, logs, screenshots) from container to Jenkins workspace   |
| **Cleanup**             | Removes the test container                                                          |
| **Post**                | Archives `output/reports/report.html` and `output/allure-results/**` as artifacts   |

#### Viewing results

1. Click the build number → **Artifacts** → open `output/reports/report.html`
2. For Allure: download `output/allure-results/`, extract, then run:

   ```powershell
   python -m http.server 8000
   # Visit http://localhost:8000
   ```

---

## 📢 MS Teams Notifications

### In MS Teams

1. Create a Team with a Channel.
2. Click the **`...`** beside the channel and select **Manage channel**.
3. Under **Connectors**, click **Edit**.
4. Search for **Incoming Webhook** and click **Add**.
5. Provide a name for the Incoming Webhook and click **Create**.
6. Copy the Webhook URL.

### In GitHub

1. Go to the repo → **Settings**.
2. In the left panel under **Secrets and variables**, click **Actions**.
3. Click **New repository secret**.
4. **Name:** `TEAMS_WEBHOOK_URL` · **Secret:** *(paste the Webhook URL from MS Teams)*
5. Click **Add secret**.

---

## 🎥 Screen Recording (ffmpeg)

Required to record videos of failed UI tests.

1. Download ffmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html).
2. For Windows, click the **Windows** logo and choose a build (e.g. from `gyan.dev` or `BtbN`).
3. Download the **release full** zip file.
4. Extract the zip and add the `bin` folder to your system `PATH` (e.g. `C:\ffmpeg\bin`).
5. Verify the installation:

   ```powershell
   ffmpeg -version
   ```

---

## 🖥️ Inspecting Environment Variables

### List all environment variables

```powershell
# PowerShell
Get-ChildItem Env:
gci env:           # shorthand
```

```bash
# Bash (Git Bash / Linux / macOS)
env
printenv
```

```cmd
:: CMD
set
```

### Show only the framework's variables (`REGION`, `BROWSER`, `HEADLESS`)

```powershell
# PowerShell
Get-ChildItem Env: | Where-Object { $_.Name -in @("REGION","BROWSER","HEADLESS") }
```

```bash
# Bash
env | grep -E "^(REGION|BROWSER|HEADLESS)="
```

---

## 📝 Conventional Commits

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

```text
<type>(<optional scope>): <short summary>

<optional body — explains WHAT and WHY>

<optional footer — e.g. BREAKING CHANGE, closes #issue>
```

### Type Prefixes

| Prefix     | When to use                                                                       | Example                                                          |
|------------|-----------------------------------------------------------------------------------|------------------------------------------------------------------|
| `feat`     | A new feature                                                                     | `feat(login): add remember-me checkbox`                          |
| `fix`      | A bug fix                                                                         | `fix(logger): release file handlers before output cleanup`       |
| `chore`    | Routine tasks, dependency updates, tooling — no production logic change           | `chore(deps): bump faker 40.13.0 → 40.15.0`                      |
| `docs`     | Documentation-only changes                                                        | `docs(readme): add conventional commits reference`               |
| `style`    | Formatting, whitespace, missing semicolons — no logic change                      | `style: reformat imports in conftest.py`                         |
| `refactor` | Code restructured without fixing a bug or adding a feature                        | `refactor(common): extract login steps into helper method`       |
| `test`     | Adding or updating tests                                                          | `test(pta): add test_pta1.py for login flow`                     |
| `perf`     | Performance improvement                                                           | `perf(conftest): load config once at session scope`              |
| `ci`       | Changes to CI/CD pipeline files (GitHub Actions, Jenkinsfile, Dockerfile)         | `ci: add headless flag to GitHub Actions workflow`               |
| `build`    | Changes affecting the build system or external dependencies                       | `build: upgrade to Python 3.13`                                  |
| `revert`   | Reverts a previous commit                                                         | `revert: revert "feat(login): add remember-me checkbox"`         |

### Scopes

The scope is a short noun describing the section of the codebase affected. Place it in parentheses after the type — e.g. `fix(conftest):`, `feat(login):`, `chore(deps):`.

| Scope             | Refers to                                          |
|-------------------|----------------------------------------------------|
| `deps`            | `requirements.txt` dependency changes              |
| `conftest`        | `tests/conftest.py` or any `conftest.py`           |
| `logger`          | `framework/utilities/custom_logger.py`             |
| `common`          | `framework/utilities/common.py`                    |
| `config`          | `config/` directory                                |
| `pta`             | PTA UI test suite                                  |
| `hirokuapp`       | The Internet Herokuapp UI test suite               |
| `jsonplaceholder` | JSONPlaceholder API test suite                     |
| `performance`     | `tests/performance/`, `config/performance/`        |
| `data`            | `tests/data/`, `config/data/`                      |
| `kwa`             | KWA mobile test suite                              |
| `ci`              | `.github/workflows/`, `Jenkinsfile`, `Dockerfile`  |
| `readme`          | `README.md`                                        |

### Breaking Changes

Add `BREAKING CHANGE:` in the footer **or** append `!` after the type:

```text
feat(config)!: rename region key from 'qa' to 'QA' in env config

BREAKING CHANGE: all config YAML files must now use uppercase region keys.
```

### Quick Examples

```text
feat(pta): add test_pta_clean_version.py with clean login test without tutorial comments

fix(conftest): release log handlers before rmtree to fix Windows file lock

chore(deps): bump faker 40.13.0 → 40.15.0, locust 2.32.x → 2.43.4,
             pylint 3.x → 4.0.5

docs(readme): add conventional commits reference section

test(pta): add detailed tutorial comments to test_pta.py for onboarding
```

---

## 🤖 MCP Servers

This project uses [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers to extend GitHub Copilot with browser automation, filesystem access, REST API testing, database queries, Excel and Word document manipulation.

The configuration file lives at:

```text
%LOCALAPPDATA%\github-copilot\intellij\mcp.json
```

### MCP Server Reference

| Server                 | Package                                       | Purpose                                                              |
|------------------------|-----------------------------------------------|----------------------------------------------------------------------|
| `github`               | GitHub Copilot MCP (remote)                   | GitHub repo, PR, issue, and search management                        |
| `playwright`           | `@playwright/mcp@latest`                      | Browser automation — navigate, click, screenshot, snapshot           |
| `selenium`             | `@angiejones/mcp-selenium`                    | Selenium WebDriver interactions for browser testing                  |
| `filesystem`           | `@modelcontextprotocol/server-filesystem`     | Read/write files within allowed local directories                    |
| `excel`                | `@negokaz/excel-mcp-server`                   | Read, write, and format Excel workbooks                              |
| `rest-api`             | `dkmaker-mcp-rest-api`                        | Test REST API endpoints (base URL: `https://rahulshettyacademy.com/`)|
| `mysql`                | `mysql_mcp_server` (via `uv`)                 | Execute SQL queries against a local MySQL database                   |
| `word-document-server` | `office-word-mcp-server` (via `uvx`)          | Create and manipulate Word `.docx` documents                         |
| `mcp-atlassian`        | `mcp-atlassian` (via `uvx`)                   | Jira and Confluence integration                                      |

### `mcp.json`

```json
{
  "servers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    },
    "selenium": {
      "command": "npx",
      "args": ["-y", "@angiejones/mcp-selenium"]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\<your-username>\\files_claude"
      ]
    },
    "excel": {
      "command": "cmd",
      "args": ["/c", "npx", "--yes", "@negokaz/excel-mcp-server"],
      "env": {
        "EXCEL_MCP_PAGING_CELLS_LIMIT": "4000"
      }
    },
    "rest-api": {
      "command": "node",
      "args": [
        "C:\\Users\\<your-username>\\AppData\\Roaming\\npm\\node_modules\\dkmaker-mcp-rest-api\\build\\index.js"
      ],
      "env": {
        "REST_BASE_URL": "https://rahulshettyacademy.com/",
        "HEADER_Accept": "application/json"
      }
    },
    "mysql": {
      "command": "C:\\Python\\3.13.7\\Scripts\\uv.exe",
      "args": [
        "--directory",
        "C:\\Python\\3.13.7\\Lib\\site-packages",
        "run",
        "mysql_mcp_server"
      ],
      "env": {
        "MYSQL_HOST": "localhost",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "root",
        "MYSQL_PASSWORD": "root",
        "MYSQL_DATABASE": "rahulshettyacademy"
      }
    },
    "word-document-server": {
      "command": "uvx",
      "args": ["--from", "office-word-mcp-server", "word_mcp_server"]
    },
    "mcp-atlassian": {
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "JIRA_URL": "https://your-domain.atlassian.net",
        "JIRA_USERNAME": "your-email@example.com",
        "JIRA_API_TOKEN": "your_jira_api_token_here",
        "CONFLUENCE_URL": "https://your-company.atlassian.net/wiki",
        "CONFLUENCE_USERNAME": "your.email@company.com",
        "CONFLUENCE_API_TOKEN": "your_api_token"
      }
    }
  }
}
```

### Prerequisites

```bash
# Node.js (for npx-based servers)
node --version   # v18+ recommended

# Python uv (for mysql_mcp_server, word-document-server and mcp-atlassian)
pip install uv
# or
winget install astral-sh.uv

# Install the REST API MCP server globally
npm install -g dkmaker-mcp-rest-api
```

> **Note:** Replace `<your-username>` in the paths above with your actual Windows username before using the config.

---

## 🤖 Claude · GitHub Integration

In the Claude Code console, run:

```text
/install-github-app
```

### Prerequisites

Install the GitHub CLI from <https://cli.github.com/>:

- **macOS:** `brew install gh`
- **Windows:** `winget install --id GitHub.cli`
- **Linux:** see installation instructions at <https://github.com/cli/cli#installation>

---

<div align="center">

### 🎭 Happy Testing! 🎭

</div>

