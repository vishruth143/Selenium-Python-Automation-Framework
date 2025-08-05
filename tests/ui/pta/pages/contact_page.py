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
    _Last_name_input = (By.XPATH, "//input[@id='wpforms-161-field_0-last']")
    _email_input = (By.XPATH, "//input[@id='wpforms-161-field_1']")
    _comment_or_message_input = (By.XPATH, "//textarea[@id='wpforms-161-field_2']")
    _submit_btn = (By.XPATH, "//button[@id='wpforms-submit-161']")

    # -----------------------------------------------------Buttons------------------------------------------------------
    _submit_btn = (By.ID, "submit")
    _logout_btn = (By.XPATH, "//a[normalize-space()='Log out']")

    # ------------------------------------------------------Texts-------------------------------------------------------
    _logged_in_successfully_txt = (By.XPATH, "//h1[normalize-space()='Logged In Successfully']")



    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Elements
    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------Input Fields---------------------------------------------------
    @property
    def username_input(self):
        return self.find_element(*self._username_input, EC.presence_of_element_located)

    @property
    def password_input(self):
        return self.find_element(*self._password_input, EC.presence_of_element_located)

    # -----------------------------------------------------Buttons------------------------------------------------------
    @property
    def submit_btn(self):
        return self.find_element(*self._submit_btn, EC.element_to_be_clickable)

    # -----------------------------------------------------texts------------------------------------------------------
    @property
    def logged_in_successfully_txt(self):
        return self.find_element(*self._logged_in_successfully_txt, EC.visibility_of_element_located)



    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Actions
    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------Is Visible------------------------------------------------------
    def username_input_visible(self):
        return self.is_element_visible(*self._username_input)

    def logged_in_successfully_txt_visible(self):
        return self.is_element_visible(*self._logged_in_successfully_txt)

    # -----------------------------------------------------Enter/Type------------------------------------------------------
    def enter_username(self, username):
        self.type_text(*self._username_input, text=username)

    def enter_password(self, password):
        self.type_text(*self._password_input, text=password)

    # -----------------------------------------------------Click------------------------------------------------------
    def click_submit_btn(self):
        self.click(*self._submit_btn)

    def click_logout_btn(self):
        self.click(*self._logout_btn)
