from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.ingestion.vector_store import get_vector_store
from app.llm.groq_client import get_llm
from app.utils.config import settings
from app.utils.logger import get_logger

logger = get_logger()


# ==========================================================
# Application Lifespan
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting Self-Corrective RAG API...")

    try:
        # Initialize ChromaDB
        get_vector_store()

        # Initialize Groq Client
        get_llm()

        logger.success("Application initialized successfully.")

    except Exception as e:
        logger.exception(f"Startup failed: {e}")

    yield

    logger.info("Shutting down application...")


# ==========================================================
# FastAPI App
# ==========================================================

app = FastAPI(
    title="Self-Corrective RAG API",
    description="""
A production-ready Self-Corrective Retrieval-Augmented
Generation (RAG) system built using:

- LangGraph
- Groq LLM
- ChromaDB
- HuggingFace Embeddings
- FastAPI
- Streamlit
""",
    version="1.0.0",
    lifespan=lifespan,
)


# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# API Routes
# ==========================================================

app.include_router(api_router)


# ==========================================================
# Health Check
# ==========================================================

@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "Self-Corrective RAG API",
        "status": "running",
        "version": app.version,
    }


@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy",
        "embedding_model": settings.EMBEDDING_MODEL,
        "collection": settings.COLLECTION_NAME,
        "llm": settings.GROQ_MODEL,
    }