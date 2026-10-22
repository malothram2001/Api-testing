import os
import allure
import pytest
from config import settings
from services.farm_service import FarmService
from utils.data_loader import load_json
from utils.assertions import assert_status, response_json
from utils.allure_helpers import attach_response

@allure.epic("Krishivaas API Automation")
@allure.feature("Farm Management")
@allure.story("Add Farm")
@allure.title("Add farm for an existing farmer")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.integration
def test_add_farm(api_client):
    farmer_id = settings.env_id("EXISTING_FARMER_ID")
    if not farmer_id:
        pytest.skip("Set EXISTING_FARMER_ID in .env or run Add Farmer first.")
    with allure.step("Prepare Add Farm data"):
        fields = load_json("farm_data.json")["add"].copy()
        fields["contact_person_id"] = farmer_id
        fields["contact_number"] = os.getenv("TEST_MOBILE_NUMBER", "")
        fields["mapIndia_token"] = os.getenv("MAPINDIA_TOKEN", "")
    with allure.step("Send Add Farm request"):
        response = FarmService(api_client).add_farm(fields)
        attach_response(response, "Add Farm response")
    with allure.step("Validate response"):
        assert_status(response)
        print("Add farm response:", response_json(response))
