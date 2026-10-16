
import pytest

from config.settings import (
    API_TIMEOUT,
    API_TOKEN,
    BASE_URL,
)
from clients.api_client import APIClient


@pytest.fixture
def api_client():
    client = APIClient(
        base_url=BASE_URL,
        token=API_TOKEN,
        timeout=API_TIMEOUT,
    )

    yield client

    client.close()
