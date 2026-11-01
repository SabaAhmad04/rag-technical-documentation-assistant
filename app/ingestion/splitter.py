from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.utils.constants import CHUNK_OVERLAP, CHUNK_SIZE
from app.utils.logger import get_logger

logger = get_logger()


class DocumentSplitter:
    """
    Splits documents into smaller chunks while preserving metadata.
    """

    def __init__(
        self,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                "? ",
                "! ",
                "; ",
                ", ",
                " ",
                "",
            ],
            keep_separator=True,
            add_start_index=True,
        )

    def split_documents(
        self,
        documents: List[Document],
    ) -> List[Document]:
        """
        Split documents into chunks while preserving metadata.

        Args:
            documents: List of LangChain Document objects.

        Returns:
            List of chunked Document objects.
        """

        logger.info(f"Splitting {len(documents)} document(s)...")

        chunks = self.text_splitter.split_documents(documents)

        for idx, chunk in enumerate(chunks):

            # Preserve metadata
            chunk.metadata = dict(chunk.metadata)

            # Unique chunk id
            chunk.metadata["chunk_id"] = idx

            # Helpful statistics
            chunk.metadata["chunk_size"] = len(chunk.page_content)

        logger.success(
            f"Generated {len(chunks)} chunks."
        )

        return chunks

    def split_single_document(
        self,
        document: Document,
    ) -> List[Document]:
        """
        Split a single document.
        """

        return self.split_documents([document])