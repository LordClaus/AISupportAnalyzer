from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str
    DATABASE_URL: str
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str
    MODEL_NAME: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()