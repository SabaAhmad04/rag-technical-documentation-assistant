from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup

from langchain_core.documents import Document

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
    BSHTMLLoader,
)

from app.utils.logger import get_logger
from app.utils.constants import SUPPORTED_EXTENSIONS

logger = get_logger()


class DocumentLoader:
    """
    Handles loading documents from:
    - PDF
    - Markdown
    - TXT
    - HTML
    - URLs
    """

    def __init__(self):
        pass

    def load_file(self, file_path: str | Path) -> List[Document]:
        """
        Load a local file.

        Args:
            file_path: Path to document

        Returns:
            List[Document]
        """

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(file_path)

        suffix = file_path.suffix.lower()

        if suffix not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {suffix}"
            )

        logger.info(f"Loading {file_path.name}")

        if suffix == ".pdf":
            loader = PyPDFLoader(str(file_path))

        elif suffix == ".md":
            loader = UnstructuredMarkdownLoader(str(file_path))

        elif suffix == ".txt":
            loader = TextLoader(
                str(file_path),
                encoding="utf-8",
            )

        elif suffix in [".html", ".htm"]:
            loader = BSHTMLLoader(str(file_path))

        else:
            raise ValueError(f"Unsupported file: {suffix}")

        documents = loader.load()

        for doc in documents:
            doc.metadata["source"] = file_path.name
            doc.metadata["path"] = str(file_path.resolve())

        logger.success(
            f"Loaded {len(documents)} document(s)"
        )

        return documents

    def load_directory(
        self,
        directory: str | Path,
    ) -> List[Document]:
        """
        Load every supported document
        from a directory.
        """

        directory = Path(directory)

        if not directory.exists():
            raise FileNotFoundError(directory)

        documents = []

        for file in directory.rglob("*"):

            if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            documents.extend(
                self.load_file(file)
            )

        logger.success(
            f"Loaded {len(documents)} total documents"
        )

        return documents

    def load_url(
        self,
        url: str,
    ) -> List[Document]:
        """
        Load webpage content from URL.
        """

        logger.info(f"Fetching {url}")

        response = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        text = soup.get_text(
            separator="\n",
            strip=True,
        )

        document = Document(
            page_content=text,
            metadata={
                "source": url,
                "url": url,
            },
        )

        logger.success("URL loaded successfully.")

        return [document]