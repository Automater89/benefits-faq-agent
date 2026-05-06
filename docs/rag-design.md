# RAG Design: Benefits FAQ Agent

## Chunking Strategy

Benefits documents are structured but not uniform. The chunking approach accounts for this:

- **Target chunk size**: ~500 tokens (roughly one Q&A pair or one plan summary section)
- **Overlap**: 50 tokens between chunks to preserve context across boundaries
- **Metadata attached to every chunk**:
  - `source_file`: document name
  - `topic`: category (medical, dental, vision, 401k, HSA, FSA, PTO, FMLA)
  - `plan_year`: coverage year
  - `chunk_id`: UUID
  - `page_number`: for PDF sources

## Index Configuration

Azure AI Search index schema:

```json
{
  "name": "benefits-faq",
  "fields": [
    { "name": "chunk_id", "type": "Edm.String", "key": true },
    { "name": "content", "type": "Edm.String", "searchable": true },
    { "name": "content_vector", "type": "Collection(Edm.Single)", "dimensions": 1536, "vectorSearchProfile": "hnsw-profile" },
    { "name": "source_file", "type": "Edm.String", "filterable": true },
    { "name": "topic", "type": "Edm.String", "filterable": true, "facetable": true },
    { "name": "plan_year", "type": "Edm.String", "filterable": true }
  ]
}
```

## Retrieval Strategy

- **Hybrid search**: keyword BM25 + vector cosine similarity
- **Semantic re-ranking**: enabled to surface the most contextually relevant chunks
- **Top-K**: retrieve top 4 chunks per query
- **Score threshold**: if max relevance score < 0.7, trigger escalation path

## Prompt Template

```
System:
You are a Benefits FAQ assistant for [Company Name].
Your job is to answer employee benefits questions using only the context provided below.
Always cite the source document in your response.
If the context does not contain enough information to answer the question, say:
"I don't have enough information to answer that question. I'll route this to the HR team for you."
Do not provide medical, legal, or financial advice. Direct those questions to appropriate professionals.
Use clear, plain language that any employee can understand.

Context:
{retrieved_chunks}

Question:
{employee_question}

Answer:
```

## Escalation Logic

If the retrieval score falls below threshold OR the model's response contains the escalation phrase:
1. Log the unanswered question with timestamp and topic category
2. Trigger Power Automate flow to send an HR inbox notification
3. HR reviews, answers, and optionally adds the Q&A pair to the knowledge base

This creates a **closed feedback loop**: unanswered questions drive handbook improvements.
