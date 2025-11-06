import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""

    PROJECT_NAME: str = "Line-Up User API"
    PROJECT_VERSION: str = "1.0.0"

    # External API configuration
    REQRES_BASE_URL: str = "https://reqres.in/api"
    REQRES_API_KEY: str = os.getenv("REQRES_API_KEY", "reqres-free-v1")
    API_KEY_HEADER: str = os.getenv("API_KEY_HEADER", "X-API-Key")

    # Application settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"


settings = Settings()
