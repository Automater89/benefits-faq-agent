# Decision Log

This file records key architectural and design decisions made during the project, along with the rationale.

---

## 2026-05-06: RAG over fine-tuning

**Decision**: Use Retrieval-Augmented Generation rather than fine-tuning a custom model.

**Rationale**: Benefits information changes every plan year. Fine-tuning would require retraining on every update. RAG allows the knowledge base to be refreshed by re-indexing updated documents without any model changes. RAG also provides source citations, which supports compliance and employee trust.

---

## 2026-05-06: Azure AI Search with semantic ranking

**Decision**: Use hybrid search (BM25 + vector) with Azure AI Search semantic ranking.

**Rationale**: Benefits questions often use specific terminology ("HDHP", "HSA", "FSA", "COBRA") that pure vector search may not handle as well as keyword search. Hybrid retrieval combines both. Semantic ranking re-scores results by meaning, not just term frequency.

---

## 2026-05-06: Copilot Studio as agent surface

**Decision**: Use Microsoft Copilot Studio for the agent interface rather than a custom chat UI.

**Rationale**: Most enterprise HR environments already have M365 licensing. Copilot Studio integrates with Teams, SharePoint, and Power Automate without additional infrastructure. This reduces time-to-value and aligns with the target deployment environment.

---

## 2026-05-06: Power Automate for escalation

**Decision**: Route unanswered questions to HR via Power Automate rather than a custom notification system.

**Rationale**: Power Automate is available in the existing M365 stack, requires no additional infrastructure, and is maintainable by non-developers. The escalation path also doubles as a feedback loop — HR responses can inform knowledge base improvements.
