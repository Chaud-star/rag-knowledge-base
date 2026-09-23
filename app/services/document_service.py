from pathlib import Path

from pypdf import PdfReader
from docx import Document


def parse_file(file_path: str) -> str:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return parse_pdf(path)
    if suffix == ".docx":
        return parse_docx(path)
    if suffix in {".md", ".txt"}:
        return parse_text(path)

    raise ValueError(f"不支持的文件格式: {suffix}")


def parse_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)

    return "\n".join(pages)


def parse_docx(path: Path) -> str:
    doc = Document(str(path))
    paragraphs = [p.text for p in doc.paragraphs]
    return "\n".join(paragraphs)


def parse_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")