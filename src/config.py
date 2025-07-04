from dotenv import load_dotenv
import os

load_dotenv()

# PostgreSQL Configuration
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DB = os.getenv("POSTGRES_DB", "rag-forge")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_CONNECTION_STRING = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Ollama Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
LLM_MODEL = os.getenv("LLM_MODEL")

# LLM Provider settings
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
GITHUB_COPILOT_TOKEN_PATH = os.getenv(
    "GITHUB_COPILOT_TOKEN_PATH", ".secrets/github_token.json"
)
GITHUB_COPILOT_MODEL = os.getenv("GITHUB_COPILOT_MODEL", "gpt-4")

# RAG Configuration
COLLECTION_NAME = "rag_forge_collection"
EMBEDDING_DIM = 1024 # Based on Qwen3-Embedding-0.6B

# Data path
DATA_DIR = "/app/data"