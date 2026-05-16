from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost/telemetry"
    SYNC_DATABASE_URL: str = "postgresql://postgres:postgres@localhost/telemetry"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT Settings
    SECRET_KEY: str = "vozmitenastazhirovkupozhaluista"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
