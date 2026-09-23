from fastapi import FastAPI

from app.api import chat, documents


app = FastAPI(
    title="RAG Knowledge Base",
    version="0.2.0",
)

app.include_router(documents.router)
app.include_router(chat.router)


@app.get("/health")
def health():
    return {"status": "ok"}