from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def find_element(self, by, locator, condition=EC.presence_of_element_located):
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                condition((by, locator))
            )
        except TimeoutException as e:
            raise Exception(f"Element not found: ({by}, {locator}) | Exception: {str(e)}")

    def find_elements(self, by, locator):
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_all_elements_located((by, locator))
            )
        except TimeoutException as e:
            raise Exception(f"Elements not found: ({by}, {locator}) | Exception: {str(e)}")

    def is_element_present(self, by, locator):
        try:
            self.driver.find_element(by, locator)
            return True
        except NoSuchElementException:
            return False

    def is_element_visible(self, by, locator):
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located((by, locator))
            )
            return True
        except TimeoutException:
            return False

    def click(self, by, locator):
        self.find_element(by, locator).click()

    def type_text(self, by, locator, text):
        element = self.find_element(by, locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, by, locator):
        return self.find_element(by, locator).text

    def wait_until_not_visible(self, by, locator):
        try:
            WebDriverWait(self.driver, self.timeout).until_not(
                EC.visibility_of_element_located((by, locator))
            )
        except TimeoutException:
            raise Exception(f"Element still visible after timeout: ({by}, {locator})")

    def wait_for_clickable(self, by, locator):
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((by, locator))
            )
        except TimeoutException as e:
            raise Exception(f"Element not clickable: ({by}, {locator}) | Exception: {str(e)}")