# Setup Guide

## Prerequisites

- Azure subscription with Contributor access
- Python 3.10+
- VS Code with Python extension
- GitHub account

## Azure Resources to Create

| Resource | Tier | Notes |
|---|---|---|
| Azure OpenAI | Standard | Deploy `gpt-4o` and `text-embedding-3-small` |
| Azure AI Search | Basic | Enable semantic search in settings |
| Azure Blob Storage | Standard LRS | Create container named `benefits-docs` |

## Local Environment

```bash
git clone https://github.com/Automater89/benefits-faq-agent.git
cd benefits-faq-agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Fill in .env with your Azure credentials
```

## Verify Connectivity

Run a quick test to confirm each Azure service is reachable:

```bash
python src/utils/config.py
```

This will attempt to load all configured environment variables and report status.

## Cost Notes

- Azure OpenAI: charged per token (embedding + generation)
- Azure AI Search: Basic tier ~$73/month; free tier available for testing (limited index size)
- Azure Blob Storage: minimal cost for document storage
- **Turn off or scale down resources when not actively testing to control costs.**
