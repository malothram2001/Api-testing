"""Creates farmer + farm, deliberately skips crop, then submits boundary."""
import os
import pytest
from services.farmer_service import FarmerService
from services.farm_service import FarmService
from services.boundary_service import BoundaryService
from utils.data_loader import load_json
from utils.assertions import assert_status, response_json, extract_id

@pytest.mark.integration
def test_farmer_farm_skip_crop_add_boundary(api_client):
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

    boundary_fields = load_json("boundary_data.json")["add"]
    boundary_fields.update({"farm_id": str(farm_id)})
    # cfa_id is included only if configured because the supplied cURL may represent an update.
    cfa_id = os.getenv("EXISTING_BOUNDARY_CFA_ID", "").strip()
    if cfa_id:
        boundary_fields["cfa_id"] = cfa_id
    boundary_response = BoundaryService(api_client).add_boundary(boundary_fields)
    assert_status(boundary_response)
    print("Crop intentionally skipped. Farmer/farm/boundary IDs:",
          {"fmr_id": farmer_id, "flu_id": farm_id, "boundary": response_json(boundary_response)})
