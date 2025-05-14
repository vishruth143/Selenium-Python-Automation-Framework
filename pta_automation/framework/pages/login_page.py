from selenium.webdriver.common.by import By
from pta_automation.framework.pages.base_page import BasePage


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



    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Elements
    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------Input Fields---------------------------------------------------
    @property
    def username_input(self):
        return self.find_element(*self._username_input)

    @property
    def password_input(self):
        return self.find_element(*self._password_input)

    # -----------------------------------------------------Buttons------------------------------------------------------
    @property
    def submit_btn(self):
        return self.find_element(*self._submit_btn)

    # -----------------------------------------------------texts------------------------------------------------------
    @property
    def logged_in_successfully_txt(self):
        return self.find_element(*self._logged_in_successfully_txt)



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

