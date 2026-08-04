from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "CyberMentorTok"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    DATABASE_URL: str = "sqlite+aiosqlite:///./cybermentortok.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672//"

    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    S3_ENDPOINT: str = "http://localhost:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET_VIDEOS: str = "cybermentortok-videos"
    S3_BUCKET_BACKGROUNDS: str = "cybermentortok-backgrounds"
    S3_BUCKET_ASSETS: str = "cybermentortok-assets"

    OPENSEARCH_URL: str = "http://localhost:9200"
    CLICKHOUSE_URL: str = "http://localhost:8123"

    RENDERING_WORKERS: int = 4
    RENDER_TIMEOUT_SECONDS: int = 300

    AI_FACT_CHECK_CONFIDENCE_THRESHOLD: float = 0.95

    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8080"]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
