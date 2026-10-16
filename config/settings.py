
import os
from pathlib import Path
from dotenv import load_dotenv

# Project root: parent directory of config/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_FILE, override=True)

BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://api.staging.krishivaas.com",
).rstrip("/")

ADD_FARMER_PATH = os.getenv(
    "ADD_FARMER_PATH",
    "/api/v1/save-farmer-detail",
).strip()

ADD_FARMER_METHOD = os.getenv(
    "ADD_FARMER_METHOD",
    "POST",
).upper()

ADD_FARMER_EXPECTED_STATUS = int(
    os.getenv("ADD_FARMER_EXPECTED_STATUS", "200")
)

API_TOKEN = os.getenv("API_TOKEN", "")
API_TIMEOUT = float(os.getenv("API_TIMEOUT", "15"))
