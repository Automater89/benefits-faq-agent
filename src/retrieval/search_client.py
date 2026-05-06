"""
search_client.py -- Hybrid and semantic search against the Azure AI Search index.
"""
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from openai import AzureOpenAI

from src.utils.config import get_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


def get_query_embedding(question: str, cfg: dict) -> list[float]:
    client = AzureOpenAI(
        azure_endpoint=cfg["AZURE_OPENAI_ENDPOINT"],
        api_key=cfg["AZURE_OPENAI_KEY"],
        api_version="2024-02-01",
    )
    response = client.embeddings.create(
        input=question,
        model=cfg["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"],
    )
    return response.data[0].embedding


def search_benefits(question: str, top_k: int = 4) -> list[dict]:
    """Run hybrid + semantic search and return top-K chunks."""
    cfg = get_config()
    query_vector = get_query_embedding(question, cfg)

    search_client = SearchClient(
        endpoint=cfg["AZURE_AI_SEARCH_ENDPOINT"],
        index_name=cfg["AZURE_AI_SEARCH_INDEX_NAME"],
        credential=AzureKeyCredential(cfg["AZURE_AI_SEARCH_KEY"]),
    )

    vector_query = VectorizedQuery(
        vector=query_vector,
        k_nearest_neighbors=top_k,
        fields="content_vector",
    )

    results = search_client.search(
        search_text=question,
        vector_queries=[vector_query],
        query_type="semantic",
        semantic_configuration_name="default",
        top=top_k,
        select=["chunk_id", "content", "source_file", "topic", "plan_year"],
    )

    chunks = []
    for r in results:
        score = r.get("@search.score", 0)
        chunks.append({
            "content": r["content"],
            "source": r["source_file"],
            "topic": r.get("topic", ""),
            "score": score,
        })
        logger.info(f"Retrieved: {r['source_file']} | score={score:.3f}")

    return chunks
