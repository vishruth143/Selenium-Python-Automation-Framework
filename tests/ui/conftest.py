# pylint: disable=[missing-function-docstring, import-error, invalid-name, global-variable-undefined, ungrouped-imports]
# pylint: disable=[line-too-long, missing-module-docstring, unnecessary-lambda, unused-argument, unspecified-encoding]
# pylint: disable=[missing-module-docstring, missing-function-docstring, redefined-outer-name, ungrouped-imports]
# pylint: disable=[logging-fstring-interpolation, import-outside-toplevel, protected-access, too-many-nested-blocks]
# pylint: disable=[broad-exception-caught, too-many-branches, not-callable]

# =============================================================================
# UI CONFTEST — Fixtures & Hooks for All Browser-Based (UI) Tests
# =============================================================================
#
# This file is automatically loaded by pytest for every test under tests/ui/.
# It provides:
#   1. A "testdata" fixture  — loads app-specific test data from YAML config.
#   2. A "region" fixture    — resolves the target environment (QA, DEV, etc.).
#   3. A "driver" fixture    — creates a Selenium WebDriver for each test,
#                              wraps it with an event listener, starts video
#                              recording, and tears everything down after.
#   4. pytest_runtest_makereport hook — captures a screenshot on test failure
#                              and deletes the video file for passed tests.
#   5. pytest_bdd_after_scenario hook — captures a screenshot when a BDD
#                              scenario fails.
#
# How the fixture chain works:
#   tests/conftest.py  (session) — cleans output/, creates dirs, writes
#                                  environment.properties, categories.json,
#                                  executor.json for Allure.
#       ↓
#   tests/ui/conftest.py (this file) — creates browser, records video,
#                                      captures screenshots on failure.
#       ↓
#   tests/ui/<app>/test_<app>.py — individual test cases use the "driver"
#                                  fixture to interact with the browser.
# =============================================================================

import os
import time
import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.events import EventFiringWebDriver

from framework.listeners.event_listeners import MyEventListener
from config.config_parser import ConfigParser
from framework.utilities.screenshot_utils import get_screenshot_path
from framework.utilities.screen_recording_utils import start_video_recording, stop_video_recording


# =============================================================================
# FIXTURE: testdata (session scope)
# =============================================================================
# Loads the UI test data configuration ONCE per test session.
# The data comes from a YAML file specific to the app under test.
#
# Example:
#   APP_NAME=PTA → loads config/ui/pta/ui_test_data_config.yml
#
# Usage in a test:
#   def test_login(driver, testdata):
#       username = testdata["QA"]["username"]
# =============================================================================
@pytest.fixture(scope="session")
def testdata():
    if os.environ.get("APP_NAME", "").upper() == "PTA":
        return ConfigParser.load_config("pta_ui_test_data_config")
    elif os.environ.get("APP_NAME", "").upper() == "HEROKU":
        return ConfigParser.load_config("heroku_ui_test_data_config")
    return None


# =============================================================================
# FIXTURE: region (session scope)
# =============================================================================
# Reads the REGION environment variable (defaults to "QA") and returns it
# in uppercase.  Tests use this to pick the right block from YAML configs.
#
# Example:
#   REGION=QA → config YAML has a "QA:" block with base_url, credentials, etc.
#
# Usage in a test:
#   def test_login(driver, testdata, region):
#       base_url = testdata[region]["base_url"]
# =============================================================================
@pytest.fixture(scope="session")
def region():
    region = os.environ.get("REGION", "QA").upper()
    return region


