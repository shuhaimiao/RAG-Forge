#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Helper Functions ---
wait_for_service() {
  local host=$1
  local port=$2
  local service_name=$3
  echo "Waiting for $service_name to be available at $host:$port..."
  while ! nc -z $host $port; do
    sleep 1
  done
  echo "$service_name is up and running."
}

pull_model() {
    local model_name=$1
    local ollama_host=$2
    echo "Checking for model: $model_name"
    # Check if the model is already available
    if ! curl -s --fail -o /dev/null "$ollama_host/api/show" -d "{\"name\": \"$model_name\"}"; then
        echo "Model '$model_name' not found. Pulling it..."
        curl -X POST "$ollama_host/api/pull" -d "{\"name\": \"$model_name\", \"stream\": false}"
        echo "Model '$model_name' pulled successfully."
    else
        echo "Model '$model_name' is already available."
    fi
}

# --- Main Script ---

# 1. Wait for dependent services
wait_for_service ollama 11434 "Ollama"
wait_for_service milvus 19530 "Milvus"

# 2. Pull required Ollama models if they don't exist
# OLLAMA_HOST is set in docker-compose.yml
pull_model "$EMBEDDING_MODEL" "$OLLAMA_HOST"
pull_model "$LLM_MODEL" "$OLLAMA_HOST"

# 3. Run the data ingestion script
# This will load data from the /data directory into Milvus
echo "Starting data ingestion..."
python /app/src/ingestion/ingest.py
echo "Data ingestion finished."

# 4. Start the FastAPI backend
echo "Starting FastAPI server on port 8000..."
uvicorn src.main:app --host 0.0.0.0 --port 8000 &

# 5. Start the Streamlit frontend
echo "Starting Streamlit UI on port 8501..."
streamlit run /app/src/ui.py --server.port 8501 --server.address 0.0.0.0

# Keep the script running
wait 