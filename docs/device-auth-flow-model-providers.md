# Device Authentication Flow for Model Providers (GitHub Copilot Example)

This document outlines the device authentication flow used by `opencode` to connect to model providers like GitHub Copilot. It is intended to guide the porting of this functionality to a Java Spring AI implementation.

## Overview

The application uses the OAuth 2.0 Device Authorization Grant flow. This is a common pattern for CLI tools and devices without a browser to obtain user authorization. The flow consists of the user authorizing the application in their browser while the application polls for an access token in the background.

## Step 1: Initiating Authentication

The process is started from the command line, specifying the provider to authenticate with.

- **Command**: `opencode auth github-copilot`
- **Implementation**: The command logic is handled in `packages/opencode/src/cli/cmd/auth.ts`. This script identifies the requested provider and triggers the corresponding authentication service.

## Step 2: The Device Authorization Flow

The core logic for the device flow is handled by the provider-specific authentication service.

- **Implementation**: `packages/opencode/src/auth/github-copilot.ts`

The flow proceeds as follows:

1.  **Device Code Request**: The application makes a `POST` request to GitHub's device code endpoint.
    - **Endpoint**: `https://github.com/login/device/code`
    - **Parameters**:
        - `client_id`: A specific client ID for the GitHub Copilot application.
        - `scope`: The required permissions (e.g., `copilot`).
    - **Response**: GitHub returns a JSON object containing a `device_code`, `user_code`, and `verification_uri`.

2.  **User Interaction**: The `user_code` and `verification_uri` are displayed to the user in the terminal. The user must open the URL in their browser and enter the code to authorize the application.

3.  **Polling for Access Token**: While the user completes the browser authorization, the application polls GitHub's token endpoint in a loop.
    - **Endpoint**: `https://github.com/login/oauth/token`
    - **Method**: `POST`
    - **Parameters**:
        - `client_id`: The same client ID as before.
        - `device_code`: The code received in step 1.
        - `grant_type`: `urn:ietf:params:oauth:grant-type:device_code`
    - **Response**: Once the user authorizes the app, this endpoint returns a JSON object containing the `access_token`.

## Step 3: Secure Token Storage

After successfully obtaining the `access_token`, it must be stored securely.

- **Implementation**: `opencode` uses the `keytar` library, which interfaces with the operating system's native keychain (e.g., macOS Keychain, Windows Credential Manager, Freedesktop Secret Service).
- **Service Name**: The token is stored under a service name unique to the provider, such as `opencode-github-copilot`.

**Java/Spring Porting Notes**:
- A Java application should use a library that can interface with the OS's secure credential store. Alternatively, other secure storage mechanisms like encrypted files with permissions restricted to the user could be considered.

## Step 4: Making Authenticated API Calls

With a valid access token stored, the application can now make authenticated requests to the model provider's API.

- **Implementation**: The provider logic in `packages/opencode/src/provider/provider.ts` is responsible for retrieving the token and making API calls.
- **API Endpoint**: `https://api.githubcopilot.com/chat/completions`
- **Authentication**: Each request to the API must include the token in the `Authorization` header.
    - **Header**: `Authorization: Bearer <access_token>`
- **Model Selection**: API requests to the provider must specify which model to use. For a comprehensive, open-source list of available models and their provider-specific identifiers, refer to [Models.dev](https://models.dev/). This resource is invaluable for finding the correct `Model ID` to use in API calls.

The provider implementation lazy-loads the token from the secure store upon initialization and attaches it to every subsequent API request for that session. A separate file, `packages/opencode/src/auth/copilot.ts`, contains specific logic for managing the Copilot API token, which has slightly different requirements than the standard GitHub API.

## Summary for Java/Spring AI Porting

To replicate this flow in Java/Spring AI:

1.  **Create an Authentication Service**: A service (e.g., `GitHubCopilotAuthService`) would handle the device flow logic. Use a Java HTTP client like Spring's `WebClient` to make the calls to the `device/code` and `/oauth/token` endpoints.
2.  **Implement a CLI Command**: Use Spring Shell or a similar library to create the `auth github-copilot` command that invokes your authentication service.
3.  **Secure Token Storage**: Implement a component responsible for securely storing and retrieving the access token using a Java-compatible keychain library.
4.  **Create a Provider Implementation**: This class would be responsible for:
    - Retrieving the stored access token.
    - Making authenticated `POST` requests to the `chat/completions` endpoint.
    - Handling the request/response bodies for the AI model. 