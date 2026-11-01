from pydantic import BaseModel, Field


class QueryAnalysis(BaseModel):
    """
    Structured output for query analysis.
    """

    rewritten_query: str = Field(
        description="Improved query for retrieval."
    )

    query_type: str = Field(
        description="conceptual | how-to | troubleshooting | api-reference | general"
    )