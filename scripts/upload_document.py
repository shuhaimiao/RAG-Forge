import os
import requests
import argparse

# The target API endpoint
API_ENDPOINT = "http://localhost:8000/upload"

def upload_document(file_path):
    """
    Uploads a single document to the RAG-Forge API.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        return

    try:
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f, "text/markdown")}
            response = requests.post(API_ENDPOINT, files=files)
            response.raise_for_status()  # Raise an exception for bad status codes
            print(f"Successfully uploaded {file_path}")
            print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error uploading {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Upload documents to the RAG-Forge API."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="documents_to_ingest/",
        type=str,
        help="Path to a file or directory. Defaults to 'documents_to_ingest/'.",
    )
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: The path '{args.path}' does not exist.")
        return

    if os.path.isdir(args.path):
        print(f"Scanning directory: {args.path}")
        supported_extensions = (".md", ".txt", ".pdf", ".json", ".yml", ".yaml")
        for filename in os.listdir(args.path):
            if filename.lower().endswith(supported_extensions):
                file_path = os.path.join(args.path, filename)
                upload_document(file_path)
    elif os.path.isfile(args.path):
        upload_document(args.path)
    else:
        print(f"Error: The path '{args.path}' is not a valid file or directory.")

if __name__ == "__main__":
    main() 