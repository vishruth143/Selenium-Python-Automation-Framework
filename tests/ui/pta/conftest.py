# pylint: disable=[missing-function-docstring, missing-module-docstring, redefined-outer-name, unused-argument]
# pylint: disable=[line-too-long]

# =============================================================================
# PTA CONFTEST - Fixtures specific to the PTA application test suite
# =============================================================================
#
# This file is automatically loaded by pytest for every test under tests/ui/pta/.
# It provides:
#   1. A "testdata" fixture - loads PTA test data from YAML config (session scope).
#
# Fixture chain:
#   tests/conftest.py          (session) - output cleanup, allure setup, log fixture
#       v
#   tests/ui/conftest.py       (ui)      - driver, region, screenshot/video hooks
#       v
#   tests/ui/pta/conftest.py   (this)    - PTA testdata fixture
#       v
#   tests/ui/pta/test_pta_*.py           - test cases
# =============================================================================

import pytest

from config.config_parser import ConfigParser


# =============================================================================
# FIXTURE: testdata (session scope)
# =============================================================================
# Loads the PTA UI test data configuration ONCE per test session.
# Data comes from config/ui/pta/ui_test_data_config.yml
#
# Usage in a test:
#   def test_login(driver, testdata, region):
#       username = testdata[region]["username"]
# =============================================================================
@pytest.fixture(scope="session")
def testdata():
    return ConfigParser.load_config("pta_ui_test_data_config")
