from pathlib import Path
import shutil
import tempfile

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
    status,
)

from app.schemas.api import (
    ErrorResponse,
    IngestionResponse,
    URLIngestionRequest,
)

from app.schemas.api import (
    ErrorResponse,
    IngestionResponse,
)

from app.services.document_service import document_service

from app.utils.logger import get_logger

logger = get_logger()

router = APIRouter(
    prefix="/ingest",
    tags=["Document Ingestion"],
)


@router.post(
    "",
    response_model=IngestionResponse,
    responses={
        500: {"model": ErrorResponse},
    },
    summary="Upload and index a document",
)
async def ingest_document(
    file: UploadFile = File(...),
):

    temp_dir = Path(tempfile.mkdtemp())

    temp_file = temp_dir / file.filename

    try:

        with temp_file.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = document_service.ingest_file(
            temp_file
        )

        return IngestionResponse(**result)

    except Exception as e:

        logger.exception(
            "Document ingestion failed."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    finally:

        try:
            temp_file.unlink(missing_ok=True)
            temp_dir.rmdir()
        except Exception:
            pass

@router.post(
    "/url",
    response_model=IngestionResponse,
    responses={
        500: {"model": ErrorResponse},
    },
    summary="Ingest documentation from URL",
)
async def ingest_url(
    request: URLIngestionRequest,
):

    try:

        logger.info(
            f"Ingesting URL: {request.url}"
        )

        result = document_service.ingest_url(
            request.url
        )

        return IngestionResponse(**result)

    except Exception as e:

        logger.exception(
            "URL ingestion failed."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )