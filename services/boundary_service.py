class BoundaryService:
    # As requested, add and update use the same endpoint.
    ENDPOINT = "/api/v1/update-farm-boundry-for-mobile"

    def __init__(self, client):
        self.client = client

    def add_boundary(self, fields):
        self._validate(fields)
        return self.client.post(
            self.ENDPOINT,
            data=fields,
            headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        )

    def update_boundary(self, fields):
        self._validate(fields)
        return self.client.post(
            self.ENDPOINT,
            data=fields,
            headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        )

    @staticmethod
    def _validate(fields):
        required = ("farm_id", "farm_updated_cord", "farm_calculated_area",
                    "farm_calculated_area_unit", "boundary_method_type")
        missing = [name for name in required if fields.get(name) in (None, "")]
        if missing:
            raise ValueError(f"Boundary request is missing required fields: {', '.join(missing)}")
