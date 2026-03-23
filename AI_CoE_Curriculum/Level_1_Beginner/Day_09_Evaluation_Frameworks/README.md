# Day 9 — Evaluation Frameworks for LLM & RAG

## Learning Objectives
- Build evaluation pipelines for both LLM outputs and RAG systems
- Create golden datasets for systematic testing
- Use LLM-as-judge and RAGAS-style evaluation metrics
- Compare system variants with a reproducible evaluation dashboard

## Prerequisites
- Completion of Day 8 (Advanced RAG Techniques)

## Required Reading
- [RAGAS: Automated Evaluation of RAG Pipelines](https://arxiv.org/abs/2309.15217)
- [LLM-as-a-Judge](https://arxiv.org/abs/2306.05685)

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `01_Why_Evaluation_Matters.ipynb` | Evaluation mindset, offline vs online eval, golden datasets | 20 min |
| 2 | `02_LLM_Output_Evaluation.ipynb` | Faithfulness, relevance, coherence scoring with LLM-as-judge | 30 min |
| 3 | `03_RAG_Retrieval_Metrics.ipynb` | Precision@K, Recall@K, MRR, retrieval quality measurement | 30 min |
| 4 | `04_Building_an_Evaluation_Pipeline.ipynb` | End-to-end eval: dataset creation → metrics → comparison dashboard | 35 min |

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| [RAGAS Documentation](https://docs.ragas.io/) | Docs | Python library for RAG evaluation |
| [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) | Paper | MT-Bench and Chatbot Arena evaluation framework |
| [Evals Cookbook — OpenAI](https://cookbook.openai.com/examples/evaluation/getting_started_with_openai_evals) | Blog | General eval patterns applicable to any LLM |
