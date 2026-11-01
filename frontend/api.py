"""
API client for communicating with the FastAPI backend.
"""

from pathlib import Path

import requests

# ==========================================================
# Backend Configuration
# ==========================================================

BACKEND_URL = "http://127.0.0.1:8000"

TIMEOUT = 120


# ==========================================================
# Health Check
# ==========================================================

def health_check():
    """Check backend status."""

    response = requests.get(
        f"{BACKEND_URL}/health",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Upload Document
# ==========================================================

def upload_document(file):

    files = {
        "file": (
            file.name,
            file,
            "application/pdf",
        )
    }

    response = requests.post(
        f"{BACKEND_URL}/documents/upload",
        files=files,
        timeout=TIMEOUT,
    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Ask Question
# ==========================================================

def ask_question(question: str):

    payload = {
        "question": question,
    }

    response = requests.post(
        f"{BACKEND_URL}/query",
        json=payload,
        timeout=TIMEOUT,
    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# List Documents
# ==========================================================

def get_documents():

    response = requests.get(
        f"{BACKEND_URL}/documents",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Delete Document
# ==========================================================

def delete_document(document_name: str):

    response = requests.delete(
        f"{BACKEND_URL}/documents/{document_name}",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Reset Database
# ==========================================================

def reset_database():

    response = requests.delete(
        f"{BACKEND_URL}/documents",
        timeout=60,
    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Database Statistics
# ==========================================================

def get_stats():

    response = requests.get(
        f"{BACKEND_URL}/documents/stats",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()