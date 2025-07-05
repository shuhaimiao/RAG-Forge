# RAG-Forge Project Plan

This document tracks the current refactoring efforts and future feature enhancements for the RAG-Forge project.

---

## Part 1: Current Refactoring Plan

*Objective: To solidify the project's foundation by improving code quality, decoupling services, and establishing best practices before adding new features.*

### Phase 1.1: Solidify `model-forge-lib` as a Standalone Library
- **Task 1.1.1: Enhance CLI with a Scalable Provider Registry** (`pending`)
- **Task 1.1.2: Implement Robust Error Handling** (`pending`)
- **Task 1.1.3: Secure API Key Input in CLI** (`pending`)

### Phase 1.2: Decouple and Refine `RAG-Forge` Application
- **Task 1.2.1: Decouple the Docker Build Process** (`pending`)
- **Task 1.2.2: Strengthen the API Contract** (`pending`)
- **Task 1.2.3: Implement Pydantic-based Settings Management** (`pending`)

---

## Part 2: Future Feature Enhancements

*Objective: To add new capabilities to RAG-Forge after the foundational refactoring is complete.*

### Feature: Document Management UI
- **Goal:** Add a dedicated page to the Streamlit application to manage the documents in the vector store.
- **Tasks:**
    - `[ ]` Backend API: Create endpoints for listing, deleting, and re-indexing documents.
    - `[ ]` UI Page: Build the Streamlit interface with a table view and action buttons.
    - `[ ]` Core Logic: Implement the business logic for all document management actions.
- **Status:** `Pending`

### Feature: Advanced RAG - Cross-Encoder Reranking
- **Goal:** Enhance retrieval accuracy by adding a reranking step to the RAG pipeline.
- **Tasks:**
    - `[ ]` Research: Identify a suitable cross-encoder model.
    - `[ ]` Configuration: Add environment variables to enable/disable reranking and specify the model.
    - `[ ]` Core Logic: Integrate `ContextualCompressionRetriever` from LangChain.
- **Status:** `Pending`

---

## Part 3: Completed Features

### ✅ Agentic RAG: Conversational Memory
- **Description:** Transformed the RAG system into a stateful conversational agent.
- **Tasks:**
    - `[x]` Core Logic: Refactored `src/core.py` to use `ConversationalRetrievalChain`.
    - `[x]` API: Updated the FastAPI endpoint to manage conversation history.
    - `[x]` UI: Modified the Streamlit interface to display chat history.
- **Status:** `Completed`

### ✅ GitHub Copilot & `model-forge-lib` Integration
- **Description:** Created and integrated a reusable library for managing generative LLMs.
- **Tasks:**
    - `[x]` Created `model-forge-lib` project.
    - `[x]` Implemented authentication, configuration, and a model registry.
    - `[x]` Integrated the library into `RAG-Forge`.
- **Status:** `Completed` 