# pylint: disable=[missing-module-docstring, missing-class-docstring, missing-function-docstring, line-too-long]

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from framework.pages.ui.base_page import BasePage


class AddRemoveElementsPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    #                                                  Element locators
    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------Input Fields---------------------------------------------------

    # -----------------------------------------------------Buttons------------------------------------------------------
    _add_element_btn = (By.XPATH, "//button[normalize-space()='Add Element']")
    _delete_btns = (By.XPATH, "//button[normalize-space()='Delete']")

    # ------------------------------------------------------Texts-------------------------------------------------------
    _page_heading_txt = (By.XPATH, "//h3[normalize-space()='Add/Remove Elements']")

    # ------------------------------------------------------Links-------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Elements
    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------Buttons------------------------------------------------------
    @property
    def add_element_btn(self):
        return self.find_element(*self._add_element_btn, ec.element_to_be_clickable)

    @property
    def delete_btns(self):
        return self.find_elements(*self._delete_btns)

    # ------------------------------------------------------Texts-------------------------------------------------------
    @property
    def page_heading_txt(self):
        return self.find_element(*self._page_heading_txt, ec.visibility_of_element_located)

    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Actions
    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------Is Visible---------------------------------------------------
    def is_page_loaded(self):
        return self.is_element_visible(*self._page_heading_txt)

    def is_add_element_btn_visible(self):
        return self.is_element_visible(*self._add_element_btn)

    def is_delete_btn_visible(self):
        return self.is_element_visible(*self._delete_btns)

    # -----------------------------------------------------Get Data-----------------------------------------------------
    def get_delete_btn_count(self):
        """Returns the current number of Delete buttons present on the page."""
        try:
            return len(self.delete_btns)
        except Exception:
            return 0

    # -----------------------------------------------------Click-------------------------------------------------------
    def click_add_element_btn(self):
        self.click(*self._add_element_btn)

    def click_first_delete_btn(self):
        self.find_element(*self._delete_btns, ec.element_to_be_clickable).click()

