# Project 1 — Customer Support Intelligence Bot

Build an AI-powered support assistant using RAG, hybrid retrieval, function calling, and a LangGraph agent.

---

## Getting started

Your environment is already set up. Open a terminal and run:

```bash
streamlit run app.py
```

Then open the Streamlit URL shown in the terminal (Codespaces will forward the port automatically).

---

## Using Gemini CLI

Open a new terminal and type `gemini` to start a conversation with Gemini CLI.
Use it to implement the `TODO` sections in each file — one at a time.

**Example first prompt:**
```
I am building a RAG-based customer support bot in Python.
I have a retriever module at retrieval/retriever.py with dense_retrieve() and bm25_retrieve() functions.
I need to implement the direct_answer node in agents/agent.py.
It should embed the query using the Gemini embedding API, run hybrid retrieval,
and call Gemini to generate an answer grounded in the retrieved chunks.
Show me the implementation.
```

---

## Project structure

```
project1_customer_support/
├── app.py                      ← Streamlit UI (shell provided, wire it up)
├── config.py                   ← All constants and paths
├── ingestion/
│   ├── loader.py               ← Load markdown articles from data/support_docs/
│   └── chunker.py              ← Split documents into chunks
├── retrieval/
│   └── retriever.py            ← ChromaDB + BM25 + RRF fusion
├── agents/
│   └── agent.py                ← LangGraph agent (nodes are stubs — implement these)
├── evaluation/
│   └── evaluator.py            ← LLM-as-judge scoring + batch runner
├── prompts/
│   ├── system_prompt.txt
│   ├── direct_answer_prompt.txt
│   ├── classify_query_prompt.txt
│   └── evaluate_prompt.txt
└── data/
    ├── setup_data.py           ← Downloads dataset (already run at setup)
    ├── support_docs/           ← Markdown support articles (auto-generated)
    └── sample_queries.csv      ← 50 evaluation queries (auto-generated)
```

---

## Build phases

| Phase | What to build | Key files |
|-------|--------------|-----------|
| 1 — Ingest & Retrieve | Ingestion pipeline + basic retrieval test | `ingestion/`, `retrieval/retriever.py` |
| 2 — Hybrid Search | Add BM25, wire up RRF fusion | `retrieval/retriever.py` |
| 3 — Agent & Tools | Implement all 4 nodes + 3 tools | `agents/agent.py` |
| 4 — UI + Evaluation | Wire app.py, run eval, fix top failures | `app.py`, `evaluation/evaluator.py` |

---

## Required features checklist

- [ ] Support articles ingested into ChromaDB with metadata
- [ ] Hybrid retrieval (dense + BM25 + RRF) working
- [ ] LangGraph agent routes correctly to all 3 nodes
- [ ] All 3 function calling tools implemented
- [ ] Evaluation pipeline runs and logs results
- [ ] Streamlit UI shows answers with source citations
- [ ] Escalation flow creates a ticket ID and displays it in the UI
