import streamlit as st
import sys
import os
import time
import re

from src.core import get_qa_chain

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="RAG-Forge",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Page Title ---
st.title("🛠️ RAG-Forge")
st.caption("A local RAG-based chatbot powered by Ollama, LangChain, and PostgreSQL with pgvector.")

# --- QA Chain Initialization ---
@st.cache_resource
def load_qa_chain():
    return get_qa_chain()

qa_chain = load_qa_chain()

# --- Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me anything about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        start_time = time.time()
        with st.spinner("Thinking..."):
            result = qa_chain({"query": prompt})
            full_response = result.get("result", "Sorry, I could not find an answer.")
            source_docs = result.get("source_documents", [])
        end_time = time.time()
        
        thinking_time = end_time - start_time

        # Use regex to find and extract the <think> block
        think_pattern = r"<think>(.*?)</think>"
        match = re.search(think_pattern, full_response, re.DOTALL)

        think_content = ""
        answer = full_response

        if match:
            think_content = match.group(1).strip()
            answer = re.sub(think_pattern, "", full_response, flags=re.DOTALL).strip()
        
        # Display the final answer
        message_placeholder.markdown(answer)
        
        # Display the thinking process in an expander if it exists
        if think_content:
            expander_label = f"Show thought process ({thinking_time:.2f}s)"
            with st.expander(expander_label):
                st.info(think_content)
        
        if source_docs:
            with st.expander("Sources"):
                for doc in source_docs:
                    st.write(f"**Source:** `{doc.metadata.get('source', 'Unknown')}`")
                    st.info(doc.page_content)

    st.session_state.messages.append({"role": "assistant", "content": answer}) 