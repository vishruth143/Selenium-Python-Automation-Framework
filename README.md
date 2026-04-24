# 🧪 Selenium-Python-Automation-Framework

A scalable and maintainable test automation framework built with Python, leveraging Selenium WebDriver, Pytest, Pytest-BDD and Appium-Python-Client.
It supports both UI, API and Mobile test automation, with environment-driven configuration for flexibility.
The framework is fully integrated with Docker for containerized execution, GitHub Actions for CI/CD pipelines, and Microsoft Teams for real-time execution notifications.

![img.png](automation_architecture.png)

![img.png](automation_coverage.png)
---
## Features

| # | Feature | Status |
|---|---------|--------|
| 1 | 🎭 Selenium-Python-Pytest Test Automation framework | ✅ Done |
| 2 | 🔧 Python programming support | ✅ Done |
| 3 | 🌐 Cross-browser UI Automation testing (Chrome, Firefox, Edge) | ✅ Done |
| 4 | 🧪 API testing support with Requests library | ✅ Done |
| 5 | 📊 HTML and Allure test reports | ✅ Done |
| 6 | 🎯 Auto-wait, parallel execution and retry mechanisms | ✅ Done |
| 7 | 🔧 CI/CD integration with Jenkins and GitHub Actions | ✅ Done |
| 8 | 📥 Docker containerization | ✅ Done |
| 9 | 📢 Microsoft Teams notifications | ✅ Done |
| 10 | 🧩 BDD support with Pytest-BDD | ✅ Done |
| 11 | 📂 Data-driven testing with JSON and Excel | ✅ Done |
| 12 | 🗂️ Page Object Model (POM) design pattern | ✅ Done |
| 13 | 🧑‍💻 Custom logging and screenshot capture on failures | ✅ Done |
| 14 | ⚙️ Environment-driven configuration management | ✅ Done |
| 15 | 🎥 Screen capture and video recording of failed UI tests | ✅ Done |
| 16 | 📱 Mobile testing support with Appium | ✅ Done |
| 17 | 🦗 Performance testing integration with Locust | ✅ Done |
| 18 | 🗄️ Data testing with REST Countries API | ✅ Done |

