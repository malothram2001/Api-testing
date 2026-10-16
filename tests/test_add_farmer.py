
import logging

import pytest

from config.settings import (
    ADD_FARMER_EXPECTED_STATUS,
    ADD_FARMER_METHOD,
    ADD_FARMER_PATH,
    API_TOKEN,
)
from utils.assertions import (
    assert_json_response,
    assert_status_code,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)


@pytest.mark.parametrize("first_name", ["API_Test_Farmer"])
def test_add_farmer(api_client, first_name):
    # Use approved staging test data.
    # Replace BU and agent values if your test account differs.
    payload = {
        "first_name": first_name,
        "chk_dummy_contact": "N",
        "mobile_number": "1000000000",
        "email": "",
        "business_unit": "devqa(All)",
        "businessunit_hiddenfield": "333",
        "agent": "Pramod FA 2",
        "agent_id": "3366",
        "dob": "",
        "age": "",
        "preferred_language": "English",
        "education": "",
        "agriculture_experience": "",
        "phone_connection_network": "",
        "service_provider": "",
        "acreage": "",
        "farmer_scale": "",
        "farming_method": "",
        "address": "",
        "address_lat": "",
        "address_long": "",
        "country": "India",
        "state": "",
        "district": "",
        "mandal": "",
        "village": "",
        "pincode": "",
        "txtPropFarmerID": "",
        "token": API_TOKEN,
        "fmr_id": "",
        "access_type": "add_access",
        "countryCode": " +91",
        "mapIndia_token": "",
        "crop_details": "[]",
        "personal_identification": "undefined",
        "land_record": "undefined",
        "bank_record": "undefined",
    }

    # A file part forces requests to encode the request as multipart/form-data.
    # Requests generates the multipart boundary automatically.
    empty_file_parts = {
        "profile_image": ("", b"", "application/octet-stream"),
        "personal_identification": (
            "", b"", "application/octet-stream"
        ),
        "landholding_records": (
            "", b"", "application/octet-stream"
        ),
        "bank_record": ("", b"", "application/octet-stream"),
    }

    logger.info("Starting Save Farmer API test")
    logger.info("Endpoint: %s", ADD_FARMER_PATH)
    logger.info("HTTP method: %s", ADD_FARMER_METHOD)

    response = api_client.request(
        method=ADD_FARMER_METHOD,
        path=ADD_FARMER_PATH,
        data=payload,
        files=empty_file_parts,
    )

    # Do not log request headers, tokens, or the full response.
    logger.info("HTTP status: %s", response.status_code)

    try:
        result = response.json()
    except ValueError:
        pytest.fail(
            "Save Farmer API returned a non-JSON response. "
            f"HTTP status: {response.status_code}"
        )

    logger.info("API success flag: %s", result.get("success"))
    logger.info("API message: %s", result.get("message"))

    assert_status_code(
        response,
        ADD_FARMER_EXPECTED_STATUS,
    )
    assert_json_response(response)

    assert result.get("success") is True, (
        f"Farmer creation failed: {result.get('message')}"
    )

    farmer = result.get("data")
    assert isinstance(farmer, dict), (
        "Expected farmer details in the response."
    )

    farmer_id = farmer.get("fmr_id")
    assert isinstance(farmer_id, int) and farmer_id > 0
    assert farmer.get("first_name") == first_name

    logger.info(
        "Save Farmer API test passed. Generated farmer ID: %s",
        farmer_id,
    )
