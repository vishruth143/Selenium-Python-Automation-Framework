# Selenium-Python-Automation-Framework
Selenium Python Automation Framework

Environment Variables for UI:
BROWSER=CHROME;HEADLESS=N;REGION=QA
(By default BROWSER is set to 'CHROME' and HEADLESS is set to 'N')

Environment Variables for API:
REGION=QA

To run the tests using command line (powershell):
$env:REGION="qa"; $env:BROWSER="CHROME"; $env:HEADLESS="N"; pytest pta_automation/tests/ui/test_pta.py

To run on docker container:
docker build -t selenium-tests .
docker run -e REGION=qa -e BROWSER=CHROME -e HEADLESS=Y selenium-tests

