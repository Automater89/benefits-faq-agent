# Architecture: Benefits FAQ Agent

## Overview

The Benefits FAQ Agent uses a Retrieval-Augmented Generation (RAG) pattern to answer employee benefits questions. Rather than fine-tuning a model on benefits data, the agent retrieves the most relevant document chunks at query time and passes them as context to Azure OpenAI for grounded answer generation.

This approach has three key advantages for benefits use cases:
1. Benefits information changes annually — RAG allows the knowledge base to be refreshed without retraining.
2. Answers are traceable back to source documents, supporting compliance and audit requirements.
3. The agent can decline questions outside its knowledge base rather than hallucinating.

---

## Component Diagram

```text
+---------------------------+
|   Employee / HR Interface |
|   (Copilot Studio / Web)  |
+---------------------------+
            |
            | Natural language question
            v
+---------------------------+
|   Query Embedding Layer   |
|   Azure OpenAI            |
|   text-embedding-3-small  |
+---------------------------+
            |
            | Query vector
            v
+---------------------------+
|   Azure AI Search         |
|   Hybrid + Semantic Rank  |
|   benefits-faq index      |
+---------------------------+
            |
            | Top-K relevant chunks
            v
+---------------------------+
|   Prompt Construction     |
|   System prompt +         |
|   retrieved context +     |
|   user question           |
+---------------------------+
            |
            v
+---------------------------+
|   Azure OpenAI GPT-4o     |
|   Answer Generation       |
+---------------------------+
            |
            | Grounded answer + source
            v
+---------------------------+
|   Employee Response       |
|   + Escalation Path       |
+---------------------------+
```

---

## Data Flow: Ingestion (One-time / Annual Refresh)

1. Benefits documents (PDFs, Word docs) are loaded from a local or SharePoint source.
2. `chunker.py` splits documents into overlapping chunks (~500 tokens, 50-token overlap) with metadata:
   - `source_file`: original document name
   - `topic`: plan type (medical, dental, 401k, HSA, etc.)
   - `plan_year`: year the document covers
   - `chunk_id`: unique identifier
3. `uploader.py` saves raw chunks to Azure Blob Storage for audit trail.
4. `embed.py` generates vector embeddings for each chunk using Azure OpenAI.
5. `index_builder.py` upserts all chunks with embeddings into the Azure AI Search index.

## Data Flow: Query (Real-time)

1. Employee submits a natural language question.
2. Question is embedded using the same model as the index.
3. Azure AI Search performs hybrid retrieval (keyword + vector) with semantic re-ranking.
4. Top 3–5 chunks are retrieved and formatted as context.
5. `answer_agent.py` builds the full prompt (system prompt + context + question).
6. Azure OpenAI GPT-4o generates a grounded answer.
7. Response is returned with source document citation.
8. If no relevant chunks are found above threshold: agent escalates to HR inbox via Power Automate.

---

## System Prompt Design

The system prompt enforces:
- Answer only from provided context
- Cite the source document in every response
- Decline and escalate if context is insufficient
- Never provide medical or legal advice
- Use plain, employee-friendly language

---

## Key Design Decisions

See [decisions.md](decisions.md) for the full decision log.

| Decision | Choice | Rationale |
|---|---|---|
| RAG vs. fine-tuning | RAG | Benefits data changes annually; RAG allows refresh without retraining |
| Search strategy | Hybrid + semantic rank | Better recall on benefits terminology than pure vector |
| Chunk size | ~500 tokens | Balances context quality with search precision |
| Agent surface | Copilot Studio | Aligns with enterprise M365 stack; no custom UI required |
| Escalation path | Power Automate to HR inbox | Unanswered questions become a feedback loop for handbook gaps |
