import json
import allure

def attach_response(response, name="API response"):
    """Attach response status/body only; never attach request headers or tokens."""
    try:
        body = json.dumps(response.json(), indent=2, ensure_ascii=False, default=str)
    except (ValueError, AttributeError):
        body = getattr(response, "text", "<No response body>")
    allure.attach(
        f"HTTP status: {getattr(response, 'status_code', 'unknown')}\n\n{body}",
        name=name,
        attachment_type=allure.attachment_type.TEXT,
    )
