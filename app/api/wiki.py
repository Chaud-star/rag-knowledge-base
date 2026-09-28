from fastapi import APIRouter

from app.schemas.wiki import WikiChatRequest, WikiChatResponse, WikiSource
from app.services.external_kb_service import search_wikipedia
from app.services.llm_service import answer


router = APIRouter(prefix="/api", tags=["wiki"])


@router.post("/chat_wiki", response_model=WikiChatResponse)
async def chat_wiki(request: WikiChatRequest):
    sources = await search_wikipedia(request.question, limit=3)
    contexts = [source["text"] for source in sources]
    reply = answer(request.question, contexts)

    return WikiChatResponse(
        answer=reply,
        sources=[WikiSource(**source) for source in sources],
    )