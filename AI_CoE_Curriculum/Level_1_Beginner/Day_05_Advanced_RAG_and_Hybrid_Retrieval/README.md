# Day 5 — Advanced RAG & Hybrid Retrieval

## Learning Objectives
- Implement hybrid retrieval (BM25 + Dense), query rewriting, multi-query retrieval.
- Understand re-ranking models and context compression techniques.
- Measure quality improvements in hybrid retrieval pipelines.

## Prerequisites
- Completion of Day 4.


## Required Reading
- [Hugging Face Blog: Matryoshka Embeddings](https://huggingface.co/blog/matryoshka)
- [Qdrant: Hybrid Search Concepts](https://qdrant.tech/documentation/concepts/hybrid-queries/)

## Video Lectures
- [Building Production-Ready RAG Applications (YouTube)](https://www.youtube.com/watch?v=1bXyG2Wv3vM)

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `Hybrid_Search_Legal.ipynb` | Matryoshka embeddings, hybrid search, miniCOIL, RRF | 60 min |
| 2 | `Search_reranking_using_embeddings.ipynb` | Function calling + Wikipedia, HyDE, cosine re-ranking | 60 min |

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| [Hybrid Queries & SPLADE](https://qdrant.tech/documentation/concepts/hybrid-queries/) | Docs | Combining dense vectors with sparse representations. |
| [HyDE Paper](https://arxiv.org/abs/2212.10496) | Paper | Deep dive into Hypothetical Document Embeddings for zero-shot retrieval. |

## Notes
- None.