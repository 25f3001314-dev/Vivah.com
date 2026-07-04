from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application configuration loaded from environment variables.

    Defaults are set to preserve existing behavior where possible.
    """

    # Environment
    APP_ENV: str = "development"

    # Ports
    PORT: int = 8000
    API_PORT: int = 8000

    # Logging
    LOG_LEVEL: str = "INFO"

    # Other settings can be added here (secrets, feature flags, third-party keys)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton settings object to import throughout the app
settings = Settings()
