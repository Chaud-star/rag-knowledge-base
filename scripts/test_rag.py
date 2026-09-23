import argparse
from pathlib import Path

from app.services.document_service import parse_file
from app.services.chunker import split_text
from app.services.embedding_service import embed_texts, embed_query
from app.services.vector_store import add_chunks, search, delete_document
from app.services.llm_service import answer


def main(file_path: str, question: str) -> None:
    path = Path(file_path)
    document_id = path.stem

    print("1. 解析文档...")
    text = parse_file(str(path))

    print("2. 切分文本...")
    chunks = split_text(text, document_id)
    print(f"   共 {len(chunks)} 个 chunk")

    print("3. 生成向量并写入向量库...")
    embeddings = embed_texts([chunk.text for chunk in chunks])
    delete_document(document_id)
    add_chunks(document_id, chunks, embeddings)

    print("4. 检索相关内容...")
    query_embedding = embed_query(question)
    results = search(query_embedding, top_k=3)
    contexts = [item["text"] for item in results]

    print("5. 生成回答...")
    reply = answer(question, contexts)

    print("\n===== 问题 =====")
    print(question)
    print("\n===== 回答 =====")
    print(reply)
    print("\n===== 引用片段 =====")
    for item in results:
        print("-", item["text"][:120].replace("\n", " "))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("question")
    args = parser.parse_args()
    main(args.file, args.question)