---
## ⚡ Quick Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vishruth143/Selenium-Python-Automation-Framework.git
   cd Selenium-Python-Automation-Framework
   ```
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set environment variables:**
   ```bash
   # Example for UI and API test
   $env:APP_NAME="PTA"
   $env:MOBILE_APP_NAME="KWA"
   $env:SERVICE_NAME="JSONPLACEHOLDER"
   $env:REGION="QA"
   $env:BROWSER="CHROME"
   $env:HEADLESS="N"
   ```
4. **Run tests:**
   ```bash
    pytest -vvv -m "pta" -n 4 --reruns 3 --html=output/reports/pta_report.html --alluredir=output/allure-results --self-contained-html --capture=tee-sys --durations=10 tests
   ```
5. **Generate Allure report:**
   ```bash
   allure generate output/allure-results --clean -o output/allure-report
   ```
6. **View HTML/Allure report:**
   - Open `output/reports/pta_report.html` in browser
   - Or serve Allure report:
     ```bash
     python -m http.server 8000
     # Visit http://localhost:8000/output/allure-report
     ```
---
## 🚀 Project Folder Structure
```
Selenium-Python-Automation-Framework/
├── .claude/
│   └── skills/
│       └── commit-message/
│           └── SKILL.md                                    # AI skill: generate conventional commit messages
│
├── .github/
│   └── workflows/
│       ├── ci.yml                                          # GitHub Actions CI workflow
│       ├── claude-code-review.yml                          # Claude AI automated code review workflow
│       └── claude.yml                                      # Claude AI GitHub integration workflow
│
├── config/                                                 # Configuration files
│   ├── api/
│   │   └── jsonplaceholder/
│   │       ├── api_test_data_config.json                   # JSONPLACEHOLDER API test data
│   │       └── api_test_env_config.yml                     # JSONPLACEHOLDER API environment config
│   │
│   ├── data/
│   │   └── restcountries/
│   │       └── data_validation_config.yml                  # Data validation rules (ranges, expected counts, regions)
│   │
│   ├── mobile/
│   │   └── kwa/
│   │       ├── mobile_test_data_config.yml                 # Mobile test data
│   │       └── mobile_test_env_config.yml                  # Mobile environment config
│   │
│   ├── performance/
│   │   └── jsonplaceholder/
│   │       └── perf_test_config.yml                        # Locust performance test config (users, rate, runtime)
│   │
│   ├── ui/
│   │   ├── heroku/
│   │   │   ├── ui_test_data_config.yml                     # Heroku UI test data
│   │   │   └── ui_test_env_config.yml                      # Heroku UI environment config
│   │   │
│   │   └── pta/
│   │       ├── ui_test_data_config.yml                     # PTA UI test data
│   │       ├── ui_test_env_config.yml                      # PTA UI environment config
│   │       └── ui_test_excel_data_config.xlsx              # Excel-driven test data
│   │
│   ├── categories.json                                     # Allure report failure categories
│   ├── common_config.yml                                   # Shared config
│   └── config_parser.py                                    # Centralized config parser
│
├── executor/                                               # One-click test + report executor scripts
│   ├── heroku_ui_tests_executor.bat                        # Run Heroku UI tests → generate + serve Allure report
│   ├── jsonplaceholder_api_tests_executor.bat              # Run JSONPlaceholder API tests → generate + serve Allure report
│   └── pta_ui_tests_executor.bat                           # Run PTA UI tests → generate + serve Allure report
│
├── framework/                                              # Core framework
│   ├── app_apk/
│   │   └── Android_Demo_App.apk                            # Android APK for mobile testing
│   │
│   ├── interfaces/
│   │   ├── __init__.py
│   │   └── api_client.py                                   # HTTP client wrapper (GET/POST/PUT/PATCH/DELETE + OAuth2)
│   │
│   ├── listeners/
│   │   ├── __init__.py
│   │   └── event_listeners.py                              # Selenium EventFiringWebDriver hooks for auto-logging
│   │
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── mobile/                                         # Mobile base page objects
│   │   └── ui/
│   │       └── base_page.py                                # BasePage — all shared WebDriver interactions & waits
│   │
│   ├── utilities/
│   │   ├── __init__.py
│   │   ├── common.py                                       # General helpers (Faker, data utils)
│   │   ├── custom_logger.py                                # Rotating file logger with colored console output
│   │   ├── emulator_launcher.py                            # Android emulator auto-start helper
│   │   ├── loaders.py                                      # YAML / JSON / Excel config loaders
│   │   ├── screen_recording_utils.py                       # ffmpeg screen recording (start/stop/delete on pass)
│   │   └── screenshot_utils.py                             # Screenshot capture on test failure
│   │
│   └── __init__.py
│
├── output/                                                 # Auto-generated test artifacts (cleaned each session)
│   ├── allure-report/                                      # Generated Allure HTML report
│   ├── allure-results/                                     # Raw Allure result files (JSON + attachments)
│   ├── logs/
│   │   └── test_execution.log                              # Rotating execution log (10 MB / 5 backups)
│   ├── reports/                                            # pytest-html self-contained HTML reports
│   ├── screenshots/                                        # PNG screenshots captured on test failure
│   └── videos/                                             # MP4 screen recordings (kept only on failure)
│
├── tests/                                                  # Test suite
│   ├── api/
│   │   ├── jsonplaceholder/
│   │   │   ├── __init__.py
│   │   │   └── test_jsonplaceholder.py                     # JSONPlaceholder API tests (GET/POST/PUT/PATCH/DELETE)
│   │   ├── __init__.py
│   │   └── conftest.py                                     # API fixtures — APIClient with base URL + optional OAuth2
│   │
│   ├── data/
│   │   ├── restcountries/
│   │   │   ├── __init__.py
│   │   │   └── test_data_restcountries.py                  # 25 data quality tests (REST Countries API)
│   │   ├── __init__.py
│   │   └── conftest.py                                     # Data fixtures (session-scoped API fetch + DataFrame merge)
│   │
│   ├── mobile/
│   │   ├── kwa/
│   │   │   ├── pages/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── contact_us_form_page.py                 # Page object — Contact Us form
│   │   │   │   ├── enter_some_value_page.py                # Page object — Enter Some Value screen
│   │   │   │   └── home_page.py                            # Page object — Home screen
│   │   │   ├── __init__.py
│   │   │   └── test_kwa.py                                 # KWA mobile functional tests
│   │   ├── __init__.py
│   │   └── conftest.py                                     # Mobile fixtures — Appium server + desired capabilities
│   │
│   ├── performance/
│   │   ├── __init__.py
│   │   └── locustfile.py                                   # Locust performance tests — JSONPlaceholder (9 tasks)
│   │
│   ├── snippet/                                            # Reusable code snippets and examples
│   │   ├── __init__.py
│   │   ├── test_excel.py                                   # Excel data-driven test snippet
│   │   ├── test_parametrize_mechanism.py                   # @pytest.mark.parametrize snippet
│   │   └── test_retry_mechanism.py                         # pytest-rerunfailures retry snippet
│   │
│   ├── ui/
│   │   ├── hirokuapp/
│   │   │   ├── pages/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── ab_test_page.py                         # Page object — A/B Testing page
│   │   │   │   ├── add_remove_elements_page.py             # Page object — Add/Remove Elements page
│   │   │   │   ├── basic_auth_page.py                      # Page object — Basic Auth page
│   │   │   │   ├── broken_images_page.py                   # Page object — Broken Images page
│   │   │   │   ├── challenging_dom_page.py                 # Page object — Challenging DOM page
│   │   │   │   ├── digest_auth_page.py                     # Page object — Digest Auth page
│   │   │   │   ├── disappearing_elements_page.py           # Page object — Disappearing Elements page
│   │   │   │   └── landing_page.py                         # Page object — Herokuapp landing page
│   │   │   ├── __init__.py
│   │   │   └── test_heroku.py                              # Heroku UI tests (broken links, A/B, add/remove, auth, images, DOM, digest auth, disappearing elements)
│   │   │
│   │   └── pta/
│   │       ├── features/
│   │       │   └── pta_app.feature                         # Gherkin feature file for PTA BDD tests
│   │       ├── pages/
│   │       │   ├── __init__.py
│   │       │   ├── contact_page.py                         # Page object — Contact page
│   │       │   ├── home_page.py                            # Page object — Home page
│   │       │   └── login_page.py                           # Page object — Login page
│   │       ├── steps/
│   │       │   ├── __init__.py
│   │       │   └── test_pta_app.py                         # pytest-bdd step definitions for PTA
│   │       ├── __init__.py
│   │       ├── test_pta_clean_version.py                   # PTA tests — minimal comments (experienced testers)
│   │       └── test_pta_tutorial_version.py                # PTA tests — full tutorial comments (onboarding)
│   │   ├── __init__.py
│   │   └── conftest.py                                     # UI fixtures — WebDriver init/teardown, screenshot & video on failure
│   │
│   ├── __init__.py
│   └── conftest.py                                         # Session fixtures — clean output/, write Allure environment.properties
│
├── tutorial/
│   └── tutorial.docx                                       # Framework tutorial document (beginner-to-advanced guide)
│
├── .gitignore                                              # Git ignore rules
├── automation_architecture.png                             # Framework architecture diagram
├── automation_coverage.png                                 # Test coverage diagram
├── CLAUDE.md                                               # AI assistant guidance (commands, architecture, patterns)
├── Dockerfile                                              # Docker container setup for headless test execution
├── Jenkinsfile                                             # Jenkins declarative CI/CD pipeline
├── open_allure_report.bat                                  # Standalone: generate + serve existing Allure report
├── pytest.ini                                              # Pytest markers, config, and plugin settings
├── README.md                                               # Framework documentation
└── requirements.txt                                        # Python dependencies
```
---
## 🚀 Environment Variables

### 🔹 UI Testing
| Variable    | Description                                                   | Default Value | Required/Optional |
|-------------|---------------------------------------------------------------|---------------|-------------------|
| `APP_NAME`  | Short name of application under test (AUT) (`PTA`, `HIROKUAPP`) | `None`      | `Required`        | 
| `REGION`    | Target region/environment (e.g., `QA`, `DEV`, `STAGE`,`PROD`) | `QA`          | `Optional`        | 
| `BROWSER`   | Browser to run tests on (`CHROME`, `FIREFOX`, `EDGE`)         | `CHROME`      | `Optional`        |
| `HEADLESS`  | Run in headless mode (`Y` or `N`)                             | `N`           | `Optional`        |

### 🔹 API Testing
| Variable       | Description                                                   | Default | Required/Optional |
|----------------|---------------------------------------------------------------|---------|-------------------|
| `SERVICE_NAME` | Short name of service under test (AUT)                        | `None`  | `Required`        |
| `REGION`       | Target region/environment (e.g., `QA`, `DEV`, `STAGE`,`PROD`) | `QA`    | `Optional`        |

---
### Explanation of Flags
| Variable                | Description                                                            |
|-------------------------|------------------------------------------------------------------------|
| `-v`                    | Verbose output (shows test names and status)                           |
| `-vv`                   | More verbose output (adds captured output, fixture info, etc.)         |
| `-vvv`                  | Most verbose output (adds internal debug logs, detailed fixture steps) |
| `-m <expression>`       | Run tests matching the given marker expression (e.g., `pta or jsonplaceholder`) |
| `--html=...`            | Save HTML report to specified path                                     |
| `--self-contained-html` | Embed CSS/JS into the report (no external files)                       |
| `--capture=tee-sys`     | Shows print() and log output in both terminal & HTML report            |
| `--durations=10`        | Shows top 10 slowest tests (for optimization)                          |
| `--maxfail=1`           | Stop after first failure                                               |
| `--disable-warnings`    | Disable warning output                                                 |
| `--log-cli-level=INFO`  | Set log level for console output (e.g., DEBUG, INFO, WARNING, ERROR)   |
| `-n 4`                  | Run tests in parallel using 4 CPU cores                                |
| `--reruns 3`            | Rerun failed tests up to 3 times                                       |
| `-s`                    | Disable output capturing — prints `print()` statements directly to terminal |
| `tests`                 | Path to your test suite root                                           |

---
## 🖥️ Running PTA UI Tests from Command Line (PowerShell)
```bash
    $env:APP_NAME="PTA"
    $env:REGION="QA"
    $env:BROWSER="CHROME"
    $env:HEADLESS="N"
    pytest -vvv -m "pta" -n 4 --maxfail=1 --log-cli-level=INFO --reruns 3 --html=output/reports/report.html --alluredir=output/allure-results --self-contained-html --capture=tee-sys --durations=10 tests
