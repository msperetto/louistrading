import os
from pathlib import Path
from dotenv import load_dotenv
from common.enums import Environment_Place

# Get secret from file in production, environment variable in development
def get_secret(secret_name: str) -> str:
    if os.getenv('ENVIRONMENT') != Environment_Place.AWS:
        env_path = Path(__file__).parent.parent.parent / '.env'
        print(f"Loading environment variables from {env_path}")
        load_dotenv(dotenv_path=env_path)  # Load environment variables from .env file
    if not os.getenv(secret_name):
        raise ValueError(f"{secret_name} environment variable not set")
        return None
    return os.getenv(secret_name)