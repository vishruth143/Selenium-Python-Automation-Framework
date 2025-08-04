# pylint: disable=[missing-module-docstring, missing-function-docstring]

import os

import pytest

from config.config_parser import ConfigParser
from framework.interfaces.api_client import APIClient

@pytest.fixture(scope="session")
def api_client():
    service_name = os.environ.get("SERVICE_NAME", "").upper()

    # Set default region to 'QA' if REGION env variable is not set
    region = os.environ.get("REGION", "QA").upper()

    headers = {}
    base_url = ""

    if service_name == "REQRES":
        reqres_api_test_env_config = ConfigParser.load_config("reqres_api_test_env_config")

        # Get the correct env block based on the region
        env_config = reqres_api_test_env_config.get(region, {})
        base_url = env_config.get("base_url")
        headers["x-api-key"] = "reqres-free-v1"

    return APIClient(base_url=base_url, headers=headers)
