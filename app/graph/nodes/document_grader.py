from app.graph.state import GraphState

from app.llm.groq_client import get_llm
from app.llm.prompts import DOCUMENT_GRADING_PROMPT

from app.utils.constants import (
    RELEVANT,
    IRRELEVANT,
)
from app.utils.logger import get_logger

logger = get_logger()


class DocumentGraderNode:
    """
    Grades each retrieved document independently.

    Responsibilities:
    -----------------
    - Evaluate every retrieved chunk
    - Keep only relevant chunks
    - Remove irrelevant chunks
    """

    def __init__(self):
        self.llm = get_llm()

    def __call__(
        self,
        state: GraphState,
    ) -> GraphState:

        logger.info("Running Document Grader Node...")

        question = state["question"]

        retrieved_docs = state.get(
            "retrieved_documents",
            [],
        )

        relevant_docs = []

        try:

            for document in retrieved_docs:

                prompt = DOCUMENT_GRADING_PROMPT.invoke(
                    {
                        "question": question,
                        "document": document.page_content,
                    }
                )

                response = self.llm.invoke(prompt)

                grade = response.content.strip().lower()

                # In case the model gives reasoning before the answer,
                # take the last non-empty line.
                grade = [
                    line.strip().lower()
                    for line in grade.splitlines()
                    if line.strip()
                ][-1]

                logger.info(f"Document Grade: {grade}")

                if grade == RELEVANT:
                    relevant_docs.append(document)

            logger.success(
                f"{len(relevant_docs)}/{len(retrieved_docs)} documents are relevant."
            )

            return {
                **state,
                "relevant_documents": relevant_docs,
            }

        except Exception as e:

            logger.exception(
                "Document grading failed."
            )

            return {
                **state,
                "relevant_documents": [],
                "error": str(e),
            }


document_grader_node = DocumentGraderNode()