```

## 🖥️ Running Heroku UI Tests from Command Line (PowerShell)
```bash
    $env:APP_NAME="HEROKU"
    $env:REGION="QA"
    $env:BROWSER="CHROME"
    $env:HEADLESS="N"
    pytest -vvv -m "heroku" --maxfail=1 --log-cli-level=INFO --reruns 3 --html=output/reports/hirokuapp_report.html --alluredir=output/allure-results --self-contained-html --capture=tee-sys --durations=10 tests
```

## 🖥️ Running API Tests from Command Line (PowerShell)
```bash
    $env:SERVICE_NAME="JSONPLACEHOLDER"
    $env:REGION="QA"    
    pytest -vvv -m "jsonplaceholder" -n 4 --maxfail=1 --log-cli-level=INFO --reruns 3 --html=output/reports/report.html --alluredir=output/allure-results --self-contained-html --capture=tee-sys --durations=10 tests
```
## 🖥️ Running Mobile Tests from Command Line (PowerShell)
```bash
    $env:MOBILE_APP_NAME="KWA"       
    pytest -vvv -m "kwa" --maxfail=1 --log-cli-level=INFO --reruns 3 --html=output/reports/report.html --alluredir=output/allure-results --self-contained-html --capture=tee-sys --durations=10 tests
