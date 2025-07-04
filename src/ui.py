import streamlit as st
import requests
import os

# Get the API host from environment variables, with a default for local running
API_HOST = os.getenv("API_HOST", "http://localhost:8000")
API_ENDPOINT = f"{API_HOST}/api/v1/ask"

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="RAG-Forge",
    page_icon="🤖",
    layout="wide"
)

# --- Page Title and Description ---
st.title("🤖 RAG-Forge: Your Expert API Assistant")
st.markdown("""
Welcome to RAG-Forge! This is a smart assistant designed to help you with your API development questions.
Ask anything about API best practices, and it will provide answers based on its knowledge base.
""")
st.divider()

# --- User Input ---
user_query = st.text_input(
    "Ask your question about API development:",
    placeholder="e.g., How should I handle API versioning?",
    label_visibility="collapsed"
)

if st.button("Get Answer", type="primary"):
    if user_query:
        with st.spinner("Forge is thinking..."):
            try:
                # --- Call the FastAPI Backend ---
                response = requests.post(API_ENDPOINT, json={"query": user_query})
                response.raise_for_status()  # Raise an exception for bad status codes

                # --- Display the Answer ---
                answer = response.json().get("answer")
                st.success("Here is the answer:")
                st.markdown(answer)

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the RAG-Forge API. Please make sure the backend is running. Error: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter a question.") 