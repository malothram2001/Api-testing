import allure
import pytest
from services.farmer_service import FarmerService
from services.farm_service import FarmService
from services.crop_service import CropService
from services.boundary_service import BoundaryService
from utils.data_loader import load_json
from utils.assertions import assert_status, response_json
from utils.allure_helpers import attach_response


def extract_id(data, *keys):
    if isinstance(data, dict):
        for key in keys:
            value = data.get(key)
            if value not in (None, ""):
                return value
        for value in data.values():
            found = extract_id(value, *keys)
            if found not in (None, ""):
                return found
    elif isinstance(data, list):
        for item in data:
            found = extract_id(item, *keys)
            if found not in (None, ""):
                return found
    return None


def response_id(response, *keys):
    assert_status(response)
    body = response_json(response)
    value = extract_id(body, *keys)
    assert value is not None, f"Could not find ID fields {keys} in response: {body}"
    return value


@allure.epic("Krishivaas API Automation")
@allure.feature("End-to-End Farmer Workflow")
@allure.story("Add/update farmer, farm, crop and boundary")
@allure.title("End-to-end workflow: Farmer to Farm Boundary")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.integration
def test_farmer_farm_crop_boundary(api_client):
    farmer_service = FarmerService(api_client)
    farm_service = FarmService(api_client)
    crop_service = CropService(api_client)
    boundary_service = BoundaryService(api_client)

    with allure.step("1. Add Farmer"):
        farmer_fields = load_json("farmer_data.json")["add"].copy()
        response = farmer_service.add_farmer(farmer_fields)
        attach_response(response, "Add Farmer response")
        farmer_id = response_id(response, "fmr_id")
        allure.attach(str(farmer_id), "Created fmr_id", allure.attachment_type.TEXT)

    with allure.step("2. Update Farmer"):
        fields = load_json("farmer_data.json")["update"].copy()
        response = farmer_service.update_farmer(fields, farmer_id)
        attach_response(response, "Update Farmer response")
        assert_status(response)

    with allure.step("3. Add Farm"):
        fields = load_json("farm_data.json")["add"].copy()
        fields["contact_person_id"] = farmer_id
        response = farm_service.add_farm(fields)
        attach_response(response, "Add Farm response")
        farm_id = response_id(response, "flu_id", "farm_id")
        allure.attach(str(farm_id), "Created farm ID", allure.attachment_type.TEXT)

    with allure.step("4. Update Farm"):
        fields = load_json("farm_data.json")["update"].copy()
        fields.update({"flu_id": farm_id, "fmr_id": farmer_id})
        response = farm_service.update_farm(fields)
        attach_response(response, "Update Farm response")
        assert_status(response)

    with allure.step("5. Add Crop"):
        fields = load_json("crop_data.json")["add"].copy()
        fields.update({"fmr_id": farmer_id, "flu_id": farm_id})
        response = crop_service.add_crop(fields)
        attach_response(response, "Add Crop response")
        allocation_id = response_id(response, "cfa_id", "allocation_id", "crop_allocation_id")
        allure.attach(str(allocation_id), "Created crop allocation ID", allure.attachment_type.TEXT)

    with allure.step("6. Update Crop"):
        fields = load_json("crop_data.json")["update"].copy()
        fields.update({"fmr_id": farmer_id, "flu_id": farm_id})
        response = crop_service.update_crop(allocation_id, fields)
        attach_response(response, "Update Crop response")
        assert_status(response)

    with allure.step("7. Add Boundary"):
        fields = load_json("boundary_data.json")["add"].copy()
        fields.update({"farm_id": farm_id, "cfa_id": allocation_id})
        response = boundary_service.add_boundary(fields)
        attach_response(response, "Add Boundary response")
        assert_status(response)
        print("Boundary response:", response_json(response))


