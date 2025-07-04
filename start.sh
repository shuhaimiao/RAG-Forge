#!/bin/bash
# This script ensures that the required services are available before starting the main application.

# Exit immediately if a command exits with a non-zero status.
set -e

# Function to wait for a service to be ready
wait_for_service() {
    local host=$1
    local port=$2
    local service_name=$3
    echo "Waiting for $service_name to be ready at $host:$port..."
    while ! nc -z $host $port; do
        echo "Still waiting for $service_name..."
        sleep 2
    done
    echo "$service_name is up and running."
}

# --- Service Dependencies ---
# The app depends on both PostgreSQL and Ollama.

# Wait for PostgreSQL
wait_for_service postgres 5432 "PostgreSQL"

# Wait for Ollama
wait_for_service ollama 11434 "Ollama"

# --- Data Ingestion ---
# The data ingestion script (`src/ingestion/ingest.py`) can be run manually 
# to bulk-load documents from the `data/` directory.
# We no longer run it on startup to give the user control over ingestion.
echo "Skipping automatic data ingestion. Use the /upload endpoint or run ingest.py manually."

# --- Application Startup ---
# Start both the FastAPI backend and the Streamlit UI.

# Start the FastAPI application in the background.
echo "Starting FastAPI application in the background..."
uvicorn src.main:app --host 0.0.0.0 --port 8000 &

# Start the Streamlit UI in the foreground.
echo "Starting Streamlit UI..."
streamlit run src/ui.py --server.port 8501 --server.address 0.0.0.0

# 3. Create a readiness file to signal that the app is ready
touch /tmp/ready
echo "Readiness probe file created."

# 4. Start the FastAPI backend and the Streamlit UI
echo "Starting FastAPI and Streamlit services..."

# Start FastAPI in the background
uvicorn src.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit in the foreground
streamlit run src/ui.py --server.port 8501 --server.address 0.0.0.0 