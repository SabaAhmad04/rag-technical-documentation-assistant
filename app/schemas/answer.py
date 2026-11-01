from typing import List

from pydantic import BaseModel, Field


class AnswerResponse(BaseModel):
    """
    Structured response produced by the generation node.
    """

    answer: str = Field(
        description="Final grounded answer."
    )

    sources: List[str] = Field(
        default_factory=list,
        description="Unique source documents."
    )