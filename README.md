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

The primary way to add your own documents to the RAG system is by using the `upload.sh` script.

1.  **Place your documents** in the `documents_to_ingest/` directory.
    - Supported file types are: `.txt`, `.md`, `.pdf`, `.json`, `.yml`, and `.yaml`.

2.  **Run the upload script:**
    ```bash
    ./upload.sh
    ```
    This will upload all files from the `documents_to_ingest/` directory to the application. The backend will process and embed them, making them available for queries.

## 🧠 LLM Configuration

This project supports multiple LLM providers for generating responses. You can switch between them by setting the `LLM_PROVIDER` environment variable in `docker-compose.yml`.

### Providers

- **`ollama`** (Default): Uses the locally running Ollama service.
- **`github_copilot`**: Uses the GitHub Copilot API.

You can set the model for each provider using the `LLM_MODEL` (for `ollama`) and `GITHUB_COPILOT_MODEL` (for `github_copilot`) environment variables in `docker-compose.yml`.

### Authenticating with GitHub Copilot

To use the `github_copilot` provider, you first need to authenticate.

1.  **Run the authentication script:**
    ```bash
    ./authenticate.sh
    ```

2.  The script will display a user code and open a browser window.

3.  Enter the code in your browser to authorize the application.

4.  Once authorized, the script will save an access token to `.secrets/github_token.json`. This token is used to make authenticated requests to the Copilot API.

## 🐳 Development

For more detailed information on the development environment, including setting up a local Python environment and running tests, please see the [Development Guide](DEV_GUIDE.md).

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
