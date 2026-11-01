from app.graph.builder import rag_graph

from app.utils.config import settings
from app.utils.logger import get_logger

logger = get_logger()


class RAGService:
    """
    Service responsible for interacting with the
    LangGraph workflow.
    """

    def __init__(self):
        self.graph = rag_graph

    def query(self, question: str) -> dict:
        """
        Execute the Self-Corrective RAG workflow.
        """

        logger.info("Executing RAG workflow...")

        try:

            initial_state = {
                "question": question,
                "rewritten_query": question,
                "query_type": "",
                "retrieved_documents": [],
                "relevant_documents": [],
                "answer": "",
                "sources": [],
                "hallucination_status": "",
                "hallucination_confidence": 0,
                "hallucination_reason": "",
                "retries": 0,
                "max_retries": settings.MAX_RETRIES,
                "feedback": "",
                "error": "",
            }

            result = self.graph.invoke(initial_state)

            logger.success("Workflow completed successfully.")

            return {
                "success": True,
                "question": question,
                "rewritten_query": result.get(
                    "rewritten_query",
                    question,
                ),
                "query_type": result.get(
                    "query_type",
                    "general",
                ),
                "answer": result.get(
                    "answer",
                    "",
                ),
                "sources": result.get(
                    "sources",
                    [],
                ),
                "hallucination": {
                    "status": result.get(
                        "hallucination_status",
                        "",
                    ),
                    "confidence": result.get(
                        "hallucination_confidence",
                        0,
                    ),
                    "reason": result.get(
                        "hallucination_reason",
                        "",
                    ),
                },
                "retries": result.get(
                    "retries",
                    0,
                ),
            }

        except Exception as e:

            logger.exception("RAG workflow failed.")

            return {
                "success": False,
                "error": str(e),
            }


rag_service = RAGService()