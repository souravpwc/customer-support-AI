"""Load and chunk all knowledge-base markdown documents."""
from __future__ import annotations
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

from config import KB_DIR


@dataclass
class Document:
    doc_id: str
    title: str
    source_file: str
    category: str          # faqs | manuals | troubleshooting | warranty | returns
    content: str
    chunk_index: int = 0
    metadata: dict = field(default_factory=dict)

    @property
    def text(self) -> str:
        return f"[{self.category.upper()}] {self.title}\n{self.content}"


def _chunk_markdown(text: str, max_chars: int = 1200, overlap: int = 100) -> List[str]:
    """Split markdown text on headers, then on size."""
    header_re = re.compile(r"^#{1,3} .+", re.MULTILINE)
    boundaries = [m.start() for m in header_re.finditer(text)] + [len(text)]

    sections: List[str] = []
    for i in range(len(boundaries) - 1):
        sections.append(text[boundaries[i]: boundaries[i + 1]].strip())

    chunks: List[str] = []
    for section in sections:
        if not section:
            continue
        if len(section) <= max_chars:
            chunks.append(section)
        else:
            # Hard-split long sections
            start = 0
            while start < len(section):
                end = min(start + max_chars, len(section))
                chunks.append(section[start:end])
                start = end - overlap
    return [c for c in chunks if len(c) > 30]


def load_documents() -> List[Document]:
    """Return all KB documents as chunked Document objects."""
    docs: List[Document] = []
    category_map = {
        "faqs": "faqs",
        "manuals": "manuals",
        "troubleshooting": "troubleshooting",
        "warranty": "warranty",
        "returns": "returns",
    }

    for category_dir, category in category_map.items():
        folder = KB_DIR / category_dir
        if not folder.exists():
            continue
        for md_file in sorted(folder.glob("*.md")):
            raw = md_file.read_text(encoding="utf-8")

            # Extract title from first H1
            title_match = re.search(r"^# (.+)", raw, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else md_file.stem

            chunks = _chunk_markdown(raw)
            for idx, chunk in enumerate(chunks):
                docs.append(
                    Document(
                        doc_id=f"{category_dir}/{md_file.stem}#{idx}",
                        title=title,
                        source_file=str(md_file.relative_to(KB_DIR)),
                        category=category,
                        content=chunk,
                        chunk_index=idx,
                        metadata={"file": md_file.name, "category": category},
                    )
                )
    return docs


# Singleton
_DOCS: List[Document] | None = None


def get_documents() -> List[Document]:
    global _DOCS
    if _DOCS is None:
        _DOCS = load_documents()
    return _DOCS
