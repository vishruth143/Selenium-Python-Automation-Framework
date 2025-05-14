# pylint: disable=[missing-module-docstring, missing-class-docstring, import-error, missing-function-docstring]
# pylint: disable=[invalid-name, too-few-public-methods]

from selenium.webdriver.support.abstract_event_listener import AbstractEventListener


class MyEventListener(AbstractEventListener):

    def before_find(self, by, value, driver):
        pass
