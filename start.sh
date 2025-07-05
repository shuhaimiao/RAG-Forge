#!/bin/bash
# This script ensures that the required services are available before starting the main application.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting RAG-Forge environment..."
echo "This will build the Docker images and start the services."
echo "The application logs will be streamed to this terminal."
echo "Press Ctrl+C to stop the services."

# The --build flag ensures images are rebuilt if the Dockerfile or source code changes.
# The --remove-orphans flag removes containers for services that are no longer in the docker-compose file.
docker-compose up --build --remove-orphans

echo ""
echo "-----------------------------------------------------"
echo "RAG-Forge has been shut down."
echo "-----------------------------------------------------" 