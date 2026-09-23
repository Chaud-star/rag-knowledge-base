from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse, SourceItem
from app.services.embedding_service import embed_query
from app.services.vector_store import search
from app.services.llm_service import answer


router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    query_embedding = embed_query(request.question)
    results = search(query_embedding, top_k=3)

    contexts = [item["text"] for item in results]
    reply = answer(request.question, contexts)

    sources = [
        SourceItem(
            document_id=item["metadata"].get("document_id", ""),
            text=item["text"][:300],
        )
        for item in results
    ]

    return ChatResponse(answer=reply, sources=sources)