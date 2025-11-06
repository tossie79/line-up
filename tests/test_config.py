import os
from app.core.config import settings


def test_settings():
    """Test that settings are loaded correctly"""
    assert settings.PROJECT_NAME == "Line-Up User API"
    assert settings.PROJECT_VERSION == "1.0.0"
    assert settings.REQRES_BASE_URL == "https://reqres.in/api"
    assert hasattr(settings, "REQRES_API_KEY")  # May be empty string
    assert hasattr(settings, "DEBUG")


def test_environment_variables(monkeypatch):
    """Test environment variable loading"""
    monkeypatch.setenv("REQRES_API_KEY", "test_key_123")
    monkeypatch.setenv("DEBUG", "True")

    # Reload settings to pick up new env vars
    from importlib import reload
    import app.core.config

    reload(app.core.config)

    from app.core.config import settings

    assert settings.REQRES_API_KEY == "test_key_123"
    assert settings.DEBUG == True
