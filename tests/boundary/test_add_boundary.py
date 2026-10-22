import allure
import pytest
from config import settings
from services.boundary_service import BoundaryService
from utils.data_loader import load_json
from utils.assertions import assert_status, response_json
from utils.allure_helpers import attach_response

@allure.epic("Krishivaas API Automation")
@allure.feature("Farm Boundary Management")
@allure.story("Add Boundary")
@allure.title("Add boundary to existing farm")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.integration
def test_add_boundary(api_client):
    farm_id = settings.env_id("EXISTING_BOUNDARY_FARM_ID") or settings.env_id("EXISTING_FARM_ID")
    cfa_id = settings.env_id("EXISTING_BOUNDARY_CFA_ID")
    if not farm_id or not cfa_id:
        pytest.skip("Set EXISTING_FARM_ID and EXISTING_BOUNDARY_CFA_ID; confirm cfa_id is required for add.")
    with allure.step("Prepare Add Boundary data"):
        fields = load_json("boundary_data.json")["add"].copy()
        fields.update({"farm_id": farm_id, "cfa_id": cfa_id})
    with allure.step("Send Add Boundary request"):
        response = BoundaryService(api_client).add_boundary(fields)
        attach_response(response, "Add Boundary response")
    with allure.step("Validate response"):
        assert_status(response)
        print("Add boundary response:", response_json(response))
