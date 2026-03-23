# Day 5 — Advanced Retrieval Augmented Generation (RAG)

## Learning Objectives
- Expand upon baseline RAG systems to build highly robust retrieval architectures.
- Implement specialized retrieval methods, such as Hybrid Search (Dense Embeddings + Keyword Sparse Vectors).
- Leverage Matryoshka representation learning to balance vector space costs and retrieval accuracy.
- Explore domain-specific applications demanding high-factual retrieval, like Legal domain Q&A.

## Prerequisites
- Completion of Day 4 fundamentals on RAG and Vector DBs.


## Required Reading
- [Hugging Face Blog: Matryoshka Embeddings](https://huggingface.co/blog/matryoshka)
- [Qdrant: Hybrid Search Concepts](https://qdrant.tech/documentation/concepts/hybrid-queries/)

## Video Lectures
- [Building Production-Ready RAG Applications (YouTube)](https://www.youtube.com/watch?v=1bXyG2Wv3vM)

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `Day_05_Advanced_RAG_with_ChromaDB.ipynb` | Implementing advanced RAG pipelines like Parent Document Retrieval and expansion locally via ChromaDB and Gemini | 60 min |

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| [HuggingFace Matryoshka Embeddings](https://huggingface.co/blog/matryoshka) | Blog | Deep dive into MRL embeddings architecture. |
| [Hybrid Qdrant Queries](https://qdrant.tech/documentation/concepts/hybrid-queries/) | Docs | Reranking and creating multi-stage queries in Qdrant. |

## Notes
- Ensure adequate rate limit quotas are available for Gemini API for processing evaluation subsets.
