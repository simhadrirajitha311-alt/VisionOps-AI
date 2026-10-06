from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "VisionOps AI"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./visionops.db"
    camera_index: int = 0
    model_name: str = "yolo11n.pt"
    confidence_threshold: float = 0.5
    tracker_type: str = "bytetrack"
    enable_ai: bool = False
    llm_provider: str = ""
    llm_api_key: str = ""
    webhook_url: str = ""
    frame_width: int = 640
    frame_height: int = 480
    event_cooldown_seconds: int = 10

    class Config:
        extra = "ignore"


settings = Settings()
