# Benefits FAQ Agent

An AI-powered agent that answers employee benefits questions using Retrieval-Augmented Generation (RAG) over a structured benefits knowledge base.

Built with Azure AI Search, Azure OpenAI, and Microsoft Copilot Studio. Designed as a portfolio project demonstrating HR domain expertise combined with enterprise AI architecture.

[![Status](https://img.shields.io/badge/status-in%20progress-yellow)](https://github.com/Automater89/benefits-faq-agent)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## Problem Statement

Employees at mid-to-large companies ask the same benefits questions repeatedly: deductibles, HSA limits, open enrollment windows, dependent coverage rules, 401k contribution deadlines. HR teams spend significant time answering questions that are already documented — just not easily findable.

This project builds a conversational agent that answers those questions instantly, accurately, and within guardrails — reducing HR workload while improving the employee experience.

---

## Goals

- Demonstrate how domain expertise in benefits administration can be converted into an AI-powered knowledge tool.
- Build a practical RAG pipeline using Azure AI services.
- Show a complete agent experience from document ingestion to conversational response.
- Create a public portfolio artifact that connects HR operations knowledge to AI product thinking.

---

## Planned Solution

The agent follows a RAG (Retrieval-Augmented Generation) pattern:

1. Benefits documents (handbooks, FAQs, plan summaries) are ingested and chunked.
2. Chunks are indexed in Azure AI Search with vector embeddings.
3. Employee asks a question via Copilot Studio or a web interface.
4. The question is embedded and matched against the index.
5. Retrieved context is passed to Azure OpenAI with a system prompt.
6. The agent returns a grounded, human-readable answer with a source reference.

---

## Architecture

```text
[Employee Question]
        |
        v
[Copilot Studio / Chat Interface]
        |
        v
[Azure OpenAI Embedding Model]
        |
        v
[Azure AI Search - Vector Index]
        |
        v
[Chunked Benefits Documents]
        |
        v
[Azure OpenAI GPT-4o - Answer Generation]
        |
        v
[Grounded Response + Source Citation]
        |
        v
[Employee / HR System]
```

For full architecture detail, see [docs/architecture.md](docs/architecture.md).

---

## Tech Stack

| Layer | Tooling |
|---|---|
| Cloud platform | Azure |
| Document storage | Azure Blob Storage |
| Vector search + retrieval | Azure AI Search (with semantic ranking) |
| Embedding model | Azure OpenAI (text-embedding-3-small) |
| LLM / answer generation | Azure OpenAI (GPT-4o) |
| Agent experience | Microsoft Copilot Studio |
| Workflow automation | Power Automate |
| Runtime / scripting | Python 3.10+, VS Code |
| Version control | GitHub |

---

## Repository Structure

```text
benefits-faq-agent/
├── README.md
├── LICENSE
├── docs/
│   ├── architecture.md
│   ├── setup.md
│   ├── rag-design.md
│   └── decisions.md
├── src/
│   ├── ingestion/
│   │   └── chunker.py
│   ├── retrieval/
│   │   └── search_client.py
│   ├── generation/
│   │   └── answer_agent.py
│   └── utils/
│       ├── config.py
│       └── logger.py
├── data/
│   ├── samples/
│   └── outputs/
├── tests/
│   └── test_chunker.py
├── .env.example
├── requirements.txt
└── .gitignore
```

---

## Milestones

### Milestone 1: Environment Setup
- Create Azure resources (Blob Storage, AI Search, OpenAI)
- Configure Python environment
- Store secrets in `.env` (never committed)
- Confirm API connectivity to all services

### Milestone 2: Document Ingestion
- Load sample benefits documents (PDFs, Word docs)
- Chunk documents by section with metadata (source, topic, plan year)
- Upload chunks to Blob Storage

### Milestone 3: Indexing Pipeline
- Generate vector embeddings for each chunk
- Build Azure AI Search index with semantic configuration
- Validate search returns relevant results for test queries

### Milestone 4: Answer Generation
- Construct grounded system prompt with retrieved context
- Call Azure OpenAI GPT-4o for answer generation
- Return answer with source document citation

### Milestone 5: Agent Integration
- Connect retrieval + generation pipeline to Copilot Studio
- Build a conversational topic flow for common benefits Q&A
- Add escalation path: unanswered questions route to HR inbox via Power Automate

### Milestone 6: Guardrails and Safety
- Add out-of-scope detection (agent declines non-benefits questions)
- Add disclaimer for medical/legal advice boundaries
- Log unanswered questions for handbook gap analysis

### Milestone 7: Portfolio Polish
- Add sample input/output pairs
- Record Loom walkthrough demo
- Publish architecture diagram
- Add LinkedIn project summary
- Link to Agent Showcase: https://automater89.github.io/Agent-Showcase/

---

## Use Cases

- "What is my medical plan deductible this year?"
- "When does open enrollment close?"
- "Can I add a domestic partner to my health plan?"
- "What is the 401k employer match?"
- "How do I file an HSA reimbursement?"
- "What does the wellbeing fund cover?"

---

## Domain Expertise Behind This Project

This project is grounded in real HR and benefits operations experience:

- 4+ years administering benefits at WACKER Chemical, Rocket Companies, and Wayne County
- Led open enrollment sessions for 50–300 employees
- Designed and built the Benefits Customer Service Tracker (SharePoint + Power Automate)
- Managed BCBSM, Health Equity, and HSA/FSA platform integrations
- Reduced processing time by 60% through benefits automation at Wayne County

The agent's knowledge structure, question taxonomy, and guardrails reflect what real employees actually ask — not synthetic demos.

---

## Setup

See [docs/setup.md](docs/setup.md) for full instructions.

```bash
git clone https://github.com/Automater89/benefits-faq-agent.git
cd benefits-faq-agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

---

## Success Criteria

- Agent correctly answers 10+ representative benefits questions using only document context
- Unanswerable questions are gracefully declined and escalated
- Repository is understandable to non-technical HR stakeholders and technical recruiters
- Demo clearly shows the HR domain problem being solved — not just the tech

---

## Related Projects

- [azure-doc-agent](https://github.com/Automater89/azure-doc-agent) — Document extraction and agent workflow pipeline
- [Agent Showcase](https://automater89.github.io/Agent-Showcase/) — Live portfolio of AI and automation projects

---

## Status

Current phase: scaffold and planning.

## License

MIT
