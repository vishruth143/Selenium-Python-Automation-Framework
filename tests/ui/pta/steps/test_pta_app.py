# pylint: disable=[missing-module-docstring, missing-function-docstring, logging-fstring-interpolation]
# pylint: disable=[redefined-outer-name, line-too-long]

import pytest
from pytest_bdd import scenarios, given, when, then

from config.config_parser import ConfigParser
from framework.utilities.common import Common
from framework.utilities.custom_logger import Logger
from framework.utilities.screenshot_utils import get_screenshot_path
from tests.ui.pta.pages.login_page import LoginPage
from tests.ui.pta.pages.home_page import HomePage

pytestmark = pytest.mark.pta
log = Logger(file_id=__name__.rsplit(".", 1)[0])

# ✅ Update this path based on where your .feature file lives
scenarios('../features/pta_app.feature')

# Store context across steps
@pytest.fixture
def context(driver, request, testdata, region):
    test_name = request.node.name.rsplit("[", 1)[0]
    screenshot_path = get_screenshot_path(test_name)

    return {
        "driver": driver,
        "testdata": testdata,
        "region": region,
        "screenshot_path": screenshot_path,
        "common": Common(driver, testdata),
        "login_page": LoginPage(driver),
        "home_page": HomePage(driver)
    }

# -----------------------------------------------
#                  GIVEN
# -----------------------------------------------
@given("the user navigates to the PTA application home page")
def navigate_to_home_page(context):
    log.info("STEP 01: Navigate to PTA application home page.")
    env_config = ConfigParser.load_config("pta_ui_test_env_config").get(context["region"].upper(), {})
    context["driver"].get(env_config["url"])

# -----------------------------------------------
#                  WHEN
# -----------------------------------------------
@when("the user clicks on the 'PRACTICE' link")
def click_practice_link(context):
    log.info("STEP 02: Click on 'PRACTICE' link.")
    context["home_page"].click_practice_lnk()

@when("the user clicks on the 'Test Login Page' link")
def click_test_login_page(context):
    log.info("STEP 03: Click on 'Test Login Page' link.")
    context["login_page"].click_test_login_page_lnk()

@when("the user login to PTA application with valid credentials")
def enter_credentials(context):
    log.info("STEP 04: Enter valid credentials.")
    # You can get username/password from testdata if needed
    context["common"].pta_login(context["region"])

# -----------------------------------------------
#                  THEN
# -----------------------------------------------
@then("the user should see a 'Logged In Successfully' message")
def verify_login_success(context):
    log.info("STEP 05: Verify login success.")
    login_page = context["login_page"]
    driver = context["driver"]
    screenshot_path = context["screenshot_path"]

    if login_page.logged_in_successfully_txt_visible():
        driver.save_screenshot(screenshot_path)
        log.info("'Logged In Successfully' text is visible.")
    else:
        driver.save_screenshot(screenshot_path)
        log.error("'Logged In Successfully' text is NOT visible.")
        raise AssertionError("'Logged In Successfully' text is not visible.")

@then("the user logs out from the PTA application")
def logout(context):
    log.info("STEP 06: Logging out.")
    try:
        context["common"].pta_logout()
        log.info("Logout completed successfully.")
    except Exception as e:
        log.error(f"Logout Exception: {e}")
        raise
