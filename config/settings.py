import os
from dotenv import load_dotenv

load_dotenv()

def _bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y"}

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.staging.krishivaas.com").rstrip("/")
WEB_BASE_URL = os.getenv("WEB_BASE_URL", "https://devqa.staging.krishivaas.com").rstrip("/")
API_TOKEN = os.getenv("API_TOKEN", "").strip()
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
VERIFY_TLS = _bool("VERIFY_TLS", True)

def env_id(name: str):
    value = os.getenv(name, "").strip()
    return value or None
