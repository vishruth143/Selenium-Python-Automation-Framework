# pylint: disable = [line-too-long, missing-function-docstring, missing-class-docstring, missing-module-docstring]

from appium.webdriver.common.appiumby import AppiumBy
from framework.pages.mobile.base_page import BasePage


class HomePage(BasePage):
    _login_menu_btn = (AppiumBy.ACCESSIBILITY_ID, "Login")

    def click_login_menu_btn(self):
        self.click(*self._login_menu_btn)
