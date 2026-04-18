# =============================================================
# FILE: test_pta_tutorial_version.py
# LOCATION: tests/ui/pta/test_pta_tutorial_version.py
#
# PURPOSE:
#   This file contains automated UI test cases for the PTA
#   (Practice Test Automation) web application.
#   It is built on top of the Selenium + pytest framework.
#
# HOW TO READ THIS FILE (for beginners):
#   1. The pylint disable comments at the top are just linting
#      suppressions — they don't affect runtime behaviour.
#   2. Imports pull in the tools (pytest, config, pages, logger).
#   3. A single class `TestPTA` groups all PTA-related tests.
#   4. Each `test_*` method is ONE test case that pytest will
#      discover and run automatically.
#
# HOW TO RUN:
#   From the project root directory, execute:
#       pytest tests/ui/pta/test_pta_tutorial_version.py -m pta
#   Environment variables you can set before running:
#       REGION   - Target environment (QA, STAGING, PROD). Default: QA.
#       BROWSER  - Browser to use (CHROME, FIREFOX, EDGE). Default: CHROME.
#       HEADLESS - Run without a visible window (Y/N). Default: N.
#
# FRAMEWORK ARCHITECTURE (high-level):
#   ┌──────────────────────────────────────────────────────────┐
#   │  test_pta_tutorial_version.py  ←─ You are here           │
#   │      │                                                    │
#   │      ├── Page Objects  (tests/ui/pta/pages/)             │
#   │      │       HomePage    – actions on the home page       │
#   │      │       LoginPage   – actions on the login page      │
#   │      │                                                    │
#   │      ├── Common Utilities  (framework/utilities/common)  │
#   │      │       pta_login()  – shared login helper           │
#   │      │       pta_logout() – shared logout helper          │
#   │      │                                                    │
#   │      ├── Config  (config/config_parser.py)               │
#   │      │       Loads YAML/JSON configs — no hard-coded URLs │
#   │      │                                                    │
#   │      └── Logger  (framework/utilities/custom_logger.py)  │
#   │              Writes structured logs to console and file.  │
#   └──────────────────────────────────────────────────────────┘
# =============================================================

# -----------------------------------------------------------
# PYLINT DISABLE DIRECTIVES
# -----------------------------------------------------------
# These lines tell the pylint static analyser to ignore certain
# style / convention warnings that are intentionally not followed
# in this test file (e.g. long lines, attributes set outside
# __init__, etc.).  They have NO effect at runtime.
# -----------------------------------------------------------
# pylint: disable=[duplicate-code, line-too-long, attribute-defined-outside-init, missing-module-docstring]
# pylint: disable=[no-else-continue, invalid-name, logging-fstring-interpolation, import-error, too-few-public-methods]
# pylint: disable=[too-many-statements, too-many-branches, unused-variable, too-many-locals, unsubscriptable-object]
# pylint: disable=[ungrouped-imports]
# pylint: disable=C0302

# -----------------------------------------------------------
# STANDARD / THIRD-PARTY IMPORTS
# -----------------------------------------------------------
# pytest is the test runner.  It discovers test files / classes /
# methods automatically and provides fixtures, markers, and
# rich reporting.
import pytest

# -----------------------------------------------------------
# PROJECT-LEVEL IMPORTS
# -----------------------------------------------------------

# ConfigParser – a thin wrapper that reads YAML / JSON config
# files from the `config/` folder and returns them as Python
# dictionaries.  Using a config file means you never hard-code
# environment-specific data (URLs, credentials) inside test code.
from config.config_parser import ConfigParser

# Common – a utility class that holds reusable helper methods
# shared across multiple tests (e.g. pta_login, pta_logout).
# Centralising these actions avoids copy-pasting the same steps
# in every test that needs to log in.
from framework.utilities.common import Common

# Logger – a custom wrapper around Python's built-in `logging`
# module.  It writes colour-coded logs to the console AND appends
# them to `output/logs/test_execution.log` for post-run analysis.
from framework.utilities.custom_logger import Logger

