import ollama
from pymilvus import MilvusClient

from src.config import MILVUS_URI, COLLECTION_NAME, EMBEDDING_MODEL, LLM_MODEL

def query_rag(query: str) -> str:
    """
    Queries the RAG system.
    1. Embeds the query.
    2. Retrieves relevant context from Milvus.
    3. Constructs a prompt.
    4. Calls the LLM to generate an answer.
    """
    print(f"Received query: {query}")

    # 1. Embed the query
    print("Embedding the query...")
    response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=query)
    query_embedding = response["embedding"]

    # 2. Retrieve relevant context
    print("Retrieving context from Milvus...")
    client = MilvusClient(uri=MILVUS_URI)
    search_results = client.search(
        collection_name=COLLECTION_NAME,
        data=[query_embedding],
        limit=3,
        output_fields=["text", "source"]
    )
    
    context_chunks = [result['entity']['text'] for result in search_results[0]]
    context_str = "\n\n---\n\n".join(context_chunks)

    if not context_str:
        return "I'm sorry, I couldn't find any relevant information to answer your question."

    print("Context retrieved successfully.")
    # print(f"Context: \n{context_str}")

    # 3. Construct the prompt
    prompt_template = """
You are an expert API assistant. Your goal is to help developers by answering their questions based on the provided documentation. Use only the information from the following context to answer the question. If the context doesn't contain the answer, say that you don't have enough information.

--- CONTEXT ---
{context}

--- QUESTION ---
{question}

--- ANSWER ---
"""
    prompt = prompt_template.format(context=context_str, question=query)

    # 4. Generate the answer
    print("Generating answer with LLM...")
    llm_response = ollama.chat(
        model=LLM_MODEL,
        messages=[{'role': 'user', 'content': prompt}]
    )

    print("Answer generated.")
    return llm_response['message']['content']

if __name__ == '__main__':
    # Example usage for direct testing
    test_query = "What are the best practices for API authentication?"
    answer = query_rag(test_query)
    print("\n--- Final Answer ---")
    print(answer) 