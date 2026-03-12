import streamlit as st
from anthropic import Anthropic
from pypdf import PdfReader
import chromadb
import uuid

# ── clients ──────────────────────────────────────────────────────────────
client = Anthropic()
chroma_client = chromadb.Client()

# ── helpers ───────────────────────────────────────────────────────────────
def extract_text_from_pdf(uploaded_file):
    """Read the PDF and return full text."""
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def split_into_chunks(text, chunk_size=500):
    """Split text into chunks of roughly chunk_size characters."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1
        if current_length >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def build_collection(chunks):
    """Store chunks in ChromaDB and return the collection."""
    collection_name = f"pdf_{uuid.uuid4().hex[:8]}"
    collection = chroma_client.create_collection(collection_name)
    collection.add(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )
    return collection

def retrieve_relevant_chunks(collection, question, n_results=3):
    """Find the most relevant chunks for the question."""
    results = collection.query(
        query_texts=[question],
        n_results=min(n_results, collection.count())
    )
    return results["documents"][0]

def ask_claude(question, context_chunks):
    """Send the question and relevant chunks to Claude."""
    context = "\n\n".join(context_chunks)
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=f"Answer the user's question based only on the context below.\n\nContext:\n{context}",
        messages=[{"role": "user", "content": question}]
    )
    return response.content[0].text

# ── ui ────────────────────────────────────────────────────────────────────
st.title("Chat with your PDF")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "collection" not in st.session_state:
    st.session_state.collection = None

if uploaded_file:
    if st.session_state.collection is None:
        with st.spinner("Reading and indexing your PDF..."):
            text = extract_text_from_pdf(uploaded_file)
            chunks = split_into_chunks(text)
            st.session_state.collection = build_collection(chunks)
            st.success(f"Ready! Indexed {len(chunks)} chunks.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input("Ask something about the PDF")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            chunks = retrieve_relevant_chunks(st.session_state.collection, question)
            answer = ask_claude(question, chunks)
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.info("Upload a PDF to get started")
    st.session_state.collection = None
    st.session_state.messages = []
