
import os
import logging
import json
import allure
import pytest

from services.farmer_service import FarmerService
from utils.data_loader import load_json
from utils.assertions import (
    assert_status,
    response_json,
    assert_response_matches,
)
logger = logging.getLogger(__name__)


@allure.epic("Krishivaas API Automation")
@allure.feature("Farmer Management")
@allure.story("Add Farmer")
@allure.title("Verify Add Farmer API creates a farmer")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.integration
def test_add_farmer(api_client):

    with allure.step("1. Load Add Farmer test data"):
        fields = load_json("farmer_data.json")["add"].copy()

        mapindia_token = os.getenv("MAPINDIA_TOKEN", "").strip()

        if fields.get("mapIndia_token") == "${MAPINDIA_TOKEN}":
            fields["mapIndia_token"] = mapindia_token

        if not fields.get("mapIndia_token"):
            pytest.fail(
                "MAPINDIA_TOKEN is missing. Configure it in .env "
                "and ensure the environment file is loaded."
            )

        # Do not log the token or the full request payload.
        logger.info("Add Farmer test data loaded.")

    with allure.step("2. Send Add Farmer API request"):
        response = FarmerService(api_client).add_farmer(fields)

    with allure.step("3. Validate HTTP response status"):
        assert_status(response)

    with allure.step("4. Validate API success and message"):
        body = response_json(response)

        assert isinstance(body, dict), "Expected a JSON object response."

        assert body.get("success") is True, (
            f"Farmer creation failed: {body.get('message')}"
        )

        assert body.get("message") == "Farmer added successfully.!", (
            f"Unexpected API message: {body.get('message')}"
        )

    with allure.step("Compare actual and expected response"):
        body = response_json(response)
    
        assert isinstance(body, dict), (
            "Expected the API response to be a JSON object."
        )
    
        expected = {
            "success": True,
            "message": "Farmer added successfully.!",
        }
    
        assert_response_matches(body, expected)
    
    with allure.step("Validate the created farmer ID"):
        farmer_data = body.get("data")
    
        assert isinstance(farmer_data, dict), (
            "Expected a data object in the response."
        )
    
        fmr_id = farmer_data.get("fmr_id")
    
        assert str(fmr_id).isdigit() and int(fmr_id) > 0, (
            f"Expected a positive numeric farmer ID; got {fmr_id!r}"
        )