# RAG-Forge TODO List

This file tracks the major features and tasks for the RAG-Forge project.

## Agentic RAG: Conversational Memory

**Status: Pending**

The goal of this feature is to transform the RAG system from a stateless question-answering service into a stateful conversational agent that remembers the context of the interaction.

-   [ ] **Core Logic:** Refactor `src/core.py` to use a chain that supports memory, like `ConversationalRetrievalChain`.
-   [ ] **API:** Update the FastAPI endpoint in `src/main.py` to manage and pass conversational history.
-   [ ] **UI:** Modify the Streamlit interface in `src/ui.py` to display the chat history and manage the conversation state on the front end.

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