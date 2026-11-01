from typing import Literal

from app.graph.state import GraphState

from app.utils.config import settings
from app.utils.constants import (
    GENERATION_NODE,
    QUERY_REWRITER_NODE,
)

from app.utils.logger import get_logger

logger = get_logger()


def route_after_document_grading(
    state: GraphState,
) -> Literal["generation", "query_rewriter", "no_answer"]:

    relevant_docs = state.get("relevant_documents", [])
    retries = state.get("retries", 0)

    if relevant_docs:
        logger.info(
            "Relevant documents found. Routing to Generation."
        )
        return GENERATION_NODE

    if retries < settings.MAX_RETRIES:
        logger.warning(
            f"No relevant documents found. Retry {retries + 1}/{settings.MAX_RETRIES}."
        )
        return QUERY_REWRITER_NODE

    logger.warning(
        "No relevant documents found after maximum retries."
    )

    return "no_answer"


def route_after_hallucination_check(
    state: GraphState,
) -> Literal["end"]:

    status = state.get(
        "hallucination_status",
        "",
    ).lower()

    logger.info(f"Hallucination status: {status}")

    return "end"