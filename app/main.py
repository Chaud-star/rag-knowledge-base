from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import chat, documents,wiki


app = FastAPI(
    title="RAG Knowledge Base",
    version="0.3.0",
)

app.include_router(documents.router)
app.include_router(chat.router)
app.include_router(wiki.router)


@app.get("/health")
def health():
    return {"status": "ok"}


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")