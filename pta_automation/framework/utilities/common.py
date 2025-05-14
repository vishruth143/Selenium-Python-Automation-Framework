import os
import time
import random
import json
from datetime import datetime, timezone

import pytest
from faker import Faker
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from pta_automation.framework.pages.login_page import LoginPage
from pta_automation.config.config_parser import ConfigParser

class Common:
    @staticmethod
    def fake_name():
        return Faker().name()

    @staticmethod
    def fake_first_name():
        return Faker().first_name()

    @staticmethod
    def fake_last_name():
        return Faker().last_name()

    @staticmethod
    def fake_ssn():
        return Faker().ssn().replace('-', '')

    @staticmethod
    def fake_phonenumber():
        return str(random.randint(2220000000, 2229999999))

    @staticmethod
    def get_date():
        return datetime.now(timezone.utc).strftime('%m-%d-%Y')

    # Copy
    @staticmethod
    def copy(driver: WebDriver):
        ActionChains(driver).key_down(Keys.CONTROL).send_keys("c").key_up(Keys.CONTROL).perform()

    @staticmethod
    def enter(driver: WebDriver):
        ActionChains(driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()

    @staticmethod
    def tab(driver: WebDriver):
        ActionChains(driver).key_down(Keys.TAB).key_up(Keys.TAB).perform()

    # Paste
    @staticmethod
    def paste(driver: WebDriver):
        ActionChains(driver).key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()

    @staticmethod
    def select_all(driver: WebDriver):
        ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()

    @staticmethod
    def delete(driver: WebDriver):
        ActionChains(driver).key_down(Keys.DELETE).key_up(Keys.DELETE).perform()

    # Scroll web page up by pressing Ctrl+Home
    @staticmethod
    def scroll_up(driver: WebDriver):
        ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.HOME).key_up(Keys.HOME).key_up(
            Keys.CONTROL).perform()

    # Scroll web page down by pressing Ctrl+End
    @staticmethod
    def scroll_down(driver: WebDriver):
        ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.END).key_up(Keys.END).key_up(
            Keys.CONTROL).perform()

    # Scroll for web element to view
    @staticmethod
    def scroll_into_view(driver: WebDriver, element: WebElement):
        driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(2)

    # Move to web element
    @staticmethod
    def move_to_element(driver: WebDriver, element: WebElement):
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        time.sleep(2)

    def __init__(self, driver=None, test_data=None):
        self.driver = driver
        self.test_data = test_data
        self.pta_login_url, self.pta_login_username, self.pta_login_password = "", "", ""

        common_config = ConfigParser.load_config("common_config")

        # Pages needed
        self.loginpage = LoginPage(self.driver)

    def pta_login(self, region):
        ui_test_env_config = ConfigParser.load_config("ui_test_env_config")

        # Get the correct env block based on the region
        env_config = ui_test_env_config.get(region.upper(), {})

        # Extract username and password
        self.pta_login_url = env_config.get("url")
        self.pta_login_username = env_config.get("username")
        self.pta_login_password = env_config.get("password")

        self.driver.get(self.pta_login_url)
        time.sleep(5)

        # Log in using credentials
        self.loginpage.enter_username(self.pta_login_username)
        self.loginpage.enter_password(self.pta_login_password)
        self.loginpage.click_submit_btn()

    def pta_logout(self):
        self.loginpage.click_logout_btn()

def get_title(self):
    return self.driver.title

def wait_for_an_element(driver, timeout, poll_frequency, element_locator):
    """Wait for the specified element to be present on the page.

    Args:
        driver (WebDriver): The webdriver instance to use.
        timeout (int): The maximum amount of time to wait in seconds.
        poll_frequency (int): The frequency at which to check for the element in seconds.
        element_locator (tuple): The locator for the element, in the format (By.TYPE, 'value').
    """
    WebDriverWait(driver, timeout, poll_frequency).until(ec.presence_of_element_located(element_locator))

def generic_wait(driver, timeout):
    wait = WebDriverWait(driver, timeout)

    # Wait for timeout
    wait.until(lambda driver: driver.execute_script("return true;"), "Timeout")

def wait_for_element_to_disappear(driver, element_locator, timeout=60):
    try:
        element_present = ec.presence_of_element_located(element_locator)
        WebDriverWait(driver, timeout).until_not(element_present)
    except TimeoutError:
        print("Timed out waiting for element to disappear")
