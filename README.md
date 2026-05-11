# Benefits FAQ Agent

**An enterprise RAG agent that turns a benefits handbook into instant, grounded, cited answers — built to show how HR domain expertise and AI enablement combine in a real workforce-facing product.**

[![Status](https://img.shields.io/badge/status-in%20progress-yellow)](https://github.com/Automater89/benefits-faq-agent)
[![Stack](https://img.shields.io/badge/stack-Azure%20%7C%20OpenAI%20%7C%20Copilot%20Studio-0078D4)](#tech-stack)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

> Portfolio project by **Wes Shelton** — IT Project Manager focused on AI enablement, HR technology, Power Platform, and enterprise workforce adoption. See related work in the [Agent Showcase](https://automater89.github.io/Agent-Showcase/).

---

## The business problem

Mid-to-large employers field the same benefits questions in cycles: deductibles, HSA limits, open enrollment windows, dependent rules, 401(k) deadlines, COBRA, FMLA. The answers already exist — in PDFs, plan summaries, and SharePoint pages — they just aren't easy for an employee to find at the moment they ask.

The cost shows up in three places:

- **HR capacity** drained by repeat tier-1 questions instead of higher-value work.
- **Employee experience** eroded when people give up and guess, or open a ticket and wait days.
- **Compliance risk** when answers come from word-of-mouth instead of the current plan document.

## What this project proves

This repo is a working blueprint for solving that problem with an enterprise-safe RAG agent, and it demonstrates the skills an IT Project Manager driving AI enablement needs to ship one:

- **Translating an HR operational pain point into an AI product spec** — chunking strategy, retrieval design, escalation logic, and guardrails all driven by how employees actually ask benefits questions.
- **Designing on the Microsoft enterprise stack** employers already license — Azure OpenAI, Azure AI Search, Copilot Studio, Power Automate — minimizing net-new infrastructure and procurement friction.
- **Building governance in from day one** — citations on every answer, refusal on out-of-scope questions, an HR escalation loop, and a `.env`-based secret pattern with nothing sensitive in the repo.
- **Closing the adoption loop** — unanswered questions become a feedback signal back to HR, so the handbook improves over time instead of the agent quietly failing.

---

## Business outcome (positioning, not invented metrics)

For an HR or People Operations team, a working version of this agent is designed to deliver:

- **Deflection of repeat tier-1 benefits questions** away from HR inboxes and Slack channels.
- **Consistent, sourced answers** drawn from the current plan year documents — no stale or inconsistent guidance across team members.
- **Faster employee self-service**, especially during open enrollment crunch windows.
- **A continuous improvement loop**: every unanswered question is logged and routed to HR, surfacing gaps in the handbook itself.

> Hard deflection percentages depend on org size, question mix, and document coverage. This README intentionally avoids fabricated numbers; outcomes above describe the mechanism by which value is realized.

The author's prior, separate work in benefits operations — including a SharePoint + Power Automate Benefits Customer Service Tracker at Wayne County — measurably reduced processing time, which is the same lever this agent applies to a different stage of the employee journey.

---

## Architecture at a glance

```text
       ┌───────────────────────┐
       │  Employee question    │
       │  (Teams / Copilot     │
       │   Studio / web chat)  │
       └──────────┬────────────┘
                  │
                  ▼
       ┌───────────────────────┐
       │  Embed query          │
       │  Azure OpenAI         │
       │  text-embedding-3-sm  │
       └──────────┬────────────┘
                  │
                  ▼
       ┌───────────────────────┐
       │  Azure AI Search      │
       │  Hybrid (BM25+vector) │
       │  + semantic re-rank   │
       └──────────┬────────────┘
                  │  top-K chunks
                  ▼
       ┌───────────────────────┐
       │  Prompt assembly      │
       │  system + context     │
       │  + employee question  │
       └──────────┬────────────┘
                  │
                  ▼
       ┌───────────────────────┐        Low retrieval score
       │  Azure OpenAI GPT-4o  │──────────────────────────────┐
       │  Grounded answer      │                              │
       └──────────┬────────────┘                              ▼
                  │                              ┌───────────────────────┐
                  ▼                              │  Power Automate flow  │
       ┌───────────────────────┐                 │  → HR inbox / ticket  │
       │  Answer + citation    │                 │  + handbook-gap log   │
       │  delivered to user    │                 └───────────────────────┘
       └───────────────────────┘
```

Full detail: [docs/architecture.md](docs/architecture.md) · RAG design: [docs/rag-design.md](docs/rag-design.md) · Decision log: [docs/decisions.md](docs/decisions.md).

---

## RAG / AI workflow pattern

A deliberate, audit-friendly RAG pattern — not a freeform chatbot.

| Stage | What happens | Why it matters for benefits |
|---|---|---|
| **Ingest** | Plan documents (PDF, Word, SharePoint) loaded into Blob Storage | Annual plan refresh is a re-index, not a retraining cycle |
| **Chunk** | ~500-token chunks, 50-token overlap, tagged with `topic`, `plan_year`, `source_file` | Lets the agent filter by plan year so a 2025 chunk never answers a 2026 question |
| **Embed** | `text-embedding-3-small` via Azure OpenAI | Same model used at index and query time for consistency |
| **Retrieve** | Hybrid keyword + vector search with Azure AI Search semantic ranking, top-K = 4 | Benefits vocabulary (HDHP, HSA, COBRA, FMLA) needs keyword precision *and* semantic recall |
| **Ground** | System prompt forces "answer only from context", requires citations, blocks medical/legal/financial advice | Keeps the agent inside its lane and inside compliance |
| **Generate** | GPT-4o at low temperature (0.1) | Deterministic, plain-language answers — not creative writing |
| **Escalate** | If max relevance score < 0.7 OR model emits the escalation phrase, Power Automate routes the question to HR | No silent failures; every miss becomes a handbook improvement |

The agent will **decline and escalate** rather than guess. That refusal behavior is the feature, not a limitation — it is what makes the agent safe to put in front of employees.

---

## Tech stack

| Layer | Tooling | Why this choice |
|---|---|---|
| Cloud platform | **Azure** | Aligns with the M365 / Entra ID environment most HR orgs already operate in |
| Document store | **Azure Blob Storage** | Cheap, durable, supports lifecycle policies for plan-year archiving |
| Retrieval | **Azure AI Search** (hybrid + semantic ranking) | Handles benefits-specific terminology better than pure-vector retrieval |
| Embeddings | **Azure OpenAI · text-embedding-3-small** | Cost-effective, sufficient quality for handbook-scale corpora |
| LLM | **Azure OpenAI · GPT-4o** | Strong instruction-following; supports tight grounding prompts |
| Agent surface | **Microsoft Copilot Studio** | Drops into Teams / SharePoint without a custom UI |
| Workflow / escalation | **Power Automate** | Existing M365 license footprint; maintainable by HR ops, not just engineers |
| Runtime | **Python 3.10+**, VS Code | Standard, transparent, easy to hand off |
| Source control | **GitHub** | Public, reviewable, recruiter-readable |

---

## Privacy, security & governance

Benefits data sits next to PHI-adjacent and PII-laden content. This project is designed with that in mind:

- **No employee data in the repo.** Sample documents under `data/samples/` are plan-language excerpts only — no names, IDs, claims, dependents, or compensation data.
- **Secrets stay out of source.** All credentials (Azure OpenAI key, AI Search key, storage connection string) load from `.env`, which is `.gitignore`'d. `.env.example` is the only template in the repo. There are no real keys anywhere in the codebase.
- **Grounded answers only.** The system prompt forces the model to answer strictly from retrieved context and to cite the source document. Out-of-context questions trigger an explicit refusal.
- **Hard limits on advice.** The agent is instructed never to provide medical, legal, or financial advice — it directs employees to the appropriate professional.
- **Audit trail by design.** Every chunk carries `source_file`, `topic`, and `plan_year` metadata. Every answer can be traced back to the document and version it came from.
- **Escalation, not fabrication.** When retrieval confidence falls below threshold, the question is routed to HR via Power Automate rather than answered speculatively.
- **Production hardening path.** For a real deployment, the recommended next steps are: managed-identity auth via Azure Entra ID (replace API keys), private endpoints on Search and OpenAI, role-based access on the Copilot Studio surface, retention policies on logged questions, and a DLP review of the chunked corpus before indexing. These are intentionally called out rather than hand-waved.

---

## Repository layout

```text
benefits-faq-agent/
├── README.md                  ← you are here
├── LICENSE
├── docs/
│   ├── architecture.md        ← component diagram, data flow, design decisions
│   ├── rag-design.md          ← chunking, index schema, prompt template, escalation
│   ├── setup.md               ← Azure resources + local env
│   └── decisions.md           ← decision log with rationale
├── src/
│   ├── ingestion/chunker.py   ← PDF/text → metadata-tagged chunks
│   ├── retrieval/search_client.py ← hybrid + semantic search
│   ├── generation/answer_agent.py ← grounded answer + escalation logic
│   └── utils/                 ← config + structured logging
├── data/
│   ├── samples/               ← (empty) drop-in benefits documents
│   └── outputs/               ← (gitignored) agent run artifacts
├── tests/test_chunker.py
├── .env.example               ← template only; no real secrets
├── requirements.txt
└── .gitignore
```

---

## Setup & demo

Full step-by-step guide: [docs/setup.md](docs/setup.md).

```bash
git clone https://github.com/Automater89/benefits-faq-agent.git
cd benefits-faq-agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # fill in your Azure endpoints + keys locally
```

Verify Azure connectivity:

```bash
python src/utils/config.py
```

Run the chunker unit tests:

```bash
pytest tests/
```

Ask the agent a benefits question end-to-end (requires populated index):

```bash
python -m src.generation.answer_agent
# > Ask a benefits question: What is the 401k employer match?
```

The script returns the answer, source citations, and an `escalate` flag indicating whether the question should be routed to HR.

### Suggested demo flow for a walkthrough

1. **Show the problem** — open a real (sanitized) benefits PDF and a question an employee actually asks.
2. **Show the ingest** — chunk it, point out the `plan_year` and `topic` metadata.
3. **Ask an in-scope question** — return a cited answer.
4. **Ask an out-of-scope question** (e.g., "Should I enroll in the HSA or FSA?") — show the agent refusing to give financial advice.
5. **Ask an unanswerable question** — show the escalation message and the Power Automate flow to HR.
6. **Close the loop** — show how an HR reply becomes a candidate addition to the next index refresh.

---

## Sample question taxonomy

The agent is scoped around questions employees actually send to HR:

- "What is my medical plan deductible this year?"
- "When does open enrollment close?"
- "Can I add a domestic partner to my health plan?"
- "What is the 401(k) employer match and vesting schedule?"
- "How do I file an HSA reimbursement?"
- "What does the wellbeing fund cover?"
- "What happens to my benefits if I go on FMLA?"
- "How do I add a new dependent after a qualifying life event?"

Out-of-scope questions (clinical advice, financial planning, individual claims disputes) are intentionally refused and redirected.

---

## Why this is a credible recruiter signal

This isn't a generic "I built a chatbot" project. It is a deliberate intersection of:

- **HR operations experience** — 4+ years administering benefits at WACKER Chemical, Rocket Companies, and Wayne County; led open enrollment sessions for 50–300 employees; managed BCBSM, Health Equity, and HSA/FSA platform integrations.
- **Power Platform delivery** — designed and shipped the Benefits Customer Service Tracker (SharePoint + Power Automate) that meaningfully cut processing time at Wayne County.
- **AI enablement on the enterprise stack** — Azure OpenAI, Azure AI Search, Copilot Studio, Power Automate, Python — chosen specifically because they slot into the M365 environments most employers already run.
- **Project management discipline** — explicit milestones, a decision log, an escalation loop, and a governance posture documented before any "look at this cool demo" content.

If you are hiring an **IT Project Manager for AI enablement, HR technology modernization, or workforce-facing automation**, this repository is the artifact version of how I'd scope, govern, and ship that work.

---

## Milestones

| # | Milestone | Status |
|---|---|---|
| 1 | Environment setup (Azure resources, secrets, connectivity) | scaffolded |
| 2 | Document ingestion (chunking, metadata, blob upload) | chunker done; uploader pending |
| 3 | Indexing pipeline (embeddings, AI Search index, semantic config) | client done; index builder pending |
| 4 | Answer generation (grounded prompt, citation, escalation flag) | implemented |
| 5 | Copilot Studio integration + Power Automate escalation flow | pending |
| 6 | Guardrails (out-of-scope detection, advice boundaries, gap logging) | partially in prompt |
| 7 | Portfolio polish (sample IO pairs, Loom walkthrough, diagram, LinkedIn post) | pending |

---

## Suggested demo / showcase assets

These do not yet exist in the repo and are good candidates to add for recruiter visibility:

- `docs/screenshots/copilot-studio-topic.png` — the Copilot Studio topic flow.
- `docs/screenshots/search-index.png` — the Azure AI Search index in the portal, showing fields and semantic config.
- `docs/screenshots/sample-answer.png` — a real Q→A→citation→escalation example.
- `docs/screenshots/power-automate-escalation.png` — the HR escalation flow.
- `docs/demo.md` — a scripted 5-minute walkthrough mirroring the demo flow above.
- A 2–3 minute Loom linked from the top of this README.

---

## Related work

- [azure-doc-agent](https://github.com/Automater89/azure-doc-agent) — document extraction and agent workflow pipeline.
- [Agent Showcase](https://automater89.github.io/Agent-Showcase/) — live portfolio of AI and automation projects.

---

## License

MIT — see [LICENSE](LICENSE).
