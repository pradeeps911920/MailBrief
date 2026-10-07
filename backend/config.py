from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "MailBrief"
    
    # OAuth Callback URL
    OAUTH_REDIRECT_URI: str = "http://localhost:8000/auth/callback"
    
    # Database
    DATABASE_URL: str = "sqlite:///./mailbrief.db"

    # AI Model
    LLM_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
