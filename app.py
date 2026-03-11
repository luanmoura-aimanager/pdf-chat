import streamlit as st
from anthropic import Anthropic

client = Anthropic()

st.title("Chat with your PDF")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if uploaded_file:
    file_content = uploaded_file.read().decode("utf-8", errors="ignore")
    file_content = file_content[:50000]
    question = st.chat_input("Ask something about the file")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            response = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=1024,
                system=f"Answer questions based on this file content:\n\n{file_content}",
                messages=[{"role": "user", "content": question}]
            )
            answer = response.content[0].text
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.info("Upload a PDF to get started")
