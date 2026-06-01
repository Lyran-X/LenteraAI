from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "EduPath AI API"
    app_version: str = "0.1.0"
    app_env: str = "development"
    api_v1_prefix: str = Field(default="/api", alias="API_V1_PREFIX")

    database_url: str = Field(..., alias="DATABASE_URL")
    jwt_secret_key: str = Field(..., alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    upload_dir: str = Field(default="uploads/documents", alias="UPLOAD_DIR")
    vector_store: str = Field(default="chroma", alias="VECTOR_STORE")
    chroma_persist_dir: str = Field(default="./storage/chroma", alias="CHROMA_PERSIST_DIR")
    # Backward-compatible alias for older environments. New installs should use CHROMA_PERSIST_DIR.
    vector_db_path: str = Field(default="./storage/chroma", alias="VECTOR_DB_PATH")
    vector_collection: str = Field(default="edupath_documents", alias="VECTOR_COLLECTION")
    embedding_model: str = Field(default="local-hash-embedding-v1", alias="EMBEDDING_MODEL")

    llm_provider: str = Field(default="placeholder", alias="LLM_PROVIDER")
    llm_model: str = Field(default="placeholder-model", alias="LLM_MODEL")
    gemini_model: str | None = Field(default=None, alias="GEMINI_MODEL")
    llm_api_key: str | None = Field(default=None, alias="LLM_API_KEY")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    gemini_api_key: str | None = Field(default=None, alias="GEMINI_API_KEY")
    groq_api_key: str | None = Field(default=None, alias="GROQ_API_KEY")

    cors_origins: list[str] = Field(
        default=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        alias="CORS_ORIGINS",
    )

    model_config = SettingsConfigDict(
        env_file=(BACKEND_ROOT / ".env", BACKEND_ROOT / ".envy"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()