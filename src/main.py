from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tempfile
import os
from typing import List, Tuple, Dict, Any

from src.core import query_rag
from src.ingestion.processing import (
    get_document_splits,
    embed_and_store_splits,
    get_embeddings_model,
)
from src.config import DB_CONNECTION_STRING

# Define the request body model
class QueryRequest(BaseModel):
    query: str
    chat_history: List[Tuple[str, str]] = []

# Define the response body model
class QueryResponse(BaseModel):
    answer: str
    source_documents: List[Dict[str, Any]]
    chat_history: List[Tuple[str, str]]

# Create the FastAPI app
app = FastAPI(
    title="RAG-Forge API",
    description="An API for the RAG-Forge application, providing access to an expert AI assistant.",
    version="1.0.0",
)

# --- Database Setup ---
engine = create_engine(DB_CONNECTION_STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.post("/upload", status_code=201)
def upload_document(file: UploadFile = File(...)):
    """
    Uploads a document, processes it, and stores it in the vector database.
    """
    supported_extensions = [".pdf", ".txt", ".md", ".json", ".yml", ".yaml"]
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in supported_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{file_extension}'. Supported types are: {supported_extensions}",
        )

    try:
        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name

        db = SessionLocal()
        embeddings = get_embeddings_model()
        try:
            # Load and split the document from the temporary file
            splits = get_document_splits(tmp_path)

            # Embed and store the splits
            chunks_added = embed_and_store_splits(
                splits, file.filename, db, embeddings
            )

            return {
                "message": f"Successfully ingested {chunks_added} chunks from {file.filename}."
            }
        finally:
            db.close()
            # Clean up the temporary file
            os.unlink(tmp_path)

    except Exception as e:
        # If the temp file was created, ensure it's cleaned up on error too
        if "tmp_path" in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    """
    FastAPI endpoint to handle RAG queries with conversational history.
    """
    result = query_rag(request.query, request.chat_history)
    
    # Update chat history
    updated_history = request.chat_history + [(request.query, result["answer"])]

    # Format source documents
    source_docs = [
        {"page_content": doc.page_content, "metadata": doc.metadata}
        for doc in result["source_documents"]
    ]
    
    return QueryResponse(
        answer=result["answer"],
        source_documents=source_docs,
        chat_history=updated_history
    )

@app.get("/")
def read_root():
    return {"message": "RAG-Forge API is running."} 