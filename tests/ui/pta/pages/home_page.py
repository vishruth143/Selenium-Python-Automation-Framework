# pylint: disable=[missing-module-docstring, missing-class-docstring, missing-function-docstring, line-too-long]

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from framework.pages.base_page import BasePage

class HomePage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    #                                                  Element locators
    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------Input Fields---------------------------------------------------

    # -----------------------------------------------------Buttons------------------------------------------------------

    # ------------------------------------------------------Texts-------------------------------------------------------

    # ------------------------------------------------------Links-------------------------------------------------------
    _home_lnk = (By.XPATH, "//a[normalize-space()='Home']")
    _practice_lnk = (By.XPATH, "//a[normalize-space()='Practice']")
    _courses_lnk = (By.XPATH, "//a[normalize-space()='Courses']")
    _blog_lnk = (By.XPATH, "//a[normalize-space()='Blog']")
    _contact_lnk = (By.XPATH, "//a[normalize-space()='Contact']")


    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Elements
    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------Input Fields---------------------------------------------------

    # -----------------------------------------------------Buttons------------------------------------------------------

    # ------------------------------------------------------texts-------------------------------------------------------

    # ------------------------------------------------------Links-------------------------------------------------------
    @property
    def home_lnk(self):
        return self.find_element(*self._home_lnk, ec.element_to_be_clickable)

    @property
    def practice_lnk(self):
        return self.find_element(*self._practice_lnk, ec.element_to_be_clickable)

    @property
    def courses_lnk(self):
        return self.find_element(*self._courses_lnk, ec.element_to_be_clickable)

    @property
    def blog_lnk(self):
        return self.find_element(*self._blog_lnk, ec.element_to_be_clickable)

    @property
    def contact_lnk(self):
        return self.find_element(*self._contact_lnk, ec.element_to_be_clickable)



    # ------------------------------------------------------------------------------------------------------------------
    #                                                      Actions
    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------Is Visible------------------------------------------------------

    # -----------------------------------------------------Enter/Type------------------------------------------------------

    # -----------------------------------------------------Click------------------------------------------------------
    def click_home_lnk(self):
        self.click(*self._home_lnk)

    def click_practice_lnk(self):
        self.click(*self._practice_lnk)

    def click_courses_lnk(self):
        self.click(*self._courses_lnk)

    def click_blog_lnk(self):
        self.click(*self._blog_lnk)

    def click_contact_lnk(self):
        self.click(*self._contact_lnk)
