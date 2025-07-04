# RAG-Forge Developer Guide

Welcome to the RAG-Forge development team! This guide will walk you through the project's architecture, design, and core concepts to get you up and running quickly.

## Vision

The goal of RAG-Forge is to create an expert AI assistant for an API ecosystem. It's designed to answer developer questions by using a knowledge base of API specifications, documentation, and best practices, ultimately providing solution designs and code examples.

## High-Level Architecture

The entire application is a set of interconnected services managed by Docker Compose. This makes setup and development consistent across different machines.

Here is a simplified view of the component interactions:

```mermaid
graph TD
    User(User) --> UI(Streamlit UI);
    UI --> API(FastAPI Backend);
    API --> Core(Core RAG Logic);

    subgraph Core Logic
        Core --> |1. Embed Query| Ollama;
        Core --> |2. Search Vectors| Milvus;
        Core --> |3. Generate Answer| Ollama;
    end

    subgraph Data Ingestion
        Ingest(Ingestion Script) --> |Reads| Docs(Data Files);
        Ingest --> |Generates Embeddings| Ollama;
        Ingest --> |Stores Data & Vectors| Milvus;
    end

    subgraph Services
        Ollama(Ollama);
        Milvus(Milvus Vector DB);
    end
```

### Service Breakdown

-   **rag-forge-app**: This is the main application container where our Python code lives. It houses three key components:
    1.  **FastAPI Backend**: A robust API that exposes the core RAG functionality.
    2.  **Streamlit UI**: A simple, user-friendly web interface for interacting with the assistant.
    3.  **Ingestion Script**: A script that runs at startup to process and load data into our vector database.
-   **ollama**: This service hosts the large language models (LLMs). We use it for two critical tasks:
    1.  **Generating Embeddings**: Converting text chunks into numerical vectors.
    2.  **Generating Answers**: Creating human-readable answers based on user questions and retrieved context.
-   **milvus**: This is our high-performance vector database. It stores the vectorized representations (embeddings) of our knowledge base and allows for incredibly fast similarity searches.
-   **milvus-etcd** & **milvus-minio**: These are essential dependencies for Milvus. `etcd` stores metadata, and `MinIO` provides object storage for the vector data itself. You can think of them as the "database" and "file system" for Milvus.

## Core Concepts: What is RAG?

RAG stands for **Retrieval-Augmented Generation**. It's a technique that makes LLMs "smarter" by giving them access to external knowledge. Instead of relying only on the data it was trained on, our model can pull in relevant, up-to-date information before answering a question.

Here's the workflow:

1.  **Retrieve**: When a user asks a question, we don't send it directly to the LLM. First, we search our Milvus database to find the most relevant pieces of text from our knowledge base (e.g., excerpts from API documentation).
2.  **Augment**: We take the user's original question and "augment" it by adding the relevant text we just retrieved. This combined text becomes a new, more detailed prompt.
3.  **Generate**: We send this augmented prompt to the LLM. With the added context, the model can generate a much more accurate and specific answer.

## Application Deep Dive

Let's look at the code inside the `rag-forge-app` container.

### Project Structure (`/src`)

-   `config.py`: A centralized file for all important configurations, such as model names, service hosts, and database settings. It reads from environment variables, allowing for easy adjustments without changing the code.
-   `ingestion/ingest.py`: This is where the magic of data preparation happens.
-   `core.py`: Contains the core logic for the RAG pipeline.
-   `main.py`: Defines the FastAPI backend and its API endpoints.
-   `ui.py`: Contains the code for the Streamlit user interface.

### The Data Ingestion Flow (`src/ingestion/ingest.py`)

This script runs automatically when the application starts. Its job is to populate the Milvus vector database.

1.  **Load Documents**: It starts by loading text files from the `/data` directory.
2.  **Chunk Text**: Documents are broken down into smaller, manageable chunks. This is crucial because LLMs have a limited context window, and smaller chunks lead to more precise search results.
3.  **Generate Embeddings**: Each text chunk is sent to the Ollama service to be converted into a vector embedding using the `dengcao/Qwen3-Embedding-0.6B:Q8_0` model.
4.  **Store in Milvus**: The script connects to Milvus and inserts the data: the original text chunk, its vector embedding, and any associated metadata (like the source document name).

### The API & RAG Logic (`src/main.py` & `src/core.py`)

This is the heart of the application, where user queries are processed.

1.  **API Endpoint**: `main.py` defines the `/api/v1/ask` endpoint, which receives the user's question from the Streamlit UI.
2.  **Query Processing**: The request is passed to the `query_rag` function in `core.py`, which executes the RAG flow:
    a.  **Embed Query**: The user's question is converted into a vector embedding using the same model as the documents.
    b.  **Search Milvus**: This query vector is used to search Milvus, which returns the most similar text chunks from its database.
    c.  **Construct Prompt**: A detailed prompt is created by combining the original question with the retrieved context chunks. This gives the LLM all the information it needs.
    d.  **Generate Answer**: The final prompt is sent to the `qwen3:1.7b` model in Ollama, which generates the final answer.
    e.  **Return Response**: The answer is sent back to the UI to be displayed to the user.

## How to Run & Develop

1.  **Start the Application**: From the project root, run:
    ```bash
    docker-compose up --build
    ```
2.  **Access the UI**: Open your browser to `http://localhost:8501`.
3.  **Access the API Docs**: The FastAPI backend provides interactive documentation at `http://localhost:8000/docs`. This is a great way to test the API directly.
4.  **Adding New Knowledge**: To add new documents to the knowledge base, simply place your `.md` or `.txt` files in the `/data` directory and restart the application. The ingestion script will automatically process them. 