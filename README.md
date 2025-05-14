# 🧪 Selenium-Python-Automation-Framework

A robust and scalable test automation framework using **Selenium WebDriver**, **Pytest**, and **Python**. Supports both UI and API testing with environment-driven configuration and Docker integration.

---

## 🚀 Environment Variables

### 🔹 UI Testing
| Variable | Description                           | Default  |
|----------|---------------------------------------|----------|
| `BROWSER` | Browser to run tests on (`CHROME`, `FIREFOX`, `EDGE`) | `CHROME` |
| `HEADLESS` | Run in headless mode (`Y` or `N`)    | `N`      |
| `REGION` | Target region/environment (e.g., `QA`, `DEV`, `PROD`) | *Required* |

### 🔹 API Testing
| Variable | Description                           | Default  |
|----------|---------------------------------------|----------|
| `REGION` | Target API environment    | *Required* |

---

## 🐳 To run on docker container: (PowerShell)

docker build -t selenium-tests .

docker run -e REGION=qa -e BROWSER=CHROME -e HEADLESS=Y selenium-tests

---

## 🖥️ Running Tests from Command Line (PowerShell)

```powershell
$env:REGION="qa"
$env:BROWSER="CHROME"
$env:HEADLESS="N"
pytest pta_automation/tests/ui/test_pta.py