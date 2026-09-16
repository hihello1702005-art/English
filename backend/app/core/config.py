from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "postgresql+psycopg://english:english@localhost:5432/english_coach"
    jwt_secret: str = "development-only-change-me"
    cors_origins: str = "http://localhost:3000"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"
    speech_provider: str = "unconfigured"
settings = Settings()
