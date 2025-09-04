# pylint: disable=[missing-module-docstring, missing-class-docstring, import-error, missing-function-docstring]
# pylint: disable=[invalid-name, too-few-public-methods, logging-fstring-interpolation, broad-exception-caught]

from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from framework.utilities.custom_logger import Logger

log = Logger(file_id=__name__.rsplit(".", 1)[1])

class MyEventListener(AbstractEventListener):

    def before_navigate_to(self, url, driver):
        print(f"[Event] Navigating to: {url}")
        log.info(f"[Event] Navigating to: {url}")

    def after_navigate_to(self, url, driver):
        print(f"[Event] Navigated to: {url}")
        log.info(f"[Event] Navigated to: {url}")

    def before_find(self, by, value, driver):
        print(f"[Event] Finding element by {by} with value {value}")
        log.info(f"[Event] Finding element by {by} with value {value}")

    def after_find(self, by, value, driver):
        print(f"[Event] Found element by {by} with value {value}")
        log.info(f"[Event] Found element by {by} with value {value}")

    def before_click(self, element, driver):
        print(f"[Event] Clicking on element: {element}")
        log.info(f"[Event] Clicking on element: {element}")

    def after_click(self, element, driver):
        print(f"[Event] Clicked on element: {element}")
        log.info(f"[Event] Clicked on element: {element}")

    def on_exception(self, exception, driver):
        print(f"[Event] Exception occurred: {exception}")
        log.info(f"[Event] Exception occurred: {exception}")