```
## 🦗 Running Performance Tests with Locust (PowerShell)
```bash
    # With web UI — open http://localhost:8089 to start/monitor the test
    $env:REGION="QA"
    locust -f tests/performance/locustfile.py

    # Headless (CI/CD)
    $env:REGION="QA"
    locust -f tests/performance/locustfile.py --headless --host=https://jsonplaceholder.typicode.com -u 10 -r 2 --run-time 60s --html=output/reports/performance_report.html
```
## 🗄️ Running Data Quality Tests (PowerShell)
```bash
    $env:REGION="QA"
    pytest -vvv -m "restcountries_data" tests/data/ --html=output/reports/data_report.html --self-contained-html --alluredir=output/allure-results tests
```
---
## 🖥️ To see all the environment variables currently set, you can run:

**PowerShell:**
```powershell
Get-ChildItem Env:
# or shorthand
gci env:
```

**Bash (Git Bash / Linux / macOS):**
```bash
env
# or
printenv
```

**CMD (Command Prompt):**
```cmd
set
```
---
## 🖥️ If you want to filter and see only the ones you set (APP_NAME, SERVICE_NAME, etc.), you can do:

**PowerShell:**
```powershell
Get-ChildItem Env: | Where-Object { $_.Name -in @("APP_NAME","SERVICE_NAME", "MOBILE_APP_NAME", "REGION","BROWSER","HEADLESS") }
```

**Bash (Git Bash / Linux / macOS):**
```bash
env | grep -E "^(APP_NAME|SERVICE_NAME|MOBILE_APP_NAME|REGION|BROWSER|HEADLESS)="
```   
---
## 🐳 To run on docker container: (PowerShell)

    # To build docker image
    docker build -t selenium-python-automation .
    
    # To run on Chrome browser
    docker run -e APP_NAME=PTA -e SERVICE_NAME=JSONPLACEHOLDER -e REGION=qa -e BROWSER=CHROME -e HEADLESS=Y selenium-python-automation pytest -vvv -m "pta or jsonplaceholder" -n 4 --maxfail=1 --log-cli-level=INFO --reruns 3 --html=output/reports/report.html --alluredir=output/allure-results --self-contained-html --capture=tee-sys --durations=10 tests
    
    # To run on Firefox browser
    docker run -e APP_NAME=PTA -e SERVICE_NAME=JSONPLACEHOLDER -e REGION=qa -e BROWSER=FIREFOX -e HEADLESS=Y selenium-python-automation pytest -vvv -m "pta or jsonplaceholder" -n 4 --maxfail=1 --log-cli-level=INFO --reruns 3 --html=output/reports/report.html --alluredir=output/allure-results --self-contained-html --capture=tee-sys --durations=10 tests
    
    # To run on Edge browser
    docker run -e APP_NAME=PTA -e SERVICE_NAME=JSONPLACEHOLDER -e REGION=qa -e BROWSER=EDGE -e HEADLESS=Y selenium-python-automation pytest -vvv -m "pta or jsonplaceholder" -n 4 --maxfail=1 --log-cli-level=INFO --reruns 3 --html=output/reports/report.html --alluredir=output/allure-results --self-contained-html --capture=tee-sys --durations=10 tests

---
## ⚡ One-Click Executor Scripts (Windows)

The `executor/` folder contains Windows batch scripts that run the full test suite **and** generate + serve the Allure report in a single step — no manual commands needed.

### Available Executors

| Script | Test Suite | App / Service | Browser |
|--------|-----------|---------------|---------|
| `executor/heroku_ui_tests_executor.bat` | Heroku UI tests | `APP_NAME=HEROKU` | Chrome (headless) |
| `executor/pta_ui_tests_executor.bat` | PTA UI tests | `APP_NAME=PTA` | Chrome (headless) |
| `executor/jsonplaceholder_api_tests_executor.bat` | JSONPlaceholder API tests | `SERVICE_NAME=JSONPLACEHOLDER` | N/A |

### How to Run

**Option A — Double-click:**
Navigate to the `executor/` folder in Windows Explorer and double-click the desired `.bat` file.

**Option B — PowerShell terminal:**
```powershell
# From the project root
cmd /c executor\heroku_ui_tests_executor.bat
cmd /c executor\pta_ui_tests_executor.bat
cmd /c executor\jsonplaceholder_api_tests_executor.bat
```

### What Each Script Does
1. Sets the required environment variables (`APP_NAME` / `SERVICE_NAME`, `REGION`, `BROWSER`, `HEADLESS`)
2. Runs pytest with `-n 4` parallel workers, Allure results, and HTML report
3. Validates that `output/allure-results/` exists and is not empty (exits with error if not)
4. Generates the Allure report via `allure generate output/allure-results --clean -o output/allure-report`
5. Opens `http://localhost:8000/output/allure-report` in your default browser and starts a local HTTP server

