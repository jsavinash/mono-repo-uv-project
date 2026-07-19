from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # API
    api_base_url: str = "http://localhost:8000/api/v1"
    api_timeout: int = 30

    # Auth
    auth_token: str = ""

    # App
    app_name: str = "Frontend"
    app_icon: str = "🚀"
    app_layout: str = "wide"
    app_sidebar_state: str = "expanded"


settings = Settings()
