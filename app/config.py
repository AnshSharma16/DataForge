
import os

from dotenv import load_dotenv

load_dotenv()


def get_database_url() -> str:
    """Return the database URL from the environment."""
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")

    return database_url
