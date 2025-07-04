from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document as LangChainDocument
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from typing import Any, List

from src.config import DB_CONNECTION_STRING, EMBEDDING_MODEL, LLM_MODEL, OLLAMA_HOST
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
    return OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_HOST)

def get_qa_chain():
    """
    Initializes and returns a RetrievalQA chain.
    """
    embeddings = get_embeddings_model()
    engine = create_engine(DB_CONNECTION_STRING)
    Session = sessionmaker(bind=engine)
    
    retriever = VectorDBRetriever(
        engine=engine,
        Session=Session,
        embeddings=embeddings
    )
    llm = OllamaLLM(
        model=LLM_MODEL, 
        base_url=OLLAMA_HOST,
        mirostat=None,
        mirostat_eta=None,
        mirostat_tau=None,
        tfs_z=None,
    )

    template = """
    You are a helpful AI assistant for the RAG-Forge project. Use the following
    context to answer the question. First, think through your plan to answer the question inside <think></think> tags.
    Then, answer the user's question. If you don't know the answer, say that you don't know, don't try to make up an answer.

    Context: {context}
    Question: {question}

    Answer:
    """
    prompt = PromptTemplate.from_template(template)

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    return qa_chain

if __name__ == '__main__':
    # Example usage for direct testing
    test_query = "What are the best practices for API authentication?"
    answer = query_rag(test_query)
    print("\n--- Final Answer ---")
    print(answer) 