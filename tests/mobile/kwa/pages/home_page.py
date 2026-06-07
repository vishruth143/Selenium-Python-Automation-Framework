# pylint: disable = [line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, wrong-import-order]

from appium.webdriver.common.appiumby import AppiumBy
from framework.pages.mobile.base_page import BasePage
from selenium.webdriver.support import expected_conditions as ec

class HomePage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    #                                                  Element locators
    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------Input Fields---------------------------------------------------


    # -----------------------------------------------------Buttons------------------------------------------------------
    _enter_some_value_btn = (AppiumBy.ID, "com.code2lead.kwad:id/EnterValue")
    _contact_us_form_btn = (AppiumBy.ID, "com.code2lead.kwad:id/ContactUs")
    _scroll_view_btn = (AppiumBy.ID, "com.code2lead.kwad:id/ScrollView")
    _tab_activity_btn = (AppiumBy.ID, "com.code2lead.kwad:id/TabView")

    # ------------------------------------------------------Texts-------------------------------------------------------




    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Elements
    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------Input Fields---------------------------------------------------


    # -----------------------------------------------------Buttons------------------------------------------------------
    @property
    def enter_some_value_btn(self):
        return self.find_element(*self._enter_some_value_btn, ec.element_to_be_clickable)

    @property
    def contact_us_form_btn(self):
        return self.find_element(*self._contact_us_form_btn, ec.element_to_be_clickable)

    @property
    def scroll_view_btn(self):
        return self.find_element(*self._scroll_view_btn, ec.element_to_be_clickable)

    @property
    def tab_activity_btn(self):
        return self.find_element(*self._tab_activity_btn, ec.element_to_be_clickable)

    # -----------------------------------------------------texts------------------------------------------------------



    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Actions
    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------Is Visible------------------------------------------------------


    # -----------------------------------------------------Enter/Type------------------------------------------------------


    # -----------------------------------------------------Click------------------------------------------------------
    def click_enter_some_value_btn(self):
        self.click(*self._enter_some_value_btn)

    def click_contact_us_form_btn(self):
        self.click(*self._contact_us_form_btn)

    def click_scroll_view_btn(self):
        self.click(*self._scroll_view_btn)

    def click_tab_activity_btn(self):
        self.click(*self._tab_activity_btn)
