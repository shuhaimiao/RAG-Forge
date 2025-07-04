from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from sqlalchemy.orm import Session
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document as LangChainDocument
from typing import List
import os

from ..config import EMBEDDING_MODEL, OLLAMA_HOST
from ..models import Document


def get_embeddings_model():
    """Initialize the Ollama embeddings model."""
    return OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_HOST)


def get_document_splits(file_path: str) -> List[LangChainDocument]:
    """Loads a document from a file path and splits it into chunks."""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == ".pdf":
        loader = PyPDFLoader(file_path)
    elif file_extension in [".txt", ".md", ".json", ".yml", ".yaml"]:
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    return splits


def embed_and_store_splits(
    splits: List[LangChainDocument],
    source: str,
    session: Session,
    embeddings: OllamaEmbeddings,
):
    """
    Deletes any existing versions, embeds the new chunks, and saves them to the database.
    """
    # 1. Delete existing document chunks from the database
    print(f"Deleting existing chunks for source: {source}")
    session.query(Document).filter(Document.source == source).delete()
    session.commit()

    # 2. Embed and store the new document chunks
    print(f"Embedding {len(splits)} new chunks from source: {source}")
    contents = [doc.page_content for doc in splits]
    embedded_docs = embeddings.embed_documents(contents)

    documents_to_add = []
    for i, split in enumerate(splits):
        documents_to_add.append(
            Document(
                content=split.page_content,
                embedding=embedded_docs[i],
                source=source,
            )
        )

    session.add_all(documents_to_add)
    session.commit()
    print(f"Successfully added {len(documents_to_add)} new chunks to the database.")
    return len(documents_to_add) 