# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    netcat-openbsd \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy our local library and install it in editable mode first
COPY model-forge-lib /app/model-forge-lib
RUN pip install -e /app/model-forge-lib

# Copy and install the rest of the Python dependencies
COPY RAG-Forge/requirements.txt .
RUN grep -v "model-forge-lib" requirements.txt > temp-requirements.txt && \
    pip install --no-cache-dir -r temp-requirements.txt && \
    rm temp-requirements.txt

# Add the app directory to the Python path
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Copy the application source code
COPY RAG-Forge/src /app/src
COPY RAG-Forge/data /app/data
COPY RAG-Forge/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"] 