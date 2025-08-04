# 🧪 Selenium-Python-Automation-Framework

A robust and scalable test automation framework using **Python**, **Selenium WebDriver**, **Pytest**, and **Pytest BDD**. 
Supports both UI and API testing with environment-driven configuration and Docker integration.

![img.png](architecture_diagram.png)

---
## 🚀 Project Folder Structure
```
Selenium-Python-Automation-Framework/
├── .github/
│   └── workflows/
│       └── ci.yml                                          # GitHub Actions CI workflow
│
├── config/                                                 # Configuration files
│   ├── api/
│   │   └── reqres/
│   │       ├── api_test_data_config.json                   # API test data
│   │       └── api_test_env_config.yml                     # API environment config
│   │
│   ├── ui/
│   │   └── pta/
│   │       ├── ui_test_data_config.yml                     # UI test data
│   │       ├── ui_test_env_config.yml                      # UI environment config
│   │       ├── ui_test_excel_data_config.xlsx              # Excel input data
│   │       └── ui_test_excel_data_config_output.xlsx       # Excel output
│   │
│   ├── common_config.yml                                   # Shared config
│   └── config_parser.py                                    # Centralized config parser
│
├── framework/                                              # Core framework
│   ├── interfaces/
│   │   ├── __init__.py
│   │   └── api_client.py                                   # API client wrapper
│   │
│   ├── listeners/
│   │   ├── __init__.py
│   │   └── event_listeners.py                              # Event hooks (e.g., for Selenium)
│   │
│   ├── pages/
│   │   ├── __init__.py
│   │   └── base_page.py                                    # Common page object base class
│   │
│   ├── utilities/                                          # Utility functions
│   │   ├── __init__.py
│   │   ├── common.py                                       # General helpers
│   │   ├── custom_logger.py                                # Logger setup
│   │   ├── loaders.py                                      # Data/config loaders
│   │   └── screenshot_utils.py                             # Screenshot helper
│   │
│   └── __init__.py
│
│   ├── output/                                             # Output directory
│   │   ├── allure-results/                                 # Allure results directory
│   │   ├── logs                                            # Log files directory
│   │       └── test_execution.log                          # Execution log file
│   │   ├── reports/                                        # Reports directory
│   │   ├── screenshots/                                    # Screenshots directory
│
├── tests/                                                  # Test suite
│   ├── api/
│   │   └── reqres/
│   │       ├── __init__.py
│   │       └── test_reqres.py                              # API test cases for Reqres
│   │   ├── __init__.py
│   │   └── conftest.py                                     # API-specific fixtures
│   │
│   ├── ui/
│   │   └── pta/
│   │       ├── features/
│   │       │   ├── pta_app.feature                         # Gherkin feature file for PTA
│   │       ├── pages/
│   │       │   ├── __init__.py
│   │       │   └── login_page.py                           # Page object for login
│   │       ├── steps/
│   │       │   ├── __init__.py
│   │       │   └── test_pta_app.py                         #  Step definitions for PTA
│   │       ├── __init__.py
│   │       ├── test_excel.py                               # Excel-driven UI test
│   │       └── test_pta.py                                 # PTA functional tests
│   │   ├── __init__.py
│   │   └── conftest.py                                     # UI-specific fixtures
│   │
│   ├── __init__.py
│   └── conftest.py                                         # Root-level fixtures
│
├── .gitignore                                              # Files to ignore in git
├── architecture_diagram.png                                # Framework architecture diagram
├── conftest.py                                             # Global fixtures (root scope)
├── Dockerfile                                              # Docker container setup
├── pytest.ini                                              # Pytest configuration
├── README.md                                               # Framework documentation
├── requirements.txt                                        # Python dependencies
├── __init__.py
```
---
## 🚀 Environment Variables

### 🔹 UI Testing
| Variable    | Description                                                   | Default Value | Required/Optional |
|-------------|---------------------------------------------------------------|---------------|-------------------|
| `APP_NAME`  | Short name of application under test (AUT)                    | `None`        | `Required`        | 
| `REGION`    | Target region/environment (e.g., `QA`, `DEV`, `STAGE`,`PROD`) | `QA`          | `Optional`        | 
| `BROWSER`   | Browser to run tests on (`CHROME`, `FIREFOX`, `EDGE`)         | `CHROME`      | `Optional`        |
| `HEADLESS`  | Run in headless mode (`Y` or `N`)                             | `N`           | `Optional`        |


