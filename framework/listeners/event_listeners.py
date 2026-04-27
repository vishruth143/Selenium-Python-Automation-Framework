# pylint: disable=[missing-module-docstring, missing-class-docstring, import-error, missing-function-docstring]
# pylint: disable=[invalid-name, too-few-public-methods, logging-fstring-interpolation, broad-exception-caught]

from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from framework.utilities.custom_logger import Logger

log = Logger(file_id=__name__.rsplit(".", 1)[1])

# Routine WebDriver events (navigate / find / click) are logged at DEBUG so
# they never pollute the INFO-level test_execution.log file. Developers who
# want to see them can pass --log-cli-level=DEBUG on the pytest command line
# or read the rich Allure attachments. Only on_exception is kept at ERROR so
# real failures are visible in the main log.
class MyEventListener(AbstractEventListener):

    def before_navigate_to(self, url, driver):
        log.debug(f"[Event] Navigating to: {url}")

    def after_navigate_to(self, url, driver):
        log.debug(f"[Event] Navigated to: {url}")

    def before_find(self, by, value, driver):
        log.debug(f"[Event] Finding element by {by} with value {value}")

    def after_find(self, by, value, driver):
        log.debug(f"[Event] Found element by {by} with value {value}")

    def before_click(self, element, driver):
        log.debug(f"[Event] Clicking on element: {element}")

    def after_click(self, element, driver):
        log.debug(f"[Event] Clicked on element: {element}")

    def on_exception(self, exception, driver):
        log.error(f"[Event] Exception occurred: {exception}")
