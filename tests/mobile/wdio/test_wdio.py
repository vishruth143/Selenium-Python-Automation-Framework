# pylint: disable = [line-too-long, missing-module-docstring, logging-fstring-interpolation, attribute-defined-outside-init, too-few-public-methods, duplicate-code]

import pytest
from framework.utilities.custom_logger import Logger
from framework.utilities.screenshot_utils import get_screenshot_path
from tests.mobile.wdio.pages.home_page import HomePage
from tests.mobile.wdio.pages.login_page import LoginPage

log = Logger(file_id=__name__.rsplit(".", 1)[1])


@pytest.mark.wdio
class TestWDIODemoApp:
    """Sample test cases for WDIO Native Demo App."""

    def test_wdio_navigate_to_login_screen(self, driver, request):
        """
        Test #01 : Verify navigation to Login / Sign up Form screen.
        Steps:
        01) Tap on the 'Login' card from home screen.
        02) Verify 'LOGIN' button is visible.
        """

        test_name = request.node.name.rsplit("[", 1)[0]
        screenshot_path = get_screenshot_path(test_name)
        self.driver = driver

        self.homepage = HomePage(self.driver)
        self.loginpage = LoginPage(self.driver)

        try:
            log.info(50 * '*')
            log.info("Test #01 : Verify navigation to Login / Sign up Form screen.")
            log.info(50 * '*')

            log.info("STEP 01: Tap on the 'Login' card from home screen.")
            self.homepage.click_login_menu_btn()

            log.info("STEP 02: Verify 'LOGIN' button is visible.")
            assert self.loginpage.is_login_button_visible(), "LOGIN button is not visible"

            log.info("Test #01 : Verify navigation to Login / Sign up Form screen. - Passed")
        except Exception as e:
            self.driver.save_screenshot(screenshot_path)
            log.error(f"Error: {e}")
            log.info("Test #01 : Verify navigation to Login / Sign up Form screen. - Failed")
            raise
