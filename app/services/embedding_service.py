from openai import OpenAI

from app.config import settings


client = OpenAI(
   api_key=settings.embedding_api_key,
    base_url=settings.embedding_base_url,
)


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    response = client.embeddings.create(
        model=settings.embedding_model,
        input=texts,
    )

    return [item.embedding for item in response.data]


def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]