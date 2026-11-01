import streamlit as st

# ==========================================================
# Statistics
# ==========================================================

def render_statistics(stats: dict):

    col1, col2, col3, col4 = st.columns(
        4,
        gap="medium",
    )

    with col1:
        st.metric(
            "📄 Documents",
            stats.get("documents", 0),
        )

    with col2:
        st.metric(
            "🧩 Chunks",
            stats.get("chunks", 0),
        )

    with col3:

        embedding = stats.get(
            "embedding_model",
            "-",
        )

        if "/" in embedding:
            embedding = embedding.split("/")[-1]

        st.metric(
            "🧠 Embedding",
            embedding,
        )

    with col4:
        st.metric(
            "🗄️ Vector Store",
            stats.get("vector_store", "-"),
        )


# ==========================================================
# Chat Messages
# ==========================================================

def render_chat_message(
    role: str,
    content: str,
):

    avatar = "👤" if role == "user" else "🤖"

    with st.chat_message(
        role,
        avatar=avatar,
    ):
        st.markdown(content)


# ==========================================================
# Retrieved Sources
# ==========================================================

def render_sources(
    sources,
):

    if not sources:
        return

    with st.expander(
        "📚 Sources Used",
        expanded=False,
    ):

        for index, source in enumerate(
            sources,
            start=1,
        ):
            st.markdown(
                f"**{index}.** 📄 {source}"
            )


# ==========================================================
# Indexed Documents
# ==========================================================

def render_document_list(
    documents,
    delete_callback=None,
):

    if not documents:

        st.info("No indexed documents.")

        return

    for doc in documents:

        col1, col2 = st.columns(
            [5, 1]
        )

        with col1:
            st.caption(f"📄 {doc}")

        with col2:

            if st.button(
                "❌",
                key=f"delete_{doc}",
                help="Delete document",
            ):

                if delete_callback:

                    try:

                        delete_callback(doc)

                        st.toast(
                            f"{doc} deleted successfully."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(str(e))


# ==========================================================
# Confidence Indicator
# ==========================================================

def render_confidence(
    score: float | None,
):

    if score is None:
        return

    score = max(
        0.0,
        min(score, 1.0),
    )

    st.progress(score)

    st.caption(
        f"Confidence: {score * 100:.1f}%"
    )