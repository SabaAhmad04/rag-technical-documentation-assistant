from langgraph.graph import StateGraph, START, END

from app.graph.state import GraphState

# -----------------------------
# Nodes
# -----------------------------

from app.graph.nodes.query_analysis import query_analysis_node
from app.graph.nodes.retrieval import retrieval_node
from app.graph.nodes.document_grader import document_grader_node
from app.graph.nodes.query_rewriter import query_rewriter_node
from app.graph.nodes.generation import generation_node
from app.graph.nodes.hallucination_checker import (
    hallucination_checker_node,
)
from app.graph.nodes.no_answer import (
    no_answer_node,
)

# -----------------------------
# Conditional Edges
# -----------------------------

from app.graph.conditional_edges import (
    route_after_document_grading,
    route_after_hallucination_check,
)


class RAGGraph:

    def __init__(self):

        self.builder = StateGraph(GraphState)

        self._add_nodes()

        self._add_edges()

        self.graph = self.builder.compile()

    # -------------------------------------------------

    def _add_nodes(self):

        self.builder.add_node(
            "query_analysis",
            query_analysis_node,
        )

        self.builder.add_node(
            "retrieval",
            retrieval_node,
        )

        self.builder.add_node(
            "document_grader",
            document_grader_node,
        )

        self.builder.add_node(
            "query_rewriter",
            query_rewriter_node,
        )

        self.builder.add_node(
            "generation",
            generation_node,
        )

        self.builder.add_node(
            "hallucination_checker",
            hallucination_checker_node,
        )

        self.builder.add_node(
            "no_answer",
            no_answer_node,
        )

    # -------------------------------------------------

    def _add_edges(self):

        # START

        self.builder.add_edge(
            START,
            "query_analysis",
        )

        self.builder.add_edge(
            "query_analysis",
            "retrieval",
        )

        self.builder.add_edge(
            "retrieval",
            "document_grader",
        )

        # --------------------------------------
        # Document Grader Routing
        # --------------------------------------

        self.builder.add_conditional_edges(
            "document_grader",
            route_after_document_grading,
            {
                "generation": "generation",
                "query_rewriter": "query_rewriter",
                "no_answer": "no_answer",
            },
        )

        # --------------------------------------
        # Retry Loop
        # --------------------------------------

        self.builder.add_edge(
            "query_rewriter",
            "retrieval",
        )

        # --------------------------------------
        # Generation
        # --------------------------------------

        self.builder.add_edge(
            "generation",
            "hallucination_checker",
        )

        # --------------------------------------
        # Hallucination Routing
        # --------------------------------------

        self.builder.add_conditional_edges(
            "hallucination_checker",
            route_after_hallucination_check,
            {
                "end": END,
            },
        )

        # --------------------------------------
        # No Answer
        # --------------------------------------

        self.builder.add_edge(
            "no_answer",
            END,
        )

    # -------------------------------------------------

    def get_graph(self):
        return self.graph


rag_graph = RAGGraph().get_graph()