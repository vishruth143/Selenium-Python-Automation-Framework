# 🧪 Selenium-Python-Automation-Framework

A robust and scalable test automation framework using **Selenium WebDriver**, **Pytest**, and **Python**. Supports both UI and API testing with environment-driven configuration and Docker integration.

![img.png](architecture_diagram.png)

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

    # To build docker image
    docker build -t selenium-tests .
    
    # To run on Chrome browser
    docker run -e REGION=qa -e BROWSER=CHROME -e HEADLESS=Y selenium-tests
    
    # To run on Firefox browser
    docker run -e REGION=qa -e BROWSER=FIREFOX -e HEADLESS=Y selenium-tests
    
    # To run on Edge browser
    docker run -e REGION=qa -e BROWSER=EDGE -e HEADLESS=Y selenium-tests
---
## 🖥️ Running Tests from Command Line (PowerShell)
    
    $env:REGION="qa"
    $env:BROWSER="CHROME"
    $env:HEADLESS="N"
    pytest --html=reports/report.html pta_automation/tests
    
---
## 🖥️ To generate Allure Results
    pytest --alluredir=allure-results pta_automation/tests
    
    # To install allure run the below commands in powershell

    Set-ExecutionPolicy RemoteSigned -scope CurrentUser
    iwr -useb get.scoop.sh | iex
    scoop install allure
    
    
    # To generate Allure Report
    allure generate allure-results --clean -o allure-report
---
## 🖥️ CI / CD
    Any changes made and commit to the files under pta_automation or merge any branch 
    to the main branch the git hub action will trigger and build the project.

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