# pylint: disable = [line-too-long, missing-function-docstring, missing-class-docstring, missing-module-docstring]

from appium.webdriver.common.appiumby import AppiumBy
from framework.pages.mobile.base_page import BasePage


class LoginPage(BasePage):
    _login_btn = (AppiumBy.ACCESSIBILITY_ID, "button-LOGIN")

    def get_login_button_text(self):
        return self.get_text(*self._login_btn)

    def is_login_button_visible(self):
        return self.is_element_visible(*self._login_btn)
