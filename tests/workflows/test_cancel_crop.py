"""API-only cancellation placeholder.

The supplied cURLs do not include a cancel-crop endpoint or cancellation contract.
This test intentionally skips until the endpoint/method/payload are supplied.
"""
import pytest

@pytest.mark.integration
def test_cancel_crop():
    pytest.skip("Cancel-crop API was not included in the supplied cURLs. Provide its endpoint, method and request body.")
