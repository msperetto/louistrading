import os
from dotenv import load_dotenv

# Get secret from file in production, environment variable in development
def get_secret(secret_name: str) -> str:
    if not os.getenv(secret_name):
        raise ValueError(f"{secret_name} environment variable not set")
        return None
    return os.getenv(secret_name)