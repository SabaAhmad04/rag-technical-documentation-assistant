"""
Application-wide constants.

This file contains all configurable constants that are not expected
to change between environments.
"""

from pathlib import Path

# ==========================================================
# Project Directories
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR = BASE_DIR / "documents"
CHROMA_DB_DIR = BASE_DIR / "chroma_db"
LOGS_DIR = BASE_DIR / "logs"
DATABASE_DIR = BASE_DIR / "database"

# ==========================================================
# Supported File Types
# ==========================================================

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".md",
    ".txt",
    ".html",
    ".htm",
}

# ==========================================================
# Chunking Configuration
# ==========================================================

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# ==========================================================
# Retrieval
# ==========================================================

DEFAULT_TOP_K = 5
MAX_QUERY_REWRITE_ATTEMPTS = 2

# ==========================================================
# LangGraph Node Names
# ==========================================================

QUERY_ANALYSIS_NODE = "query_analysis"
RETRIEVAL_NODE = "retrieval"
DOCUMENT_GRADER_NODE = "document_grader"
QUERY_REWRITER_NODE = "query_rewriter"
GENERATION_NODE = "generation"
HALLUCINATION_CHECK_NODE = "hallucination_checker"

# ==========================================================
# Query Types
# ==========================================================

QUERY_TYPES = {
    "conceptual",
    "how-to",
    "troubleshooting",
    "api-reference",
    "general",
}

# ==========================================================
# Document Grades
# ==========================================================

RELEVANT = "relevant"
IRRELEVANT = "irrelevant"

# ==========================================================
# Hallucination Check
# ==========================================================

SUPPORTED = "supported"
UNSUPPORTED = "unsupported"

# ==========================================================
# Feedback
# ==========================================================

THUMBS_UP = "up"
THUMBS_DOWN = "down"

# ==========================================================
# API Messages
# ==========================================================

SUCCESS = "success"
FAILED = "failed"

NO_DOCUMENTS_FOUND = "No documents found."

NO_RELEVANT_DOCUMENTS = (
    "I couldn't find any relevant information in the uploaded documents "
    "to answer your question."
)

NO_ANSWER_FOUND = (
    "The uploaded documents do not contain enough information "
    "to answer this question."
)

INGESTION_SUCCESS = "Documents ingested successfully."
QUERY_SUCCESS = "Query executed successfully."

# ==========================================================
# Database
# ==========================================================

FEEDBACK_DB = DATABASE_DIR / "feedback.db"

# ==========================================================
# Default Collection
# ==========================================================

DEFAULT_COLLECTION = "technical_docs"

# ==========================================================
# Prompt Labels
# ==========================================================

QUERY_REWRITE_PROMPT = "query_rewrite"
DOCUMENT_GRADING_PROMPT = "document_grading"
ANSWER_GENERATION_PROMPT = "answer_generation"
HALLUCINATION_PROMPT = "hallucination_check"

# ==========================================================
# Streamlit
# ==========================================================

APP_TITLE = "📚 RAG Technical Documentation Assistant"
PAGE_ICON = "🤖"
LAYOUT = "wide"

# ==========================================================
# Allowed Web URLs
# ==========================================================

SUPPORTED_URL_PREFIXES = (
    "https://",
    "http://",
)