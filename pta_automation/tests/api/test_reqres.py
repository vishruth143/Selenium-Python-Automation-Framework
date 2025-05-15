# pylint: disable=[duplicate-code, line-too-long, attribute-defined-outside-init, missing-module-docstring]
# pylint: disable=[no-else-continue, invalid-name, logging-fstring-interpolation, import-error]
# pylint: disable=[too-many-statements, too-many-branches, unused-variable, too-many-locals, unsubscriptable-object]
# pylint: disable=C0302

import os
import pytest

from pta_automation.config.config_parser import ConfigParser
from pta_automation.framework.utilities.custom_logger import Logger

log = Logger(file_id=__name__.rsplit(".", 1)[1])
api_test_data = ConfigParser.load_config('api_test_data_config')

@pytest.mark.req_res
class TestReqRes:

    """
    Test cases for Reqres API
    """

    def test_single_user(self, api_client, request):
        """
        Test #01 : Verify GET /api/users/2
        Steps:
        01) Send GET request to Reqres API for user ID 2.
        02) Verify status code is 200.
        03) Validate user details in the response body.
        """
        test_name = request.node.name.rsplit("[", 1)[0]
        endpoint = "/api/users/2"

        try:
            log.info(50 * '*')
            log.info("Test #01 : Verify GET /api/users/2 from Reqres API.")
            log.info(50 * '*')

            log.info("STEP 01: Sending GET request to Reqres API.")
            response = api_client.get(endpoint)
            log.info(f"Response received: {response.status_code}")
            log.info(f"Response body: {response.text}")

            log.info("STEP 02: Validating status code.")
            assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
            log.info("Status code is 200 as expected.")

            log.info("STEP 03: Validating response body structure and content.")
            json_data = response.json()
            assert "data" in json_data, "Missing 'data' key in the response"
            user_data = json_data["data"]

            assert user_data["id"] == 2, f"Expected user ID 2, but got {user_data['id']}"
            assert user_data["email"] == "janet.weaver@reqres.in", f"Expected email 'janet.weaver@reqres.in', but got {user_data['email']}"
            assert user_data["first_name"] == "Janet", f"Expected first name 'Janet', but got {user_data['first_name']}"
            assert user_data["last_name"] == "Weaver", f"Expected last name 'Weaver', but got {user_data['last_name']}"
            log.info("User details validated successfully.")

            log.info("Test #01 : Verify GET /api/users/2 - Completed Successfully.")
        except Exception as e:
            log.error(f"Exception occurred: {e}")
            log.info("Test #01 : Verify GET /api/users/2 - Failed")
            raise

    def test_create(self, api_client, request):
        """
        Test #02 : Verify POST /api/users
        Steps:
        01) Send POST request to Reqres API to create a user.
        02) Validate status code is 201.
        03) Validate response contains the expected user details.
        """
        test_name = request.node.name.rsplit("[", 1)[0]
        endpoint = "/api/users"
        payload = api_test_data.get("Create", {})

        try:
            log.info(50 * '*')
            log.info("Test #02 : Verify POST /api/users to create a user.")
            log.info(50 * '*')

            log.info("STEP 01: Sending POST request to create user.")
            response = api_client.post(endpoint, json=payload)
            log.info(f"Response received: {response.status_code}")
            log.info(f"Response body: {response.text}")

            log.info("STEP 02: Validating status code.")
            assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
            log.info("Status code is 201 as expected.")

            log.info("STEP 03: Validating response body content.")
            response_data = response.json()

            assert response_data["name"] == "morpheus", f"Expected name 'morpheus', got {response_data.get('name')}"
            assert response_data["job"] == "leader", f"Expected job 'leader', got {response_data.get('job')}"
            assert "id" in response_data, "Expected response to contain 'id'"
            assert "createdAt" in response_data, "Expected response to contain 'createdAt'"
            log.info("User creation response validated successfully.")

            log.info("Test #02 : Verify POST /api/users - Completed Successfully.")
        except Exception as e:
            log.error(f"Exception occurred: {e}")
            log.info("Test #02 : Verify POST /api/users - Failed")
            raise
