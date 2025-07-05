from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document as LangChainDocument
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from typing import Any, List, Tuple
from modelforge.registry import ModelForgeRegistry

from src.config import DB_CONNECTION_STRING
from src.models import Document as AppDocument  # Alias to avoid name conflict

class VectorDBRetriever(BaseRetriever):
    """A custom retriever that fetches documents from a PostgreSQL+pgvector database."""
    engine: Any
    Session: Any
    embeddings: Any
    k: int = 5

    class Config:
        arbitrary_types_allowed = True

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[LangChainDocument]:
        """
        Embeds a query and retrieves the top-k most similar documents.
        """
        session = self.Session()
        try:
            query_embedding = self.embeddings.embed_query(query)
            similar_docs = session.query(AppDocument).order_by(
                AppDocument.embedding.l2_distance(query_embedding)
            ).limit(self.k).all()
            
            return [
                LangChainDocument(
                    page_content=doc.content, 
                    metadata={"source": doc.source}
                )
                for doc in similar_docs
            ]
        finally:
            session.close()

def get_embeddings_model():
    """Initialize the Ollama embeddings model."""
    from src.ingestion.processing import get_embeddings_model
    return get_embeddings_model()

def get_qa_chain():
    """
    Initializes and returns a ConversationalRetrievalChain.
    """
    embeddings = get_embeddings_model()
    engine = create_engine(DB_CONNECTION_STRING)
    Session = sessionmaker(bind=engine)
    
    retriever = VectorDBRetriever(
        engine=engine,
        Session=Session,
        embeddings=embeddings
    )
    
    # Use ModelForge to get the currently selected LLM
    registry = ModelForgeRegistry()
    llm = registry.get_llm()
    if not llm:
        raise RuntimeError("Failed to get LLM from ModelForgeRegistry. Please check its configuration.")

    # This memory object will store the chat history.
    # We explicitly set the output_key to 'answer' so the memory knows which
    # part of the chain's output to store in the history.
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    # Note: We are no longer using the custom prompt template directly here.
    # ConversationalRetrievalChain has its own internal prompting mechanisms.
    # We can customize this later if needed.
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
    )
    return qa_chain

# This will be the main entry point for the API
def query_rag(query: str, chat_history: List[Tuple[str, str]]):
    """
    Performs a query against the RAG chain with conversation history.
    """
    qa_chain = get_qa_chain()
    # The chain now expects a dictionary with "question" and "chat_history"
    result = qa_chain({"question": query, "chat_history": chat_history})
    return result

if __name__ == '__main__':
    # Example usage for direct testing
    # Note: The interaction flow is now conversational
    history = []
    
    # First question
    q1 = "What are the best practices for API authentication?"
    print(f"User: {q1}")
    result1 = query_rag(q1, history)
    print(f"AI: {result1['answer']}")
    history.append((q1, result1['answer']))

    print("\n" + "-"*30 + "\n")

    # Follow-up question
    q2 = "Can you elaborate on token-based methods?"
    print(f"User: {q2}")
    result2 = query_rag(q2, history)
    print(f"AI: {result2['answer']}")
    history.append((q2, result2['answer'])) 