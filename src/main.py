from fastapi import FastAPI
from pydantic import BaseModel
from src.core import get_qa_chain

# Initialize the QA chain
qa_chain = get_qa_chain()

# Define the request body model
class QueryRequest(BaseModel):
    query: str

# Define the response body model
class QueryResponse(BaseModel):
    answer: str
    source_documents: list

# Create the FastAPI app
app = FastAPI(
    title="RAG-Forge API",
    description="An API for the RAG-Forge application, providing access to an expert AI assistant.",
    version="1.0.0",
)

@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    """
    FastAPI endpoint to handle RAG queries.
    """
    result = qa_chain({"query": request.query})
    
    return QueryResponse(
        answer=result["result"],
        source_documents=[doc.dict() for doc in result["source_documents"]]
    )

@app.get("/")
def read_root():
    return {"message": "RAG-Forge API is running."} 