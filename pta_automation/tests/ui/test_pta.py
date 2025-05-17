# pylint: disable=[duplicate-code, line-too-long, attribute-defined-outside-init, missing-module-docstring]
# pylint: disable=[no-else-continue, invalid-name, logging-fstring-interpolation, import-error, too-few-public-methods]
# pylint: disable=[too-many-statements, too-many-branches, unused-variable, too-many-locals, unsubscriptable-object]
# pylint: disable=C0302

import pytest
from pta_automation.framework.utilities.common import Common
from pta_automation.framework.utilities.custom_logger import Logger
from pta_automation.framework.pages.login_page import LoginPage
from pta_automation.framework.utilities.screenshot_utils import get_screenshot_path

log = Logger(file_id=__name__.rsplit(".", 1)[1])

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
        01) Login to PTA application.
        02) Logout of PTA application.
        """
        test_name = request.node.name.rsplit("[", 1)[0]
        screenshot_path = get_screenshot_path(test_name)
        self.driver = driver

        # Libraries needed
        common = Common(self.driver, testdata)

        # Pages needed
        self.loginpage = LoginPage(self.driver)

        try:
            log.info(50 * '*')
            log.info("Test #01 : Verify login to PTA application.")
            log.info(50 * '*')

            # Login to Insights application with appropriate user role
            log.info("STEP 01: Login to PTA application with sample credentials.")
            log.info("Login to PTA application - Started.")
            common.pta_login(region)
            if self.loginpage.logged_in_successfully_txt_visible():
                self.driver.save_screenshot(screenshot_path)
                log.info("'Logged In Successfully' text is visible.")
                log.info("Login to PTA application - Completed Successfully.")
            else:
                self.driver.save_screenshot(screenshot_path)
                log.info("'Logged In Successfully' text is not visible.")
                log.info("Test #01 : Verify PTA Application Login. - Failed")
            # Logout of PTA application
            log.info(" STEP 02: Logout from PTA application.")
            log.info("Logout from PTA application - Started.")
            common.pta_logout()
            log.info("Logout from PTA application - Completed Successfully.")
        except Exception as e:
            self.driver.save_screenshot(screenshot_path)
            log.error(f"Error: {e}")
            log.info("Test #01 : Verify PTA Application Login. - Failed")
            raise

        # @pytest.mark.skip

    def test_pta_login1(self, driver, request, testdata, region):
        """
        Test #01 : Verify PTA Application Login.
        Steps:
        01) Login to PTA application.
        02) Logout of PTA application.
        """
        test_name = request.node.name.rsplit("[", 1)[0]
        screenshot_path = get_screenshot_path(test_name)
        self.driver = driver

        # Libraries needed
        common = Common(self.driver, testdata)

        # Pages needed
        self.loginpage = LoginPage(self.driver)

        try:
            log.info(50 * '*')
            log.info("Test #01 : Verify login to PTA application.")
            log.info(50 * '*')

            # Login to Insights application with appropriate user role
            log.info("STEP 01: Login to PTA application with sample credentials.")
            log.info("Login to PTA application - Started.")
            common.pta_login(region)
            if self.loginpage.logged_in_successfully_txt_visible():
                self.driver.save_screenshot(screenshot_path)
                log.info("'Logged In Successfully' text is visible.")
                log.info("Login to PTA application - Completed Successfully.")
            else:
                self.driver.save_screenshot(screenshot_path)
                log.info("'Logged In Successfully' text is not visible.")
                log.info("Test #01 : Verify PTA Application Login. - Failed")
            # Logout of PTA application
            log.info(" STEP 02: Logout from PTA application.")
            log.info("Logout from PTA application - Started.")
            common.pta_logout()
            log.info("Logout from PTA application - Completed Successfully.")
        except Exception as e:
            self.driver.save_screenshot(screenshot_path)
            log.error(f"Error: {e}")
            log.info("Test #01 : Verify PTA Application Login. - Failed")
            raise
