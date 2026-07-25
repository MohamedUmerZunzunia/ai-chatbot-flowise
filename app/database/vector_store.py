import os
import shutil

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

DB_DIRECTORY = "chroma_db"


def create_vector_store(documents):
  

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=DB_DIRECTORY
    )

    print("=" * 60)
    print("VECTOR STORE CREATED")
    print(f"Chunks indexed: {vector_store._collection.count()}")
    print("=" * 60)

    # Print every stored document
    stored_docs = vector_store.similarity_search("", k=20)

    for i, doc in enumerate(stored_docs, start=1):
        print(f"\n===== STORED CHUNK {i} =====")
        print("Metadata:", doc.metadata)
        print(doc.page_content)

    return vector_store