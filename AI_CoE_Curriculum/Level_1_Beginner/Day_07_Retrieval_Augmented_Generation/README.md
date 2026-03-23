# Day 7 — Retrieval Augmented Generation (RAG)

## Learning Objectives
- Understand the RAG architecture and why it solves hallucination and knowledge cutoff problems
- Build a complete RAG system from scratch using Gemini + ChromaDB
- Use LangChain to streamline the RAG pipeline
- Compare vanilla LLM answers vs. RAG-grounded answers side by side

## Prerequisites
- Completion of Day 6 (Vector Databases & Document Processing)

## Required Reading
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401)
- [Gemini + LangChain RAG Quickstart](https://python.langchain.com/docs/integrations/llms/google_ai/)

## Video Lectures
- [Retrieval Augmented Generation (RAG) Explained — IBM Technology (YouTube)](https://www.youtube.com/watch?v=T-D1OfcDW1M)

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `01_RAG_Architecture_Overview.ipynb` | Retriever + Generator pattern, when to use RAG, architecture walkthrough | 25 min |
| 2 | `02_Building_a_Basic_RAG_System.ipynb` | End-to-end RAG from scratch: query → retrieve → augment → generate | 40 min |
| 3 | `03_RAG_with_LangChain.ipynb` | LangChain document loaders, retrievers, and RAG chains | 35 min |
| 4 | `04_RAG_vs_Vanilla_LLM.ipynb` | Side-by-side comparison, grounding analysis, when RAG helps | 20 min |

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| [RAG Paper (Lewis et al.)](https://arxiv.org/abs/2005.11401) | Paper | Original RAG research paper |
| [LangChain RAG Docs](https://python.langchain.com/docs/use_cases/question_answering/) | Docs | LangChain Q&A over documents |
| [ChromaDB Docs](https://docs.trychroma.com/) | Docs | Vector database reference |
