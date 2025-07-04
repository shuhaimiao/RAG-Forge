# Project: RAG-Forge

**Vision:** To create an expert AI assistant for an API ecosystem, improving developer experience by providing solution designs and code examples based on a knowledge base of OpenAPI specifications, documentation, and best practices.

---

## Phase 1: The Solid Foundation

**Goal:** Create a working, locally-hosted RAG application that can answer questions based on an initial set of text-based developer documentation. The foundation will be "future-proof" to support more advanced features later.

### Core Architecture

* **Orchestrator/API:** FastAPI (Python)
* **Vector Database:** Milvus
* **LLM & Embedding Provider:** Ollama (self-hosted)
* **Frontend UI:** Streamlit
* **Containerization:** Docker Compose

### Future Vision Considerations (Kept in Mind for Phase 1 Design)

* **Diverse Data Sources:** The system will eventually ingest OpenAPI specs, multi-language code snippets, and structured documentation.
* **Metadata is Crucial:** The design must prioritize attaching rich metadata to each data chunk to enable context-aware retrieval and generation in later phases.

### Actionable Implementation Steps

**1. Setup the Environment:**
* Use the `docker-compose.yml` to launch Milvus, Ollama, and the main application container.
* Pull required models via Ollama: `nomic-embed-text` for embeddings and `llama3` for generation.

**2. Implement the Ingestion Pipeline (`src/ingestion/ingest.py`):**
* **Focus:** Start with a single document type (e.g., Markdown files containing best practices) placed in the `/data` directory.
* **Chunking:** Use a standard text splitter (e.g., `RecursiveCharacterTextSplitter`) to break documents into manageable, overlapping chunks.
* **Metadata:** For each chunk, create and attach a metadata dictionary. This is a critical step for future functionality.
    * *Example:* `{'source': 'api-best-practices.md', 'doc_type': 'best_practice'}`
* **Embedding & Loading:**
    * Connect to the local Ollama service.
    * Generate a vector embedding for each chunk using `nomic-embed-text`.
    * Connect to the Milvus service and load the vector, the raw text chunk, and its metadata into a new collection.

**3. Implement the Core RAG API (`src/main.py` & `src/core.py`):**
* Create a FastAPI endpoint: `POST /api/v1/ask`.
* The endpoint will receive a JSON payload: `{'query': 'User question here'}`.
* **RAG Flow:**
    1.  Embed the incoming `query` using the same Ollama model.
    2.  Query Milvus to retrieve the top-k most relevant chunks based on vector similarity.
    3.  Construct a detailed prompt for the generator LLM using the retrieved chunks as context.
        ```prompt
        You are an expert API assistant. Your goal is to help developers by answering their questions based on the provided documentation. Use only the information from the following context to answer the question. If the context doesn't contain the answer, say that you don't have enough information.

        --- CONTEXT ---
        {context_from_milvus}

        --- QUESTION ---
        {user_query}

        --- ANSWER ---
        ```
    4.  Send the complete prompt to the Ollama `llama3` model for generation.
    5.  Return the LLM's response.

**4. Build the Simple UI (`src/ui.py`):**
* Use Streamlit to create a simple web interface.
* Include a text input box for the user's question and a button to submit.
* On submission, the UI calls the FastAPI backend and displays the returned answer.

---
## Future Phases (The Vision)

* **Phase 2 (The Flexible & Smart RAG):**
    * Implement a model abstraction layer to seamlessly switch between local Ollama and external OpenAI APIs.
    * Introduce a re-ranking model to improve the relevance of retrieved context before sending it to the LLM.
    * Add specialized parsers for new data types (e.g., JSON from OpenAPI specs).

* **Phase 3 (The Advanced RAG):**
    * Implement query transformation techniques to better understand user intent.
    * Explore hybrid search (vector + keyword) for more robust retrieval.
    * Build an evaluation pipeline using a framework like RAGAs to objectively measure performance.
