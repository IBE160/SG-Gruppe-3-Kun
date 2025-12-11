from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@host:port/dbname" # Placeholder

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
