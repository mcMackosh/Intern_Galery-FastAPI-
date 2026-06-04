from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    NODE_ENV: str

    APPLICATION_PORT: int
    APPLICATION_URL: str
    ALLOWED_ORIGIN: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    REDIS_USER: str
    REDIS_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: int
    JWT_REFRESH_SECRET: str

    JWT_SECRET: str
    COOKIES_SECRET: str

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )

settings = Settings() # type: ignore