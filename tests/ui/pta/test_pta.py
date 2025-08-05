# pylint: disable=[duplicate-code, line-too-long, attribute-defined-outside-init, missing-module-docstring]
# pylint: disable=[no-else-continue, invalid-name, logging-fstring-interpolation, import-error, too-few-public-methods]
# pylint: disable=[too-many-statements, too-many-branches, unused-variable, too-many-locals, unsubscriptable-object]
# pylint: disable=[ungrouped-imports]
# pylint: disable=C0302

import pytest

from config.config_parser import ConfigParser
from framework.utilities.common import Common
from framework.utilities.custom_logger import Logger
from tests.ui.pta.pages.home_page import HomePage
from tests.ui.pta.pages.login_page import LoginPage
from framework.utilities.screenshot_utils import get_screenshot_path

log = Logger(file_id=__name__.rsplit(".", 1)[1])
ui_test_env_config = ConfigParser.load_config("pta_ui_test_env_config")

@pytest.mark.pta
class TestPTA:

    """
    Test cases for PTA Application
    """

    # @pytest.mark.skip
    def test_pta_login(self, driver, request, testdata, region):
        """
        Test #01 : Verify PTA Application Login.
        Steps:
        01) Navigate to PTA application 'Home' page.
        02) Click on 'PRACTICE' link.
        03) Click on 'Test Login Page' link.
        04) Login to PTA application with sample credentials.
        05) Verify 'Logged In Successfully' text is visible.
        06) Logout of PTA application.
        """
        test_name = request.node.name.rsplit("[", 1)[0]
        screenshot_path = get_screenshot_path(test_name)
        self.driver = driver
        # Get the correct env block based on the region
        env_config = ui_test_env_config.get(region.upper(), {})

        # Libraries needed
        common = Common(self.driver, testdata)

        # Pages needed
        self.homepage = HomePage(self.driver)
        self.loginpage = LoginPage(self.driver)


        try:
            log.info(50 * '*')
            log.info("Test #01 : Verify login to PTA application.")
            log.info(50 * '*')

            log.info("STEP 01: Navigate to PTA application 'Home' page.")
            driver.get(env_config["url"])

            log.info("STEP 02: Click on 'PRACTICE' link.")
            self.homepage.click_practice_lnk()

            log.info("STEP 03: Click on 'Test Login Page' link.")
            self.loginpage.click_test_login_page_lnk()

            log.info("STEP 04: Login to PTA application with sample credentials.")
            log.info("Login to PTA application - Started.")
            common.pta_login(region)

            log.info("STEP 05: Verify 'Logged In Successfully' text is visible.")
            if self.loginpage.logged_in_successfully_txt_visible():
                self.driver.save_screenshot(screenshot_path)
                log.info("'Logged In Successfully' text is visible.")
                log.info("Login to PTA application - Completed Successfully.")
            else:
                self.driver.save_screenshot(screenshot_path)
                log.info("'Logged In Successfully' text is not visible.")
                log.info("Test #01 : Verify PTA Application Login. - Failed")

            log.info(" STEP 06: Logout of PTA application.")
            log.info("Logout from PTA application - Started.")
            common.pta_logout()
            log.info("Logout from PTA application - Completed Successfully.")
        except Exception as e:
            self.driver.save_screenshot(screenshot_path)
            log.error(f"Error: {e}")
            log.info("Test #01 : Verify PTA Application Login. - Failed")
            raise
