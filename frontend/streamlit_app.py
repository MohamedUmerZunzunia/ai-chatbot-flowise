import hashlib
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Document Chatbot",
    page_icon="🤖",
    layout="wide",
)

st.markdown("""
<style>

/* Main content */
.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
    max-width:1200px;
}

/* Sidebar */
[data-testid="stSidebar"]{
    border-right:1px solid #e6e6e6;
}

/* Chat messages */
[data-testid="stChatMessage"]{
    border-radius:14px;
    padding:0.8rem;
    margin-bottom:0.8rem;
}

/* Metric cards */
[data-testid="metric-container"]{
    border:1px solid #e6e6e6;
    border-radius:12px;
    padding:12px;
}

/* Expanders */
.streamlit-expanderHeader{
    font-weight:600;
}

/* Info boxes */
.stAlert{
    border-radius:12px;
}

/* Buttons */
.stButton > button{
    width:100%;
    border-radius:10px;
}

/* Chat input */
[data-testid="stChatInput"]{
    padding-top:1rem;
}

</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 6])

with col1:
    st.markdown("# 🤖")

with col2:
    st.title("AI Document Chatbot")
    st.caption(
        "Upload a PDF, ask questions in natural language, and receive AI-powered answers with supporting source citations."
    )

st.divider()

# -------------------------------
# Session State
# -------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_document" not in st.session_state:
    st.session_state.current_document = None

if "document_name" not in st.session_state:
    st.session_state.document_name = None

if "document_info" not in st.session_state:
    st.session_state.document_info = None

# -------------------------------
# Sidebar
# -------------------------------

st.sidebar.title("📄 Document Manager")

st.sidebar.caption(
    "Upload a PDF to begin chatting with your documents."
)

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    # Generate a unique hash for the uploaded file
    file_hash = hashlib.md5(uploaded_file.getvalue()).hexdigest()

    # Upload only if this is a new document
    if st.session_state.current_document != file_hash:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        with st.spinner("📄 Uploading PDF and creating embeddings..."):

            response = requests.post(
                f"{API_URL}/upload",
                files=files
            )

        if response.status_code == 200:

            data = response.json()

            st.session_state.current_document = file_hash
            st.session_state.document_name = uploaded_file.name
            st.session_state.document_info = data
            st.session_state.messages = []

            st.sidebar.success(
    "✅ Document uploaded and indexed successfully!"
)

        else:

            st.sidebar.error(
    "❌ Upload failed. Please try again."
)    

# -------------------------------
# Sidebar Information
# -------------------------------

if st.session_state.document_name:

    st.sidebar.divider()

    st.sidebar.subheader("📄 Current Document")

    st.sidebar.info(
    f"**{st.session_state.document_name}**"
)

st.sidebar.success("🟢 Ready for questions")

if st.sidebar.button(
    "🗑 Clear Chat",
    use_container_width=True
):
    st.session_state.messages = []
    st.rerun()

if st.session_state.document_info:

    info = st.session_state.document_info

    st.sidebar.divider()

    st.sidebar.subheader("📄 Current Document")
    st.sidebar.write(f"**{info['filename']}**")

    st.sidebar.divider()

    st.sidebar.subheader("📊 Document Statistics")

    col1, col2 = st.sidebar.columns(2)

    with col1:
        st.metric(
    "Characters",
    f"{info['characters']:,}"
)

    with col2:
        st.metric("Chunks", info["chunks"])

    st.sidebar.divider()

    st.sidebar.subheader("🧠 AI Models")

    st.sidebar.info(
    f"🧠 **Embedding Model**\n\n{info['embedding_model']}"
)

    st.sidebar.info(
    f"🤖 **Language Model**\n\n{info['llm_model']}"
)

    st.sidebar.divider()

    st.sidebar.success("🟢 Ready")
# -------------------------------
# Sidebar Information
# -------------------------------

...

# -------------------------------
# Empty State
# -------------------------------

if st.session_state.current_document is None:

    st.info(
        """
👋 **Welcome!**

To get started:

1. Upload a PDF using the sidebar.
2. Wait for the document to be indexed.
3. Ask questions in natural language.

Example questions:

- What is this document about?
- Summarise the document.
- What are the key points?
- Who is the CEO?
- What technologies are mentioned?
"""
    )


# -------------------------------
# Display Chat History
# -------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------
# Chat Input
# -------------------------------

question = st.chat_input(
    "💬 Ask a question about your uploaded document..."
)

if question:

    if st.session_state.current_document is None:

        st.warning("⚠️ Please upload a PDF first.")

    else:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    response = requests.post(
                        f"{API_URL}/chat",
                        json={
                            "question": question
                        }
                    )

                    if response.status_code == 200:

                        data = response.json()

                        answer = data["answer"]
                        sources = data.get("sources", [])

                        st.markdown("### 🤖 Answer")
                        st.markdown(answer)

                        if sources:

                            st.markdown("---")
                            st.markdown("### 📚 Supporting Sources")

                            for source in sources:

                                with st.expander(f"📄 Page {source['page']}"):
                                    st.caption(f"Similarity Score: {source['score']}")
                                    st.write(source["content"])

                    else:

                        answer = "❌ Unable to get a response from the server."
                        st.error(answer)

                except Exception as e:

                    answer = (
    "❌ Unable to connect to the backend.\n\n"
    "Please make sure the FastAPI server is running."
)
                    st.error(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )