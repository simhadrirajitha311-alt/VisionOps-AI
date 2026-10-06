from app.core.config import Settings


def test_settings_defaults_and_env_overrides():
    settings = Settings()
    assert settings.model_name
    assert settings.confidence_threshold >= 0.0
    assert settings.tracker_type in {"bytetrack", "sort", "none"}
