import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file only if present (useful for local dev)
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

def get_env_variable(key: str, default: str | None = None) -> str:
    """
    Gets an environment variable.
    - First checks system environment (CI/CD secrets, etc.)
    - Falls back to .env file if available.
    - Optionally returns default if not found.
    """
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"Missing required environment variable: {key}")
    return value
