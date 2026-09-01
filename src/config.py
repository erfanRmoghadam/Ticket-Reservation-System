from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    RESERVATION_HOLD_MINUTES: int = 10
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
