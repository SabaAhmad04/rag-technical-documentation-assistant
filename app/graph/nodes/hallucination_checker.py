from app.graph.state import GraphState

from app.llm.groq_client import get_llm
from app.llm.prompts import HALLUCINATION_CHECK_PROMPT

from app.schemas.hallucination import HallucinationResult

from app.utils.logger import get_logger

logger = get_logger()


class HallucinationCheckerNode:
    """
    Verifies whether the generated answer is
    grounded in the retrieved context.
    """

    def __init__(self):
        self.llm = get_llm().with_structured_output(
            HallucinationResult
        )

    def __call__(
        self,
        state: GraphState,
    ) -> GraphState:

        logger.info(
            "Running Hallucination Checker..."
        )

        documents = state.get(
            "relevant_documents",
            []
        )

        answer = state.get(
            "answer",
            ""
        )

        try:

            context = "\n\n".join(
                doc.page_content
                for doc in documents
            )

            prompt = HALLUCINATION_CHECK_PROMPT.invoke(
                {
                    "context": context,
                    "answer": answer,
                }
            )

            result: HallucinationResult = self.llm.invoke(
                prompt
            )

            logger.success(
                f"Hallucination Check: {result.verdict} "
                f"({result.confidence}%)"
            )

            return {
                **state,
                "hallucination_status": result.verdict.lower(),
                "hallucination_confidence": result.confidence,
                "hallucination_reason": result.explanation,
            }

        except Exception as e:

            logger.exception(
                "Hallucination check failed."
            )

            return {
                **state,
                "hallucination_status": "unsupported",
                "hallucination_confidence": 0,
                "hallucination_reason": str(e),
                "error": str(e),
            }


hallucination_checker_node = HallucinationCheckerNode()