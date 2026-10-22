"""Creates farmer, farm and crop, then submits boundary using the same boundary endpoint."""
import os
import pytest
from services.farmer_service import FarmerService
from services.farm_service import FarmService
from services.crop_service import CropService
from services.boundary_service import BoundaryService
from utils.data_loader import load_json
from utils.assertions import assert_status, response_json, extract_id

@pytest.mark.integration
def test_farmer_farm_crop_boundary_workflow(api_client):
    mobile = os.getenv("TEST_MOBILE_NUMBER", "")
    if not mobile:
        pytest.skip("Set a unique TEST_MOBILE_NUMBER in .env.")
    farmer_fields = load_json("farmer_data.json")["add"]
    farmer_fields.update({
        "mobile_number": mobile,
        "business_unit": os.getenv("BUSINESS_UNIT", "devqa(All)"),
        "businessunit_hiddenfield": os.getenv("BUSINESS_UNIT_ID", "333"),
        "agent": os.getenv("AGENT_NAME", "Aryan New FA1"),
        "agent_id": os.getenv("AGENT_ID", "3411"),
        "mapIndia_token": os.getenv("MAPINDIA_TOKEN", ""),
    })
    fr = FarmerService(api_client).add_farmer(farmer_fields)
    assert_status(fr)
    farmer_id = extract_id(response_json(fr), ["fmr_id", "farmer_id", "id"])
    assert farmer_id, f"Farmer response did not expose an ID: {response_json(fr)}"

    farm_fields = load_json("farm_data.json")["add"]
    farm_fields.update({"contact_person_id": str(farmer_id), "contact_number": mobile,
                        "mapIndia_token": os.getenv("MAPINDIA_TOKEN", "")})
    farm_response = FarmService(api_client).add_farm(farm_fields)
    assert_status(farm_response)
    farm_id = extract_id(response_json(farm_response), ["flu_id", "farm_id", "id"])
    assert farm_id, f"Farm response did not expose an ID: {response_json(farm_response)}"

    crop_fields = load_json("crop_data.json")["add"]
    crop_fields.update({"fmr_id": str(farmer_id), "flu_id": str(farm_id),
                        "token": os.getenv("API_TOKEN", "")})
    crop_response = CropService(api_client).add_crop(crop_fields)
    assert_status(crop_response)

    boundary_fields = load_json("boundary_data.json")["add"]
    boundary_fields["farm_id"] = str(farm_id)
    cfa_id = os.getenv("EXISTING_BOUNDARY_CFA_ID", "").strip()
    if cfa_id:
        boundary_fields["cfa_id"] = cfa_id
    boundary_response = BoundaryService(api_client).add_boundary(boundary_fields)
    assert_status(boundary_response)
    print("Workflow completed:", {
        "fmr_id": farmer_id, "flu_id": farm_id,
        "crop": response_json(crop_response), "boundary": response_json(boundary_response)
    })
