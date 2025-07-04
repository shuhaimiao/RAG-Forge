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

1.  **Ingestion**:
    *   Documents from the `data/` directory are loaded.
    *   They are split into smaller, manageable chunks.
    *   The chunks are converted into vector embeddings using a local embedding model (via Ollama).
    *   The text chunks and their corresponding embeddings are stored in a PostgreSQL database.

2.  **Retrieval & Generation**:
    *   When you ask a question, the query is converted into a vector embedding.
    *   The application queries PostgreSQL to find the most relevant text chunks from the database using vector similarity search.
    *   The retrieved chunks (context) are combined with your original question into a prompt.
    *   This prompt is sent to a local LLM (via Ollama) to generate a final answer.

## Getting Started

### Prerequisites

*   Docker and Docker Compose
*   Git

### Installation & Running

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/RAG-Forge.git
    cd RAG-Forge
    ```

2.  **Start the application:**
    This command will build the Docker containers and start all the services. The first launch will take some time as it needs to download the Docker images and the Ollama models.
    ```bash
    docker-compose up --build
    ```

3.  **Access the application:**
    *   **API**: The FastAPI backend is available at `http://localhost:8000`.
    *   **UI**: The Streamlit interface is available at `http://localhost:8501`.

## Project Structure

```
.
├── data/                 # Your source documents go here
├── src/
│   ├── main.py           # FastAPI application
│   ├── ui.py             # Streamlit UI
│   ├── core.py           # Core RAG logic (retrieval & generation)
│   ├── config.py         # Configuration settings
│   └── ingestion/
│       └── ingest.py     # Data ingestion and embedding script
├── Dockerfile            # Dockerfile for the main application
├── ollama.Dockerfile     # Dockerfile for the custom Ollama service
├── docker-compose.yml    # Defines all services
└── requirements.txt      # Python dependencies
```
