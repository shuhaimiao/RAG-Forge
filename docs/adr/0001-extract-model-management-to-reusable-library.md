# 0001. Extract Model Management to a Reusable Library

**Date**: 2025-07-05

**Status**: Accepted

## Context

The RAG-Forge application currently implements logic for selecting between different Large Language Model (LLM) providers (e.g., local Ollama, remote GitHub Copilot), handling OAuth 2.0 device authentication flows, and managing model configurations. This functionality is tightly coupled within the RAG-Forge codebase, primarily in `src/core.py` and various scripts.

There is a foreseeable need to reuse this authentication and model management logic across other, future Python-based AI projects. Maintaining this logic within each project would lead to significant code duplication, increased maintenance effort, and potential inconsistencies between projects.

## Decision

We will extract the core logic for provider authentication, secure token management, and model selection into a new, standalone Python library.

This library will be responsible for:
1.  Handling the authentication flow for different providers (starting with the existing GitHub Copilot device flow).
2.  Storing and retrieving API tokens securely, using the appropriate mechanism for the host OS (e.g., Keychain, Credential Manager).
3.  Managing a registry of available models from different providers, loaded from a central configuration file.
4.  Providing a simple factory function (e.g., `get_model_instance(model_id)`) that returns a ready-to-use, LangChain-compatible model object.

RAG-Forge will then be refactored to become a consumer of this new library, removing the specialized authentication and model selection logic from its codebase and simplifying its concerns to focus on the core RAG pipeline.

## Consequences

### Positive
-   **Reusability**: The centralized logic can be easily shared across multiple projects, promoting the "Don't Repeat Yourself" (DRY) principle.
-   **Improved Maintainability**: Bug fixes, security updates, or the addition of new model providers only need to be implemented in one place.
-   **Clear Separation of Concerns**: The main application (RAG-Forge) can focus on its primary task (RAG), while the library handles the distinct concern of model lifecycle and authentication.
-   **Consistency**: All projects that use the library will handle models and authentication in a uniform way.

### Negative
-   **Initial Development Overhead**: There is an upfront cost to design, build, test, and package the new library.
-   **Dependency Management**: Consumer projects, including RAG-Forge, will have a new internal dependency. Changes to the library will require version updates and potential integration work in downstream projects.

## Alternatives Considered

### 1. Keep Logic within Each Project

-   **Description**: Continue to build and maintain the model management logic within RAG-Forge and copy/paste/adapt it for new projects.
-   **Reason for Rejection**: This approach leads to code duplication, drift between projects, and a significantly higher maintenance burden in the long term. A bug fix in one project would need to be manually patched in all others.

### 2. Create a Shared Microservice

-   **Description**: Expose the model management and authentication logic via a network-accessible microservice.
-   **Reason for Rejection**: This was deemed overly complex for the current requirements. A microservice introduces network latency, deployment complexity (it would need to be hosted and managed), and a more complicated development workflow. This architecture is better suited for scenarios where non-Python applications need to share the logic, which is not a current requirement. A direct library dependency is simpler, faster, and more efficient for a suite of Python-based tools. 