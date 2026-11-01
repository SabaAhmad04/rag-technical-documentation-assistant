from app.graph.state import GraphState

from app.llm.groq_client import get_llm
from app.llm.prompts import QUERY_ANALYSIS_PROMPT

from app.schemas.query import QueryAnalysis

from app.utils.logger import get_logger

logger = get_logger()


class QueryAnalysisNode:
    """
    Analyze the user query before retrieval.

    Responsibilities:
    - Rewrite the question
    - Classify query type
    """

    def __init__(self):
        self.llm = get_llm().with_structured_output(QueryAnalysis)

    def __call__(
        self,
        state: GraphState,
    ) -> GraphState:

        question = state["question"]

        logger.info("Running Query Analysis Node...")

        try:

            prompt = QUERY_ANALYSIS_PROMPT.invoke(
                {
                    "question": question
                }
            )

            response: QueryAnalysis = self.llm.invoke(prompt)

            logger.success(
                "Query analysis completed."
            )

            return {
                **state,
                "rewritten_query": response.rewritten_query,
                "query_type": response.query_type,
            }

        except Exception as e:

            logger.exception(
                "Query Analysis failed."
            )

            return {
                **state,
                "rewritten_query": question,
                "query_type": "general",
                "error": str(e),
            }


query_analysis_node = QueryAnalysisNode()