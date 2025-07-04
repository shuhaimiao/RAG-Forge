import argparse
import json
import os
import time
import webbrowser

import requests

# Constants
GITHUB_DEVICE_CODE_URL = "https://github.com/login/device/code"
GITHUB_OAUTH_TOKEN_URL = "https://github.com/login/oauth/access_token"
CLIENT_ID = "01ab8ac9400c4e429b23"  # From https://github.com/microsoft/vscode/blob/main/extensions/git-base/src/common/git.ts#L33
SCOPE = "read:user"


def request_device_code():
    """Request a device and user code from GitHub."""
    try:
        response = requests.post(
            GITHUB_DEVICE_CODE_URL,
            headers={"Accept": "application/json"},
            data={"client_id": CLIENT_ID, "scope": SCOPE},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error requesting device code: {e}")
        return None


def prompt_user_verification(code_data):
    """Display the user code and open the verification URL."""
    user_code = code_data["user_code"]
    verification_uri = code_data["verification_uri"]
    
    print("-" * 50)
    print(f"Please go to: {verification_uri}")
    print(f"And enter the code: {user_code}")
    print("-" * 50)
    
    try:
        webbrowser.open(verification_uri)
    except Exception:
        # Silently fail if webbrowser fails, user can still copy-paste.
        pass


def poll_for_token(code_data):
    """Poll GitHub's token endpoint until the user authorizes the app."""
    device_code = code_data["device_code"]
    interval = code_data.get("interval", 5)
    
    print("Waiting for you to authorize in the browser...")

    while True:
        time.sleep(interval)
        try:
            response = requests.post(
                GITHUB_OAUTH_TOKEN_URL,
                headers={"Accept": "application/json"},
                data={
                    "client_id": CLIENT_ID,
                    "device_code": device_code,
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                },
                timeout=10,
            )
            response.raise_for_status()
            token_data = response.json()

            if "error" in token_data:
                error = token_data["error"]
                if error == "authorization_pending":
                    continue
                elif error == "slow_down":
                    interval += 5  # Increase poll interval as requested
                    continue
                else:
                    print(f"Error getting token: {token_data.get('error_description')}")
                    return None
            elif "access_token" in token_data:
                return token_data
        except requests.RequestException as e:
            print(f"Error polling for token: {e}")
            return None


def save_token(token_data, token_path):
    """Save the access token to a file."""
    try:
        with open(token_path, "w") as f:
            json.dump(token_data, f, indent=4)
        # Set restrictive permissions on the token file
        os.chmod(token_path, 0o600)
    except IOError as e:
        print(f"Error saving token to {token_path}: {e}")


def get_token_path():
    """Parse command-line arguments to get the token path."""
    parser = argparse.ArgumentParser(
        description="Authenticate with GitHub to get a Copilot token."
    )
    parser.add_argument(
        "--token-path",
        type=str,
        default=".secrets/github_token.json",
        help="Path to save the GitHub token.",
    )
    args = parser.parse_args()
    return args.token_path


def main():
    """Main function to handle the device authentication flow."""
    token_path = get_token_path()
    
    # Ensure the .secrets directory exists
    os.makedirs(os.path.dirname(token_path), exist_ok=True)

    print("Starting GitHub Copilot authentication...")
    
    # Step 1: Request a device and user code from GitHub
    code_data = request_device_code()
    if not code_data:
        return

    # Step 2: Display the user code and open the verification URL
    prompt_user_verification(code_data)

    # Step 3: Poll for the access token
    token_data = poll_for_token(code_data)
    if not token_data:
        return

    # Step 4: Save the token
    save_token(token_data, token_path)

    print(f"Authentication successful. Token saved to {token_path}")


if __name__ == "__main__":
    main() 