#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Start the main Ollama server process in the background
/bin/ollama serve &
OLLAMA_PID=$!

echo "Ollama server started with PID $OLLAMA_PID"

# Wait for the Ollama API to be available
echo "Waiting for Ollama API to be ready..."
while ! curl -s --fail -o /dev/null http://localhost:11434; do
    sleep 1
done
echo "Ollama API is up and running."

# Check for and pull models if the OLLAMA_MODELS_TO_PULL variable is set
if [ -n "$OLLAMA_MODELS_TO_PULL" ]; then
    # Split the comma-separated string into an array of model names
    IFS=',' read -r -a models <<< "$OLLAMA_MODELS_TO_PULL"
    for model in "${models[@]}"; do
        # Check if the model is already available locally
        if ! ollama list | grep -q "^${model}"; then
            echo "Model '$model' not found. Pulling it..."
            ollama pull "$model"
            echo "Model '$model' pulled successfully."
        else
            echo "Model '$model' is already available."
        fi
    done
else
    echo "No models specified in OLLAMA_MODELS_TO_PULL. Skipping automatic pull."
fi

echo "Model setup complete. Ollama is fully operational."

# Wait for the background Ollama server process to exit
wait $OLLAMA_PID 