# =============================================================================
# FIXTURE: driver (function scope — one fresh browser per test)
# =============================================================================
# This is the core fixture that every UI test depends on.
#
# What it does step-by-step:
#   1. Reads BROWSER env var (CHROME / FIREFOX / EDGE) and HEADLESS flag.
#   2. Creates the appropriate Selenium WebDriver with browser-specific options.
#   3. Wraps the driver in an EventFiringWebDriver so that every navigation,
#      click, and exception is automatically logged via MyEventListener.
#   4. Maximizes the browser window for consistent test execution.
#   5. Starts an ffmpeg video recording of the desktop (saved to output/videos/).
#   6. After the test finishes (pass or fail), the teardown:
#      a. Closes and quits the browser.
#      b. Stops the video recording.
#
# Usage in a test:
#   def test_homepage(driver):
#       driver.get("https://example.com")
#       assert "Example" in driver.title
# =============================================================================
@pytest.fixture()
def driver(request):
    print('-' * 10 + ' Driver - Setup ' + '-' * 10)

    # ── Read browser configuration from environment variables ──
    browser = os.environ.get("BROWSER", "CHROME").upper()
    headless = os.environ.get("HEADLESS", "N").upper() == "Y"
    firefox_path = "/usr/bin/firefox-esr"  # Default binary path for Firefox in Docker/Linux

    # ── Inner helper: instantiate the correct WebDriver ──
    def get_driver():
        if browser == "CHROME":
            return webdriver.Chrome(options=create_chrome_options(headless))
        if browser == "FIREFOX":
            return webdriver.Firefox(options=create_firefox_options(headless, firefox_path))
        if browser == "EDGE":
            return webdriver.Edge(options=create_chrome_options(headless)) if headless else webdriver.Edge()
        raise ValueError(f"Unsupported browser: {browser}")

    # ── Create the browser instance ──
    driver_instance = get_driver()

    # ── Wrap with EventFiringWebDriver ──
    # This adds automatic logging for every navigate, find, click, and exception.
    # The listener class (MyEventListener) is defined in framework/listeners/event_listeners.py.
    driver_instance = EventFiringWebDriver(driver_instance, MyEventListener())

    # ── Maximize the browser window for consistent element visibility ──
    if not headless:
        driver_instance.maximize_window()

    # ── Start video recording (ffmpeg captures the desktop) ──
    # The video file is stored at output/videos/test_<name>_<timestamp>.mp4
    # It will be kept only if the test FAILS; deleted otherwise (see hook below).
    test_name = request.node.name
    video_path = start_video_recording(test_name)
    request.node._video_path = video_path  # Stash the path so the hook can access it later

    # ── Teardown: runs AFTER the test function finishes ──
    def teardown():
        print('-' * 10 + ' Driver - Teardown ' + '-' * 10)
        driver_instance.close()  # Close the current browser tab
        driver_instance.quit()   # Shut down the entire browser process
        stop_video_recording()   # Send 'q' to ffmpeg to stop recording gracefully
    request.addfinalizer(teardown)

    # Return the wrapped driver to the test function
    return driver_instance


# =============================================================================
# HELPER: create_chrome_options
# =============================================================================
# Builds a ChromeOptions object.
#
# In headless mode (HEADLESS=Y) it adds flags needed for running Chrome
# without a visible GUI — common in CI/CD and Docker environments:
#   --headless=new       → use Chrome's new headless mode
#   --no-sandbox         → required in Docker containers
#   --disable-dev-shm-usage → prevents /dev/shm out-of-memory crashes
#   images disabled      → speeds up page loads in headless
#
# The fixed window size (1920x1080) ensures screenshots and videos have
# a consistent resolution regardless of the host display.
# =============================================================================
def create_chrome_options(headless: bool):
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("prefs", {
            "profile.managed_default_content_settings.images": 2
        })
    options.add_argument("--window-size=1920,1080")
    return options


# =============================================================================
# HELPER: create_firefox_options
# =============================================================================
# Builds a FirefoxOptions object.
#   --headless → runs Firefox without a visible window
#   binary_location → path to the Firefox binary (e.g., /usr/bin/firefox-esr
#                     inside the Docker image)
# =============================================================================
def create_firefox_options(headless: bool, binary_path: str):
    options = FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    options.binary_location = binary_path
    options.add_argument("--window-size=1920,1080")
    return options