### 🔹 API Testing
| Variable       | Description                                                   | Default | Required/Optional |
|----------------|---------------------------------------------------------------|---------|-------------------|
| `SERVICE_NAME` | Short name of service under test (AUT)                        | `None`  | `Required`        |
| `REGION`       | Target region/environment (e.g., `QA`, `DEV`, `STAGE`,`PROD`) | `QA`    | `Optional`        |

---
## 🖥️ Running Tests from Command Line (PowerShell)
    $env:APP_NAME="PTA"
    $env:SERVICE_NAME="REQRES"
    $env:REGION="qa"
    $env:BROWSER="CHROME"
    $env:HEADLESS="N"
    pytest -vvv -m "pta or reqres" --html=output/reports/pta_report.html --self-contained-html --capture=tee-sys --durations=10 tests
---
### Explanation of Flags
| Variable                | Description                                                            |
|-------------------------|------------------------------------------------------------------------|
| `-v`                    | Verbose output (shows test names and status)                           |
| `-vv`                   | More verbose output (adds captured output, fixture info, etc.)         |
| `-vvv`                  | Most verbose output (adds internal debug logs, detailed fixture steps) |
| `-m <expression>`       | Run tests matching the given marker expression (e.g., `pta or reqres`) |
| `--html=...`            | Save HTML report to specified path                                     |
| `--self-contained-html` | Embed CSS/JS into the report (no external files)                       |
| `--capture=tee-sys`     | Shows print() and log output in both terminal & HTML report            |
| `--durations=10`        | Shows top 10 slowest tests (for optimization)                          |
| `tests`                 | Path to your test suite root                                           | 

---
## 🐳 To run on docker container: (PowerShell)

    # To build docker image
    docker build -t selenium-tests .
    
    # To run on Chrome browser
    docker run -e APP_NAME=PTA -e SERVICE_NAME=REQRES -e REGION=qa -e BROWSER=CHROME -e HEADLESS=Y selenium-tests
    
    # To run on Firefox browser
    docker run -e APP_NAME=PTA -e SERVICE_NAME=REQRES -e REGION=qa -e BROWSER=FIREFOX -e HEADLESS=Y selenium-tests
    
    # To run on Edge browser
    docker run -e APP_NAME=PTA -e SERVICE_NAME=REQRES -e REGION=qa -e BROWSER=EDGE -e HEADLESS=Y selenium-tests

---
## 🖥️ To generate Allure Results
    pytest --alluredir=allure-results tests
    
    # To install allure run the below commands in powershell
    Set-ExecutionPolicy RemoteSigned -scope CurrentUser
    iwr -useb get.scoop.sh | iex
    scoop install allure    
    
    # To generate Allure Report
    allure generate allure-results --clean -o allure-report
---
## 🖥️ CI / CD
    Any changes made and commit to the
    Folder files i.e. '.gihub', 'config', 'framework', 'tests' 
    or
    Files i.e. 'Dockerfile', 'pytest.ini' 
    or 
    merge any branch to the main branch the git hub action will trigger and build the project.

    After the pipeline ran we can download the allure-report as artifact from the 
    github actions

    To view the allure report extract the downloaded 'allure-report.zip' and git 
    bash to the folder
    python -m http.server 8000
    http://localhost:8000    
---
## 🖥️ Notification to MS Team
### On MS Teams
1. Create a Team with Channel in MS Team
2. Click on the ... beside the channel you want the notifications to be sent
3. Under Connector Click 'Edit'
4. Search for Incoming Webhook and Click Add
5. Provide the name for the 'Incoming Webhook' and click on 'Create'
6. Copy the Webhook URL

### On GitHub
1. Go to your workflow and click on the Settings
2. On the left side panel under 'Secrets and variables' Click on Actions
3. Click on the 'New repository secret' 
4. Provide Name=TEAMS_WEBHOOK_URL Secret="<Webhook URL from the MS Teams>"
5. Click on Add secret