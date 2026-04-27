# pylint: disable=[missing-module-docstring, missing-class-docstring, missing-function-docstring, line-too-long]

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from framework.pages.ui.base_page import BasePage


class ABTestPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    #                                                  Element locators
    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------Input Fields---------------------------------------------------

    # -----------------------------------------------------Buttons------------------------------------------------------

    # ------------------------------------------------------Texts-------------------------------------------------------
    # The heading alternates between "A/B Test Control" and "A/B Test Variation 1"
    # depending on which variant the server serves — both are valid outcomes.
    _ab_test_control_heading_txt = (By.XPATH, "//h3[normalize-space()='A/B Test Control']")
    _ab_test_variation_heading_txt = (By.XPATH, "//h3[normalize-space()='A/B Test Variation 1']")
    _ab_test_description_txt = (By.XPATH, "//p[contains(text(),'split testing')]")

    # ------------------------------------------------------Links-------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Elements
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------Texts-------------------------------------------------------
    @property
    def ab_test_control_heading_txt(self):
        return self.find_element(*self._ab_test_control_heading_txt, ec.visibility_of_element_located)

    @property
    def ab_test_variation_heading_txt(self):
        return self.find_element(*self._ab_test_variation_heading_txt, ec.visibility_of_element_located)

    @property
    def ab_test_description_txt(self):
        return self.find_element(*self._ab_test_description_txt, ec.visibility_of_element_located)

    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Actions
    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------Is Visible---------------------------------------------------
    def is_ab_test_page_loaded(self):
        """
        Returns True if either the Control or Variation 1 heading is visible.
        Both are valid — the server randomly serves one of the two variants.
        """
        return (
            self.is_element_visible(*self._ab_test_control_heading_txt)
            or self.is_element_visible(*self._ab_test_variation_heading_txt)
        )

    def is_description_visible(self):
        return self.is_element_visible(*self._ab_test_description_txt)

    # -----------------------------------------------------Get Data-----------------------------------------------------
    def get_heading_text(self):
        """Returns the visible heading text regardless of which variant is served."""
        if self.is_element_visible(*self._ab_test_control_heading_txt):
            return self.get_text(*self._ab_test_control_heading_txt)
        if self.is_element_visible(*self._ab_test_variation_heading_txt):
            return self.get_text(*self._ab_test_variation_heading_txt)
        return ""
