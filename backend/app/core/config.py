from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    CHROMA_PERSIST_DIRECTORY: str = "chroma_data"
    RAG_CONFIDENCE_THRESHOLD: float = 0.7
    REDIS_URL: str = "redis://localhost:6379/0"
    RATE_LIMIT_PER_MINUTE: str = "60/minute"
    LOG_LEVEL: str = "INFO"
    LOGFIRE_TOKEN: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
