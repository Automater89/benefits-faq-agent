"""
chunker.py -- Splits benefits documents into indexed chunks with metadata.

Supports PDF and plain text input.
Target chunk size: ~500 tokens with 50-token overlap.
"""
import uuid
from pathlib import Path

import pdfplumber
import tiktoken

from src.utils.logger import get_logger

logger = get_logger(__name__)
ENCODING = tiktoken.get_encoding("cl100k_base")
CHUNK_SIZE = 500
OVERLAP = 50


def count_tokens(text: str) -> int:
    return len(ENCODING.encode(text))


def chunk_text(
    text: str,
    source_file: str,
    topic: str = "general",
    plan_year: str = "2026",
) -> list[dict]:
    """Split text into overlapping token-bounded chunks with metadata."""
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        chunk_words = []
        token_count = 0
        i = start
        while i < len(words) and token_count < CHUNK_SIZE:
            chunk_words.append(words[i])
            token_count = count_tokens(" ".join(chunk_words))
            i += 1

        chunk_str = " ".join(chunk_words)
        chunks.append({
            "chunk_id": str(uuid.uuid4()),
            "content": chunk_str,
            "source_file": source_file,
            "topic": topic,
            "plan_year": plan_year,
        })

        # Step back by overlap amount
        overlap_words: list[str] = []
        for word in reversed(chunk_words):
            overlap_words.insert(0, word)
            if count_tokens(" ".join(overlap_words)) >= OVERLAP:
                break
        start = i - len(overlap_words)

    logger.info(f"Chunked '{source_file}' into {len(chunks)} chunks.")
    return chunks


def chunk_pdf(
    pdf_path: str,
    topic: str = "general",
    plan_year: str = "2026",
) -> list[dict]:
    """Extract text from a PDF and chunk it."""
    path = Path(pdf_path)
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + " "
    return chunk_text(full_text.strip(), source_file=path.name, topic=topic, plan_year=plan_year)
