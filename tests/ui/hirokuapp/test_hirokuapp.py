# pylint: disable=[duplicate-code, line-too-long, attribute-defined-outside-init, missing-module-docstring]
# pylint: disable=[no-else-continue, invalid-name, logging-fstring-interpolation, import-error, too-few-public-methods]
# pylint: disable=[too-many-statements, too-many-branches, unused-variable, too-many-locals, unsubscriptable-object]
# pylint: disable=[ungrouped-imports]
# pylint: disable=C0302

import requests
import pytest

from config.config_parser import ConfigParser
from framework.utilities.custom_logger import Logger
from tests.ui.hirokuapp.pages.landing_page import LandingPage

log = Logger(file_id=__name__.rsplit(".", 1)[1])
ui_test_env_config = ConfigParser.load_config("hirokuapp_ui_test_env_config")


@pytest.mark.hirokuapp
class TestHirokuApp:

    """
    Test suite for The Internet Herokuapp (https://the-internet.herokuapp.com/)
    """

    # @pytest.mark.skip
    def test_broken_links(self, driver, region):
        """
        Test #01 : Verify there are no broken links on the landing page.
        Steps:
        01) Navigate to the Herokuapp landing page.
        02) Verify the landing page has loaded successfully.
        03) Collect all hyperlinks present on the landing page.
        04) Send an HTTP request to each link and record any that return
            a non-2xx HTTP status code (broken links).
        05) Assert that no broken links were found and log a full report.
        """
        self.driver = driver
        env_config = ui_test_env_config.get(region.upper(), {})

        self.landingpage = LandingPage(self.driver)

        try:
            log.info(50 * '*')
            log.info("Test #01 : Verify there are no broken links on the landing page.")
            log.info(50 * '*')

            log.info("STEP 01: Navigate to the Herokuapp landing page.")
            driver.get(env_config["url"])

            log.info("STEP 02: Verify the landing page has loaded successfully.")
            if not self.landingpage.is_landing_page_loaded():
                raise AssertionError("Landing page did not load — heading 'Welcome to the-internet' not visible.")
            log.info("Landing page loaded successfully.")

            log.info("STEP 03: Collect all hyperlinks present on the landing page.")
            links = self.landingpage.get_all_links()
            log.info(f"Total links found: {len(links)}")

            log.info("STEP 04: Check each link for broken status (non-2xx HTTP response).")
            broken_links = []
            passed_count = 0

            for link in links:
                href = link["href"]
                text = link["text"]
                try:
                    # Use HEAD first (faster); fall back to GET if the server
                    # rejects HEAD requests (some servers return 405).
                    response = requests.head(href, allow_redirects=True, timeout=10)
                    if response.status_code == 405:
                        response = requests.get(href, allow_redirects=True, timeout=10)

                    status = response.status_code
                    if 200 <= status < 300:
                        log.info(f"  [PASS] [{status}] {text} -> {href}")
                        passed_count += 1
                    else:
                        msg = f"[BROKEN] [{status}] {text} -> {href}"
                        log.error(f"  {msg}")
                        broken_links.append(msg)

                except requests.exceptions.RequestException as req_err:
                    msg = f"[ERROR] {text} -> {href} | Exception: {req_err}"
                    log.error(f"  {msg}")
                    broken_links.append(msg)

            log.info(50 * '-')
            log.info(f"Link check summary: {passed_count} passed, {len(broken_links)} broken/error.")
            log.info(50 * '-')

            log.info("STEP 05: Assert that no broken links were found.")
            if broken_links:
                broken_summary = "\n".join(broken_links)
                log.error(f"The following broken/error links were found:\n{broken_summary}")
                raise AssertionError(
                    f"{len(broken_links)} broken link(s) found on the landing page:\n{broken_summary}"
                )

            log.info("Test #01 : Verify there are no broken links on the landing page. - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #01 : Verify there are no broken links on the landing page. - Failed")
            raise

