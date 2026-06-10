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
9. [Mobile Testing Setup (KWA · Android Emulator)](#-mobile-testing-setup-kwa--android-emulator)
   - [Step 1 — Install Appium and the UiAutomator2 driver](#step-1--install-appium-and-the-uiautomator2-driver)
   - [Step 2 — Create an Android Virtual Device (AVD)](#step-2--create-an-android-virtual-device-avd)
   - [Step 3 — Launch the Android Emulator](#step-3--launch-the-android-emulator)
   - [Step 4 — Verify the environment](#step-4--verify-the-environment)
   - [Step 4a — Install the APK on the emulator (manual)](#step-4a--install-the-apk-on-the-emulator-manual)
   - [Step 4b — Find an App's `APP_PACKAGE` and `APP_ACTIVITY`](#step-4b--find-an-apps-app_package-and-app_activity)
   - [Step 5 — Connect Appium Inspector (optional, for locator discovery)](#step-5--connect-appium-inspector-optional-for-locator-discovery)
   - [Step 6 — Use the `mcp-appium` Server (optional, AI-driven locator discovery)](#step-6--use-the-mcp-appium-server-optional-ai-driven-locator-discovery)
   - [Step 6b — Use the `appium-mcp` Server (npm-published, embedded drivers)](#step-6b--use-the-appium-mcp-server-npm-published-embedded-drivers)
   - [Step 7 — Run the KWA Mobile Tests](#step-7--run-the-kwa-mobile-tests)
   - [Step 8 — Run on LambdaTest Cloud (optional)](#step-8--run-on-lambdatest-cloud-optional)
   - [Troubleshooting](#troubleshooting)
10. [Reports](#-reports)
    - [HTML Report](#html-report)
    - [Allure Report](#allure-report)
    - [One-Click Executor Scripts](#-one-click-executor-scripts-windows)
11. [Docker](#-docker)
12. [CI/CD Integration](#-cicd-integration)
    - [GitHub Actions](#-github-actions)
    - [Jenkins](#-jenkins)
13. [MS Teams Notifications](#-ms-teams-notifications)
14. [Screen Recording (ffmpeg)](#-screen-recording-ffmpeg)
15. [Inspecting Environment Variables](#-inspecting-environment-variables)
16. [Conventional Commits](#-conventional-commits)
17. [MCP Servers](#-mcp-servers)
18. [GitHub Copilot Instructions](#-github-copilot-instructions)
19. [Claude · GitHub Integration](#-claude--github-integration)

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
| Allure CLI    | Latest  | Generate and serve Allure test reports            | [allurereport.org](https://allurereport.org/docs/install/)   |
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
│   │   │   ├── conftest.py                                # KWA fixtures: Appium driver + testdata
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
├── Interview_preparations/                                # Interview prep materials
│   ├── interview_prep_mcq.md                              # Multiple-choice questions for interview preparation
│   └── interview_preparations.docx                        # Detailed interview preparation notes
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

## 📱 Mobile Testing Setup (KWA · Android Emulator)

This section walks you through setting up Android tooling, launching an emulator, and running the KWA mobile test suite end-to-end.

### 🛠 Prerequisites

| Tool                     | Version  | Purpose                                          | Install                                                                                           |
|--------------------------|----------|--------------------------------------------------|---------------------------------------------------------------------------------------------------|
| Java JDK                 | 11+      | Required by Android SDK & Appium                 | [adoptium.net](https://adoptium.net/)                                                             |
| Android Studio           | Latest   | Provides Android SDK, AVD Manager & emulator     | [developer.android.com](https://developer.android.com/studio)                                     |
| Appium Server            | 2.x      | Mobile automation server                         | `npm install -g appium`                                                                           |
| UiAutomator2 driver      | Latest   | Appium driver for Android                        | `appium driver install uiautomator2`                                                              |
| Node.js                  | 18+      | Required by Appium                               | [nodejs.org](https://nodejs.org/)                                                                 |

**Environment variables** — run these **once** in PowerShell to persist them permanently across all sessions:

```powershell
# 1. Set ANDROID_HOME permanently (User scope)
[System.Environment]::SetEnvironmentVariable("ANDROID_HOME", "$env:LOCALAPPDATA\Android\Sdk", [System.EnvironmentVariableTarget]::User)

# 2. Append Android tools to PATH permanently (User scope)
$androidHome = "$env:LOCALAPPDATA\Android\Sdk"
$current = [System.Environment]::GetEnvironmentVariable("Path", "User")
$additions = "$androidHome\emulator;$androidHome\platform-tools;$androidHome\tools"
[System.Environment]::SetEnvironmentVariable("Path", "$current;$additions", [System.EnvironmentVariableTarget]::User)
```

After running the above, **close and reopen** your terminal for the changes to take effect. Verify with:

```powershell
$env:ANDROID_HOME          # should print the SDK path
adb --version              # should print ADB version
emulator -list-avds        # should list your AVDs
```

> ⚠️ Avoid using `$env:Path +=` — that only applies to the **current session** and is lost when the terminal is closed.

---

### Step 1 — Install Appium and the UiAutomator2 driver

```powershell
npm install -g appium
appium driver install uiautomator2
appium driver list   # confirm uiautomator2 is listed as 'installed'
```

Verify Appium is working:

```powershell
appium --version
```

---

### Step 2 — Create an Android Virtual Device (AVD)

1. Open **Android Studio** → click on **Device Manager** (or go to *Tools → Device Manager*).
2. Click + icon and **Create Virtual Device**.
3. Select a device definition — e.g. **Pixel 9 Pro XL** — and click **Next**.
4. Choose a system image (e.g. **API 35, Android 15.0, x86_64**) → download if needed → click **Next**.
5. Set the AVD name to `Pixel_9_Pro_XL` *(this must match the `avd_name` parameter in `framework/utilities/emulator_launcher.py`)*.
6. Click **Finish**.

> **Tip:** You can list all existing AVDs from the command line:

```powershell
emulator -list-avds
```

---

### Step 3 — Launch the Android Emulator

#### Option A — Automatic (recommended)

The framework auto-launches the emulator for you. When you run the KWA tests, `framework/utilities/emulator_launcher.py` is called automatically inside the `driver` fixture:

- Checks if an emulator is already running via `adb devices`.
- If not, starts `emulator -avd Pixel_9_Pro_XL` as a background process.
- Polls `adb devices` until the device appears, then waits for `sys.boot_completed=1`.
- Raises `RuntimeError` if boot does not complete within ~5 minutes.

No manual action needed — just run the tests (Step 5).

#### Option B — Manual launch

Start the emulator yourself before running tests:

```powershell
# Launch by AVD name
emulator -avd Pixel_9_Pro_XL

# Verify it is online
adb devices
# Expected output:
# List of devices attached
# emulator-5554   device
```

Wait until the emulator home screen appears before proceeding.

---

### Step 4 — Verify the environment

Run these checks to confirm everything is wired up correctly before executing tests:

```powershell
# 1. Confirm adb sees the emulator
adb devices

# 2. Confirm Appium can see the device
appium --version

# 3. Check the APK is in place
Test-Path "framework\app_apk\Android_Demo_App.apk"   # should print True

# 4. Inspect the env config (local emulator mode)
Get-Content config\mobile\kwa\mobile_test_env_config.yml
# RUN_ON_CLOUD must be: false
```

---

### Step 4a — Install the APK on the emulator (manual)

The framework installs the APK automatically during test startup, but you can also pre-install it manually to validate the app and package before running tests.

#### Option A — Fresh install (APK not installed yet)

```powershell
adb install -r .\framework\app_apk\Android_Demo_App.apk
```

#### Option B — Replace an existing install and clear app data

```powershell
adb uninstall com.code2lead.kwad
adb install .\framework\app_apk\Android_Demo_App.apk
```

#### Verify install and launch

```powershell
# Confirm package is installed
adb shell pm list packages | Select-String "com.code2lead.kwad"

# Launch app using package/activity
adb shell am start -n com.code2lead.kwad/com.code2lead.kwad.MainActivity

# Optional: verify the foreground activity
adb shell dumpsys activity activities | Select-String "mResumedActivity|topResumedActivity"
```

> If `adb install` fails with `INSTALL_FAILED_VERSION_DOWNGRADE`, uninstall first and install again.

---

### Step 4b — Find an App's `APP_PACKAGE` and `APP_ACTIVITY`

`config/mobile/kwa/mobile_test_env_config.yml` requires two Android-specific values that uniquely identify the app and its launch screen:

```yaml
APP_PACKAGE : com.code2lead.kwad
APP_ACTIVITY : com.code2lead.kwad.MainActivity
```

- **`APP_PACKAGE`** — the Android application ID (e.g. `com.code2lead.kwad`). One value per APK.
- **`APP_ACTIVITY`** — the fully-qualified class name of the activity Appium should launch first (usually the `MAIN` / `LAUNCHER` activity, e.g. `com.code2lead.kwad.MainActivity`).

Use any of the methods below — pick the one that matches your starting point.

#### Option A — APK file is on disk (use `aapt` / `aapt2`)

`aapt` ships with the Android SDK Build-Tools (`%ANDROID_HOME%\build-tools\<version>\aapt.exe`). Note that `aapt.exe` lives directly inside the versioned build-tools folder — there is no `bin` subfolder. Make sure the build-tools folder itself is on `PATH`, then:

```powershell
aapt dump badging .\framework\app_apk\Android_Demo_App.apk | Select-String "package:|launchable-activity"
```

Expected output:

```text
package: name='com.code2lead.kwad' versionCode='1' versionName='1.0'
launchable-activity: name='com.code2lead.kwad.MainActivity'  label='KWA' icon=''
```

- The `name=` after `package:` → `APP_PACKAGE`
- The `name=` after `launchable-activity:` → `APP_ACTIVITY`

> 💡 If `aapt` is not on `PATH`, run it directly: `& "$env:ANDROID_HOME\build-tools\34.0.0\aapt.exe" dump badging .\framework\app_apk\Android_Demo_App.apk`

#### Option B — App is already installed on the emulator/device (use `adb`)

1. **List installed packages** — filter by a keyword to find the app ID:

   ```powershell
   adb shell pm list packages | Select-String "code2lead"
   # package:com.code2lead.kwad
   ```

2. **Get the launcher activity** for that package:

   ```powershell
   adb shell cmd package resolve-activity --brief com.code2lead.kwad
   # com.code2lead.kwad
   # com.code2lead.kwad/.MainActivity
   ```

   The second line is `<package>/<activity>`. A leading `.` means the activity is in the package's root namespace, so `.MainActivity` expands to `com.code2lead.kwad.MainActivity`.

3. **Alternative — launch the app manually and read the foreground activity:**

   ```powershell
   # Launch the app, then run:
   adb shell "dumpsys activity activities | Select-String 'mResumedActivity|topResumedActivity'"
   # ActivityRecord{... com.code2lead.kwad/.MainActivity ...}
   ```

#### Option C — Use the `appium-mcp` / `mcp-appium` server

After starting a session, ask the agent in plain English:

> *"What's the current foreground app's package and activity?"*

The agent calls `appium_mobile_device_info` (or the equivalent `getCurrentPackage` / `getCurrentActivity` capabilities) and returns both values.

#### Option D — Read it from `build.gradle` (if you own the source)

In the app module's `build.gradle`:

```groovy
android {
    defaultConfig {
        applicationId "com.code2lead.kwad"   // → APP_PACKAGE
    }
}
```

The launcher activity is declared in `AndroidManifest.xml`:

```xml
<activity android:name=".MainActivity">
  <intent-filter>
    <action android:name="android.intent.action.MAIN" />
    <category android:name="android.intent.category.LAUNCHER" />
  </intent-filter>
</activity>
```

The `android:name` (resolved against the manifest's `package` attribute) → `APP_ACTIVITY`.

---

### Step 5 — Connect Appium Inspector (optional, for locator discovery)

Appium Inspector is a GUI tool for browsing the element hierarchy of your Android app — useful for finding locators when building or debugging page objects.

#### Prerequisites

- Appium Inspector installed: download from [github.com/appium/appium-inspector/releases](https://github.com/appium/appium-inspector/releases)
- Appium server running and an emulator/device online (see Steps 3–4)

#### 1 — Start the Appium server

```powershell
appium --address 127.0.0.1 --port 4723
```

#### 2 — Open Appium Inspector and configure the connection

Launch Appium Inspector and fill in the **New Session** form under the **Appium Server** tab:

| Field       | Value       |
|-------------|-------------|
| Remote Host | `127.0.0.1` |
| Remote Port | `4723`      |
| Remote Path | `/`         |

#### 3 — Add Desired Capabilities

Switch to **JSON Representation** and paste:

```json
{
  "platformName": "Android",
  "appium:automationName": "UiAutomator2",
  "appium:deviceName": "emulator-5554",
  "appium:app": "C:\\Selenium-Python-Automation-Framework\\framework\\app_apk\\Android_Demo_App.apk",
  "appium:noReset": true
}
```

> **Tip:** Set `"appium:noReset": true` to reuse an already-installed APK. Set it to `false` when you need a clean install.

#### 4 — Start the session

Click **Start Session**. Appium Inspector launches the app on the emulator and displays the element tree on the right alongside a live screenshot on the left.

#### 5 — Inspect elements and copy locators

- Click any element in the screenshot or the XML source tree.
- The **Selected Element** panel shows all attributes (`resource-id`, `content-desc`, `class`, `xpath`, etc.).
- Copy the value and use it in your page object following the framework's locator convention:

  ```python
  _some_element_btn = (AppiumBy.ID, "com.example.app:id/someButton")
  _some_label_txt   = (AppiumBy.XPATH, "//android.widget.TextView[@text='Hello']")
  ```

---

### Step 6 — Use the `mcp-appium` Server (optional, AI-driven locator discovery)

For an AI-assisted alternative to Appium Inspector, this project ships with the [`mcp-appium`](#-mcp-servers) server (custom Node.js Appium MCP). Instead of clicking through a GUI, you can ask GitHub Copilot / Claude in natural language to launch the app, traverse screens, and return locator suggestions ready to paste into your page object.

#### Prerequisites

- `mcp-appium` configured in `%LOCALAPPDATA%\github-copilot\intellij\mcp.json` (see [MCP Servers](#-mcp-servers) for the full block).
- An Android emulator/device online (`adb devices` shows it).
- The KWA APK installed (Appium will install `framework/app_apk/Android_Demo_App.apk` on first launch, or the package `com.code2lead.kwad` if already installed).

#### What the server exposes

The `mcp-appium` server exposes Appium WebDriver primitives as tools the AI agent can call directly:

| Tool                  | Purpose                                                                    |
|-----------------------|----------------------------------------------------------------------------|
| `start_session`       | Auto-detects an iOS simulator or Android emulator/device and starts Appium |
| `launch_app`          | Launches an app by bundle ID (iOS) / package name (Android)                |
| `get_page_source`     | Returns the full XML element hierarchy of the current screen               |
| `get_screenshot_file` | Captures a screenshot and saves it to a temp file                          |
| `find_element`        | Finds an element by `id`, `xpath`, `accessibility id`, `-android uiautomator`, etc. |
| `tap_element`         | Taps an element by its element ID                                          |
| `enter_text`          | Clears and types text into an input field                                  |
| `get_element_text`    | Reads the visible text from an element                                     |
| `simulate_gesture`    | Custom W3C gesture (swipe, scroll, pinch) using normalized coordinates     |
| `press_home_button`   | Sends the app to the background                                            |
| `get_device_logs`     | Pulls device console logs since the last call                              |
| `end_session`         | Tears the Appium session down                                              |

#### Example — Ask the agent to find a locator

In Copilot Chat / Claude, simply prompt:

> *"Launch the KWA app on the emulator and find the locator for the ZOOM button on the home page."*

The agent will autonomously:

1. Call `start_session` (auto-detects `emulator-5554`).
2. Call `launch_app` with `com.code2lead.kwad`.
3. Call `get_page_source` + `get_screenshot_file` to inspect the home screen.
4. Identify the ZOOM button and return a ready-to-paste locator:

   ```python
   _zoom_btn = (AppiumBy.ID, "com.code2lead.kwad:id/Zoom")

   @property
   def zoom_btn(self):
       return self.find_element(*self._zoom_btn, ec.element_to_be_clickable)

   def click_zoom_btn(self):
       self.click(*self._zoom_btn)
   ```

5. Call `end_session` to clean up.

#### When to use which

| Use case                                                       | Tool                          |
|----------------------------------------------------------------|-------------------------------|
| Visually browse the entire element tree, copy attributes by hand | **Appium Inspector** (Step 5) |
| Ask the agent in plain English to discover, verify or patch locators | **mcp-appium** (Step 6)       |
| Run the full pytest suite                                      | **pytest + Appium server**    |

> 💡 The `mcp-appium` server connects to the **same** Appium endpoint (`127.0.0.1:4723`) as the rest of the framework — make sure the Appium server (`appium`) is running before invoking it.

---

### Step 6b — Use the `appium-mcp` Server (npm-published, embedded drivers)

In addition to the legacy `mcp-appium` server above, this project also wires up the official npm package [`appium-mcp`](https://www.npmjs.com/package/appium-mcp) — a richer MCP server that runs Appium drivers **embedded in-process** (no separate `appium` server required) and exposes a much larger toolset for AI-driven mobile automation.

#### Configuration

`appium-mcp` is already declared in `%LOCALAPPDATA%\github-copilot\intellij\mcp.json`:

```json
"appium-mcp": {
  "disabled": false,
  "timeout": 100,
  "type": "stdio",
  "command": "npx",
  "args": ["appium-mcp@latest"],
  "env": {
    "ANDROID_HOME": "C:\\Users\\<you>\\AppData\\Local\\Android\\Sdk",
    "CAPABILITIES_CONFIG": "C:\\Selenium-Python-Automation-Framework\\framework\\config_cap\\capabilities.json"
  }
}
```

The `CAPABILITIES_CONFIG` env var points at `framework/config_cap/capabilities.json` so the agent can pull the same KWA capabilities (`appPackage`, `appActivity`, `app`, `automationName`, etc.) the pytest suite uses.

#### Key differences vs. `mcp-appium` (Step 6)

| Aspect                    | `mcp-appium` (Step 6)                  | `appium-mcp` (Step 6b)                                 |
|---------------------------|----------------------------------------|--------------------------------------------------------|
| Source                    | Local Node script (`@gavrix/appium-mcp`) | npm package `appium-mcp@latest`                        |
| Appium server             | Connects to external `appium` on `:4723` | Drivers embedded — **no external Appium needed**       |
| Device discovery          | Manual capabilities                    | `select_device` lists & auto-selects emulator/device   |
| iOS support               | Limited                                | Full (XCUITest + simulator boot, WDA prebuild)         |
| Toolset                   | ~12 primitives                         | 30+ tools (gestures, AI find, geo, clipboard, perms…)  |
| Best for                  | Lightweight locator probing            | Full exploratory automation + test generation         |

#### Selected tools exposed

| Tool                            | Purpose                                                                  |
|---------------------------------|--------------------------------------------------------------------------|
| `select_device`                 | Lists Android/iOS devices and auto-selects when only one is connected    |
| `appium_session_management`     | `create` / `delete` / `list` / `attach` / `select` Appium sessions       |
| `appium_app_lifecycle`          | `activate`, `terminate`, `install`, `query_state`, `clear`, `deep_link`  |
| `appium_find_element`           | Find element by `accessibility id`, `id`, `-android uiautomator`, xpath… |
| `appium_gesture`                | `tap`, `double_tap`, `long_press`, `scroll`, `swipe`, `pinch_zoom`, `back` |
| `appium_drag_and_drop`          | Drag-and-drop with element or coordinate source/target                   |
| `appium_set_value` / `appium_get_text` | Type into / read text from an element                              |
| `appium_mobile_keyboard`        | `hide` / `is_shown` for the soft keyboard                                |
| `appium_screenshot`             | Full-screen or per-element PNG capture                                   |
| `appium_get_page_source`        | XML element hierarchy of current screen                                  |
| `generate_locators`             | Snapshot of all interactable elements with locator suggestions           |
| `appium_generate_tests`         | Drives the live session through given steps and emits test code         |
| `appium_geolocation`            | `get` / `set` / `reset` GPS coordinates                                  |
| `appium_mobile_clipboard`       | Read/write the device clipboard                                          |
| `appium_mobile_permissions`     | Grant/revoke runtime permissions (Android) or privacy services (iOS)    |
| `appium_screen_recording`       | `start` / `stop` MP4 recording                                           |

> See the full list at [npmjs.com/package/appium-mcp](https://www.npmjs.com/package/appium-mcp).

#### Example — open KWA, click HYBRID, type "VISHVA", click SUBMIT

In Copilot Chat / Claude, simply prompt:

> *"Use appium-mcp to open the KWA app on the emulator, click the HYBRID button, type VISHVA into the text input, then click SUBMIT."*

The agent autonomously:

1. `select_device` → picks `emulator-5554` (Pixel_9_Pro_XL).
2. `appium_session_management action=create` → starts an embedded UiAutomator2 session with `com.code2lead.kwad` from `capabilities.json`.
3. `appium_find_element strategy="-android uiautomator" selector='new UiSelector().text("HYBRID")'` → returns element UUID.
4. `appium_gesture action=tap` on that UUID.
5. `appium_find_element` for the EditText → `appium_set_value text="VISHVA"`.
6. `appium_mobile_keyboard action=hide`.
7. `appium_find_element` for `text("SUBMIT")` → `appium_gesture action=tap`.
8. `appium_screenshot` to confirm the result.

#### Generating a pytest from a recorded flow

After driving a flow interactively, ask the agent:

> *"Now use appium_generate_tests to emit the pytest version of the steps above for `tests/mobile/kwa/`."*

Move locators into a page object under `framework/pages/mobile/` (extending `BasePage`), and keep the test thin per the framework's POM convention.

#### Troubleshooting

| Symptom                                                                 | Fix                                                                                       |
|-------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| `'GET /screenshot' cannot be proxied… instrumentation process is not running` | `appium_session_management action=delete` then `create` again — UiAutomator2 sometimes crashes on first launch with `disableWindowAnimation` |
| `npx` not found                                                         | Install Node.js LTS                                                                       |
| No devices listed by `select_device`                                    | Start the emulator (`emulator -avd Pixel_9_Pro_XL`) or plug a device with USB debugging   |
| Driver download slow on first run                                       | Normal — UiAutomator2 driver is fetched once and cached                                   |
| Capabilities ignored                                                    | Validate `framework/config_cap/capabilities.json`; pass overrides via the `capabilities` arg of `appium_session_management` |

---

### Step 7 — Run the KWA Mobile Tests

```powershell
# Activate the virtual environment first
.venv\Scripts\activate

# Run all KWA mobile tests
pytest -vvv -m "kwa" --maxfail=1 --log-cli-level=INFO --reruns 3 `
  --html=output/reports/kwa_mobile_report.html --self-contained-html `
  --alluredir=output/allure-results --capture=tee-sys --durations=10 tests
```

The framework will automatically:
1. Start a local Appium server (`tests/mobile/conftest.py`).
2. Launch the emulator if it is not already running.
3. Install and launch `Android_Demo_App.apk` on the emulator.
4. Execute the two KWA test cases (`test_kwa_enter_some_value`, `test_kwa_contact_us_form`).
5. Stop the Appium server after the session ends.

---

### Step 8 — Run on LambdaTest Cloud (optional)

To run on a real cloud device instead of a local emulator:

1. Sign up at [lambdatest.com](https://www.lambdatest.com/) and upload the APK to LambdaTest App Center.
2. Copy your **Username**, **Access Key**, and the uploaded **App ID**.
3. Update `config/mobile/kwa/mobile_test_env_config.yml`:

   ```yaml
   RUN_ON_CLOUD: true
   CLOUD_PROVIDER: lambdatest
   IS_VIRTUAL_DEVICE: true          # true = emulator, false = real device
   LAMBDATEST_USERNAME: <your-username>
   LAMBDATEST_ACCESS_KEY: <your-access-key>
   APP: lt://APP<your-app-id>       # app ID from LambdaTest App Center
   ```

4. Run the same pytest command from Step 7 — the `driver` fixture detects `RUN_ON_CLOUD: true` and connects to `hub.lambdatest.com` instead of the local Appium server.

---

### Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `adb: command not found` | `platform-tools` not on `PATH` | Add `$ANDROID_HOME\platform-tools` to `PATH` |
| `emulator: command not found` | `emulator` not on `PATH` | Add `$ANDROID_HOME\emulator` to `PATH` |
| `Emulator did not appear in adb devices` | AVD name mismatch | Run `emulator -list-avds` and check it matches `avd_name` in `emulator_launcher.py` |
| `Appium server failed to start` | Port 4723 in use or Appium not installed | Run `appium` manually to see the error; kill any process on port 4723 |
| `FileNotFoundError: APK file not found` | APK missing from `framework/app_apk/` | Ensure `Android_Demo_App.apk` exists at `framework/app_apk/Android_Demo_App.apk` |
| `SessionNotCreatedException` | UiAutomator2 driver not installed | Run `appium driver install uiautomator2` |

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
    },
    "mcp-appium": {
      "command": "C:\\Program Files\\nodejs\\node.exe",
      "args": [
        "C:\\@gavrix\\appium-mcp\\server.js"
      ]
    },
    "appium-mcp": {
      "disabled": false,
      "timeout": 100,
      "type": "stdio",
      "command": "npx",
      "args": ["appium-mcp@latest"],
      "env": {
        "ANDROID_HOME": "C:\\Users\\<your-username>\\AppData\\Local\\Android\\Sdk",
        "CAPABILITIES_CONFIG": "C:\\Selenium-Python-Automation-Framework\\framework\\config_cap\\capabilities.json"
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

## 🤖 GitHub Copilot Instructions

Project-specific Copilot guidance lives in [`/.github/copilot-instructions.md`](./.github/copilot-instructions.md).

Use that file for repository-specific coding rules such as:

- layered POM and per-app config auto-discovery
- marker-based test routing
- no central `APP_NAME` / `SERVICE_NAME` / `MOBILE_APP_NAME` branching
- `BasePage`-driven Selenium interactions
- validation and commit conventions for this repository

For broader agent guidance, also see `AGENTS.md` and `CLAUDE.md`.

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

