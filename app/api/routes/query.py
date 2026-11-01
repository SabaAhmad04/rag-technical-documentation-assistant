from fastapi import APIRouter, HTTPException, status

from app.schemas.api import (
    ErrorResponse,
    QueryRequest,
    QueryResponse,
)

from app.services.rag_service import rag_service

from app.utils.logger import get_logger

logger = get_logger()

router = APIRouter(
    prefix="/query",
    tags=["Query"],
)


@router.post(
    "",
    response_model=QueryResponse,
    responses={
        500: {"model": ErrorResponse},
    },
    summary="Query the RAG system",
    description="Ask a question to the Self-Corrective RAG Assistant.",
)
async def query_documents(
    request: QueryRequest,
):
    """
    Query the RAG workflow.
    """

    try:

        logger.info(
            f"Received query: {request.question}"
        )

        result = rag_service.query(
            request.question
        )

        if not result["success"]:

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"],
            )

        return QueryResponse(**result)

    except HTTPException:

        raise

    except Exception as e:

        logger.exception(
            "Unexpected error while processing query."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )