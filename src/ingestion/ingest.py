import os
import ollama
from pymilvus import MilvusClient, DataType
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader

from src.config import MILVUS_URI, COLLECTION_NAME, EMBEDDING_DIM, EMBEDDING_MODEL, DATA_DIR

def create_milvus_collection():
    """Creates a Milvus collection if it doesn't already exist."""
    print("Connecting to Milvus...")
    client = MilvusClient(uri=MILVUS_URI)
    
    if client.has_collection(collection_name=COLLECTION_NAME):
        print(f"Collection '{COLLECTION_NAME}' already exists. Skipping creation.")
        return client

    print(f"Collection '{COLLECTION_NAME}' not found. Creating collection...")
    schema = MilvusClient.create_schema(
        auto_id=True,
        enable_dynamic_field=True,
    )
    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=65535)
    schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM)
    
    index_params = MilvusClient.prepare_index_params()
    index_params.add_index(
        field_name="vector",
        index_type="AUTOINDEX",
        metric_type="L2"
    )

    client.create_collection(
        collection_name=COLLECTION_NAME,
        schema=schema,
        index_params=index_params
    )
    print("Collection created successfully.")
    return client

def ingest_data(client: MilvusClient):
    """Loads, chunks, embeds, and ingests data into Milvus."""
    print("Starting data ingestion process...")
    
    # Load documents from the data directory
    loader = DirectoryLoader(DATA_DIR, glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()

    if not documents:
        print("No documents found in the data directory. Exiting.")
        return

    print(f"Loaded {len(documents)} document(s).")

    # Chunk the documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    print(f"Split documents into {len(chunks)} chunks.")

    # Generate embeddings and prepare data for Milvus
    data_to_insert = []
    for chunk in chunks:
        # Generate embedding
        response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=chunk.page_content)
        embedding = response['embedding']
        
        # Prepare data dictionary
        data_to_insert.append({
            "text": chunk.page_content,
            "vector": embedding,
            "source": chunk.metadata.get('source', 'Unknown') # Add metadata
        })

    print(f"Generated embeddings for {len(data_to_insert)} chunks.")

    # Insert data into Milvus
    print("Inserting data into Milvus...")
    res = client.insert(collection_name=COLLECTION_NAME, data=data_to_insert)
    print(f"Successfully inserted {res['insert_count']} records into Milvus.")


if __name__ == "__main__":
    milvus_client = create_milvus_collection()
    ingest_data(milvus_client) 