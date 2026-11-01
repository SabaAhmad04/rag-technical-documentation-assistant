from fastapi import APIRouter, HTTPException, status

from app.schemas.api import (
    DocumentsResponse,
    ErrorResponse,
)

from app.services.document_service import document_service

from app.ingestion.vector_store import get_vector_store

from app.utils.config import settings
from app.utils.logger import get_logger

from fastapi import UploadFile, File
from pathlib import Path
import shutil
import tempfile

logger = get_logger()

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    summary="Upload and index a PDF document",
)
async def upload_document(
    file: UploadFile = File(...),
):
    try:

        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported.",
            )

        # Create temporary file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf",
        ) as temp_file:

            shutil.copyfileobj(file.file, temp_file)

            temp_path = Path(temp_file.name)

        # Index document
        result = document_service.ingest_file(temp_path)

        # Delete temporary file
        temp_path.unlink(missing_ok=True)

        return result

    except Exception as e:

        logger.exception("Document upload failed.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

# ==========================================================
# List Indexed Documents
# ==========================================================

@router.get(
    "",
    response_model=DocumentsResponse,
    responses={
        500: {"model": ErrorResponse},
    },
    summary="List indexed documents",
)
async def list_documents():

    try:

        documents = document_service.list_documents()

        return DocumentsResponse(
            documents=documents
        )

    except Exception as e:

        logger.exception(
            "Failed to list documents."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# ==========================================================
# Delete Single Document
# ==========================================================

@router.delete(
    "/{document_name}",
    summary="Delete indexed document",
)
async def delete_document(
    document_name: str,
):

    try:

        return document_service.delete_document(
            document_name
        )

    except Exception as e:

        logger.exception(
            "Failed to delete document."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# ==========================================================
# Reset Vector Database
# ==========================================================

@router.delete(
    "",
    summary="Clear entire vector database",
)
async def reset_database():

    try:

        return document_service.reset_database()

    except Exception as e:

        logger.exception(
            "Failed to clear database."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# ==========================================================
# Database Statistics
# ==========================================================

@router.get(
    "/stats",
    summary="Vector database statistics",
)
async def database_stats():

    try:

        vector_store = get_vector_store()

        documents = vector_store.list_documents()

        total_chunks = vector_store.count()

        return {
            "documents": len(documents),
            "chunks": total_chunks,
            "embedding_model": settings.EMBEDDING_MODEL,
            "vector_store": "ChromaDB",
            "collection": settings.COLLECTION_NAME,
        }

    except Exception as e:

        logger.exception(
            "Failed to fetch statistics."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )