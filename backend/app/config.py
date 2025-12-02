from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "Q-Loyal"

    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_ANON_KEY: str

    TELEGRAM_BOT_TOKEN: str

settings = Settings()
