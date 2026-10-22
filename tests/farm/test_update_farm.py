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
@allure.story("Update Farm")
@allure.title("Update existing farm")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.integration
def test_update_farm(api_client):
    farm_id = settings.env_id("EXISTING_FARM_ID")
    farmer_id = settings.env_id("EXISTING_FARMER_ID")
    if not farm_id or not farmer_id:
        pytest.skip("Set EXISTING_FARM_ID and EXISTING_FARMER_ID in .env.")
    with allure.step("Prepare Update Farm data"):
        fields = load_json("farm_data.json")["update"].copy()
        fields.update({
            "flu_id": farm_id, "fmr_id": farmer_id,
            "contact_number": os.getenv("TEST_MOBILE_NUMBER", ""),
            "mapIndia_token": os.getenv("MAPINDIA_TOKEN", ""),
        })
    with allure.step(f"Update farm flu_id={farm_id}"):
        response = FarmService(api_client).update_farm(fields)
        attach_response(response, "Update Farm response")
    with allure.step("Validate response"):
        assert_status(response)
        print("Update farm response:", response_json(response))
