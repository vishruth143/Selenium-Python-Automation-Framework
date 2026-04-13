# pylint: disable=[missing-module-docstring, missing-class-docstring, missing-function-docstring, line-too-long]

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from framework.pages.ui.base_page import BasePage


class LandingPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    #                                                  Element locators
    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------Input Fields---------------------------------------------------

    # -----------------------------------------------------Buttons------------------------------------------------------

    # ------------------------------------------------------Texts-------------------------------------------------------
    _page_heading_txt = (By.XPATH, "//h1[normalize-space()='Welcome to the-internet']")

    # ------------------------------------------------------Links-------------------------------------------------------
    # All example links listed on the landing page
    _all_example_lnks = (By.XPATH, "//ul/li/a")

    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Elements
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------Texts-------------------------------------------------------
    @property
    def page_heading_txt(self):
        return self.find_element(*self._page_heading_txt, ec.visibility_of_element_located)

    # ------------------------------------------------------Links-------------------------------------------------------
    @property
    def all_example_lnks(self):
        return self.find_elements(*self._all_example_lnks)

    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Actions
    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------Is Visible---------------------------------------------------
    def is_landing_page_loaded(self):
        return self.is_element_visible(*self._page_heading_txt)

    # -----------------------------------------------------Get Data-----------------------------------------------------
    def get_all_links(self):
        """
        Returns a list of dicts for every <a> element on the landing page.
        Each dict contains:
          - text  : visible link text
          - href  : absolute href attribute value
        """
        links = []
        for element in self.all_example_lnks:
            href = element.get_attribute("href") or ""
            text = element.text.strip()
            if href:
                links.append({"text": text, "href": href})
        return links

