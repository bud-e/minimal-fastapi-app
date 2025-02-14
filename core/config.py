import os

from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings

load_dotenv(".env")

# API config
API_V1_PREFIX = "/v1"

# Service config
SERVICE_NAME = os.getenv("SERVICE_NAME", "Minimal FastAPI APP")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "v1.0.0")
ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))

# DB config
SQLITE_FILE_NAME = os.getenv("SQLITE_FILE_NAME", "database.db")
