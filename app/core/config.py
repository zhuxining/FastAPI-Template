import tomllib
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    PostgresDsn,
    computed_field,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

with open("pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",  # Allow extra fields from env file
    )

    ENVIRONMENT: Literal["dev", "test", "prod"] = "dev"

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = pyproject.get("project", {}).get("name")
    VERSION: str = pyproject.get("project", {}).get("version")
    DESCRIPTION: str = pyproject.get("project", {}).get("description")

    # CORS Settings
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []

    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS]

    # Allowed Hosts
    TRUSTED_HOSTS: Annotated[list | str, BeforeValidator(parse_cors)] = []

    # Database Settings
    SQLITE_URL: str = "sqlite+aiosqlite:///./dev.db"

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "app"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"

    @computed_field
    @property
    def POSTGRES_URI(self) -> PostgresDsn:  # noqa: N802
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    # JWT Settings
    SECRET_KEY: str = "YOUR-SECRET-KEY-123"  # Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days

    # First Superuser
    FIRST_SUPERUSER_EMAIL: str = "admin@admin.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin@admin.com"


settings = Settings()
