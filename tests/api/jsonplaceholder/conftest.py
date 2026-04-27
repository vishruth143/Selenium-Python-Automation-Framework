# pylint: disable=[missing-function-docstring, missing-module-docstring, redefined-outer-name, unused-argument]
# pylint: disable=[line-too-long]

# =============================================================================
# JSONPLACEHOLDER CONFTEST - Fixtures specific to the JSONPlaceholder API suite
# =============================================================================
#
# Auto-loaded by pytest for every test under tests/api/jsonplaceholder/.
#
# Provides:
#   1. "api_client"  - configured APIClient pointing at the JSONPlaceholder
#                      base URL for the current REGION (session scope).
#   2. "testdata"    - loads JSONPlaceholder request/response payloads from
#                      config/api/jsonplaceholder/api_test_data_config.json.
#
# Fixture chain:
#   tests/conftest.py                       (session) - output cleanup, allure
#       v
#   tests/api/conftest.py                   (api)     - shared API helpers
#       v
#   tests/api/jsonplaceholder/conftest.py   (this)    - service-specific fixtures
#       v
#   tests/api/jsonplaceholder/test_*.py               - test cases
# =============================================================================

import os
import pytest

from config.config_parser import ConfigParser
from framework.interfaces.api_client import APIClient


@pytest.fixture(scope="session")
def api_client():
    """Configured APIClient for the JSONPlaceholder service."""
    region = os.environ.get("REGION", "QA").upper()
    env_config = ConfigParser.load_config("jsonplaceholder_api_test_env_config")
    base_url = env_config.get(region, {}).get("base_url")
    if not base_url:
        raise ValueError(
            f"No base_url configured for region '{region}' in "
            "jsonplaceholder_api_test_env_config.yml"
        )
    return APIClient(base_url=base_url, headers={})


@pytest.fixture(scope="session")
def testdata():
    """Load JSONPlaceholder request/response payloads."""
    return ConfigParser.load_config("jsonplaceholder_api_test_data_config")
