from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Smart Traffic Management AI"
    environment: str = "development"
    database_url: str = "sqlite:///./smart_traffic.db"
    jwt_secret: str = "change-this-secret-in-production"
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    openweather_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
