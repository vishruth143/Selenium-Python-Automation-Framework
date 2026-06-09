@echo off

REM Move to repository root regardless of where the script is launched from.
cd /d "%~dp0.."

REM Default execution context for Heroku UI tests.
set REGION=QA
set BROWSER=CHROME
set HEADLESS=Y

REM Run Heroku tests with verbose logs, parallel workers, HTML report, and Allure raw results.
pytest -vvv -m "heroku" -n 4 --log-cli-level=INFO --html=output/reports/report.html --alluredir=output/allure-results --self-contained-html --capture=tee-sys --durations=10 tests

REM Guardrail: fail fast if Allure results folder was not produced.
if not exist "output\allure-results\" (
    echo ERROR: allure-results folder does not exist. Please run the tests first.
    exit /b 1
)

REM Guardrail: fail fast if results folder exists but contains no files.
dir /b "output\allure-results\" 2>nul | findstr "." >nul
if errorlevel 1 (
    echo ERROR: allure-results folder is empty. Please run the tests first.
    exit /b 1
)

REM Build a fresh Allure HTML report from the current results set.
echo Generating Allure Report...
call allure generate output/allure-results --clean -o output/allure-report

REM Open the report URL and start a local static server on port 8000.
REM Keep this terminal open; press Ctrl+C to stop the server.
echo Serving Allure Report...
start "" "http://localhost:8000/output/allure-report"
python -m http.server 8000
