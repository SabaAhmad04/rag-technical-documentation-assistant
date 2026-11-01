from app.graph.state import GraphState

from app.llm.groq_client import get_llm
from app.llm.prompts import QUERY_REWRITE_PROMPT

from app.utils.logger import get_logger

logger = get_logger()


class QueryRewriterNode:
    """
    Rewrites the user's query when retrieval fails.

    Responsibilities:
    -----------------
    - Improve the search query
    - Increment retry counter
    - Preserve original question
    """

    def __init__(self):
        self.llm = get_llm()

    def __call__(
        self,
        state: GraphState,
    ) -> GraphState:

        logger.info("Running Query Rewriter Node...")

        original_question = state["question"]

        retries = state.get("retries", 0) + 1

        try:

            prompt = QUERY_REWRITE_PROMPT.invoke(
                {
                    "question": original_question,
                }
            )

            response = self.llm.invoke(prompt)

            rewritten_query = response.content.strip()

            logger.success(
                f"Query rewritten successfully (Retry {retries})."
            )

            return {
                **state,
                "rewritten_query": rewritten_query,
                "retries": retries,
            }

        except Exception as e:

            logger.exception(
                "Query rewriting failed."
            )

            return {
                **state,
                "rewritten_query": original_question,
                "retries": retries,
                "error": str(e),
            }


query_rewriter_node = QueryRewriterNode()