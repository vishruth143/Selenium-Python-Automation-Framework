# pylint: disable=[missing-function-docstring, missing-module-docstring, redefined-outer-name, unused-argument]
# pylint: disable=[line-too-long]

# =============================================================================
# HEROKU CONFTEST - Fixtures specific to the Heroku application test suite
# =============================================================================
#
# This file is automatically loaded by pytest for every test under tests/ui/heroku/.
# It provides:
#   1. A "testdata" fixture - loads Heroku test data from YAML config (session scope).
#
# Fixture chain:
#   tests/conftest.py              (session) - output cleanup, allure setup, log fixture
#       v
#   tests/ui/conftest.py           (ui)      - driver, region, screenshot/video hooks
#       v
#   tests/ui/heroku/conftest.py    (this)    - Heroku testdata fixture
#       v
#   tests/ui/heroku/test_heroku.py           - test cases
# =============================================================================

import pytest

from config.config_parser import ConfigParser


# =============================================================================
# FIXTURE: testdata (session scope)
# =============================================================================
# Loads the Heroku UI test data configuration ONCE per test session.
# Data comes from config/ui/heroku/ui_test_data_config.yml
#
# Usage in a test:
#   def test_ab_test_page(driver, testdata, region):
#       url = testdata[region]["ab_test_url"]
# =============================================================================
@pytest.fixture(scope="session")
def testdata():
    return ConfigParser.load_config("heroku_ui_test_data_config")
