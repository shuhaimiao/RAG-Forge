from fastapi import FastAPI
from pydantic import BaseModel
from src.core import query_rag

# Define the request body model
class AskRequest(BaseModel):
    query: str

# Define the response body model
class AskResponse(BaseModel):
    answer: str

# Create the FastAPI app
app = FastAPI(
    title="RAG-Forge API",
    description="An API for the RAG-Forge application, providing access to an expert AI assistant.",
    version="1.0.0",
)

@app.post("/api/v1/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    """
    Receives a user's query, processes it through the RAG pipeline,
    and returns the generated answer.
    """
    answer = query_rag(request.query)
    return {"answer": answer}

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG-Forge API. Use the /api/v1/ask endpoint to post your questions."} 