# =============================================================================
# HOOK: pytest_runtest_makereport
# =============================================================================
# This is a pytest hook that runs automatically after every test phase
# (setup → call → teardown).  We only care about the "call" phase — the
# actual test body execution.
#
# What it does:
#   • On FAILURE:
#       1. Retrieves the WebDriver instance from the test's fixtures.
#       2. Takes a PNG screenshot → saved to output/screenshots/.
#       3. Keeps the video recording file for debugging.
#
#   • On PASS:
#       1. Deletes the video file to save disk space.
#          (Retries up to 10 times because ffmpeg may still hold the file lock.)
#
# Why "tryfirst=True, hookwrapper=True"?
#   - tryfirst  → ensures this hook runs before other plugins (e.g., HTML report)
#                  so the screenshot is available when the report is generated.
#   - hookwrapper → uses "yield" to let the default pytest reporting run first,
#                   then we inspect the result and act on it.
# =============================================================================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture screenshot and retain video only for failed UI test cases.
    """
    # Let pytest generate the test result first
    outcome = yield
    rep = outcome.get_result()

    # We only act on the "call" phase (the actual test body), not setup/teardown
    if rep.when == "call":

        # ── Retrieve the WebDriver instance from the test's fixtures ──
        driver = item.funcargs.get("driver", None)
        if not driver:
            try:
                driver = item._request.getfixturevalue("driver")
                logging.info(f"Driver fixture retrieved via getfixturevalue for test: {item.name}")
            except Exception as e:
                logging.warning(f"Could not retrieve driver fixture via getfixturevalue for test: {item.name}: {e}")

        # ── Stop the video recording (regardless of pass/fail) ──
        video_path = stop_video_recording() or getattr(item, "_video_path", None)
        logging.info(f"Video recording stopped for test: {item.name}, path: {video_path}")

        if rep.failed:
            # ── TEST FAILED — capture a screenshot ──
            if driver:
                test_name = item.name
                screenshot_path = get_screenshot_path(test_name)
                logging.info(f"Test failed: {test_name}. Attempting to save screenshot to: {screenshot_path}")
                try:
                    success = driver.save_screenshot(screenshot_path)
                    if success:
                        logging.info(f"Screenshot successfully captured for failed test: {test_name}, path: {screenshot_path}")
                    else:
                        logging.error(f"driver.save_screenshot returned False for test: {test_name}")
                except Exception as e:
                    logging.error(f"Exception during screenshot capture for test {test_name}: {e}")
            else:
                logging.warning(f"Test failed and driver fixture could not be found for test: {item.name}. Screenshot not captured.")
            # Video file is kept for failed tests — useful for debugging
        else:
            # ── TEST PASSED — delete the video to save disk space ──
            # Retry up to 10 times because ffmpeg may still hold the file lock
            # for a brief moment after being stopped.
            if video_path:
                deleted = False
                for i in range(10):
                    if os.path.exists(video_path):
                        try:
                            os.remove(video_path)
                            logging.info(f"Deleted video file for passed test: {video_path}")
                            deleted = True
                            break
                        except Exception as e:
                            logging.warning(f"Failed to delete video file {video_path} (attempt {i+1}): {e}")
                            time.sleep(0.5)  # Wait 500ms before retrying
                    else:
                        time.sleep(0.5)
                if not deleted:
                    logging.warning(f"Video file not found or could not be deleted for: {video_path}")


# =============================================================================
# HOOK: pytest_bdd_after_scenario (pytest-bdd integration)
# =============================================================================
# This hook is called by the pytest-bdd plugin after each Gherkin scenario
# finishes execution.  If the scenario failed, it captures a screenshot
# the same way as the regular pytest hook above.
#
# Note: This only fires when tests are written using Gherkin .feature files
# and pytest-bdd step definitions (e.g., tests/ui/pta/steps/test_pta_app.py).
# =============================================================================
def pytest_bdd_after_scenario(request, feature, scenario):
    """
    Capture screenshot for failed pytest-bdd scenarios with robust logging and error handling.
    """
    logging.info(f"pytest_bdd_after_scenario called for scenario: {scenario.name}")
    failed = getattr(scenario, "_pytest_bdd_failed", False)
    logging.info(f"Scenario failed status: {failed}")
    if failed:
        try:
            # Get the driver fixture from the current test request
            driver = request.getfixturevalue("driver")
            screenshot_path = get_screenshot_path(scenario.name)
            logging.info(f"Attempting to save screenshot to: {screenshot_path}")
            if hasattr(driver, "save_screenshot"):
                success = driver.save_screenshot(screenshot_path)
                if success:
                    logging.info(f"Screenshot successfully captured for failed scenario: {scenario.name}, path: {screenshot_path}")
                else:
                    logging.error(f"driver.save_screenshot returned False for scenario: {scenario.name}")
            else:
                logging.warning(f"Driver does not support save_screenshot for scenario: {scenario.name}")
        except Exception as e:
            logging.error(f"Exception during screenshot capture for scenario {scenario.name}: {e}")
    else:
        logging.info(f"Scenario passed, no screenshot needed: {scenario.name}")
