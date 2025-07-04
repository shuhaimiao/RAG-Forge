FROM ollama/ollama

# Install curl for health checks and readiness probes
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy the custom startup script that will pull the models
COPY start-ollama.sh /start-ollama.sh

# Make the script executable
RUN chmod +x /start-ollama.sh

# Set the entrypoint to our custom script
ENTRYPOINT [ "/start-ollama.sh" ] 