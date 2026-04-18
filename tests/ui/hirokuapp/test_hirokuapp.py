# pylint: disable=[duplicate-code, line-too-long, attribute-defined-outside-init, missing-module-docstring]
# pylint: disable=[no-else-continue, invalid-name, logging-fstring-interpolation, import-error, too-few-public-methods]
# pylint: disable=[too-many-statements, too-many-branches, unused-variable, too-many-locals, unsubscriptable-object]
# pylint: disable=[ungrouped-imports]
# pylint: disable=C0302

import requests
import requests.auth
import pytest
from selenium.common.exceptions import WebDriverException

from config.config_parser import ConfigParser
from framework.utilities.custom_logger import Logger
from tests.ui.hirokuapp.pages.landing_page import LandingPage
from tests.ui.hirokuapp.pages.ab_test_page import ABTestPage
from tests.ui.hirokuapp.pages.add_remove_elements_page import AddRemoveElementsPage
from tests.ui.hirokuapp.pages.basic_auth_page import BasicAuthPage
from tests.ui.hirokuapp.pages.broken_images_page import BrokenImagesPage
from tests.ui.hirokuapp.pages.challenging_dom_page import ChallengingDomPage
from tests.ui.hirokuapp.pages.digest_auth_page import DigestAuthPage

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

    # @pytest.mark.skip
    def test_ab_testing(self, driver, region):
        """
        Test #02 : Verify the A/B Testing page loads correctly.
        Steps:
        01) Navigate to the Herokuapp landing page.
        02) Verify the landing page has loaded successfully.
        03) Click on the 'A/B Testing' link.
        04) Verify the A/B Test page URL contains '/abtest'.
        05) Verify the A/B Test page heading is visible (Control or Variation 1).
        06) Verify the A/B Test description text is visible.
        """
        self.driver = driver
        env_config = ui_test_env_config.get(region.upper(), {})

        self.landingpage = LandingPage(self.driver)
        self.abtestpage = ABTestPage(self.driver)

        try:
            log.info(50 * '*')
            log.info("Test #02 : Verify the A/B Testing page loads correctly.")
            log.info(50 * '*')

            log.info("STEP 01: Navigate to the Herokuapp landing page.")
            driver.get(env_config["url"])

            log.info("STEP 02: Verify the landing page has loaded successfully.")
            if not self.landingpage.is_landing_page_loaded():
                raise AssertionError("Landing page did not load — heading 'Welcome to the-internet' not visible.")
            log.info("Landing page loaded successfully.")

            log.info("STEP 03: Click on the 'A/B Testing' link.")
            self.landingpage.click_ab_testing_lnk()

            log.info("STEP 04: Verify the A/B Test page URL contains '/abtest'.")
            if self.abtestpage.is_url_contains("/abtest"):
                log.info(f"A/B Test page URL verified. Current URL: {self.abtestpage.get_current_url()}")
            else:
                raise AssertionError(
                    f"A/B Test page URL did not contain '/abtest'. "
                    f"Current URL: {self.abtestpage.get_current_url()}"
                )

            log.info("STEP 05: Verify the A/B Test page heading is visible (Control or Variation 1).")
            if self.abtestpage.is_ab_test_page_loaded():
                heading = self.abtestpage.get_heading_text()
                log.info(f"A/B Test page heading visible: '{heading}'")
            else:
                raise AssertionError(
                    "A/B Test page heading not visible. "
                    "Expected 'A/B Test Control' or 'A/B Test Variation 1'."
                )

            log.info("STEP 06: Verify the A/B Test description text is visible.")
            if self.abtestpage.is_description_visible():
                log.info("A/B Test description text is visible.")
            else:
                raise AssertionError("A/B Test description text is not visible.")

            log.info("Test #02 : Verify the A/B Testing page loads correctly. - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #02 : Verify the A/B Testing page loads correctly. - Failed")
            raise

    # @pytest.mark.skip
    def test_add_remove_elements(self, driver, region):
        """
        Test #03 : Verify Add/Remove Elements functionality.
        Steps:
        01) Navigate to the Herokuapp landing page.
        02) Verify the landing page has loaded successfully.
        03) Click on the 'Add/Remove Elements' link.
        04) Verify the Add/Remove Elements page URL contains '/add_remove_elements'.
        05) Verify the page heading 'Add/Remove Elements' is visible.
        06) Verify the 'Add Element' button is visible.
        07) Click 'Add Element' 3 times and verify 3 Delete buttons appear.
        08) Click the first 'Delete' button and verify Delete button count reduces by 1.
        09) Click all remaining 'Delete' buttons and verify no Delete buttons remain.
        """
        self.driver = driver
        env_config = ui_test_env_config.get(region.upper(), {})

        self.landingpage = LandingPage(self.driver)
        self.addremovepage = AddRemoveElementsPage(self.driver)

        try:
            log.info(50 * '*')
            log.info("Test #03 : Verify Add/Remove Elements functionality.")
            log.info(50 * '*')

            log.info("STEP 01: Navigate to the Herokuapp landing page.")
            driver.get(env_config["url"])

            log.info("STEP 02: Verify the landing page has loaded successfully.")
            if not self.landingpage.is_landing_page_loaded():
                raise AssertionError("Landing page did not load — heading 'Welcome to the-internet' not visible.")
            log.info("Landing page loaded successfully.")

            log.info("STEP 03: Click on the 'Add/Remove Elements' link.")
            self.landingpage.click_add_remove_elements_lnk()

            log.info("STEP 04: Verify the Add/Remove Elements page URL contains '/add_remove_elements'.")
            if self.addremovepage.is_url_contains("/add_remove_elements"):
                log.info(f"Add/Remove Elements page URL verified. Current URL: {self.addremovepage.get_current_url()}")
            else:
                raise AssertionError(
                    f"URL did not contain '/add_remove_elements'. "
                    f"Current URL: {self.addremovepage.get_current_url()}"
                )

            log.info("STEP 05: Verify the page heading 'Add/Remove Elements' is visible.")
            if self.addremovepage.is_page_loaded():
                log.info("Page heading 'Add/Remove Elements' is visible.")
            else:
                raise AssertionError("Page heading 'Add/Remove Elements' is not visible.")

            log.info("STEP 06: Verify the 'Add Element' button is visible.")
            if self.addremovepage.is_add_element_btn_visible():
                log.info("'Add Element' button is visible.")
            else:
                raise AssertionError("'Add Element' button is not visible.")

            log.info("STEP 07: Click 'Add Element' 3 times and verify 3 Delete buttons appear.")
            add_count = 3
            for i in range(1, add_count + 1):
                self.addremovepage.click_add_element_btn()
                log.info(f"  Clicked 'Add Element' ({i}/{add_count}).")

            actual_count = self.addremovepage.get_delete_btn_count()
            if actual_count == add_count:
                log.info(f"  {actual_count} Delete button(s) present as expected.")
            else:
                raise AssertionError(
                    f"Expected {add_count} Delete button(s) after {add_count} additions, "
                    f"but found {actual_count}."
                )

            log.info("STEP 08: Click the first 'Delete' button and verify count reduces by 1.")
            self.addremovepage.click_first_delete_btn()
            actual_count = self.addremovepage.get_delete_btn_count()
            expected_count = add_count - 1
            if actual_count == expected_count:
                log.info(f"  Delete button count reduced to {actual_count} as expected.")
            else:
                raise AssertionError(
                    f"Expected {expected_count} Delete button(s) after removal, "
                    f"but found {actual_count}."
                )

            log.info("STEP 09: Click all remaining 'Delete' buttons and verify none remain.")
            remaining = self.addremovepage.get_delete_btn_count()
            for i in range(remaining):
                self.addremovepage.click_first_delete_btn()
                log.info(f"  Deleted button {i + 1}/{remaining}.")

            final_count = self.addremovepage.get_delete_btn_count()
            if final_count == 0:
                log.info("  All Delete buttons removed. No Delete buttons remain.")
            else:
                raise AssertionError(
                    f"Expected 0 Delete buttons after removing all, but found {final_count}."
                )

            log.info("Test #03 : Verify Add/Remove Elements functionality. - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #03 : Verify Add/Remove Elements functionality. - Failed")
            raise

    # @pytest.mark.skip
    def test_basic_auth(self, driver, region):
        """
        Test #04 : Verify Basic Auth authentication.
        Steps:
        01) Read Basic Auth credentials (username / password) from the env config.
        02) Navigate directly to the Basic Auth page with credentials embedded in
            the URL (https://username:password@host/basic_auth) — the standard
            Selenium approach that bypasses the browser's native auth dialog.
        03) Verify the page URL contains '/basic_auth'.
        04) Verify the 'Basic Auth' page heading is visible.
        05) Verify the success message 'Congratulations! You must have the proper
            credentials.' is visible, confirming authentication succeeded.
        """
        self.driver = driver
        env_config = ui_test_env_config.get(region.upper(), {})

        self.basicauthpage = BasicAuthPage(self.driver)

        try:
            log.info(50 * '*')
            log.info("Test #04 : Verify Basic Auth authentication.")
            log.info(50 * '*')

            log.info("STEP 01: Read Basic Auth credentials from env config.")
            username = env_config.get("basic_auth_username")
            password = env_config.get("basic_auth_password")
            base_url = env_config.get("url", "")

            # Strip the scheme so we can reconstruct the URL with credentials embedded.
            # e.g. https://the-internet.herokuapp.com -> https://admin:admin@the-internet.herokuapp.com/basic_auth
            scheme, host = base_url.split("://", 1)
            auth_url = f"{scheme}://{username}:{password}@{host}/basic_auth"
            log.info(f"Basic Auth URL constructed (credentials embedded in URL).")

            log.info("STEP 02: Navigate to the Basic Auth page with credentials embedded in URL.")
            driver.get(auth_url)

            log.info("STEP 03: Verify the page URL contains '/basic_auth'.")
            if self.basicauthpage.is_url_contains("/basic_auth"):
                log.info(f"Basic Auth page URL verified. Current URL: {self.basicauthpage.get_current_url()}")
            else:
                raise AssertionError(
                    f"URL did not contain '/basic_auth'. "
                    f"Current URL: {self.basicauthpage.get_current_url()}"
                )

            log.info("STEP 04: Verify the 'Basic Auth' page heading is visible.")
            if self.basicauthpage.is_page_loaded():
                log.info("'Basic Auth' page heading is visible.")
            else:
                raise AssertionError("'Basic Auth' page heading is not visible.")

            log.info("STEP 05: Verify the success message is visible — authentication succeeded.")
            if self.basicauthpage.is_authenticated():
                log.info("Success message 'Congratulations! You must have the proper credentials.' is visible.")
                log.info("Basic Auth authentication - Completed Successfully.")
            else:
                raise AssertionError(
                    "Success message not visible. "
                    "Authentication may have failed — check credentials in ui_test_env_config.yml."
                )

            log.info("Test #04 : Verify Basic Auth authentication. - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #04 : Verify Basic Auth authentication. - Failed")
            raise

    # @pytest.mark.skip
    def test_broken_images(self, driver, region):
        """
        Test #05 : Verify broken images on the Broken Images page.
        Steps:
        01) Navigate to the Herokuapp landing page.
        02) Verify the landing page has loaded successfully.
        03) Click on the 'Broken Images' link.
        04) Verify the page URL contains '/broken_images'.
        05) Verify the 'Broken Images' page heading is visible.
        06) Collect all images and inspect each using JavaScript naturalWidth.
            (naturalWidth == 0 means the image failed to load i.e. broken)
        07) Log a full report of broken vs valid images.
        08) Assert that broken images were found (this page intentionally has them)
            and that valid images are also present.
        """
        self.driver = driver
        env_config = ui_test_env_config.get(region.upper(), {})

        self.landingpage = LandingPage(self.driver)
        self.brokenimagepage = BrokenImagesPage(self.driver)

        try:
            log.info(50 * '*')
            log.info("Test #05 : Verify broken images on the Broken Images page.")
            log.info(50 * '*')

            log.info("STEP 01: Navigate to the Herokuapp landing page.")
            driver.get(env_config["url"])

            log.info("STEP 02: Verify the landing page has loaded successfully.")
            if not self.landingpage.is_landing_page_loaded():
                raise AssertionError("Landing page did not load — heading 'Welcome to the-internet' not visible.")
            log.info("Landing page loaded successfully.")

            log.info("STEP 03: Click on the 'Broken Images' link.")
            self.landingpage.click_broken_images_lnk()

            log.info("STEP 04: Verify the page URL contains '/broken_images'.")
            if self.brokenimagepage.is_url_contains("/broken_images"):
                log.info(f"Broken Images page URL verified. Current URL: {self.brokenimagepage.get_current_url()}")
            else:
                raise AssertionError(
                    f"URL did not contain '/broken_images'. "
                    f"Current URL: {self.brokenimagepage.get_current_url()}"
                )

            log.info("STEP 05: Verify the 'Broken Images' page heading is visible.")
            if self.brokenimagepage.is_page_loaded():
                log.info("'Broken Images' page heading is visible.")
            else:
                raise AssertionError("'Broken Images' page heading is not visible.")

            log.info("STEP 06: Collect all images and inspect each using JavaScript naturalWidth.")
            broken, valid = self.brokenimagepage.get_image_report()
            total = len(broken) + len(valid)
            log.info(f"Total images found: {total}")

            log.info("STEP 07: Log full image report.")
            for img in valid:
                log.info(f"  [VALID]  naturalWidth={img['naturalWidth']}  src={img['src']}")
            for img in broken:
                log.error(f"  [BROKEN] naturalWidth={img['naturalWidth']}  src={img['src']}")

            log.info(50 * '-')
            log.info(f"Image report summary: {len(valid)} valid, {len(broken)} broken out of {total} total.")
            log.info(50 * '-')

            log.info("STEP 08: Assert broken and valid images are present as expected by the page design.")
            if len(broken) == 0:
                raise AssertionError(
                    "Expected broken images on this page but none were detected. "
                    "The page may have changed or the detection logic needs review."
                )
            log.info(f"  {len(broken)} broken image(s) detected as expected.")

            if len(valid) == 0:
                raise AssertionError(
                    "Expected at least one valid image on this page but none were found."
                )
            log.info(f"  {len(valid)} valid image(s) present as expected.")

            log.info("Test #05 : Verify broken images on the Broken Images page. - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #05 : Verify broken images on the Broken Images page. - Failed")
            raise

    # @pytest.mark.skip
    def test_challenging_dom(self, driver, region):
        """
        Test #06 : Verify the Challenging DOM page.
        Steps:
        01) Navigate to the Herokuapp landing page.
        02) Verify the landing page has loaded successfully.
        03) Click on the 'Challenging DOM' link.
        04) Verify the page URL contains '/challenging_dom'.
        05) Verify the 'Challenging DOM' page heading is visible.
        06) Verify the table is rendered with the expected column headers.
        07) Verify the table body contains at least one row.
        08) Verify the answer canvas element is visible.
        09) Click the blue button and verify the canvas answer value changes.
        10) Click the red button and verify the canvas answer value changes again.
        11) Click the green button and verify the canvas answer value changes again.
        """
        self.driver = driver
        env_config = ui_test_env_config.get(region.upper(), {})

        self.landingpage = LandingPage(self.driver)
        self.challengingdompage = ChallengingDomPage(self.driver)

        try:
            log.info(50 * '*')
            log.info("Test #06 : Verify the Challenging DOM page.")
            log.info(50 * '*')

            log.info("STEP 01: Navigate to the Herokuapp landing page.")
            driver.get(env_config["url"])

            log.info("STEP 02: Verify the landing page has loaded successfully.")
            if not self.landingpage.is_landing_page_loaded():
                raise AssertionError("Landing page did not load — heading 'Welcome to the-internet' not visible.")
            log.info("Landing page loaded successfully.")

            log.info("STEP 03: Click on the 'Challenging DOM' link.")
            self.landingpage.click_challenging_dom_lnk()

            log.info("STEP 04: Verify the page URL contains '/challenging_dom'.")
            if self.challengingdompage.is_url_contains("/challenging_dom"):
                log.info(f"Challenging DOM page URL verified. Current URL: {self.challengingdompage.get_current_url()}")
            else:
                raise AssertionError(
                    f"URL did not contain '/challenging_dom'. "
                    f"Current URL: {self.challengingdompage.get_current_url()}"
                )

            log.info("STEP 05: Verify the 'Challenging DOM' page heading is visible.")
            if self.challengingdompage.is_page_loaded():
                log.info("'Challenging DOM' page heading is visible.")
            else:
                raise AssertionError("'Challenging DOM' page heading is not visible.")

            log.info("STEP 06: Verify the table is rendered with the expected column headers.")
            expected_headers = ["Lorem", "Ipsum", "Dolor", "Sit", "Amet", "Diceret", "Action"]
            actual_headers = self.challengingdompage.get_table_headers()
            log.info(f"Table headers found: {actual_headers}")
            for header in expected_headers:
                if header not in actual_headers:
                    raise AssertionError(
                        f"Expected table header '{header}' not found. "
                        f"Actual headers: {actual_headers}"
                    )
            log.info(f"All expected table headers are present: {expected_headers}")

            log.info("STEP 07: Verify the table body contains at least one row.")
            row_count = self.challengingdompage.get_table_row_count()
            if row_count > 0:
                log.info(f"Table body contains {row_count} row(s).")
            else:
                raise AssertionError("Table body contains no rows — expected at least one row.")

            log.info("STEP 08: Capture initial button IDs before any button click.")
            initial_blue_id = self.challengingdompage.get_blue_btn_id()
            initial_red_id = self.challengingdompage.get_red_btn_id()
            initial_green_id = self.challengingdompage.get_green_btn_id()
            log.info(f"  Initial blue btn id : '{initial_blue_id}'")
            log.info(f"  Initial red  btn id : '{initial_red_id}'")
            log.info(f"  Initial green btn id: '{initial_green_id}'")

            log.info("STEP 09: Click the blue button; verify DOM regenerates — button ID changes and table becomes stale.")
            stale_row = self.challengingdompage.find_element(*self.challengingdompage._first_row_first_cell)
            self.challengingdompage.click_blue_btn()
            if not self.challengingdompage.wait_for_table_to_regenerate(stale_row):
                raise AssertionError("Table did not regenerate after clicking the blue button (stale element not detected).")
            blue_id_after = self.challengingdompage.get_blue_btn_id()
            log.info(f"  Blue btn id after click : '{blue_id_after}'")
            if blue_id_after == initial_blue_id:
                raise AssertionError(
                    f"Blue button ID did not change after click — DOM may not have regenerated. "
                    f"Before: '{initial_blue_id}', After: '{blue_id_after}'"
                )
            log.info("  DOM regenerated after blue button click — button ID changed and table was re-rendered.")

            log.info("STEP 10: Click the red button; verify DOM regenerates again.")
            stale_row = self.challengingdompage.find_element(*self.challengingdompage._first_row_first_cell)
            self.challengingdompage.click_red_btn()
            if not self.challengingdompage.wait_for_table_to_regenerate(stale_row):
                raise AssertionError("Table did not regenerate after clicking the red button.")
            red_id_after = self.challengingdompage.get_red_btn_id()
            log.info(f"  Red btn id after click  : '{red_id_after}'")
            if red_id_after == blue_id_after:
                raise AssertionError(
                    f"Red button ID did not change after click — DOM may not have regenerated. "
                    f"Before: '{blue_id_after}', After: '{red_id_after}'"
                )
            log.info("  DOM regenerated after red button click — button ID changed and table was re-rendered.")

            log.info("STEP 11: Click the green button; verify DOM regenerates again.")
            stale_row = self.challengingdompage.find_element(*self.challengingdompage._first_row_first_cell)
            self.challengingdompage.click_green_btn()
            if not self.challengingdompage.wait_for_table_to_regenerate(stale_row):
                raise AssertionError("Table did not regenerate after clicking the green button.")
            green_id_after = self.challengingdompage.get_green_btn_id()
            log.info(f"  Green btn id after click: '{green_id_after}'")
            if green_id_after == red_id_after:
                raise AssertionError(
                    f"Green button ID did not change after click — DOM may not have regenerated. "
                    f"Before: '{red_id_after}', After: '{green_id_after}'"
                )
            log.info("  DOM regenerated after green button click — button ID changed and table was re-rendered.")

            log.info("Test #06 : Verify the Challenging DOM page. - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #06 : Verify the Challenging DOM page. - Failed")
            raise

    # @pytest.mark.skip
    def test_digest_auth(self, driver, region):
        """
        Test #07 : Verify Digest Authentication.

        Unlike Basic Auth, Digest Auth uses a server challenge-response mechanism —
        the browser cannot be pre-authenticated via a URL-embedded credential trick.
        The test therefore uses a two-pronged strategy:

          HTTP level  — Python `requests` library with HTTPDigestAuth verifies
                        that the endpoint correctly enforces authentication.
          Browser level — Chrome DevTools Protocol (CDP) is used to replay the
                          pre-computed Authorization header from the successful
                          requests session so the browser can render the page.

        Steps:
        01) Read Digest Auth credentials (username / password) from the env config.
        02) Send an unauthenticated GET to /digest_auth and verify a 401 response
            is returned with a 'WWW-Authenticate: Digest' challenge header.
        03) Send an authenticated GET using HTTPDigestAuth with CORRECT credentials
            and verify a 200 OK response is returned.
        04) Send an authenticated GET using HTTPDigestAuth with WRONG credentials
            and verify a 401 Unauthorized response is returned.
        05) Navigate to the Herokuapp landing page in the browser.
        06) Verify the landing page has loaded successfully.
        07) Use CDP to inject the Authorization header computed from the successful
            requests session, then navigate directly to /digest_auth in the browser.
        08) Verify the page URL contains '/digest_auth'.
        09) Verify the 'Digest Auth' page heading is visible.
        10) Verify the success message is visible — confirming the browser rendered
            the authenticated page correctly.
        """
        self.driver = driver
        env_config = ui_test_env_config.get(region.upper(), {})

        self.digestauthpage = DigestAuthPage(self.driver)

        try:
            log.info(50 * '*')
            log.info("Test #07 : Verify Digest Authentication.")
            log.info(50 * '*')

            log.info("STEP 01: Read Digest Auth credentials from env config.")
            username = env_config.get("digest_auth_username")
            password = env_config.get("digest_auth_password")
            base_url = env_config.get("url", "").rstrip("/")
            digest_url = f"{base_url}/digest_auth"
            log.info(f"  Digest Auth URL : {digest_url}")
            log.info(f"  Username        : {username}")

            log.info("STEP 02: Verify unauthenticated request returns 401 with Digest challenge.")
            resp_no_auth = requests.get(digest_url, timeout=10)
            if resp_no_auth.status_code != 401:
                raise AssertionError(
                    f"Expected 401 for unauthenticated request, got {resp_no_auth.status_code}."
                )
            www_auth_header = resp_no_auth.headers.get("WWW-Authenticate", "")
            if "Digest" not in www_auth_header:
                raise AssertionError(
                    f"Expected 'WWW-Authenticate: Digest' header, got: '{www_auth_header}'."
                )
            log.info(f"  401 returned as expected. WWW-Authenticate: {www_auth_header}")

            log.info("STEP 03: Verify correct credentials return 200 OK via HTTPDigestAuth.")
            digest_auth = requests.auth.HTTPDigestAuth(username, password)
            resp_correct = requests.get(digest_url, auth=digest_auth, timeout=10)
            if resp_correct.status_code != 200:
                raise AssertionError(
                    f"Expected 200 with correct credentials, got {resp_correct.status_code}."
                )
            log.info(f"  200 OK returned with correct credentials as expected.")

            log.info("STEP 04: Verify wrong credentials return 401 Unauthorized.")
            wrong_auth = requests.auth.HTTPDigestAuth(username, "wrong_password")
            resp_wrong = requests.get(digest_url, auth=wrong_auth, timeout=10)
            if resp_wrong.status_code != 401:
                raise AssertionError(
                    f"Expected 401 with wrong credentials, got {resp_wrong.status_code}."
                )
            log.info(f"  401 returned with wrong credentials as expected.")

            log.info("STEP 05: Navigate to the Herokuapp landing page in the browser.")
            driver.get(base_url)

            log.info("STEP 06: Verify the landing page has loaded successfully.")
            self.landingpage = LandingPage(self.driver)
            if not self.landingpage.is_landing_page_loaded():
                raise AssertionError("Landing page did not load — heading 'Welcome to the-internet' not visible.")
            log.info("Landing page loaded successfully.")

            log.info("STEP 07: Inject the Digest Authorization header via CDP and navigate to /digest_auth.")
            # Extract the Authorization header that requests computed during the successful
            # digest handshake — this header is valid for one request but lets the browser
            # render the page without needing to handle a native auth dialog.
            auth_header_value = resp_correct.request.headers.get("Authorization", "")
            if not auth_header_value:
                raise AssertionError(
                    "Could not extract Authorization header from the successful digest auth session."
                )
            log.info(f"  Authorization header extracted: {auth_header_value[:60]}...")

            # Get the raw ChromeDriver (unwrap EventFiringWebDriver if needed)
            raw_driver = driver.wrapped_driver if hasattr(driver, "wrapped_driver") else driver
            raw_driver.execute_cdp_cmd(
                "Network.enable", {}
            )
            raw_driver.execute_cdp_cmd(
                "Network.setExtraHTTPHeaders",
                {"headers": {"Authorization": auth_header_value}}
            )
            driver.get(digest_url)

            log.info("STEP 08: Verify the page URL contains '/digest_auth'.")
            if self.digestauthpage.is_url_contains("/digest_auth"):
                log.info(f"Digest Auth page URL verified. Current URL: {self.digestauthpage.get_current_url()}")
            else:
                raise AssertionError(
                    f"URL did not contain '/digest_auth'. "
                    f"Current URL: {self.digestauthpage.get_current_url()}"
                )

            log.info("STEP 09: Verify the 'Digest Auth' page heading is visible.")
            if self.digestauthpage.is_page_loaded():
                log.info("'Digest Auth' page heading is visible.")
            else:
                raise AssertionError("'Digest Auth' page heading is not visible.")

            log.info("STEP 10: Verify the success message is visible — authenticated page rendered correctly.")
            if self.digestauthpage.is_authenticated():
                log.info("Success message 'Congratulations! You must have the proper credentials.' is visible.")
                log.info("Digest Auth authentication - Completed Successfully.")
            else:
                raise AssertionError(
                    "Success message not visible after injecting Authorization header. "
                    "The Digest auth header may have been rejected by the server."
                )

            log.info("Test #07 : Verify Digest Authentication. - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #07 : Verify Digest Authentication. - Failed")
            raise
        finally:
            # Always clear the injected header so it doesn't bleed into subsequent tests
            try:
                raw_driver = driver.wrapped_driver if hasattr(driver, "wrapped_driver") else driver
                raw_driver.execute_cdp_cmd(
                    "Network.setExtraHTTPHeaders", {"headers": {}}
                )
            except WebDriverException:
                pass

