# pylint: disable=[missing-module-docstring, missing-function-docstring]

import os

import pytest

from pta_automation.config.config_parser import ConfigParser
from pta_automation.framework.interfaces.api_client import APIClient

@pytest.fixture(scope="session")
def api_client():
    api_test_env_config = ConfigParser.load_config("api_test_env_config")

    # Get the correct env block based on the region
    env_config = api_test_env_config.get(os.environ["REGION"].upper(), {})

    base_url = env_config.get("base_url")
    return APIClient(base_url)
