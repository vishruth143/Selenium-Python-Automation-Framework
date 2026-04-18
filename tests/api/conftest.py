# pylint: disable=[missing-module-docstring, missing-function-docstring, line-too-long]

import os
import pytest

from config.config_parser import ConfigParser
from framework.interfaces.api_client import APIClient

@pytest.fixture(scope="session")
def api_client():
    service_name = os.environ.get("SERVICE_NAME", "").upper()
    if not service_name:
        raise ValueError("SERVICE_NAME environment variable must be set and non-blank.")

    # Set default region to 'QA' if REGION env variable is not set
    region = os.environ.get("REGION", "QA").upper()

    headers = {}
    base_url = ""

    if service_name == "JSONPLACEHOLDER":
        jsonplaceholder_api_test_env_config = ConfigParser.load_config("jsonplaceholder_api_test_env_config")
        env_config = jsonplaceholder_api_test_env_config.get(region, {})
        base_url = env_config.get("base_url")
    else:
        raise ValueError(f"Unsupported SERVICE_NAME: '{service_name}'. Supported: JSONPLACEHOLDER.")

    return APIClient(base_url=base_url, headers=headers)
