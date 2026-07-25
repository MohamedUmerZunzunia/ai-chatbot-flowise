from fastapi import APIRouter
from pydantic import BaseModel

from app.chatbot.rag import RAGChatbot

router = APIRouter()

chatbot = RAGChatbot()


class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
async def chat(request: ChatRequest):

    chatbot = RAGChatbot()

    result = chatbot.ask(request.question)

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }