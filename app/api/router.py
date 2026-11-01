from fastapi import APIRouter

from app.api.routes.query import router as query_router
from app.api.routes.ingest import router as ingest_router
from app.api.routes.documents import router as documents_router
from app.api.routes.feedback import router as feedback_router

api_router = APIRouter()

api_router.include_router(query_router)
api_router.include_router(ingest_router)
api_router.include_router(documents_router)
api_router.include_router(feedback_router)