> Press **Ctrl+C** in the terminal to stop the HTTP server when done viewing the report.

### Prerequisites for Executor Scripts
- Python virtual environment must be activated (`.venv\Scripts\activate`)
- Allure CLI must be on your PATH — install via:
  ```powershell
  Set-ExecutionPolicy RemoteSigned -scope CurrentUser
  iwr -useb get.scoop.sh | iex
  scoop install allure
  ```
- Google Chrome must be installed (for UI executor scripts)

---
## 📊 Allure Report

### Step 1 — Install Allure CLI (once)
```powershell
Set-ExecutionPolicy RemoteSigned -scope CurrentUser
iwr -useb get.scoop.sh | iex
scoop install allure
```

### Step 2 — Run Tests and Collect Results
```powershell
pytest --alluredir=output/allure-results tests
```

### Step 3 — Generate the Allure Report
```powershell
allure generate output/allure-results --clean -o output/allure-report
```

### Step 4 — Serve and View the Report
```powershell
python -m http.server 8000
# Visit http://localhost:8000/output/allure-report
```
> Press **Ctrl+C** to stop the server when done.

---

### ⚡ One-Click: Run Tests + Generate + Open Report
Use the executor scripts to do all of the above in a single double-click:
```powershell
# From the project root
cmd /c executor\jsonplaceholder_api_tests_executor.bat
cmd /c executor\pta_ui_tests_executor.bat
cmd /c executor\heroku_ui_tests_executor.bat
```
     The default browser will automatically open `http://localhost:8000/output/allure-report` when the report is ready.
