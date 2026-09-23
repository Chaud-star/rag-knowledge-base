import shutil
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.document_service import parse_file
from app.services.chunker import split_text
from app.services.embedding_service import embed_texts
from app.services.vector_store import add_chunks, delete_document


router = APIRouter(prefix="/api/documents", tags=["documents"])

SUPPORTED_SUFFIXES = {".pdf", ".docx", ".md", ".txt"}
UPLOAD_DIR = Path("data/uploads")


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise HTTPException(status_code=400, detail=f"不支持的文件格式: {suffix}")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    dest = UPLOAD_DIR / file.filename

    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document_id = dest.stem
    text = parse_file(str(dest))
    chunks = split_text(text, document_id)
    embeddings = embed_texts([chunk.text for chunk in chunks])

    delete_document(document_id)
    add_chunks(document_id, chunks, embeddings)

    return {
        "document_id": document_id,
        "filename": dest.name,
        "chunks": len(chunks),
    }


@router.get("")
async def list_documents():
    if not UPLOAD_DIR.exists():
        return []

    documents = []
    for path in UPLOAD_DIR.iterdir():
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            documents.append(
                {
                    "document_id": path.stem,
                    "filename": path.name,
                }
            )
    return documents


@router.delete("/{document_id}")
async def remove_document(document_id: str):
    matched = [
        path
        for path in UPLOAD_DIR.iterdir()
        if path.is_file() and path.stem == document_id
    ]

    if not matched:
        raise HTTPException(status_code=404, detail="文档不存在")

    for path in matched:
        path.unlink()

    delete_document(document_id)
    return {"message": "已删除", "document_id": document_id}