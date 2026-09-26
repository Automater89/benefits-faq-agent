# Benefits FAQ Agent

A planned agent that answers employee benefits questions using Retrieval-Augmented Generation (RAG) over a structured benefits knowledge base.

Planned stack: Azure AI Search, Azure OpenAI, and Microsoft Copilot Studio. This is a portfolio project that connects benefits operations knowledge with AI product design. It is not deployed at an employer.

[![Status](https://img.shields.io/badge/status-in%20progress-yellow)](https://github.com/Automater89/benefits-faq-agent)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## Problem Statement

Employees ask the same benefits questions every year: deductibles, HSA limits, open enrollment windows, dependent coverage rules, 401(k) contribution deadlines. HR teams answer many of them by hand.

This project designs an agent that answers those questions from approved plan documents, cites its source, and hands anything it can't answer to a person.

---

## Goals

- Show how benefits operations knowledge can shape an AI knowledge tool.
- Build a practical RAG pipeline using Azure AI services.
- Show the full path from document ingestion to a conversational answer.
- Create a public portfolio example that connects HR operations with AI product thinking.

---

## Planned Solution

The agent follows a RAG pattern:

1. Benefits documents (handbooks, FAQs, plan summaries) are ingested and chunked.
2. Chunks are indexed in Azure AI Search with vector embeddings.
3. An employee asks a question through Copilot Studio or a web interface.
4. The question is embedded and matched against the index.
5. Retrieved context goes to Azure OpenAI with a system prompt.
6. The agent returns an answer grounded in the documents, with a source reference.

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
[Azure OpenAI - Answer Generation]
        |
        v
[Grounded Response + Source Citation]
        |
        v
[Employee, or escalation to HR]
```

For more detail, see [docs/architecture.md](docs/architecture.md).

---

## Planned Tech Stack

| Layer | Tooling |
|---|---|
| Cloud platform | Azure |
| Document storage | Azure Blob Storage |
| Vector search and retrieval | Azure AI Search (with semantic ranking) |
| Embedding model | Azure OpenAI (text-embedding-3-small) |
| Answer generation | Azure OpenAI (GPT-4o) |
| Agent experience | Microsoft Copilot Studio |
| Escalation workflow | Power Automate |
| Runtime and scripting | Python 3.10+, VS Code |
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
- Configure the Python environment
- Store secrets in `.env` (never committed)
- Confirm API connectivity to all services

### Milestone 2: Document Ingestion
- Load sample benefits documents (PDFs, Word docs)
- Chunk documents by section with metadata (source, topic, plan year)
- Upload chunks to Blob Storage

### Milestone 3: Indexing Pipeline
- Generate vector embeddings for each chunk
- Build an Azure AI Search index with semantic configuration
- Check that search returns relevant results for test queries

### Milestone 4: Answer Generation
- Build a grounded system prompt with retrieved context
- Call Azure OpenAI for answer generation
- Return each answer with a source citation

### Milestone 5: Agent Integration
- Connect the retrieval and generation pipeline to Copilot Studio
- Build a conversational topic flow for common benefits questions
- Add an escalation path: unanswered questions route to an HR inbox through Power Automate

### Milestone 6: Guardrails and Safety
- Decline questions outside benefits
- Add a disclaimer for medical and legal advice boundaries
- Log unanswered questions to find gaps in the handbook

### Milestone 7: Portfolio Polish
- Add sample input and output pairs
- Record a short walkthrough demo
- Publish the architecture diagram
- Add a LinkedIn project summary

---

## Sample Questions

- "What is my medical plan deductible this year?"
- "When does open enrollment close?"
- "Can I add a domestic partner to my health plan?"
- "What is the 401(k) employer match?"
- "How do I file an HSA reimbursement?"

All sample documents in this repository are synthetic. No employer plan documents or employee data are used.

---

## Why I Built This

I worked in benefits operations at Wayne County, Rocket, and WACKER. That work included enrollment and eligibility, EDI 834 file processing and reject resolution, HSA and FSA processes, open-enrollment sessions, and employee education. I also contributed to a cross-functional Benefits Customer Service Tracker on SharePoint with Power Automate routing and notifications, supporting service intake and workload visibility.

The question list and guardrails in this project come from the kinds of questions employees asked in that work.

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

- The agent answers 10+ representative benefits questions using only document context
- Questions it can't answer are declined and escalated
- The repository makes sense to HR stakeholders and technical recruiters
- The demo shows the benefits problem being solved, not just the technology

---

## Status

Current phase: scaffold and planning. Nothing in this repository has been deployed.

## License

MIT
