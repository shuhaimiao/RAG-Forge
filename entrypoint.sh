#!/bin/bash
set -e

# The `depends_on` with `service_healthy` in docker-compose.yml makes these checks
# redundant, but they provide useful, immediate feedback in the logs if something is wrong.
echo "Waiting for PostgreSQL to be ready..."
while ! nc -z postgres 5432; do
    sleep 1
done
echo "PostgreSQL is ready."

echo "Waiting for Ollama to be ready..."
while ! nc -z ollama 11434; do
    sleep 1
done
echo "Ollama is ready."

# Create the readiness file first, so the healthcheck passes.
touch /tmp/ready
echo "Readiness probe file created at /tmp/ready"

# Start FastAPI in the background
echo "Starting FastAPI application..."
uvicorn src.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit in the foreground. This will keep the container running.
echo "Starting Streamlit UI..."
streamlit run src/ui.py --server.port 8501 --server.address 0.0.0.0 