from datetime import datetime
from typing import List, Literal

from pydantic import BaseModel, Field


# ==========================================================
# Query API
# ==========================================================

class QueryRequest(BaseModel):
    """
    Request body for /query endpoint.
    """

    question: str = Field(
        ...,
        min_length=1,
        description="User question."
    )


class HallucinationResponse(BaseModel):
    """
    Hallucination verification result.
    """

    status: str
    confidence: int
    reason: str


class QueryResponse(BaseModel):
    """
    Response returned by /query.
    """

    success: bool
    question: str
    rewritten_query: str
    query_type: str
    answer: str
    sources: List[str]
    hallucination: HallucinationResponse
    retries: int


# ==========================================================
# Error Response
# ==========================================================

class ErrorResponse(BaseModel):

    success: bool = False
    error: str


# ==========================================================
# Ingestion
# ==========================================================

class IngestionResponse(BaseModel):

    success: bool
    documents_loaded: int
    chunks_created: int
    message: str


class URLIngestionRequest(BaseModel):
    """
    Request body for URL ingestion.
    """

    url: str = Field(
        ...,
        description="Website URL to ingest."
    )


# ==========================================================
# Documents
# ==========================================================

class DocumentsResponse(BaseModel):

    documents: List[str]


# ==========================================================
# Feedback
# ==========================================================

class FeedbackRequest(BaseModel):
    """
    User feedback for a generated answer.
    """

    question: str
    answer: str
    feedback: Literal["up", "down"]


class FeedbackResponse(BaseModel):

    success: bool
    message: str


class FeedbackRecord(BaseModel):

    question: str
    answer: str
    feedback: Literal["up", "down"]
    timestamp: datetime