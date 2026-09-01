from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://postgres:%400110688635@localhost:5432/ticketdb"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "a-really-really-long-hard-to-guess-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    RESERVATION_HOLD_MINUTES: int = 10
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
