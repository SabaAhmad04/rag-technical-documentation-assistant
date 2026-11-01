from functools import lru_cache

from langchain_groq import ChatGroq

from app.utils.config import settings
from app.utils.logger import get_logger

logger = get_logger()


class GroqClient:
    """
    Singleton wrapper around the Groq Chat model.
    Used throughout the application for:
    - Query Analysis
    - Query Rewriting
    - Document Grading
    - Answer Generation
    - Hallucination Checking
    """

    def __init__(self):
        logger.info(f"Initializing Groq model: {settings.GROQ_MODEL}")

        self._llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL,
            temperature=0,
            max_retries=2,
            timeout=60,
        )

    @property
    def llm(self):
        return self._llm

    def invoke(self, prompt: str) -> str:
        """
        Invoke the LLM with a prompt.

        Args:
            prompt: Prompt string

        Returns:
            Model response as string
        """
        try:
            response = self._llm.invoke(prompt)

            if hasattr(response, "content"):
                return response.content.strip()

            return str(response).strip()

        except Exception as e:
            logger.exception("Groq invocation failed.")
            raise RuntimeError(f"Groq Error: {e}") from e


@lru_cache
def get_llm() -> ChatGroq:
    """
    Returns a cached ChatGroq instance.
    """
    return GroqClient().llm


@lru_cache
def get_groq_client() -> GroqClient:
    """
    Returns a cached GroqClient instance.
    """
    return GroqClient()