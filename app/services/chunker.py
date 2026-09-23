from dataclasses import dataclass

from app.config import settings


@dataclass
class Chunk:
    id: str
    text: str
    chunk_index: int


def split_text(text: str, document_id: str) -> list[Chunk]:
    text = text.strip()
    if not text:
        return []

    chunk_size = settings.chunk_size
    overlap = settings.chunk_overlap

    chunks: list[Chunk] = []
    start = 0
    index = 0
    total_length = len(text)

    while start < total_length:
        end = min(start + chunk_size, total_length)
        chunk_text = text[start:end].strip()

        if chunk_text:
            chunk_id = f"{document_id}-{index}"
            chunks.append(
                Chunk(
                    id=chunk_id,
                    text=chunk_text,
                    chunk_index=index,
                )
            )
            index += 1

        if end >= total_length:
            break

        next_start = end - overlap
        if next_start <= start:
            next_start = end

        start = next_start

    return chunks