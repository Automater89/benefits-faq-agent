"""
answer_agent.py -- Generates grounded benefits answers from retrieved context.

Run directly for a quick interactive test:
    python src/generation/answer_agent.py
"""
from openai import AzureOpenAI

from src.retrieval.search_client import search_benefits
from src.utils.config import get_config
from src.utils.logger import get_logger

logger = get_logger(__name__)

SYSTEM_PROMPT = """\
You are a Benefits FAQ assistant.
Your job is to answer employee benefits questions using only the context provided below.
Always cite the source document in your response.
If the context does not contain enough information to answer the question, respond with exactly:
"I don't have enough information to answer that question. I'll route this to the HR team for you."
Do not provide medical, legal, or financial advice. Direct those questions to appropriate professionals.
Use clear, plain language that any employee can understand. Be concise.
"""

ESCALATION_PHRASE = "I'll route this to the HR team for you"
SCORE_THRESHOLD = 0.7


def build_context(chunks: list[dict]) -> str:
    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(f"[Source {i}: {chunk['source']}]\n{chunk['content']}")
    return "\n\n".join(parts)


def answer_question(question: str) -> dict:
    """
    End-to-end: retrieve relevant context, generate a grounded answer.

    Returns:
        dict with keys:
            - answer (str): the generated response
            - sources (list[str]): source documents used
            - escalate (bool): True if question should be routed to HR
    """
    cfg = get_config()
    chunks = search_benefits(question)

    escalate = False
    if not chunks or max(c["score"] for c in chunks) < SCORE_THRESHOLD:
        logger.warning(f"Low-confidence retrieval for: '{question}'")
        escalate = True

    context = build_context(chunks)
    sources = list({c["source"] for c in chunks})

    client = AzureOpenAI(
        azure_endpoint=cfg["AZURE_OPENAI_ENDPOINT"],
        api_key=cfg["AZURE_OPENAI_KEY"],
        api_version="2024-05-01-preview",
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]

    response = client.chat.completions.create(
        model=cfg["AZURE_OPENAI_DEPLOYMENT"],
        messages=messages,
        temperature=0.1,
        max_tokens=600,
    )

    answer = response.choices[0].message.content
    if ESCALATION_PHRASE in answer:
        escalate = True

    logger.info(f"Answer generated. escalate={escalate}")
    return {"answer": answer, "sources": sources, "escalate": escalate}


if __name__ == "__main__":
    q = input("Ask a benefits question: ")
    result = answer_question(q)
    print(f"\nAnswer:\n{result['answer']}")
    print(f"\nSources: {result['sources']}")
    if result["escalate"]:
        print("[ESCALATE] Routing to HR inbox via Power Automate.")
