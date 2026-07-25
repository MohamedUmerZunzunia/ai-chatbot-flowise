from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import ollama

DB_DIRECTORY = "chroma_db"


class RAGChatbot:

    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model="nomic-embed-text"
        )

        self.vector_store = Chroma(
            persist_directory=DB_DIRECTORY,
            embedding_function=self.embeddings
        )

        print("\n" + "=" * 80)
        print("RAG INITIALIZED")
        print(f"Chunks in database: {self.vector_store._collection.count()}")
        print("=" * 80)

    def ask(self, question: str):

        results = self.vector_store.similarity_search_with_score(
            question,
            k=2
        )

        print(f"Results returned: {len(results)}")

        docs = []
        sources = []

        print("\n" + "=" * 80)
        print(f"Question: {question}")
        print("=" * 80)

        for index, (doc, score) in enumerate(results, start=1):

            docs.append(doc)

            print(f"\nResult {index}")
            print(f"Similarity Score: {score}")
            print("-" * 40)
            print(doc.page_content)
            print("-" * 40)

            sources.append(
                {
                    "chunk": index,
                    "score": round(float(score), 4),
                    "content": doc.page_content[:250]
                    + ("..." if len(doc.page_content) > 250 else ""),
                    "page": doc.metadata.get("page", "Unknown")
                }
            )

        print("=" * 80)

        context = "\n\n".join(
            doc.page_content for doc in docs
        )

        print("\n" + "=" * 80)
        print("CONTEXT SENT TO LLM")
        print("=" * 80)
        print(context)
        print("=" * 80)

        prompt = f"""
You are an AI assistant.

Answer the user's question using ONLY the context below.

If the answer exists in the context, answer it directly.

Do NOT say the information is missing if it appears in the context.

If the answer is not in the context, reply exactly:

I couldn't find that information in the uploaded document.

Context:
{context}

Question:
{question}

Answer:
"""

        print("\n" + "=" * 80)
        print("PROMPT SENT TO OLLAMA")
        print("=" * 80)
        print(prompt)
        print("=" * 80)

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        print("\n" + "=" * 80)
        print("MODEL RESPONSE")
        print("=" * 80)
        print(response["message"]["content"])
        print("=" * 80)

        return {
            "answer": response["message"]["content"].strip(),
            "sources": sources
        }