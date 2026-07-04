"""Application configuration.

Loads environment variables (from a local ``.env`` file, if present, via
``python-dotenv``) and exposes them as module-level constants used
throughout the app (database credentials, TBA API credentials, default
season year).

Required variables (see ``.env.exemple``):
    ``TBA_KEY``, ``TBA_BASE_URL``, ``DB_NAME``, ``DB_USER``, ``DB_PASSWORD``,
    ``DB_HOST``, ``DB_PORT``.

Optional variables:
    ``FRC_YEAR`` (defaults to ``2026``).

Importing this module raises :class:`ValueError` immediately if any
*required* variable is missing or empty, so configuration problems are
caught at startup rather than at first use.
"""

import os
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv()


def must_getenv(key: str) -> str:
    """Fetch a required environment variable or raise.

    :param key: Name of the environment variable to read.
    :type key: str
    :raises ValueError: If the variable is unset or blank (empty/whitespace).
    :return: The variable's value.
    :rtype: str
    """
    value = os.getenv(key)
    if value is None or value.strip() == "":
        raise ValueError(f"Variable {key} is not set in the environment")
    return value

# TBA configuration
TBA_KEY = must_getenv("TBA_KEY")           # TBA Read API key (X-TBA-Auth-Key)
TBA_BASE_URL = must_getenv("TBA_BASE_URL")  # e.g. https://www.thebluealliance.com/api/v3

# Database configuration
DB_NAME = must_getenv("DB_NAME")
DB_USER = must_getenv("DB_USER")
DB_PASSWORD = must_getenv("DB_PASSWORD")
DB_HOST = must_getenv("DB_HOST")
DB_PORT = must_getenv("DB_PORT")

# Optional has a default value
FRC_YEAR = int(os.getenv("FRC_YEAR", "2026"))  # Current/default competition season