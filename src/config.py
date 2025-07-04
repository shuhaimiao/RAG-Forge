import os
from dotenv import load_dotenv

load_dotenv()

# Milvus Configuration
MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
MILVUS_PORT = int(os.getenv("MILVUS_PORT", 19530))
MILVUS_URI = f"http://{MILVUS_HOST}:{MILVUS_PORT}"

# Ollama Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")

# RAG Configuration
COLLECTION_NAME = "rag_forge_collection"
EMBEDDING_DIM = 768 # Based on nomic-embed-text

# Data path
DATA_DIR = "/app/data" 