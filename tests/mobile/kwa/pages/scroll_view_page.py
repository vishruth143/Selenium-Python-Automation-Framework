# pylint: disable = [line-too-long, missing-function-docstring, missing-class-docstring, missing-module-docstring, wrong-import-order]

from appium.webdriver.common.appiumby import AppiumBy
from framework.pages.mobile.base_page import BasePage
from selenium.webdriver.support import expected_conditions as ec


class ScrollViewPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    #                                                  Element locators
    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------Buttons------------------------------------------------------
    _button16 = (AppiumBy.XPATH, "//*[@text='BUTTON16']")

    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Elements
    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------Buttons------------------------------------------------------
    @property
    def button16(self):
        return self.find_element(*self._button16, ec.element_to_be_clickable)

    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Actions
    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------Click------------------------------------------------------
    def scroll_to_button16_and_click(self):
        self.scroll_to_element("BUTTON16")
        self.click(*self._button16)

    def accept_button16_alert(self):
        self.accept_alert()
