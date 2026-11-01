from app.graph.state import GraphState

from app.llm.groq_client import get_llm
from app.llm.prompts import (
    ANSWER_GENERATION_PROMPT,
    WEB_SEARCH_PROMPT,
)

from app.utils.logger import get_logger

logger = get_logger()


class GenerationNode:
    """
    Generate the final answer from either:
    1. Local retrieved documents
    2. Web search documents (fallback)
    """

    def __init__(self):
        self.llm = get_llm()

    def __call__(
        self,
        state: GraphState,
    ) -> GraphState:

        logger.info("Running Generation Node...")

        question = state["question"]

        # ---------------------------------------
        # Prefer local documents
        # ---------------------------------------

        if state.get("use_web_search", False):
            documents = state.get("web_documents", [])
        else:
            documents = state.get("relevant_documents", [])

        using_web = False

        if not documents:
            documents = state.get("web_documents", [])
            using_web = True

        try:

            context = "\n\n".join(
                doc.page_content
                for doc in documents
            )

            # ---------------------------------------
            # Select prompt
            # ---------------------------------------

            if using_web:

                prompt = WEB_SEARCH_PROMPT.invoke(
                    {
                        "question": question,
                        "context": context,
                    }
                )

            else:

                prompt = ANSWER_GENERATION_PROMPT.invoke(
                    {
                        "question": question,
                        "context": context,
                    }
                )

            response = self.llm.invoke(prompt)

            answer = response.content.strip()

            sources = sorted(
                {
                    doc.metadata.get("source", "Unknown")
                    for doc in documents
                }
            )

            logger.success(
                f"Answer generated successfully. "
                f"Using {'web' if using_web else 'local'} documents."
            )

            return {
                **state,
                "answer": answer,
                "sources": sources,
            }

        except Exception as e:

            logger.exception(
                "Generation failed."
            )

            return {
                **state,
                "answer": "",
                "sources": [],
                "error": str(e),
            }


generation_node = GenerationNode()