from src.config import Settings


def test_settings_defaults():
    settings = Settings()
    assert settings.app_name is not None
    assert settings.api_base_url is not None
