import os
from dotenv import load_dotenv


load_dotenv()


def must_getenv(key: str) -> str:
    value = os.getenv(key)
    if value is None or value.strip() == "":
        raise ValueError(f"variable {key} is not set in the environment")
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


# FRC_YEAR is set to 2026 by default, but can be overridden by an environment variable.
FRC_YEAR = int(os.getenv("FRC_YEAR", "2026"))