# RAG-Forge TODO List

This file tracks the major features and tasks for the RAG-Forge project.

## Document Management UI

**Status: Pending**

This feature will add a dedicated page to the Streamlit application to manage the documents in the vector store.

-   [ ] **Backend API (`src/main.py`):**
    -   Create a new endpoint to list all ingested documents (`GET /documents`).
    -   Create an endpoint to delete a document and its embeddings by its source (`DELETE /documents`).
    -   Create an endpoint to re-index a document (`POST /documents/reindex`).
    -   Create an endpoint to "un-index" a document (i.e., mark it as inactive) without deleting it (`PUT /documents/status`).
-   [ ] **UI Page (`src/pages/1_Manage_Documents.py`):**
    -   Create a new Streamlit page to serve as the management interface.
    -   Implement a table view to display the list of all ingested documents, showing their source and status.
    -   Add action buttons (Delete, Re-index, Un-index) for each document in the list.
-   [ ] **Core Logic (`src/ingestion/processing.py`, `src/core.py`):**
    -   Implement the business logic for deleting, re-indexing, and changing the status of documents in the database.

---

## Agentic RAG: Conversational Memory

**Status: Pending**

The goal of this feature is to transform the RAG system from a stateless question-answering service into a stateful conversational agent that remembers the context of the interaction.

-   [ ] **Core Logic:** Refactor `src/core.py` to use a chain that supports memory, like `ConversationalRetrievalChain`.
-   [ ] **API:** Update the FastAPI endpoint in `src/main.py` to manage and pass conversational history.
-   [ ] **UI:** Modify the Streamlit interface in `src/ui.py` to display the chat history and manage the conversation state on the front end.

---

## Advanced RAG: Cross-Encoder Reranking

**Status: Pending**

This feature will enhance retrieval accuracy by adding a reranking step to the RAG pipeline. This will use a more powerful cross-encoder model to re-score the documents returned by the initial vector search.

-   [ ] **Research:**
    -   Identify a suitable cross-encoder model from Ollama Hub (e.g., `rank-zephyr`, `bge-reranker-v2`) that balances performance and resource requirements.
-   [ ] **Configuration (`docker-compose.yml`, `src/config.py`):**
    -   Add a `RERANKER_MODEL` environment variable to specify the model.
    -   Add a `USE_RERANKER` boolean flag to easily enable or disable the feature.
    -   Update the `OLLAMA_MODELS_TO_PULL` list in `docker-compose.yml` to automatically download the chosen reranker model.
-   [ ] **Core Logic (`src/core.py`):**
    -   Integrate the `ContextualCompressionRetriever` from LangChain.
    -   Implement the `RankLLMRerank` document compressor, configuring it to use the specified Ollama model.
    -   Modify the `get_qa_chain` function to wrap the base `VectorDBRetriever` with the new compression retriever when `USE_RERANKER` is true.
-   [ ] **UI Enhancement (`src/ui.py`) (Optional):**
    -   Add a toggle switch to the sidebar to allow real-time switching between the standard retriever and the reranking retriever for comparison.

---

## Completed Features

### ✅ GitHub Copilot Integration

**Status: Completed**

This feature added support for using GitHub Copilot as an alternative, cloud-based LLM provider, authenticated via a secure device flow.

-   **Configuration:** Added environment variables for `LLM_PROVIDER` and token paths.
-   **Authentication:** Created the `scripts/authenticate_github.py` script for the OAuth2 device flow.
-   **Core Logic:** Implemented a factory function in `src/core.py` to select the LLM provider.
-   **Docker:** Updated `docker-compose.yml` to mount the secrets.
-   **Documentation:** Updated `README.md` and `DEV_GUIDE.md` with setup instructions.
-   **Bugfix:** Corrected startup scripts (`start.sh`, `entrypoint.sh`) and fixed various bugs related to imports and API endpoints. 