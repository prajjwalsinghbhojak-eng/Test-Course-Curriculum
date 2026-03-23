# Day 6 — Vector Databases & Document Processing

## Learning Objectives
- Understand vector database fundamentals: indexing, ANN search, and why they beat brute-force
- Set up and use ChromaDB for persistent vector storage
- Apply metadata filtering to narrow search results
- Build a complete document processing pipeline: load → chunk → embed → store

## Prerequisites
- Completion of Day 5 (Embeddings & Semantic Search)

## Required Reading
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [HNSW Algorithm Explained](https://www.pinecone.io/learn/series/faiss/hnsw/)

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `01_Vector_Database_Fundamentals.ipynb` | What are vector DBs, HNSW indexing, ANN vs exact search, why they matter | 25 min |
| 2 | `02_Getting_Started_with_ChromaDB.ipynb` | Installation, collections, CRUD operations, metadata filtering | 30 min |
| 3 | `03_Document_Chunking_Strategies.ipynb` | Fixed-size, recursive, sentence-aware chunking, overlap strategies | 30 min |
| 4 | `04_Document_Processing_Pipeline.ipynb` | Text loading → chunking → embedding → ChromaDB storage, end-to-end | 35 min |

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| [ChromaDB Docs](https://docs.trychroma.com/) | Docs | Full ChromaDB reference |
| [Vector Database Comparison](https://www.pinecone.io/learn/vector-database/) | Blog | Overview of the vector DB landscape |
| [Chunking Strategies for RAG](https://www.pinecone.io/learn/chunking-strategies/) | Blog | Deep dive into chunking approaches |
