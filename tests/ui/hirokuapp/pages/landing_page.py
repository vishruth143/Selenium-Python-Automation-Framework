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
    _ab_testing_lnk = (By.XPATH, "//a[normalize-space()='A/B Testing']")
    _add_remove_elements_lnk = (By.XPATH, "//a[normalize-space()='Add/Remove Elements']")
    _basic_auth_lnk = (By.XPATH, "//a[normalize-space()='Basic Auth']")
    _broken_images_lnk = (By.XPATH, "//a[normalize-space()='Broken Images']")

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

    @property
    def ab_testing_lnk(self):
        return self.find_element(*self._ab_testing_lnk, ec.element_to_be_clickable)

    @property
    def add_remove_elements_lnk(self):
        return self.find_element(*self._add_remove_elements_lnk, ec.element_to_be_clickable)

    @property
    def basic_auth_lnk(self):
        return self.find_element(*self._basic_auth_lnk, ec.element_to_be_clickable)

    @property
    def broken_images_lnk(self):
        return self.find_element(*self._broken_images_lnk, ec.element_to_be_clickable)

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

    # -----------------------------------------------------Click-------------------------------------------------------
    def click_ab_testing_lnk(self):
        self.click(*self._ab_testing_lnk)

    def click_add_remove_elements_lnk(self):
        self.click(*self._add_remove_elements_lnk)

    def click_basic_auth_lnk(self):
        self.click(*self._basic_auth_lnk)

    def click_broken_images_lnk(self):
        self.click(*self._broken_images_lnk)

