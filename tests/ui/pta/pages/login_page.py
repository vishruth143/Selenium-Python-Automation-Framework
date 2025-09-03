# pylint: disable=[missing-module-docstring, missing-class-docstring, missing-function-docstring, line-too-long]

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from framework.pages.base_page import BasePage

class LoginPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    #                                                  Element locators
    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------Input Fields---------------------------------------------------
    _username_input = (By.ID, "username")
    _password_input = (By.ID, "password")

    # -----------------------------------------------------Buttons------------------------------------------------------
    _submit_btn = (By.ID, "submit")
    _logout_btn = (By.XPATH, "//a[normalize-space()='Log out']")

    # ------------------------------------------------------Texts-------------------------------------------------------
    _logged_in_successfully_txt = (By.XPATH, "//h1[normalize-space()='Logged In Successfully']")

    # ------------------------------------------------------Links-------------------------------------------------------
    _test_login_page_lnk = (By.XPATH, "//a[normalize-space()='Test Login Page']")
    _test_exceptions_lnk = (By.XPATH, "//a[normalize-space()='Test Exceptions']")



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

    # ------------------------------------------------------Links-------------------------------------------------------
    @property
    def test_login_page_lnk(self):
        return self.find_element(*self._test_login_page_lnk, EC.element_to_be_clickable)

    @property
    def test_exceptions_lnk(self):
        return self.find_element(*self._test_exceptions_lnk, EC.element_to_be_clickable)



    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Actions
    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------Is Visible---------------------------------------------------
    def username_input_visible(self):
        return self.is_element_visible(*self._username_input)

    def logged_in_successfully_txt_visible(self):
        return self.is_element_visible(*self._logged_in_successfully_txt)

    # -----------------------------------------------------Enter/Type---------------------------------------------------
    def type_username_input(self, username):
        self.type_text(*self._username_input, text=username)

    def type_password_input(self, password):
        self.type_text(*self._password_input, text=password)

    # -----------------------------------------------------Click--------------------------------------------------------
    def click_submit_btn(self):
        self.click(*self._submit_btn)

    def click_logout_btn(self):
        self.click(*self._logout_btn)

    def click_test_login_page_lnk(self):
        self.click(*self._test_login_page_lnk)

    def click_test_exception_lnk(self):
        self.click(*self._test_exceptions_lnk)
