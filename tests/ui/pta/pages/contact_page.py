# pylint: disable=[missing-module-docstring, missing-class-docstring, missing-function-docstring, line-too-long]

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from framework.pages.base_page import BasePage

class ContactPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    #                                                  Element locators
    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------Input Fields---------------------------------------------------
    _first_name_input = (By.XPATH, "//input[@id='wpforms-161-field_0']")
    _last_name_input = (By.XPATH, "//input[@id='wpforms-161-field_0-last']")
    _email_input = (By.XPATH, "//input[@id='wpforms-161-field_1']")
    _comment_or_message_input = (By.XPATH, "//textarea[@id='wpforms-161-field_2']")

    # -----------------------------------------------------Buttons------------------------------------------------------
    _submit_btn = (By.XPATH, "//button[@id='wpforms-submit-161']")

    # ------------------------------------------------------Texts-------------------------------------------------------


    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Elements
    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------Input Fields---------------------------------------------------
    @property
    def first_name_input(self):
        return self.find_element(*self._first_name_input, EC.presence_of_element_located)

    @property
    def last_name_input(self):
        return self.find_element(*self._last_name_input, EC.presence_of_element_located)

    @property
    def email_input(self):
        return self.find_element(*self._email_input, EC.presence_of_element_located)

    @property
    def comment_or_message_input(self):
        return self.find_element(*self._comment_or_message_input, EC.presence_of_element_located)

    # -----------------------------------------------------Buttons------------------------------------------------------
    @property
    def submit_btn(self):
        return self.find_element(*self._submit_btn, EC.element_to_be_clickable)

    # -----------------------------------------------------texts------------------------------------------------------



    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Actions
    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------Is Visible------------------------------------------------------

    # -----------------------------------------------------Enter/Type------------------------------------------------------
    def type_first_name_input(self, first_name):
        self.type_text(*self._first_name_input, text=first_name)

    def type_last_name_input(self, last_name):
        self.type_text(*self._last_name_input, text=last_name)

    def type_email_input(self, email):
        self.type_text(*self._email_input, text=email)

    def type_comment_or_message_input(self, comment_or_message):
        self.type_text(*self._comment_or_message_input, text=comment_or_message)

    # -----------------------------------------------------Click------------------------------------------------------
    def click_submit_btn(self):
        self.click(*self._submit_btn)
