from fastapi import APIRouter, UploadFile, File
from app.services.pdf_service import extract_text_from_pdf
from app.services.text_splitter import split_text
from app.database.vector_store import create_vector_store

import os
import shutil

router = APIRouter()

UPLOAD_FOLDER = "documents"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pages = extract_text_from_pdf(file_path)

    chunks = split_text(pages)
    for i, chunk in enumerate(chunks, 1):
        print(f"\n===== Chunk {i} =====")
        print(chunk.page_content)

    create_vector_store(chunks)

    characters = sum(len(page["text"]) for page in pages)

    return {
        "filename": file.filename,
        "characters": characters,
        "chunks": len(chunks),
        "embedding_model": "nomic-embed-text",
        "llm_model": "llama3.2",
        "status": "Ready"
}