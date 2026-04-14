# pylint: disable=[missing-module-docstring, missing-class-docstring, missing-function-docstring, line-too-long]

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from framework.pages.ui.base_page import BasePage


class BasicAuthPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    #                                                  Element locators
    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------Input Fields---------------------------------------------------

    # -----------------------------------------------------Buttons------------------------------------------------------

    # ------------------------------------------------------Texts-------------------------------------------------------
    _page_heading_txt = (By.XPATH, "//h3[normalize-space()='Basic Auth']")
    _success_msg_txt = (By.XPATH, "//p[normalize-space()='Congratulations! You must have the proper credentials.']")

    # ------------------------------------------------------Links-------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Elements
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------Texts-------------------------------------------------------
    @property
    def page_heading_txt(self):
        return self.find_element(*self._page_heading_txt, ec.visibility_of_element_located)

    @property
    def success_msg_txt(self):
        return self.find_element(*self._success_msg_txt, ec.visibility_of_element_located)

    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Actions
    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------Is Visible---------------------------------------------------
    def is_page_loaded(self):
        return self.is_element_visible(*self._page_heading_txt)

    def is_authenticated(self):
        """Returns True if the success message 'Congratulations! ...' is visible."""
        return self.is_element_visible(*self._success_msg_txt)

