from pydantic import BaseModel, Field


class DocumentGrade(BaseModel):
    """
    Structured output for document grading.
    """

    grade: str = Field(
        description="Either 'relevant' or 'irrelevant'."
    )