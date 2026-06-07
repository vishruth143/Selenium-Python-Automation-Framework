# pylint: disable = [line-too-long, missing-function-docstring, missing-class-docstring, missing-module-docstring, wrong-import-order]

from appium.webdriver.common.appiumby import AppiumBy
from framework.pages.mobile.base_page import BasePage
from selenium.webdriver.support import expected_conditions as ec


class TabActivityPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    #                                                  Element locators
    # ------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------Containers----------------------------------------------------
    _tab_layout = (AppiumBy.ID, "com.code2lead.kwad:id/tabLayout")
    _view_pager = (AppiumBy.ID, "com.code2lead.kwad:id/viewPager")

    # ------------------------------------------------------Tabs--------------------------------------------------------
    _home_tab = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Home")')
    _sport_tab = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Sport")')
    _movie_tab = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Movie")')

    # ------------------------------------------------------Texts-------------------------------------------------------
    _fragment_txt = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Fragment")')

    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Elements
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------Tabs--------------------------------------------------------
    @property
    def home_tab(self):
        return self.find_element(*self._home_tab, ec.element_to_be_clickable)

    @property
    def sport_tab(self):
        return self.find_element(*self._sport_tab, ec.element_to_be_clickable)

    @property
    def movie_tab(self):
        return self.find_element(*self._movie_tab, ec.element_to_be_clickable)

    # ------------------------------------------------------Texts-------------------------------------------------------
    @property
    def fragment_txt(self):
        return self.find_element(*self._fragment_txt, ec.visibility_of_element_located)

    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Actions
    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------Is Visible---------------------------------------------------
    def is_tab_layout_visible(self):
        return self.is_element_visible(*self._tab_layout)

    def is_home_tab_visible(self):
        return self.is_element_visible(*self._home_tab)

    def is_sport_tab_visible(self):
        return self.is_element_visible(*self._sport_tab)

    def is_movie_tab_visible(self):
        return self.is_element_visible(*self._movie_tab)

    # -------------------------------------------------------Click------------------------------------------------------
    def click_home_tab(self):
        self.click(*self._home_tab)

    def click_sport_tab(self):
        self.click(*self._sport_tab)

    def click_movie_tab(self):
        self.click(*self._movie_tab)

    # ------------------------------------------------------Get text----------------------------------------------------
    def get_fragment_txt(self):
        return self.get_text(*self._fragment_txt)
