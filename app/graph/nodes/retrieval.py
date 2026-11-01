from app.graph.state import GraphState

from app.ingestion.vector_store import get_vector_store

from app.utils.config import settings
from app.utils.logger import get_logger

logger = get_logger()


class RetrievalNode:
    """
    Retrieve relevant document chunks from ChromaDB.

    Responsibilities:
    -----------------
    - Perform similarity search
    - Return Top-K chunks
    - Preserve similarity scores
    """

    def __init__(self):
        self.vector_store = get_vector_store()

    def __call__(self, state: GraphState) -> GraphState:

        logger.info("Running Retrieval Node...")

        query = state.get("rewritten_query") or state["question"]

        try:

            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=settings.TOP_K,
            )

            retrieved_docs = []

            for document, score in results:

                metadata = dict(document.metadata)

                metadata["similarity_score"] = float(score)

                document.metadata = metadata

                retrieved_docs.append(document)

            logger.success(
                f"Retrieved {len(retrieved_docs)} document(s)."
            )

            return {
                **state,
                "retrieved_documents": retrieved_docs,
            }

        except Exception as e:

            logger.exception("Retrieval failed.")

            return {
                **state,
                "retrieved_documents": [],
                "error": str(e),
            }


retrieval_node = RetrievalNode()