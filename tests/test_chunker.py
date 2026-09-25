"""
test_chunker.py -- Unit tests for the document chunker.
"""
from src.ingestion.chunker import chunk_text

SAMPLE_TEXT = (
    "The medical plan deductible for 2026 is $1,500 for individual coverage and $3,000 for family coverage. "
    "The out-of-pocket maximum is $4,000 individual and $8,000 family. "
    "Preventive care visits are covered at 100 percent with no deductible. "
    "Specialist visits require a referral from your primary care physician. "
    "Emergency room visits are subject to a $350 copay, waived if admitted. "
) * 20  # Repeat to generate sufficient text for multi-chunk testing


def test_chunk_produces_multiple_chunks():
    chunks = chunk_text(SAMPLE_TEXT, source_file="test_plan.txt", topic="medical", plan_year="2026")
    assert len(chunks) > 1, "Expected more than one chunk for long text"


def test_chunk_metadata():
    chunks = chunk_text(SAMPLE_TEXT, source_file="test_plan.txt", topic="medical", plan_year="2026")
    for chunk in chunks:
        assert "chunk_id" in chunk
        assert "content" in chunk
        assert chunk["source_file"] == "test_plan.txt"
        assert chunk["topic"] == "medical"
        assert chunk["plan_year"] == "2026"


def test_chunk_content_not_empty():
    chunks = chunk_text(SAMPLE_TEXT, source_file="test_plan.txt")
    for chunk in chunks:
        assert len(chunk["content"]) > 0
