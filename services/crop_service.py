
class CropService:
    """Service methods for crop-related API operations."""

    ADD_CROP_ENDPOINT = "/api/v1/update-farm-boundry-for-mobile"

    def __init__(self, api_client):
        self.client = api_client

    def add_crop(self, fields):
        """Submit a crop creation request."""
        if not isinstance(fields, dict):
            raise TypeError("fields must be a dictionary")

        return self.client.post(
            self.ADD_CROP_ENDPOINT,
            data=fields.copy(),
        )


    def update_crop(self, fields, farm_id, allocation_id):
        payload = fields.copy()
        payload["farm_id"] = str(farm_id)
        payload["cfa_id"] = str(allocation_id)

        return self.client.post(
            "/api/v1/update-farm-boundry-for-mobile",
            data=payload,
        )

    def check_farm_status(self, farm_id, cfa_id, token=None):
        if not farm_id:
            raise ValueError("farm_id is required")

        if not cfa_id:
            raise ValueError("cfa_id is required")

        payload = {
            "farm_id": farm_id,
            "cfa_id": cfa_id,
        }

        if token:
            payload["_token"] = token

        return self.client.post(
            self.CHECK_FARM_STATUS_ENDPOINT,
            data=payload,
        )
