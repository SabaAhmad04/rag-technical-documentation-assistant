# 📚 Self-Corrective RAG Technical Documentation Assistant

A production-style **Self-Corrective Retrieval-Augmented Generation (RAG)** system built using **LangGraph, LangChain, Groq, ChromaDB, FastAPI, and Streamlit**.

The application allows users to upload technical PDF documents, indexes them into a vector database, and answers natural language questions using a self-corrective retrieval workflow. If the initial retrieval fails, the system rewrites the query, retrieves again, grades retrieved documents, detects hallucinations, and generates a grounded response with document citations.

---

# ✨ Features

- 📄 Upload and index PDF documents
- 🔍 Semantic retrieval using vector embeddings
- 🧠 Self-Corrective RAG workflow with LangGraph
- 🔄 Automatic query rewriting when retrieval fails
- ✅ LLM-based document relevance grading
- 🤖 Context-aware answer generation
- 🛡️ Hallucination detection
- 📚 Source attribution
- 📊 Interactive Streamlit interface
- 📝 Logging using Loguru

---

# 🏗️ Architecture

```
                    User Question
                           │
                           ▼
                  Query Analysis
                           │
                           ▼
                 Retrieve Documents
                           │
                           ▼
                  Grade Documents
                   │            │
         Relevant Docs      No Relevant Docs
               │                  │
               ▼                  ▼
      Generate Answer      Rewrite Query
               │                  │
               └──────────┬───────┘
                          ▼
               Hallucination Check
                          │
                          ▼
                  Final Response
```

---

# 🚀 Tech Stack

## Backend

- Python
- FastAPI
- LangGraph
- LangChain
- Groq
- ChromaDB

## Frontend

- Streamlit

## Embeddings

- BAAI/bge-small-en-v1.5

## LLM

- Llama 3.3 70B Versatile (Groq)

## PDF Processing

- PyMuPDF

## Logging

- Loguru

---

# 📂 Project Structure

```
rag-technical-documentation-assistant/

│
├── app/
│   ├── api/
│   ├── database/
│   ├── graph/
│   ├── llm/
│   ├── loaders/
│   ├── prompts/
│   ├── services/
│   ├── utils/
│   └── vectorstore/
│
├── frontend/
│   ├── streamlit_app.py
│   ├── api.py
│   ├── components.py
│   └── styles.py
│
├── documents/
├── chroma_db/
├── logs/
│
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example
```

---

# 📄 Document Corpus

This project uses a **local document corpus** stored in the `documents/` directory.

The PDFs were manually downloaded from official technical documentation sources and indexed locally before querying.

Example documents include:

- LangGraph Documentation
- LangChain Documentation
- ChromaDB Documentation
- FastAPI Documentation

> **Note:** The assignment allows submitting either the document corpus or a script/URLs to fetch it. This project includes the local PDF corpus used for indexing.

---

# ⚙️ Self-Corrective Workflow

The application follows these steps:

### 1. Query Analysis

Analyzes the user's question.

↓

### 2. Retrieval

Performs semantic search over ChromaDB.

↓

### 3. Document Grading

Evaluates whether retrieved chunks are relevant.

↓

### 4. Query Rewriting

If retrieval quality is poor, rewrites the query and retries retrieval.

↓

### 5. Answer Generation

Generates an answer only from relevant retrieved context.

↓

### 6. Hallucination Checking

Verifies that the generated answer is supported by the retrieved documents.

↓

### 7. Final Response

Returns the validated answer together with document sources.

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/<your-username>/rag-technical-documentation-assistant.git

cd rag-technical-documentation-assistant
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_groq_api_key

LLM_MODEL=llama-3.3-70b-versatile

EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

MAX_RETRIES=2
```

---

# ▶️ Running the Application

## Start FastAPI Backend

```bash
uvicorn app.main:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

---

## Launch Streamlit Frontend

```bash
streamlit run frontend/streamlit_app.py
```

Frontend:

```
http://localhost:8501
```

---

# 📖 Usage

1. Start the backend server.
2. Launch the Streamlit application.
3. Upload one or more PDF documents.
4. Wait until indexing completes.
5. Ask questions about the uploaded documents.
6. View the generated response and cited document sources.

---


# 💬 Example Query

### Question

```
What is Retrieval-Augmented Generation?
```

### Answer

```
Retrieval-Augmented Generation (RAG) combines semantic retrieval
with Large Language Models by retrieving relevant context from
an external knowledge base before generating a response.
```

### Sources

```
✔ langgraph.pdf

✔ chromadb.pdf
```

---

# 🌐 API Endpoints

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | `/health` | Backend health |
| POST | `/query` | Ask question |
| POST | `/documents/upload` | Upload PDF |
| GET | `/documents` | List indexed documents |
| DELETE | `/documents/{filename}` | Delete document |
| POST | `/documents/reset` | Clear vector database |
| GET | `/documents/stats` | Statistics |

---

# 🔮 Future Improvements

- Hybrid Search (Dense + BM25)
- Multi-document summarization
- OCR support
- Conversation memory
- Web search fallback
- Authentication
- Docker deployment
- Kubernetes deployment

---

# 🤝 Contributing

1. Fork the repository.

2. Create a branch.

```bash
git checkout -b feature-name
```

3. Commit changes.

```bash
git commit -m "Add feature"
```

4. Push changes.

```bash
git push origin feature-name
```

5. Open a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Saba Ahmad**

B.Tech
National Institute of Technology Jamshedpur

---

⭐ If you found this project useful, consider giving it a star on GitHub.