---
## 🖥️ CI / CD Integration with GitHub Actions and Jenkins

---

### 🐙 GitHub Actions

The pipeline triggers automatically when changes are pushed or merged to `main` for any of the following:

**Folders:** `.github/`, `config/`, `framework/`, `tests/`  
**Files:** `Dockerfile`, `pytest.ini`

**Viewing Results:**
1. Go to the **Actions** tab in GitHub → select the latest workflow run
2. Download `allure-report.zip` from the **Artifacts** section
3. Extract the zip, open a terminal in the extracted folder and run:
   ```powershell
   python -m http.server 8000
   # Visit http://localhost:8000
   ```

---

### 🔧 Jenkins

#### Prerequisites
- Jenkins installed and running (default: `http://localhost:8080`)
- Docker installed and accessible to Jenkins
- This repo connected to Jenkins via SCM (Git)

#### One-Time Setup — Create the Pipeline Job
1. Open Jenkins → **New Item**
2. Enter a name (e.g., `Selenium-Python-Automation-Framework`) → select **Pipeline** → click **OK**
3. Under the **Pipeline** section:
   - Set **Definition** to `Pipeline script from SCM`
   - Set **SCM** to `Git`
   - Enter repo URL: `https://github.com/vishruth143/Selenium-Python-Automation-Framework.git`
   - Set **Script Path** to `Jenkinsfile`
