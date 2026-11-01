from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from app.schemas.api import (
    ErrorResponse,
    FeedbackRecord,
    FeedbackRequest,
    FeedbackResponse,
)

from app.services.feedback_service import feedback_service

from app.utils.logger import get_logger

logger = get_logger()

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
)


@router.post(
    "",
    response_model=FeedbackResponse,
    responses={
        500: {
            "model": ErrorResponse
        }
    },
    summary="Submit answer feedback",
)
async def submit_feedback(
    request: FeedbackRequest,
):

    try:

        record = FeedbackRecord(
            question=request.question,
            answer=request.answer,
            feedback=request.feedback,
            timestamp=datetime.utcnow(),
        )

        result = feedback_service.save_feedback(
            record
        )

        return FeedbackResponse(
            **result
        )

    except Exception as e:

        logger.exception(
            "Feedback submission failed."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get(
    "",
    summary="View feedback",
)
async def view_feedback():

    try:

        return feedback_service.get_feedback()

    except Exception as e:

        logger.exception(
            "Failed to load feedback."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )