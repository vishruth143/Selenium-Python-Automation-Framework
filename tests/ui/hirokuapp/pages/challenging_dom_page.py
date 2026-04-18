# pylint: disable=[missing-module-docstring, missing-class-docstring, missing-function-docstring, line-too-long]

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from framework.pages.ui.base_page import BasePage


class ChallengingDomPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    #                                                  Element locators
    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------Buttons------------------------------------------------------
    # The three action buttons share the "button" class; alert = red, success = green, plain = blue
    _blue_btn = (By.XPATH, "//a[contains(@class,'button') and not(contains(@class,'alert')) and not(contains(@class,'success'))]")
    _red_btn = (By.XPATH, "//a[contains(@class,'button alert')]")
    _green_btn = (By.XPATH, "//a[contains(@class,'button success')]")

    # ------------------------------------------------------Texts-------------------------------------------------------
    _page_heading_txt = (By.XPATH, "//h3[normalize-space()='Challenging DOM']")

    # ------------------------------------------------------Table-------------------------------------------------------
    _table_header_cells = (By.XPATH, "//table/thead/tr/th")
    _table_body_rows = (By.XPATH, "//table/tbody/tr")
    # First cell of the first body row — used to detect DOM regeneration via staleness
    _first_row_first_cell = (By.XPATH, "//table/tbody/tr[1]/td[1]")

    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Elements
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------Texts-------------------------------------------------------
    @property
    def page_heading_txt(self):
        return self.find_element(*self._page_heading_txt, ec.visibility_of_element_located)

    # -----------------------------------------------------Buttons------------------------------------------------------
    @property
    def blue_btn(self):
        return self.find_element(*self._blue_btn, ec.element_to_be_clickable)

    @property
    def red_btn(self):
        return self.find_element(*self._red_btn, ec.element_to_be_clickable)

    @property
    def green_btn(self):
        return self.find_element(*self._green_btn, ec.element_to_be_clickable)

    # ------------------------------------------------------Table-------------------------------------------------------
    @property
    def table_header_cells(self):
        return self.find_elements(*self._table_header_cells)

    @property
    def table_body_rows(self):
        return self.find_elements(*self._table_body_rows)

    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Actions
    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------Is Visible---------------------------------------------------
    def is_page_loaded(self):
        return self.is_element_visible(*self._page_heading_txt)

    # -----------------------------------------------------Get Data-----------------------------------------------------
    def get_table_headers(self):
        """Returns a list of visible header texts from the table."""
        return [cell.text.strip() for cell in self.table_header_cells]

    def get_table_row_count(self):
        """Returns the number of body rows in the table."""
        return len(self.table_body_rows)

    def get_first_row_text(self):
        """Returns the text of the first cell in the first table body row."""
        return self.find_element(*self._first_row_first_cell).text.strip()


    def get_blue_btn_id(self):
        """Returns the 'id' attribute of the blue button (regenerated on each click)."""
        return self.blue_btn.get_attribute("id") or ""

    def get_red_btn_id(self):
        """Returns the 'id' attribute of the red button (regenerated on each click)."""
        return self.red_btn.get_attribute("id") or ""

    def get_green_btn_id(self):
        """Returns the 'id' attribute of the green button (regenerated on each click)."""
        return self.green_btn.get_attribute("id") or ""

    def wait_for_table_to_regenerate(self, stale_row_element, timeout=10):
        """
        Waits until the previously captured first-row element becomes stale,
        which confirms the table was re-rendered by a button click.
        Returns True if staleness detected within timeout, False otherwise.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                ec.staleness_of(stale_row_element)
            )
            return True
        except Exception:  # pylint: disable=broad-except
            return False

    # -----------------------------------------------------Click-------------------------------------------------------
    def click_blue_btn(self):
        self.click(*self._blue_btn)

    def click_red_btn(self):
        self.click(*self._red_btn)

    def click_green_btn(self):
        self.click(*self._green_btn)
