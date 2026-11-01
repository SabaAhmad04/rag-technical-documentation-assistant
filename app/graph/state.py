from typing import List, TypedDict

from langchain_core.documents import Document


class GraphState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    """

    # ==========================================================
    # User Input
    # ==========================================================

    question: str
    rewritten_query: str
    query_type: str

    # ==========================================================
    # Retrieval
    # ==========================================================

    retrieved_documents: List[Document]

    relevant_documents: List[Document]

    # ==========================================================
    # Generation
    # ==========================================================

    answer: str

    hallucination_status: str
    hallucination_confidence: int
    hallucination_reason: str

    # ==========================================================
    # Routing
    # ==========================================================

    retries: int
    max_retries: int

    # ==========================================================
    # Metadata
    # ==========================================================

    sources: List[str]

    feedback: str
    error: str