from functools import lru_cache
from typing import List

from langchain_core.documents import Document
from langchain_chroma import Chroma

from app.ingestion.embedder import get_embeddings
from app.utils.config import settings
from app.utils.logger import get_logger

logger = get_logger()


class VectorStore:
    """
    Wrapper around ChromaDB.

    Handles:
    - Create/Open Collection
    - Add Documents
    - Similarity Search
    - Delete Documents
    - Reset Collection
    """

    def __init__(self):
        logger.info("Initializing ChromaDB...")

        self.embeddings = get_embeddings()

        self.vectorstore = Chroma(
            collection_name=settings.COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=settings.CHROMA_DB_PATH,
        )

        logger.success("ChromaDB initialized successfully.")

    # ----------------------------------------------------
    # Add Documents
    # ----------------------------------------------------

    def add_documents(
        self,
        documents: List[Document],
    ) -> None:

        if not documents:
            logger.warning("No documents to add.")
            return

        logger.info(
            f"Adding {len(documents)} chunks to ChromaDB..."
        )

        self.vectorstore.add_documents(documents)

        logger.success("Documents indexed successfully.")

    # ----------------------------------------------------
    # Similarity Search
    # ----------------------------------------------------

    def similarity_search(
        self,
        query: str,
        k: int | None = None,
    ) -> List[Document]:

        if k is None:
            k = settings.TOP_K

        logger.info(f"Searching top-{k} chunks...")

        docs = self.vectorstore.similarity_search(
            query=query,
            k=k,
        )

        logger.success(f"Retrieved {len(docs)} chunks.")

        return docs

    # ----------------------------------------------------
    # Similarity Search With Score
    # ----------------------------------------------------

    def similarity_search_with_score(
        self,
        query: str,
        k: int | None = None,
    ):

        if k is None:
            k = settings.TOP_K

        return self.vectorstore.similarity_search_with_score(
            query=query,
            k=k,
        )

    # ----------------------------------------------------
    # List Sources
    # ----------------------------------------------------

    def list_documents(self) -> list[str]:
        """
        Returns unique document names stored
        inside the vector database.
        """

        collection = self.vectorstore.get()

        metadata = collection.get("metadatas", [])

        sources = set()

        for meta in metadata:

            source = meta.get("source")

            if source:
                sources.add(source)

        return sorted(list(sources))

    # ----------------------------------------------------
    # Delete by Source
    # ----------------------------------------------------

    def delete_document(
        self,
        source_name: str,
    ) -> None:

        collection = self.vectorstore.get()

        ids_to_delete = []

        ids = collection["ids"]
        metadatas = collection["metadatas"]

        for idx, metadata in zip(ids, metadatas):

            if metadata.get("source") == source_name:
                ids_to_delete.append(idx)

        if ids_to_delete:

            self.vectorstore.delete(ids=ids_to_delete)

            logger.success(
                f"Deleted '{source_name}' from ChromaDB."
            )

        else:

            logger.warning(
                f"No document named '{source_name}' found."
            )

    # ----------------------------------------------------
    # Reset Collection
    # ----------------------------------------------------

    def reset(self):

        collection = self.vectorstore.get()

        ids = collection["ids"]

        if ids:

            self.vectorstore.delete(ids=ids)

            logger.success("Vector database cleared.")

        else:

            logger.info("Vector database already empty.")

    # ----------------------------------------------------
    # Count Documents
    # ----------------------------------------------------

    def count(self) -> int:

        collection = self.vectorstore.get()

        return len(collection["ids"])

    # ----------------------------------------------------
    # Retriever
    # ----------------------------------------------------

    def as_retriever(self):

        return self.vectorstore.as_retriever(
            search_kwargs={
                "k": settings.TOP_K
            }
        )


@lru_cache
def get_vector_store() -> VectorStore:
    """
    Returns a singleton VectorStore instance.
    """
    return VectorStore()