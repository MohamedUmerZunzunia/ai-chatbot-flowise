from fastapi import FastAPI
from app.api.upload import router as upload_router
from app.api.chat import router as chat_router

app = FastAPI(
    title="AI Chatbot API",
    version="1.0.0",
    description="AI-powered document chatbot"
)

app.include_router(upload_router)
app.include_router(chat_router)

@app.get("/")
def home():
    return {"message": "AI Chatbot API is running 🚀"}