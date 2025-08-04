import pytest
from pytest_bdd import scenarios, given, then, parsers

from framework.utilities.common import Common
from framework.utilities.custom_logger import Logger
from framework.utilities.screenshot_utils import get_screenshot_path
from tests.ui.pta.pages.login_page import LoginPage

# ✅ Apply the marker to all tests in this module
pytestmark = pytest.mark.pta

log = Logger(file_id=__name__.rsplit(".", 1)[0])

# ✅ Update the path based on your folder structure
scenarios('../features/pta_app.feature')

@given("Login to PTA application with sample credentials.", target_fixture="login_result")
def login_to_pta(driver, request, testdata, region):
    log.info("STEP 01: Login to PTA application.")

    test_name = request.node.name.rsplit("[", 1)[0]
    screenshot_path = get_screenshot_path(test_name)

    # Libraries needed
    common = Common(driver, testdata)

    # Pages needed
    loginpage = LoginPage(driver)

    try:
        common.pta_login(region)
        driver.save_screenshot(screenshot_path)
        log.info("Login action performed successfully.")
    except Exception as e:
        driver.save_screenshot(screenshot_path)
        log.error(f"Login Exception: {e}")
        raise

    return {
        "common": common,
        "login_page": loginpage,
        "screenshot_path": screenshot_path,
        "driver": driver
    }

@then(parsers.parse('"Logged In Successfully" text is visible.'))
def verify_logged_in_text(login_result):
    login_page = login_result["login_page"]
    driver = login_result["driver"]
    screenshot_path = login_result["screenshot_path"]

    if login_page.logged_in_successfully_txt_visible():
        log.info("'Logged In Successfully' text is visible.")
    else:
        driver.save_screenshot(screenshot_path)
        log.error("'Logged In Successfully' text is NOT visible.")
        raise AssertionError("'Logged In Successfully' text is not visible.")

@then("Logout from PTA application.")
def logout_from_pta(login_result):
    try:
        log.info("STEP 02: Logout from PTA application.")
        login_result["common"].pta_logout()
        log.info("Logout completed successfully.")
    except Exception as e:
        log.error(f"Logout Exception: {e}")
        raise
