from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",  # Allow extra fields from env file
    )

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "YLSH Backend"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Modern FastAPI backend with FastAPI Users"

    # CORS Settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # Database Settings
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"

    # JWT Settings
    SECRET_KEY: str = "YOUR-SECRET-KEY-123"  # Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # First Superuser
    FIRST_SUPERUSER_EMAIL: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin123"


settings = Settings()
