from app.graph.state import GraphState

from app.utils.logger import get_logger

logger = get_logger()


class NoAnswerNode:
    """
    Returns a response when no relevant
    documents are found after all retries.
    """

    def __call__(
        self,
        state: GraphState,
    ) -> GraphState:

        logger.info("Running No Answer Node...")

        return {
            **state,
            "answer": (
                "I couldn't find any relevant information in the uploaded "
                "documents to answer your question."
            ),
            "sources": [],
            "hallucination_status": "not_applicable",
            "hallucination_confidence": 0,
            "hallucination_reason": (
                "No relevant documents were found after all retrieval attempts."
            ),
        }


no_answer_node = NoAnswerNode()