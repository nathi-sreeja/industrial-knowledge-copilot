# Industrial Knowledge Copilot
### ET AI Hackathon 2026 — Problem Statement #8

An AI-powered platform that makes industrial knowledge instantly queryable.

## Features
- Q&A Copilot — ask questions across all industrial documents with source citations
- Compliance Gap Checker — audit procedures against regulatory checklists automatically

## Tech Stack
- Python, Streamlit, Groq API (llama-3.3-70b-versatile)
- FAISS vector store, sentence-transformers, pdfplumber

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Add PDF documents to `docs/` folder
3. Run ingestion: `python ingest.py`
4. Launch app: `streamlit run app.py`

## Team
GPREC, Kurnool — Sreeja Nathi & [Teammate Name]
