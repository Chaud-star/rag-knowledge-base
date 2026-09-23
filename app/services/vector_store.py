from chromadb import PersistentClient

from app.config import settings
from app.services.chunker import Chunk


client = PersistentClient(path=settings.chroma_dir)
collection = client.get_or_create_collection(name="rag_knowledge_base")


def add_chunks(
    document_id: str,
    chunks: list[Chunk],
    embeddings: list[list[float]],
) -> None:
    if not chunks:
        return

    ids = [chunk.id for chunk in chunks]
    documents = [chunk.text for chunk in chunks]
    metadatas = [
        {
            "document_id": document_id,
            "chunk_index": chunk.chunk_index,
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )


def search(
    query_embedding: list[float],
    top_k: int | None = None,
) -> list[dict]:
    k = top_k or settings.top_k

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
    )

    ids = result.get("ids", [[]])[0]
    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    return [
        {
            "id": item_id,
            "text": text,
            "metadata": metadata,
            "distance": distance,
        }
        for item_id, text, metadata, distance in zip(
            ids,
            documents,
            metadatas,
            distances,
        )
    ]


def delete_document(document_id: str) -> None:
    collection.delete(where={"document_id": document_id})