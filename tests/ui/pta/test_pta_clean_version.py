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

log = Logger(file_id=__name__.rsplit(".", 1)[1])
ui_test_env_config = ConfigParser.load_config("pta_ui_test_env_config")

@pytest.mark.pta
class TestPTACleanVersion:

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
        self.driver = driver
        env_config = ui_test_env_config.get(region.upper(), {})

        common = Common(self.driver, testdata)

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
                log.info("'Logged In Successfully' text is visible.")
                log.info("Login to PTA application - Completed Successfully.")
            else:
                msg = "'Logged In Successfully' text is not visible. Login verification failed."
                log.error(msg)
                raise AssertionError(msg)

            log.info("STEP 06: Logout of PTA application.")
            log.info("Logout from PTA application - Started.")
            common.pta_logout()
            log.info("Logout from PTA application - Completed Successfully.")

            log.info("Test #01 : Verify PTA Application Login. - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #01 : Verify PTA Application Login. - Failed")
            raise

    # @pytest.mark.skip
    def test_pta_header_links(self, driver, request, testdata, region):
        """
        Test #02 : Verify all header navigation links on the PTA application.
        Steps:
        01) Navigate to PTA application 'Home' page.
        02) Verify 'HOME' link navigates to the home page.
        03) Verify 'PRACTICE' link navigates to the practice page.
        04) Verify 'COURSES' link navigates to the courses page.
        05) Verify 'BLOG' link navigates to the blog page.
        06) Verify 'CONTACT' link navigates to the contact page.
        """
        self.driver = driver
        env_config = ui_test_env_config.get(region.upper(), {})

        self.homepage = HomePage(self.driver)

        # Map of each header link to its click action and URL keyword for verification.
        # Each tuple: (link_label, click_method, expected_url_fragment)
        header_links = [
            ("HOME",     self.homepage.click_home_lnk,     "/"),
            ("PRACTICE", self.homepage.click_practice_lnk, "/practice/"),
            ("COURSES",  self.homepage.click_courses_lnk,  "/courses/"),
            ("BLOG",     self.homepage.click_blog_lnk,     "/blog/"),
            ("CONTACT",  self.homepage.click_contact_lnk,  "/contact/"),
        ]

        try:
            log.info(50 * '*')
            log.info("Test #02 : Verify all header navigation links on the PTA application.")
            log.info(50 * '*')

            log.info("STEP 01: Navigate to PTA application 'Home' page.")
            driver.get(env_config["url"])

            failures = []

            for step_num, (link_label, click_action, expected_fragment) in enumerate(header_links, start=2):
                log.info(f"STEP {step_num:02d}: Verify '{link_label}' header link.")

                # Always return to home before clicking the next header link so the
                # full navigation bar is guaranteed to be present.
                driver.get(env_config["url"])

                log.info(f"  Clicking '{link_label}' link.")
                click_action()

                if self.homepage.is_url_contains(expected_fragment):
                    current_url = self.homepage.get_current_url()
                    log.info(f"  '{link_label}' link navigation - PASSED. Current URL: {current_url}")
                else:
                    current_url = self.homepage.get_current_url()
                    msg = (
                        f"'{link_label}' link navigation - FAILED. "
                        f"Expected URL to contain '{expected_fragment}', "
                        f"but got '{current_url}'."
                    )
                    log.error(msg)
                    failures.append(msg)

            if failures:
                failure_summary = "\n".join(failures)
                log.error(f"Test #02 - The following header link(s) failed:\n{failure_summary}")
                raise AssertionError(
                    f"One or more header links failed:\n{failure_summary}"
                )

            log.info("Test #02 : Verify all header navigation links on the PTA application. - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #02 : Verify all header navigation links on the PTA application. - Failed")
            raise

