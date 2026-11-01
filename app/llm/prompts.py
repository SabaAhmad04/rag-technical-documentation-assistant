from langchain_core.prompts import ChatPromptTemplate

# ==========================================================
# Query Analysis
# ==========================================================

QUERY_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert AI assistant that analyzes user questions before retrieval.

Your tasks:
1. Rewrite the user's question to improve retrieval.
2. Expand abbreviations if necessary.
3. Remove unnecessary words.
4. Preserve the original meaning.
5. Classify the question into ONE category:

- conceptual
- how-to
- troubleshooting
- api-reference
- general

Return the rewritten query and query type.
            """,
        ),
        ("human", "{question}"),
    ]
)

# ==========================================================
# Query Rewriter
# ==========================================================

QUERY_REWRITE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
The previous retrieval failed.

Rewrite the question so that a vector database has a better chance
of finding relevant documentation.

Guidelines:
- Keep the intent unchanged.
- Add important technical keywords.
- Remove ambiguity.
- Return ONLY the rewritten query.
            """,
        ),
        (
            "human",
            """
Original Question:

{question}
            """,
        ),
    ]
)

# ==========================================================
# Document Grading
# ==========================================================
DOCUMENT_GRADING_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a document relevance evaluator.

Determine whether the retrieved document contains information that helps answer the user's question.

Reply with ONLY one word:

relevant

or

irrelevant

Do not explain your answer.
            """,
        ),
        (
            "human",
            """
Question:
{question}

Retrieved Document:
{document}
            """,
        ),
    ]
)

# ==========================================================
# Answer Generation
# ==========================================================

ANSWER_GENERATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a Technical Documentation Assistant.

Answer ONLY using the retrieved context.

Rules:

- Do not make up information.
- If the answer is unavailable, say:

"I couldn't find this information in the indexed documentation."

- Be concise.
- Use markdown.
- Mention important API names exactly as written.
- At the end include:

Sources:
- source 1
- source 2
            """,
        ),
        (
            "human",
            """
Question:

{question}

Context:

{context}
            """,
        ),
    ]
)

# ==========================================================
# Hallucination Checker
# ==========================================================

HALLUCINATION_CHECK_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a factual verification assistant.

Compare the generated answer with the provided context.

Determine whether every factual statement in the answer
is supported by the context.

Return your response using the required structured output.

Rules:

- supported → Every important claim is grounded in the context.

- unsupported → The answer contains unsupported,
hallucinated, or missing information.

Confidence should be between 0 and 100.

Provide a one-sentence explanation.
            """,
        ),
        (
            "human",
            """
Context:

{context}

Generated Answer:

{answer}
            """,
        ),
    ]
)

# ==========================================================
# Web Search Answer Generation
# ==========================================================

WEB_SEARCH_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an AI assistant.

The local documentation did not contain enough information.

Answer ONLY from the provided web search results.

Never use your own knowledge.

Always include Sources.
            """,
        ),
        (
            "human",
            """
Question:

{question}

Web Search Results:

{context}
            """,
        ),
    ]
)