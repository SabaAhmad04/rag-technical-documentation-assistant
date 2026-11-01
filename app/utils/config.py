from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load environment variables from .env
load_dotenv()


class Settings(BaseSettings):
    """
    Centralized application configuration.
    Every module should import `settings` from this file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ==========================
    # Groq
    # ==========================
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # ==========================
    # Embeddings
    # ==========================
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    # ==========================
    # ChromaDB
    # ==========================
    CHROMA_DB_PATH: str = "./chroma_db"
    COLLECTION_NAME: str = "technical_docs"

    # ==========================
    # Tavily
    # ==========================
    TAVILY_API_KEY: str | None = None

    # ==========================
    # FastAPI
    # ==========================
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ==========================
    # Retrieval
    # ==========================
    TOP_K: int = Field(default=5, ge=1)
    MAX_RETRIES: int = Field(default=2, ge=1)

    # ==========================
    # Logging
    # ==========================
    LOG_LEVEL: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.
    """
    return Settings()


settings = get_settings()