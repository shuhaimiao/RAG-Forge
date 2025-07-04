# Project TODO List

This file tracks the upcoming features and tasks for the RAG-Forge project.

## Implement Conversational Memory (Agentic RAG)

The current RAG implementation is stateless. The following tasks will introduce conversational memory to allow for follow-up questions and a more natural, stateful interaction.

- [ ] **Refactor Core Logic (`src/core.py`):**
    - [ID: `conversational_chain`]
    - Replace the `RetrievalQA` chain with `ConversationalRetrievalChain`.
    - Integrate a memory component (e.g., `ConversationBufferMemory`) to manage chat history.

- [ ] **Update API Endpoint (`src/main.py`):**
    - [ID: `update_api`]
    - Depends on: `conversational_chain`
    - Modify the `/query` endpoint to accept and pass conversation history.

- [ ] **Enhance User Interface (`src/ui.py`):**
    - [ID: `update_ui`]
    - Depends on: `update_api`
    - Update the Streamlit UI to maintain and display the full chat history.
    - Pass the history to the backend with each new user query.

## GitHub Copilot Integration via Device Auth

This feature will add support for using GitHub Copilot as an alternative LLM for response generation, keeping Ollama for embeddings. This requires implementing the OAuth 2.0 Device Authorization Flow to securely obtain an access token.

- [ ] **Configuration Setup:**
    - [ID: `gh_config`]
    - Add `LLM_PROVIDER` and `GITHUB_COPILOT_TOKEN_PATH` to the configuration.
    - Create a `.secrets` directory for token storage and add it to `.gitignore`.

- [ ] **Create Authentication Script (`scripts/authenticate_github.py`):**
    - [ID: `gh_auth_script`]
    - Depends on: `gh_config`
    - Develop a script to handle the device auth flow: fetch user code, poll for the token, and save it securely.

- [ ] **Core Logic Integration (`src/core.py`):**
    - [ID: `gh_core_logic`]
    - Depends on: `gh_config`
    - Implement a factory function (`get_llm`) to select the LLM provider (`ollama` or `github_copilot`) based on the environment variable.
    - Add logic to load the GitHub Copilot token and instantiate a LangChain chat model for it.

- [ ] **Update Docker Configuration (`docker-compose.yml`):**
    - [ID: `gh_docker_update`]
    - Depends on: `gh_config`
    - Mount the `.secrets` directory into the application container to make the token accessible.

- [ ] **Documentation (`README.md`, `DEV_GUIDE.md`):**
    - [ID: `gh_docs`]
    - Depends on: `gh_auth_script`, `gh_core_logic`
    - Document the new authentication process and how to switch between LLM providers. 