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

# --- Main Execution ---

# 1. Wait for core services to be ready.
#    The `depends_on` in docker-compose handles the health checks,
#    but this adds an extra layer of robustness.
wait_for_service ollama 11434 "Ollama"
wait_for_service milvus 19530 "Milvus"


# 2. Run the data ingestion script to populate the vector database
echo "Running data ingestion..."
python -m src.ingestion.ingest


# 3. Start the FastAPI backend and the Streamlit UI
echo "Starting FastAPI and Streamlit services..."

# Start FastAPI in the background
uvicorn src.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit in the foreground
streamlit run src/ui.py --server.port 8501 --server.address 0.0.0.0 