4. Click **Save**

#### Running the Pipeline
1. Open the job → click **Build with Parameters**
2. Select **BROWSER**: `CHROME`, `FIREFOX`, or `EDGE`
3. Click **Build**

#### What the Pipeline Does

| Stage | Action |
|-------|--------|
| **Checkout** | Pulls latest code from Git |
| **Build Docker Image** | `docker build -t selenium-python-automation .` |
| **Run Tests** | Runs `pytest -m "pta or reqres"` inside the container with `HEADLESS=Y` |
| **Copy Results** | Copies `output/` (reports, logs, screenshots) from container to Jenkins workspace |
| **Cleanup** | Removes the test container |
| **Post** | Archives `output/reports/report.html` and `output/allure-results/**` as artifacts |

#### Viewing Results
1. Click the build number → **Artifacts** → open `output/reports/report.html`
2. For Allure: download `output/allure-results/`, extract, then run:
   ```powershell
   python -m http.server 8000
   # Visit http://localhost:8000
   ```


## 🖥️ Notification to MS Team
### On MS Teams
```text
1. Create a Team with Channel in MS Team.
2. Click on the ... beside the channel you want the notifications to be sent and select 'Manage channel'.
3. Under 'Connectors' section Click 'Edit'.
4. Search for 'Incoming Webhook' and click 'Add'.
5. Provide the name for the 'Incoming Webhook' and click on 'Create'.
6. Copy the Webhook URL.
```

### On GitHub
```text
1. Go to your workflow and click on the Settings.
2. On the left side panel under 'Secrets and variables' click on 'Actions'.
3. Click on the 'New repository secret'.
4. Provide Name=TEAMS_WEBHOOK_URL Secret="<Webhook URL from the MS Teams>".
5. Click on 'Add secret'.
```

### Screen Recording for failed UI tests
```text
1. Download and Install ffmpeg from: https://ffmpeg.org/download.html
2. For Windows, click on the “Windows” logo and choose a build (e.g., from gyan.dev or BtbN).
3. Download the “release full” zip file.
4. Extract the zip file and add the bin folder to your system PATH i.e. C:\ffmpeg\bin
5. Verify the installation by running `ffmpeg -version` in your command prompt.
```

---
## 📝 Conventional Commit Message Reference

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) specification for all commit messages.

### ✅ Format
```
<type>(<optional scope>): <short summary>

<optional body — explains WHAT and WHY>

<optional footer — e.g. BREAKING CHANGE, closes #issue>
```

### 🏷️ Commit Type Prefixes

| Prefix | When to use | Example |
|--------|-------------|---------|
| `feat` | A new feature is added | `feat(login): add remember-me checkbox` |
| `fix` | A bug fix | `fix(logger): release file handlers before output cleanup` |
| `chore` | Routine tasks, dependency updates, tooling — no production logic change | `chore(deps): bump selenium 4.41.0 → 4.43.0` |
| `docs` | Documentation changes only | `docs(readme): add conventional commits reference` |
| `style` | Code formatting, whitespace, missing semicolons — no logic change | `style: reformat imports in conftest.py` |
| `refactor` | Code restructured without fixing a bug or adding a feature | `refactor(common): extract login steps into helper method` |
| `test` | Adding or updating tests | `test(pta): add test_pta1.py for login flow` |
| `perf` | Performance improvement | `perf(conftest): load config once at session scope` |
| `ci` | Changes to CI/CD pipeline files (GitHub Actions, Jenkinsfile, Dockerfile) | `ci: add headless flag to GitHub Actions workflow` |
| `build` | Changes that affect the build system or external dependencies | `build: upgrade to Python 3.13` |
| `revert` | Reverts a previous commit | `revert: revert "feat(login): add remember-me checkbox"` |

### 🔍 Scope (optional)
The scope is a short noun describing the section of the codebase affected.  
Place it in parentheses after the type: `fix(conftest):`, `feat(login):`, `chore(deps):`

Common scopes used in this project:

