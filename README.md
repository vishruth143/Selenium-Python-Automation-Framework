# 🧪 Selenium-Python-Automation-Framework

A robust and scalable test automation framework using **Selenium WebDriver**, **Pytest**, and **Python**. Supports both UI and API testing with environment-driven configuration and Docker integration.

---

## 🚀 Environment Variables

### 🔹 UI Testing
| Variable | Description                                                  | Default  |
|----------|--------------------------------------------------------------|----------|
| `BROWSER` | Browser to run tests on (`CHROME`, `FIREFOX`, `EDGE`)        | `CHROME` |
| `HEADLESS` | Run in headless mode (`Y` or `N`)                            | `N`      |
| `REGION` | Target region/environment (e.g., `QA`, `DEV`, `STAGE`,`PROD`) | *Required* |

### 🔹 API Testing
| Variable | Description                           | Default  |
|----------|---------------------------------------|----------|
| `REGION` | Target API environment    | *Required* |

---

## 🐳 To run on docker container: (PowerShell)

## To build docker image
### `docker build -t selenium-tests .`

## To run on Chrome browser
### `docker run -e REGION=qa -e BROWSER=CHROME -e HEADLESS=Y selenium-tests`

## To run on Firefox browser
### `docker run -e REGION=qa -e BROWSER=FIREFOX -e HEADLESS=Y selenium-tests`

## To run on Edge browser
### `docker run -e REGION=qa -e BROWSER=EDGE -e HEADLESS=Y selenium-tests`


---

## 🖥️ Running Tests from Command Line (PowerShell)

```powershell
$env:REGION="qa"
$env:BROWSER="CHROME"
$env:HEADLESS="N"
pytest pta_automation/tests/ui/test_pta.py