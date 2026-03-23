# Day 8 — Advanced RAG Techniques

## Learning Objectives
- Implement hybrid retrieval combining BM25 keyword search with dense semantic search
- Apply query transformation techniques to improve retrieval quality
- Use re-ranking models to improve precision of retrieved results
- Reduce noise in retrieved context using compression and filtering

## Prerequisites
- Completion of Day 7 (Retrieval Augmented Generation)

## Required Reading
- [Advanced RAG — Pinecone](https://www.pinecone.io/learn/advanced-rag/)
- [HyDE Paper — Precise Zero-Shot Dense Retrieval](https://arxiv.org/abs/2212.10496)

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `01_Hybrid_Retrieval.ipynb` | BM25 + dense retrieval, reciprocal rank fusion | 35 min |
| 2 | `02_Query_Transformation.ipynb` | Query rewriting, HyDE, multi-query retrieval | 30 min |
| 3 | `03_Reranking_Models.ipynb` | Cross-encoder reranking, improving precision | 30 min |
| 4 | `04_Context_Compression_and_Filtering.ipynb` | LLM-based compression, relevant context extraction | 25 min |

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| [Advanced RAG Survey](https://arxiv.org/abs/2312.10997) | Paper | Comprehensive survey of RAG improvements |
| [BM25 Explained](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables) | Blog | BM25 algorithm deep dive |
| [LangChain Advanced Retrieval](https://python.langchain.com/docs/modules/data_connection/retrievers/) | Docs | LangChain retriever options |
