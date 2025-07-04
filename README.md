# RAG-Forge

RAG-Forge is a boilerplate project for building a local Retrieval-Augmented Generation (RAG) application. It provides a solid foundation for creating chatbots and other AI-powered tools that can reason about your private documents. This project is powered by Ollama, LangChain, and PostgreSQL with the `pgvector` extension.

## Features

*   **Local-First**: Runs entirely on your machine. No data leaves your network.
*   **Powered by Ollama**: Easily experiment with different open-source LLMs.
*   **Vector Database**: Uses PostgreSQL with `pgvector` for efficient, local, and combined storage of documents and vectors.
*   **FastAPI Backend**: A robust API for handling queries.
*   **Streamlit UI**: A simple and clean user interface for interacting with the chatbot.
*   **Dockerized**: Get up and running with a single command.

## How It Works

The application follows a standard RAG pipeline:

### 1. Ingestion

Data ingestion is now a manual process, giving you full control over what's in your knowledge base. You can ingest documents using the `POST /upload` endpoint. This is the recommended method for all updates, both for single documents and for bulk-loading. An example script is provided in `scripts/upload_document.py`.

The ingestion process is idempotent: if you upload a document with the same filename, the old version will be deleted and replaced with the new one.

Once a document is ingested:
1.  It is split into smaller, manageable chunks.
2.  The chunks are converted into vector embeddings using a local embedding model (via Ollama).
3.  The text chunks and their corresponding embeddings are stored in a PostgreSQL database.

### 2. Retrieval & Generation

When you ask a question, the query is converted into a vector embedding.
The application queries PostgreSQL to find the most relevant text chunks from the database using vector similarity search.
The retrieved chunks (context) are combined with your original question into a prompt.
This prompt is sent to a local LLM (via Ollama) to generate a final answer.

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for the upload script)
- Git

### Installation & Startup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/shuhaimiao/RAG-Forge.git
    cd RAG-Forge
    ```

2.  **Start the application stack:**
    This command will build the Docker images and start the FastAPI backend, the Streamlit UI, the Ollama service, and the PostgreSQL database.
    ```bash
    ./start.sh
    ```
    The first time you run this, it will download the LLM and embedding models, which may take some time depending on your internet connection.

3.  **Access the services:**
    - **Streamlit UI**: [http://localhost:8501](http://localhost:8501)
    - **FastAPI Backend Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📄 Document Ingestion

The primary way to add your own documents to the RAG system is through the `/upload` API endpoint. You can place your files in the `documents_to_ingest/` directory (which is git-ignored) and use the provided script to upload them.

**Supported File Types:**
- Markdown (`.md`)
- Plain Text (`.txt`)
- PDF (`.pdf`)
- JSON (`.json`)
- YAML (`.yml`, `.yaml`)

To upload all supported documents from the `documents_to_ingest/` directory, run:
```bash
./upload.sh
```

You can also upload a specific file or all files in a different directory:
```bash
# Upload a single file
./upload.sh my_document.pdf

# Upload all supported files from a different directory
./upload.sh path/to/my/docs/
```

When a document is uploaded, any existing data associated with the same filename is automatically removed and replaced with the new content, ensuring your knowledge base stays up-to-date.

## 🛠️ Development

For development guidelines, contribution instructions, and the project's architectural decisions, please refer to the [Developer's Guide (DEV_GUIDE.md)](DEV_GUIDE.md).

## 📄 License
