import pytest
from clients.api_client import APIClient
from config import settings
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="session")
def api_client():
    if not settings.API_TOKEN:
        pytest.fail("API_TOKEN is missing. Copy .env.example to .env and add a fresh staging token.")
    client = APIClient()
    yield client
    client.close()
