from fastapi import FastAPI

app = FastAPI(
    title="AI Chatbot API",
    version="1.0.0",
    description="AI-powered document chatbot using FastAPI and Ollama"
)

@app.get("/")
def home():
    return {
        "message": "AI Chatbot API is running 🚀"
    }