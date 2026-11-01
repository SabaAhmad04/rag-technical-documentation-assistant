import streamlit as st

from api import (
    ask_question,
    delete_document,
    get_documents,
    get_stats,
    health_check,
    reset_database,
    upload_document,
)

from components import (
    render_chat_message,
    render_document_list,
    render_sources,
    render_statistics,
)

from styles import load_css


# ==========================================================
# Page Config
# ==========================================================

st.set_page_config(
    page_title="Self-Corrective RAG Assistant",
    page_icon="📚",
    layout="wide",
)

st.markdown(load_css(), unsafe_allow_html=True)


# ==========================================================
# Session State
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.title("📚 RAG Assistant")
    st.caption("Upload technical documents and ask questions.")

    st.divider()

    # ------------------------------------------------------
    # Backend Status
    # ------------------------------------------------------

    st.subheader("Backend Status")

    try:
        health = health_check()

        st.success("Backend Running")

        st.write(f"**LLM:** {health['llm']}")
        st.write(f"**Embedding:** {health['embedding_model']}")

    except Exception:
        st.error("Backend Offline")

    st.divider()

    # ------------------------------------------------------
    # Upload
    # ------------------------------------------------------

    st.subheader("Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose PDF",
        type=["pdf"],
    )

    if uploaded_file:

        if st.button(
            "Upload Document",
            use_container_width=True,
        ):

            with st.spinner("Uploading..."):

                try:

                    result = upload_document(uploaded_file)

                    st.success(result["message"])

                    st.rerun()

                except Exception as e:

                    st.error(str(e))

    st.divider()

    # ------------------------------------------------------
    # Indexed Documents
    # ------------------------------------------------------

    st.subheader("Indexed Documents")

    try:

        docs = get_documents()

        render_document_list(
            docs["documents"],
            delete_callback=delete_document,
        )

    except Exception:

        st.warning("Unable to load documents.")

    st.divider()

    # ------------------------------------------------------
    # Reset DB
    # ------------------------------------------------------

    if st.button(
        "🗑️ Clear Vector Database",
        use_container_width=True,
    ):

        try:

            reset_database()

            st.success("Database cleared.")

            st.rerun()

        except Exception as e:

            st.error(str(e))


# ==========================================================
# Main Page
# ==========================================================

st.title("🤖 Self-Corrective RAG Assistant")

st.caption(
    "Ask questions from your uploaded technical documentation using a Self-Corrective RAG pipeline."
)


# ==========================================================
# Statistics
# ==========================================================

try:

    stats = get_stats()

    render_statistics(stats)

except Exception:
    pass

st.divider()


# ==========================================================
# Chat History
# ==========================================================

for message in st.session_state.messages:

    render_chat_message(
        message["role"],
        message["content"],
    )


# ==========================================================
# Chat Input
# ==========================================================

question = st.chat_input(
    "Ask a question..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    render_chat_message(
        "user",
        question,
    )

    with st.spinner("Searching documents..."):

        try:

            response = ask_question(question)

            answer = response.get(
                "answer",
                "No response generated.",
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

            render_chat_message(
                "assistant",
                answer,
            )

            if response.get("sources"):

                render_sources(
                    response["sources"]
                )

        except Exception as e:

            st.error(str(e))