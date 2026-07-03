import os
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv()


def must_getenv(key: str) -> str:
    value = os.getenv(key)
    if value is None or value.strip() == "":
        raise ValueError(f"Variable {key} is not set in the environment")
    return value

# TBA configuration
TBA_KEY = must_getenv("TBA_KEY")
TBA_BASE_URL = must_getenv("TBA_BASE_URL")

# Database configuration
DB_NAME = must_getenv("DB_NAME")
DB_USER = must_getenv("DB_USER")
DB_PASSWORD = must_getenv("DB_PASSWORD")
DB_HOST = must_getenv("DB_HOST")
DB_PORT = must_getenv("DB_PORT")

# Optional has a default value
FRC_YEAR = int(os.getenv("FRC_YEAR", "2026"))