# Page Object imports
# -------------------
# The Page Object Model (POM) is a design pattern used in UI
# automation.  Instead of writing raw Selenium locators inside
# each test, every web page is represented as a Python class
# (a "Page Object").  Each class exposes high-level action
# methods (click_practice_lnk, type_username_input, etc.) so
# tests read like plain English and are easy to maintain.
#
# HomePage  – represents the PTA application's main/home page.
#             Contains locators and actions for the top navigation
#             bar (Home, Practice, Courses, Blog, Contact links).
from tests.ui.pta.pages.home_page import HomePage

# LoginPage – represents the PTA login page.
#             Contains locators for the username/password inputs,
#             the Submit button, the logout link, and the
#             "Logged In Successfully" heading, plus action
#             methods to interact with each of them.
from tests.ui.pta.pages.login_page import LoginPage

# -----------------------------------------------------------
# MODULE-LEVEL SETUP
# -----------------------------------------------------------

# Create a Logger instance for this file.
#
# `__name__` is the fully-qualified module name (e.g.
# "tests.ui.pta.test_pta").  `rsplit(".", 1)[1]` extracts just
# the last part ("test_pta_tutorial_version") which is used as the logger's name /
# file_id so log messages are easy to trace back to this file.
log = Logger(file_id=__name__.rsplit(".", 1)[1])

# Load the UI environment configuration once at module level.
#
# ConfigParser.load_config("pta_ui_test_env_config") reads the
# YAML file at:
#   config/ui/pta/ui_test_env_config.yml
#
# The resulting dictionary typically looks like:
#   {
#     "QA":      { "url": "https://...", "username": "...", "password": "..." },
#     "STAGING": { "url": "https://...", "username": "...", "password": "..." },
#   }
#
# Loading it here (outside any test method) means the file is
# parsed only once per test session, which is more efficient.
ui_test_env_config = ConfigParser.load_config("pta_ui_test_env_config")

# -----------------------------------------------------------
# TEST CLASS
# -----------------------------------------------------------

