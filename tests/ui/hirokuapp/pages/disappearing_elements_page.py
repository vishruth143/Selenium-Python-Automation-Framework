# pylint: disable=[missing-module-docstring, missing-class-docstring, missing-function-docstring, line-too-long]

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from framework.pages.ui.base_page import BasePage


class DisappearingElementsPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    #                                                  Element locators
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------Texts-------------------------------------------------------
    _page_heading_txt = (By.XPATH, "//h3[normalize-space()='Disappearing Elements']")

    # ------------------------------------------------------Links-------------------------------------------------------
    # The nav menu items — 'Gallery' is the element that randomly disappears/reappears.
    # The <ul> on this page has NO class attribute, so we target it without a class filter.
    _nav_menu_items = (By.XPATH, "//ul/li/a")
    _gallery_nav_lnk = (By.XPATH, "//ul/li/a[normalize-space()='Gallery']")

    # Static nav items that are always present
    _home_nav_lnk = (By.XPATH, "//ul/li/a[normalize-space()='Home']")
    _about_nav_lnk = (By.XPATH, "//ul/li/a[normalize-space()='About']")
    _contact_us_nav_lnk = (By.XPATH, "//ul/li/a[normalize-space()='Contact Us']")
    _portfolio_nav_lnk = (By.XPATH, "//ul/li/a[normalize-space()='Portfolio']")

    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Elements
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------Texts-------------------------------------------------------
    @property
    def page_heading_txt(self):
        return self.find_element(*self._page_heading_txt, ec.visibility_of_element_located)

    # ------------------------------------------------------Links-------------------------------------------------------
    @property
    def nav_menu_items(self):
        return self.find_elements(*self._nav_menu_items)

    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Actions
    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------Is Visible---------------------------------------------------
    def is_page_loaded(self):
        return self.is_element_visible(*self._page_heading_txt)

    def is_gallery_lnk_visible(self):
        # Use is_element_present (no WebDriverWait) so the check returns immediately
        # when Gallery is absent — avoids a 10-second wait on every refresh cycle.
        return self.is_element_present(*self._gallery_nav_lnk)

    def is_home_lnk_visible(self):
        return self.is_element_visible(*self._home_nav_lnk)

    def is_about_lnk_visible(self):
        return self.is_element_visible(*self._about_nav_lnk)

    def is_contact_us_lnk_visible(self):
        return self.is_element_visible(*self._contact_us_nav_lnk)

    def is_portfolio_lnk_visible(self):
        return self.is_element_visible(*self._portfolio_nav_lnk)

    # -----------------------------------------------------Get Data-----------------------------------------------------
    def get_nav_item_texts(self):
        """Returns a list of visible nav item texts from the menu."""
        return [item.text.strip() for item in self.nav_menu_items if item.text.strip()]

    def get_nav_item_count(self):
        """Returns the current count of nav menu items."""
        return len(self.nav_menu_items)

