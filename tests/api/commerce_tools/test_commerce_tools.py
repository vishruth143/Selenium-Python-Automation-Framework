# pylint: disable=[duplicate-code, line-too-long, attribute-defined-outside-init, missing-module-docstring]
# pylint: disable=[no-else-continue, invalid-name, logging-fstring-interpolation, import-error]
# pylint: disable=[too-many-statements, too-many-branches, unused-variable, too-many-locals, unsubscriptable-object]
# pylint: disable=[f-string-without-interpolation, broad-exception-caught]
# pylint: disable=C0302

import os
import json
import pytest

from config.config_parser import ConfigParser
from framework.utilities.custom_logger import Logger

log = Logger(file_id=__name__.rsplit(".", 1)[1])
darden_commerce_tools_api_test_data = ConfigParser.load_config('commerce_tools_api_test_data_config')

@pytest.mark.commerce_tools
class TestCommercetools:
    """
    Test cases for Commercetools API
    """
    def test_query_products(self, api_client, request):
        """
        Test #01 : Verify GET /{project-key}/products
        Steps:
        01) Send GET request to Commercetools API for querying products.
        02) Verify status code is 200.
        03) Validate response structure (must contain 'results').
        """
        test_name = request.node.name.rsplit("[", 1)[0]
        endpoint = f"/darden/products"

        try:
            log.info(50 * "*")
            log.info("Test #01 : Verify GET /{project-key}/products from Commercetools API.")
            log.info(50 * "*")

            log.info("STEP 01: Sending GET request to Commercetools API.")
            response = api_client.get(endpoint)
            log.info(f"Response received: {response.status_code}")
            log.info(f"Response body: {response.text}")

            log.info("STEP 02: Validating status code.")
            assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
            log.info("Status code is 200 as expected.")

            log.info("STEP 03: Validating response body structure and content.")
            json_data = response.json()
            assert "results" in json_data, "Missing 'results' key in the response"

            total = json_data.get("total")
            log.info(f"Total products: {total}")

            results = json_data["results"]
            assert isinstance(results, list), "'results' should be a list"
            log.info(f"Products retrieved: {len(results)}")

            if results:  # Optional: validate structure of first product
                product = results[0]
                assert "id" in product, "Product missing 'id'"
                assert "masterData" in product, "Product missing 'masterData'"
                log.info("First product validated successfully.")

            # Save response to output/response/test_get_product_by_id.json
            output_dir = "output/response"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, test_name+'.json')
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=2)

            log.info("Test #01 : Verify GET /{project-key}/products - Completed Successfully.")
        except Exception as e:
            log.error(f"Exception occurred: {e}")
            log.info("Test #01 : Verify GET /{project-key}/products - Failed")

    def test_get_product_by_id(self, api_client, request):
        """
        Test #01 : Verify GET /{project-key}/products/{product-id}
        Steps:
        01) Send GET request to Commercetools API for querying products by product id.
        02) Verify status code is 200.
        03) Validate response structure (must contain 'results').
        """
        test_name = request.node.name.rsplit("[", 1)[0]
        product_id = darden_commerce_tools_api_test_data.get("get_product_by_id").get("product_id")
        endpoint = f"/darden/products/"+ f"{product_id}"

        try:
            log.info(50 * "*")
            log.info("Test #01 : Verify GET /{project-key}/products/{product-id} from Commercetools API.")
            log.info(50 * "*")

            log.info("STEP 01: Sending GET request to Commercetools API.")
            response = api_client.get(endpoint)
            log.info(f"Response received: {response.status_code}")
            log.info(f"Response body: {response.text}")

            log.info("STEP 02: Validating status code.")
            assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
            log.info("Status code is 200 as expected.")

            log.info("STEP 03: Validating response body structure and content.")
            json_data = response.json()
            assert "masterData" in json_data, "Missing 'masterData' key in the response"

            # Save response to output/response/test_get_product_by_id.json
            output_dir = "output/response"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, test_name+'.json')
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=2)

            log.info("Test #01 : Verify GET /{project-key}/products/{product-id} - Completed Successfully.")
        except Exception as e:
            log.error(f"Exception occurred: {e}")
            log.info("Test #01 : Verify GET /{project-key}/products/{product-id} - Failed")
