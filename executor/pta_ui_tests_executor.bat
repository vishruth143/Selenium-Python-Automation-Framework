@echo off
cd /d "%~dp0.."

set REGION=QA
set BROWSER=CHROME
set HEADLESS=Y
pytest -vvv -m "pta" -n 4 --log-cli-level=INFO --html=output/reports/report.html --alluredir=output/allure-results --self-contained-html --capture=tee-sys --durations=10 tests

if not exist "output\allure-results\" (
    echo ERROR: allure-results folder does not exist. Please run the tests first.
    exit /b 1
)

dir /b "output\allure-results\" 2>nul | findstr "." >nul
if errorlevel 1 (
    echo ERROR: allure-results folder is empty. Please run the tests first.
    exit /b 1
)

echo Generating Allure Report...
call allure generate output/allure-results --clean -o output/allure-report

echo Serving Allure Report...
start "" "http://localhost:8000/output/allure-report"
python -m http.server 8000
