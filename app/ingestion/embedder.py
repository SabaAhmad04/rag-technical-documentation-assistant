from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from app.utils.config import settings
from app.utils.logger import get_logger

logger = get_logger()


class EmbeddingModel:
    """
    Singleton wrapper for the HuggingFace embedding model.
    """

    def __init__(self):
        logger.info(
            f"Loading embedding model: {settings.EMBEDDING_MODEL}"
        )

        self._embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={
                "device": "cpu",
            },
            encode_kwargs={
                "normalize_embeddings": True,
            },
        )

        logger.success("Embedding model loaded successfully.")

    @property
    def embeddings(self) -> HuggingFaceEmbeddings:
        return self._embeddings

    def embed_query(self, text: str):
        """
        Generate embedding for a query.
        """
        return self._embeddings.embed_query(text)

    def embed_documents(self, texts: list[str]):
        """
        Generate embeddings for multiple documents.
        """
        return self._embeddings.embed_documents(texts)


@lru_cache
def get_embeddings() -> HuggingFaceEmbeddings:
    """
    Returns a cached HuggingFaceEmbeddings instance.
    """
    return EmbeddingModel().embeddings


@lru_cache
def get_embedding_model() -> EmbeddingModel:
    """
    Returns the cached embedding wrapper.
    """
    return EmbeddingModel()