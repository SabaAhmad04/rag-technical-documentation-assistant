from pydantic import BaseModel, Field


class HallucinationResult(BaseModel):
    """
    Structured output for hallucination verification.
    """

    verdict: str = Field(
        description="supported or unsupported"
    )

    confidence: int = Field(
        ge=0,
        le=100,
        description="Confidence score between 0 and 100."
    )

    explanation: str = Field(
        description="Short explanation of the verdict."
    )