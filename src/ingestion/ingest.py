import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column
from pgvector.sqlalchemy import VECTOR
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings

from src.config import (
    DB_CONNECTION_STRING,
    EMBEDDING_MODEL,
    OLLAMA_HOST,
    SOURCE_DATA_DIR,
)

# SQLAlchemy setup
engine = create_engine(DB_CONNECTION_STRING)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define the Document ORM model
class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column()
    embedding: Mapped[VECTOR] = mapped_column(VECTOR(1024)) # Default, will be updated
    source: Mapped[str] = mapped_column()

def setup_database(embedding_dim):
    """Create the vector extension and tables if they don't exist."""
    # Update the embedding dimension in the Document model
    Document.__table__.c.embedding.type.dim = embedding_dim
    
    with engine.connect() as connection:
        connection.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
        connection.commit()
    Base.metadata.create_all(engine)
    print(f"Database setup complete. Vector dimension: {embedding_dim}. 'documents' table is created.")

def get_embeddings_model():
    """Initialize the Ollama embeddings model."""
    return OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_HOST)

def process_and_embed_documents(embeddings):
    """Load, split, and embed documents from the source directory."""
    loader = DirectoryLoader(
        SOURCE_DATA_DIR, glob="**/*.md", loader_cls=TextLoader, show_progress=True
    )
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    print(f"Embedding {len(splits)} document splits...")
    contents = [doc.page_content for doc in splits]
    embedded_docs = embeddings.embed_documents(contents)
    
    documents_to_add = []
    for i, split in enumerate(splits):
        documents_to_add.append(
            Document(
                content=split.page_content,
                embedding=embedded_docs[i],
                source=split.metadata.get("source", "Unknown"),
            )
        )
    return documents_to_add

def main():
    """Main function to set up the database and ingest documents."""
    print("Initializing embeddings model to determine dimensions...")
    embeddings = get_embeddings_model()
    
    # Determine embedding dimensions dynamically
    try:
        dummy_embedding = embeddings.embed_query("get embedding dimension")
        embedding_dim = len(dummy_embedding)
        print(f"Determined embedding dimension: {embedding_dim}")
    except Exception as e:
        print(f"Error determining embedding dimension: {e}")
        sys.exit(1)

    print("Starting database setup...")
    setup_database(embedding_dim)

    print("Processing and embedding documents...")
    documents = process_and_embed_documents(embeddings)

    print(f"Adding {len(documents)} documents to the database...")
    with Session() as session:
        session.add_all(documents)
        session.commit()
    
    print("Ingestion complete.")

if __name__ == "__main__":
    main() 