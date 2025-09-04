# pylint: disable=[missing-function-docstring, import-error, invalid-name, global-variable-undefined, ungrouped-imports]
# pylint: disable=[line-too-long, missing-module-docstring, unnecessary-lambda, unused-argument, unspecified-encoding]
# pylint: disable=[missing-module-docstring, missing-function-docstring, redefined-outer-name, ungrouped-imports]

import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.events import EventFiringWebDriver

from framework.listeners.event_listeners import MyEventListener
from config.config_parser import ConfigParser
from framework.utilities.screenshot_utils import get_screenshot_path

@pytest.fixture(scope="session")
def testdata():
    if os.environ["APP_NAME"].upper() == "PTA":
        return ConfigParser.load_config("pta_ui_test_data_config")
    return None


@pytest.fixture(scope="session")
def region():
    region = os.environ.get("REGION", "QA").upper()
    return region

@pytest.fixture()
def driver(request):
    print('-' * 10 + ' Driver - Setup ' + '-' * 10)

    browser = os.environ.get("BROWSER", "CHROME").upper()
    headless = os.environ.get("HEADLESS", "N").upper() == "Y"
    firefox_path = "/usr/bin/firefox-esr"

    def get_driver():
        if browser == "CHROME":
            return webdriver.Chrome(options=create_chrome_options(headless))
        if browser == "FIREFOX":
            return webdriver.Firefox(options=create_firefox_options(headless, firefox_path))
        if browser == "EDGE":
            return webdriver.Edge(options=create_chrome_options(headless)) if headless else webdriver.Edge()
        raise ValueError(f"Unsupported browser: {browser}")

    driver_instance = get_driver()
    driver_instance = EventFiringWebDriver(driver_instance, MyEventListener())
    driver_instance.maximize_window()

    def teardown():
        print('-' * 10 + ' Driver - Teardown ' + '-' * 10)
        driver_instance.close()
        driver_instance.quit()
    request.addfinalizer(teardown)
    return driver_instance

def create_chrome_options(headless: bool):
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("prefs", {
            "profile.managed_default_content_settings.images": 2
        })
    options.add_argument("window-size=1920,1080")
    return options

def create_firefox_options(headless: bool, binary_path: str):
    options = FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    options.binary_location = binary_path
    options.add_argument("window-size=1920,1080")
    return options

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture screenshot only once for failed UI test cases.
    """
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            test_name = item.name
            screenshot_path = get_screenshot_path(test_name)
            driver.save_screenshot(screenshot_path)
