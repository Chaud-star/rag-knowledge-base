from pydantic import BaseModel


class WikiChatRequest(BaseModel):
    question: str


class WikiSource(BaseModel):
    title: str
    url: str
    text: str


class WikiChatResponse(BaseModel):
    answer: str
    sources: list[WikiSource]