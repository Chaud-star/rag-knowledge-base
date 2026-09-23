from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class SourceItem(BaseModel):
    document_id: str
    text: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceItem]