import streamlit as st
import requests
import time

# FastAPI server URL
FASTAPI_URL = "http://127.0.0.1:8000/chat/"

# Streamlit UI elements
st.title("Finance RAG Chatbot")
st.markdown("Ask your finance-related question, and get an answer.")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for user question
question = st.chat_input("Ask your finance question:")

if question:
    # Add user question to chat history
    st.session_state.chat_history.append({"role": "user", "content": question})
    
    # Display user question
    with st.chat_message("user"):
        st.markdown(question)
    
    # Display a typing animation while waiting for the response
    with st.chat_message("assistant"):
        with st.spinner("Assistant is typing..."):
            # Make a request to the FastAPI backend
            response = requests.post(FASTAPI_URL, json={"query": question})  # Changed "question" to "query"
            
            if response.status_code == 200:
                answer = response.json().get("response", "No answer available.")
                
                # Simulate typing animation
                placeholder = st.empty()
                typed_answer = ""
                for char in answer:
                    typed_answer += char
                    placeholder.markdown(typed_answer)
                    time.sleep(0.02)  # Adjust the speed of the typing animation
                
                # Add bot answer to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
            else:
                st.error("Error: Unable to get an answer.")