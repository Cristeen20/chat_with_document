import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Document Chatbot", layout="centered")
st.title("📄 Chat with your Documents")
# 2. Message input stays below chat history
st.write("### Ask a question about your documents:")

# Sidebar for uploading
st.sidebar.header("Upload Document")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=None)
if uploaded_file and st.sidebar.button("Upload"):
    with st.spinner("Uploading..."):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        response = requests.post(f"{API_URL}/upload_document", files=files)
        if response.ok:
            st.sidebar.success("File uploaded and indexed successfully!")
        else:
            st.sidebar.error(f"Upload failed: {response.text}")

# Chat history and input
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

for speaker, message in st.session_state.chat_history:
    if speaker == "user": 
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**Bot:** {message}")


user_query = st.chat_input("Type your question:")

if user_query and user_query.strip() != "":
    st.session_state.chat_history.append(("user", user_query))
    
    payload = {"query": user_query}
    with st.spinner("Getting answer..."):
        resp = requests.post(f"{API_URL}/query", json=payload)
        if resp.ok:
            answer = resp.json()["response"]
            st.session_state.chat_history.append(("bot", answer))
            st.rerun()
            
