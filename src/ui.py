import streamlit as st
import requests
import os
import re
from modelforge import config as modelforge_config

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="RAG-Forge",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Check for selected model ---
selected_model = modelforge_config.get_current_model()
if not selected_model:
    st.error(
        "**Error: No model has been selected.**\n\n"
        "From the `RAG-Forge` directory, please configure a model from your terminal before starting the application.\n\n"
        "**Example for Google Gemini:**\n"
        "1. `modelforge config add --provider google --model gemini-1.5-pro-latest --api-key \"YOUR_API_KEY\"`\n"
        "2. `modelforge config select --provider google --model gemini-1.5-pro-latest`\n\n"
        "**Example for Ollama:**\n"
        "1. `modelforge config add --provider ollama --model qwen3:1.7b`\n"
        "2. `modelforge config select --provider ollama --model qwen3:1.7b`\n\n"
        "After configuring, please restart the application with `./start.sh`."
    )
    st.stop()

# --- API Endpoint ---
API_URL = os.getenv("API_URL", "http://localhost:8000/query")

# --- Page Title ---
st.title("🛠️ RAG-Forge")
st.caption("A local, conversational RAG-based chatbot.")

# --- Chat Interface ---
# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display past messages
for role, text in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(text)

# Handle user input
if prompt := st.chat_input("Ask me anything about your documents..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare request payload
    payload = {"query": prompt, "chat_history": st.session_state.chat_history}

    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json=payload)
                response.raise_for_status()  # Raise an exception for bad status codes
                
                result = response.json()
                full_response = result.get("answer", "Sorry, I encountered an error.")
                source_docs = result.get("source_documents", [])
                
                # --- Parse the response ---
                think_pattern = r"<think>(.*?)</think>"
                match = re.search(think_pattern, full_response, re.DOTALL)

                think_content = ""
                answer = full_response

                if match:
                    think_content = match.group(1).strip()
                    answer = re.sub(think_pattern, "", full_response, flags=re.DOTALL).strip()
                
                # Update chat history with the clean answer
                st.session_state.chat_history = result.get("chat_history", [])
                # The history from the API already includes the latest turn, but it has the raw answer.
                # We need to replace the last raw answer with our clean, parsed answer.
                if st.session_state.chat_history:
                    last_turn = list(st.session_state.chat_history[-1])
                    last_turn[1] = answer # Update the assistant's message
                    st.session_state.chat_history[-1] = tuple(last_turn)

                # Display the final answer
                st.markdown(answer)
                
                # Display the thinking process in an expander if it exists
                if think_content:
                    with st.expander("Show thought process"):
                        st.info(think_content)

                # Display source documents
                if source_docs:
                    with st.expander("Sources"):
                        for doc in source_docs:
                            source_name = doc.get("metadata", {}).get("source", "Unknown")
                            st.write(f"**Source:** `{source_name}`")
                            st.info(doc.get("page_content", "No content available."))

            except requests.exceptions.RequestException as e:
                st.error(f"API Error: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}") 