| Scope | Refers to |
|-------|-----------|
| `deps` | `requirements.txt` dependency changes |
| `conftest` | `tests/conftest.py` or any `conftest.py` |
| `logger` | `framework/utilities/custom_logger.py` |
| `common` | `framework/utilities/common.py` |
| `config` | `config/` directory |
| `pta` | PTA UI test suite |
| `hirokuapp` | The Internet Herokuapp UI test suite |
| `jsonplaceholder` | JSONPlaceholder API test suite |
| `performance` | `tests/performance/`, `config/performance/` |
| `data` | `tests/data/`, `config/data/` |
| `kwa` | KWA mobile test suite |
| `ci` | `.github/workflows/`, `Jenkinsfile`, `Dockerfile` |
| `readme` | `README.md` |

### ⚠️ Breaking Changes
If a commit introduces a breaking change, add `BREAKING CHANGE:` in the footer or append `!` after the type:
```
feat(config)!: rename region key from 'qa' to 'QA' in env config

BREAKING CHANGE: all config YAML files must now use uppercase region keys.
```

### 💡 Quick Examples Used in This Project

```
feat(pta): add test_pta_clean_version.py with clean login test without tutorial comments

fix(conftest): release log handlers before rmtree to fix Windows file lock

chore(deps): bump pytest 8.4.2 → 9.0.3, selenium 4.41.0 → 4.43.0, faker 40.11.1 → 40.13.0, requests 2.33.0 → 2.33.1

docs(readme): add conventional commits reference section

test(pta): add detailed tutorial comments to test_pta.py for onboarding
```

---
## 🤖 MCP Servers Configuration

This project uses [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers to extend GitHub Copilot with additional tools (browser automation, file system access, REST API testing, database queries, Excel, and Word document manipulation).

The configuration file is located at:
```
%LOCALAPPDATA%\github-copilot\intellij\mcp.json
```

### `mcp.json`
```json
{
  "servers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest"
      ]
    },
    "selenium": {
      "command": "npx",
      "args": [
        "-y",
        "@angiejones/mcp-selenium"
      ]
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
      "args": [
        "/c",
        "npx",
        "--yes",
        "@negokaz/excel-mcp-server"
      ],
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
    }
  }
}
```

### MCP Server Reference

| Server | Package | Purpose |
|--------|---------|---------|
| `github` | GitHub Copilot MCP (remote) | GitHub repo, PR, issue, and search management |
| `playwright` | `@playwright/mcp@latest` | Browser automation — navigate, click, screenshot, snapshot |
| `selenium` | `@angiejones/mcp-selenium` | Selenium WebDriver interactions for browser testing |
| `filesystem` | `@modelcontextprotocol/server-filesystem` | Read/write files within allowed local directories |
| `excel` | `@negokaz/excel-mcp-server` | Read, write, and format Excel workbooks |
| `rest-api` | `dkmaker-mcp-rest-api` | Test REST API endpoints (base URL: `https://rahulshettyacademy.com/`) |
| `mysql` | `mysql_mcp_server` (via `uv`) | Execute SQL queries against a local MySQL database |
| `word-document-server` | `office-word-mcp-server` (via `uvx`) | Create and manipulate Word `.docx` documents |

### Prerequisites

```bash
# Node.js (for npx-based servers)
node --version   # v18+ recommended

# Python uv (for mysql_mcp_server and word-document-server)
pip install uv
# or
winget install astral-sh.uv

# Install the REST API MCP server globally
npm install -g dkmaker-mcp-rest-api
```

> **Note:** Replace `<your-username>` in the paths above with your actual Windows username before using the config.

---
## 🤖 Calude-Github integration
Open the Claude Code console and execute the below command

```claude
/install-github-app
```

### Prerequisites
Install GitHub CLI from https://cli.github.com/ 

   - macOS: brew install gh
   - Windows: winget install --id GitHub.cli
   - Linux: See installation instructions at https://github.com/cli/cli#installation
   
---
# 🎭 Happy testing! 🎭