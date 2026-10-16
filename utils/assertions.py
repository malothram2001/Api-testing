
def assert_status_code(response, expected_status: int) -> None:
    assert response.status_code == expected_status, (
        f"Expected HTTP {expected_status}, "
        f"received HTTP {response.status_code}."
    )


def assert_json_response(response) -> dict:
    content_type = response.headers.get("Content-Type", "")

    assert "application/json" in content_type.lower(), (
        f"Expected a JSON response, received: {content_type}"
    )

    data = response.json()

    assert isinstance(data, dict), (
        "Expected the response to be a JSON object."
    )

    return data
