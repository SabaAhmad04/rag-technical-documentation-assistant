from pathlib import Path

from langchain_core.documents import Document

from app.ingestion.loader import DocumentLoader
from app.ingestion.splitter import DocumentSplitter
from app.ingestion.vector_store import get_vector_store

from app.utils.logger import get_logger

logger = get_logger()


class DocumentService:
    """
    Service responsible for document ingestion and
    vector database operations.
    """

    def __init__(self):
        self.loader = DocumentLoader()
        self.splitter = DocumentSplitter()
        self.vector_store = get_vector_store()

    # ----------------------------------------------------
    # Ingest File
    # ----------------------------------------------------

    def ingest_file(self, file_path: str | Path) -> dict:

        logger.info(f"Ingesting {file_path}")

        documents = self.loader.load_file(file_path)

        chunks = self.splitter.split_documents(documents)

        self.vector_store.add_documents(chunks)

        logger.success(
            f"{len(documents)} document(s) indexed."
        )

        return {
            "success": True,
            "documents_loaded": len(documents),
            "chunks_created": len(chunks),
            "message": "Document indexed successfully.",
        }

    # ----------------------------------------------------
    # Ingest Directory
    # ----------------------------------------------------

    def ingest_directory(
        self,
        directory: str | Path,
    ) -> dict:

        documents = self.loader.load_directory(directory)

        chunks = self.splitter.split_documents(documents)

        self.vector_store.add_documents(chunks)

        return {
            "success": True,
            "documents_loaded": len(documents),
            "chunks_created": len(chunks),
            "message": "Directory indexed successfully.",
        }

    # ----------------------------------------------------
    # Ingest URL
    # ----------------------------------------------------

    def ingest_url(
        self,
        url: str,
    ) -> dict:

        documents = self.loader.load_url(url)

        chunks = self.splitter.split_documents(documents)

        self.vector_store.add_documents(chunks)

        return {
            "success": True,
            "documents_loaded": len(documents),
            "chunks_created": len(chunks),
            "message": "URL indexed successfully.",
        }

    # ----------------------------------------------------
    # List Documents
    # ----------------------------------------------------

    def list_documents(self):

        return self.vector_store.list_documents()

    # ----------------------------------------------------
    # Delete Document
    # ----------------------------------------------------

    def delete_document(
        self,
        source: str,
    ):

        self.vector_store.delete_document(source)

        return {
            "success": True,
            "message": f"{source} deleted successfully.",
        }

    # ----------------------------------------------------
    # Reset Database
    # ----------------------------------------------------

    def reset_database(self):

        self.vector_store.reset()

        return {
            "success": True,
            "message": "Vector database cleared.",
        }


document_service = DocumentService()