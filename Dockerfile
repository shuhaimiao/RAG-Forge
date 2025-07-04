# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY ./requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container
COPY ./src /app/src
COPY ./data /app/data
COPY ./start.sh /app/

# Make the startup script executable
RUN chmod +x /app/start.sh

# Run start.sh when the container launches
ENTRYPOINT ["/app/start.sh"] 