# @pytest.mark.pta
# -----------------
# This is a pytest MARKER.  Markers act as labels / tags on tests.
# They let you run only a subset of tests from the command line:
#
#   pytest -m pta          → runs ONLY tests tagged with "pta"
#   pytest -m "not pta"    → runs everything EXCEPT pta tests
#
# Markers must be registered in pytest.ini (see the project root)
# to avoid the "PytestUnknownMarkWarning" warning.
#
# Applying the marker to the CLASS means every test method inside
# automatically inherits the "pta" tag — you don't need to repeat
# it on each individual test.
@pytest.mark.pta
class TestPTATutorialVersion:

    """
    Test Suite for the PTA (Practice Test Automation) web application.

    WHY A CLASS?
    ------------
    Grouping tests in a class is optional in pytest, but it has
    benefits:
      • Logical grouping – all PTA tests are in one place.
      • Shared marker (@pytest.mark.pta) applied once at class level.
      • Instance attributes (self.driver, self.homepage, …) are
        available to every method, avoiding repetition.

    NOTE ON FIXTURES:
    -----------------
    pytest fixtures are special functions that set up (and later
    tear down) resources a test needs.  They are defined in
    `conftest.py` files in the same directory tree and are
    injected automatically by pytest when a test method lists them
    as parameters.

    The fixtures used in this class are:
      • driver    – Initialises a Selenium WebDriver instance
                    (Chrome / Firefox / Edge based on the BROWSER
                    env var), wraps it in an EventFiringWebDriver
                    for logging, and tears it down after the test.
                    Defined in: tests/ui/conftest.py

      • request   – Built-in pytest fixture that gives access to
                    meta-information about the currently running
                    test (e.g. test name, parameters).

      • testdata  – Loads the test data YAML config for PTA.
                    Defined in: tests/ui/conftest.py

      • region    – Reads the REGION environment variable (default
                    "QA") and makes it available to tests so they
                    can select the correct environment block from
                    the config.
                    Defined in: tests/ui/conftest.py
    """

    # ----------------------------------------------------------
    # TIP: @pytest.mark.skip
    # ----------------------------------------------------------
    # Uncommenting the line below disables this test temporarily.
    # Useful when a feature is broken in an environment and you
    # don't want the whole pipeline to fail.
    # @pytest.mark.skip
    def test_pta_login(self, driver, request, testdata, region):
        """
        Test #01 : Verify PTA Application Login.

        OBJECTIVE:
            Confirm that a user can navigate to the PTA login page,
            enter valid credentials, see the "Logged In Successfully"
            confirmation message, and then log out cleanly.

        PRECONDITIONS:
            • The PTA application is accessible at the URL specified
              in config/ui/pta/ui_test_env_config.yml for the given
              REGION.
            • Valid username and password are stored in the same
              config file.

        STEPS:
            01) Navigate to the PTA application Home page.
            02) Click on the 'PRACTICE' navigation link.
            03) Click on the 'Test Login Page' link (on the Practice page).
            04) Enter credentials and submit the login form.
            05) Assert that the 'Logged In Successfully' heading appears.
            06) Click the 'Log out' link to clean up the session.
        """

        # ----------------------------------------------------------
        # STEP 0 – Test setup / local variable initialisation
        # ----------------------------------------------------------

        # request.node.name contains the full parametrised test name,
        # e.g. "test_pta_login[QA]".  rsplit("[", 1)[0] strips the
        # parameter suffix, leaving just "test_pta_login".
        # `test_name` can be used for logging or screenshot naming.
        test_name = request.node.name.rsplit("[", 1)[0]

        # Store the WebDriver instance as an instance attribute so
        # it is accessible in helper calls later in the method.
        # `driver` here is the pytest fixture value injected above.
        self.driver = driver

        # Select the environment-specific sub-dictionary from the
        # full config loaded at module level.
        # Example: if region == "QA", env_config will be
        #   { "url": "https://...", "username": "...", "password": "..." }
        # region.upper() ensures the lookup is case-insensitive.
        # .get(key, {}) returns an empty dict (not an error) if the
        # region key doesn't exist – a safe fallback.
        env_config = ui_test_env_config.get(region.upper(), {})

        # Instantiate the Common utility class.
        # Common wraps shared, reusable UI operations (login, logout,
        # keyboard shortcuts, etc.) so they don't have to be repeated
        # in every test.  It receives `driver` so it can interact
        # with the browser, and `testdata` for data-driven scenarios.
        common = Common(self.driver, testdata)

        # Instantiate the Page Objects.
        # Each Page Object class wraps the Selenium interactions for
        # one specific page.  Passing `self.driver` lets the Page
        # Object use the same browser session as the test.
        self.homepage = HomePage(self.driver)    # Home page navigation actions
        self.loginpage = LoginPage(self.driver)  # Login page form actions

        # ----------------------------------------------------------
        # MAIN TEST BODY wrapped in try/except
        # ----------------------------------------------------------
        # The try/except block ensures that:
        #   1. All steps are logged clearly.
        #   2. If any step raises an exception (element not found,
        #      timeout, assertion error, etc.) the error is logged
        #      with full details.
        #   3. `raise` re-raises the original exception so pytest
        #      correctly marks the test as FAILED (not just as
        #      "errored silently").
        try:
            # Visual separator in the log to make it easy to find
            # where this specific test starts.
            log.info(50 * '*')
            log.info("Test #01 : Verify login to PTA application.")
            log.info(50 * '*')

            # ------------------------------------------------------
            # STEP 01 – Open the PTA application home page
            # ------------------------------------------------------
            # driver.get(url) instructs the WebDriver to open the
            # given URL in the browser.  The URL comes from the
            # environment config so it's easy to switch between QA,
            # Staging, and Production without touching test code.
            log.info("STEP 01: Navigate to PTA application 'Home' page.")
            driver.get(env_config["url"])

            # ------------------------------------------------------
            # STEP 02 – Click the 'PRACTICE' navigation link
            # ------------------------------------------------------
            # self.homepage.click_practice_lnk() is a Page Object
            # method defined in tests/ui/pta/pages/home_page.py.
            # Under the hood it:
            #   1. Waits for the element (XPATH: "//a[normalize-space()='Practice']")
            #      to become clickable.
            #   2. Clicks it.
            # Using Page Objects here keeps the test clean and means
            # that if the locator ever changes, you only update it
            # in home_page.py – not in every test that clicks the link.
            log.info("STEP 02: Click on 'PRACTICE' link.")
            self.homepage.click_practice_lnk()

            # ------------------------------------------------------
            # STEP 03 – Click the 'Test Login Page' link
            # ------------------------------------------------------
            # After clicking 'PRACTICE', a list of practice pages
            # appears.  click_test_login_page_lnk() navigates to
            # the dedicated login practice page.
            log.info("STEP 03: Click on 'Test Login Page' link.")
            self.loginpage.click_test_login_page_lnk()

            # ------------------------------------------------------
            # STEP 04 – Enter credentials and submit the login form
            # ------------------------------------------------------
            # common.pta_login(region) is a shared helper in
            # framework/utilities/common.py that:
            #   1. Loads the env config for the given region.
            #   2. Extracts username and password.
            #   3. Types the username into the username input field.
            #   4. Types the password into the password input field.
            #   5. Clicks the Submit button.
            #
            # Delegating login to a Common method means ALL tests
            # that need to log in share the same implementation.
            # If the login flow ever changes, you only fix it once.
            log.info("STEP 04: Login to PTA application with sample credentials.")
            log.info("Login to PTA application - Started.")
            common.pta_login(region)

            # ------------------------------------------------------
            # STEP 05 – Verify the success message is displayed
            # ------------------------------------------------------
            # self.loginpage.logged_in_successfully_txt_visible()
            # calls is_element_visible() from the base page, which
            # checks whether the element with XPATH
            # "//h1[normalize-space()='Logged In Successfully']"
            # is currently visible on the page.
            #
            # Returns True  → login succeeded.
            # Returns False → login failed (wrong credentials, page
            #                 didn't load, element not present, etc.)
            #
            # NOTE: In a stricter test you would use an assertion
            # (assert … or pytest.fail(…)) here to mark the test as
            # FAILED when the element is not visible.  Currently the
            # code only logs a warning – consider upgrading this if
            # you need hard failures.
            log.info("STEP 05: Verify 'Logged In Successfully' text is visible.")
            if self.loginpage.logged_in_successfully_txt_visible():
                log.info("'Logged In Successfully' text is visible.")
                log.info("Login to PTA application - Completed Successfully.")
            else:
                log.info("'Logged In Successfully' text is not visible.")
                log.info("Test #01 : Verify PTA Application Login. - Failed")

            # ------------------------------------------------------
            # STEP 06 – Log out to restore a clean application state
            # ------------------------------------------------------
            # common.pta_logout() internally calls
            # self.loginpage.click_logout_btn(), which clicks the
            # "Log out" link on the post-login page.
            #
            # Logging out as part of the test (rather than relying
            # on browser teardown) is a best practice because:
            #   • It verifies the logout functionality itself.
            #   • It leaves the application in a neutral state,
            #     which is important if tests share a browser session.
            log.info(" STEP 06: Logout of PTA application.")
            log.info("Logout from PTA application - Started.")
            common.pta_logout()
            log.info("Logout from PTA application - Completed Successfully.")

        except Exception as e:
            # log.error logs the Python exception message so you can
            # quickly see WHAT went wrong (e.g. "ElementNotFound",
            # "TimeoutException") in the log file.
            log.error(f"Error: {e}")
            log.info("Test #01 : Verify PTA Application Login. - Failed")

            # `raise` without arguments re-raises the caught exception
            # so pytest receives the failure signal and marks this
            # test as FAILED in the test report.  Without `raise`,
            # the exception would be silently swallowed and pytest
            # would incorrectly show the test as PASSED.
            raise
