"""
Retrieval module — hybrid search with Reciprocal Rank Fusion.

Dense retrieval  : ChromaDB (embedding similarity)
Sparse retrieval : BM25 (keyword matching)
Fusion           : Reciprocal Rank Fusion (RRF)
"""
import chromadb
from rank_bm25 import BM25Okapi
from typing import List, Dict, Optional

from config import CHROMA_PERSIST_DIR, CHROMA_COLLECTION, TOP_K_DENSE, TOP_K_BM25, TOP_K_FINAL


# ── ChromaDB client ───────────────────────────────────────────────────────────

_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)


def get_collection():
    return _client.get_or_create_collection(CHROMA_COLLECTION)


# ── Indexing ──────────────────────────────────────────────────────────────────

def index_chunks(chunks: List[Dict], embeddings: List[List[float]]) -> None:
    """Store chunks and their embeddings in ChromaDB."""
    collection = get_collection()
    collection.add(
        ids=[f"{c['source']}_{c['chunk_index']}" for c in chunks],
        embeddings=embeddings,
        documents=[c["text"] for c in chunks],
        metadatas=[{k: v for k, v in c.items() if k != "text"} for c in chunks],
    )
    print(f"Indexed {len(chunks)} chunks into ChromaDB")


def is_indexed() -> bool:
    """Return True if the collection already contains documents."""
    return get_collection().count() > 0


# ── Dense retrieval ───────────────────────────────────────────────────────────

def dense_retrieve(
    query_embedding: List[float],
    product_area: Optional[str] = None,
    top_k: int = TOP_K_DENSE,
) -> List[Dict]:
    """
    Retrieve top-k chunks by embedding similarity.
    Optionally filter by product_area metadata.
    """
    collection = get_collection()
    where = {"product_area": product_area} if product_area else None

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where,
        include=["documents", "metadatas", "distances"],
    )
    return _format_chroma_results(results)


# ── BM25 retrieval ────────────────────────────────────────────────────────────

def build_bm25_index(chunks: List[Dict]) -> BM25Okapi:
    """Build an in-memory BM25 index from a list of chunks."""
    tokenised = [c["text"].lower().split() for c in chunks]
    return BM25Okapi(tokenised)


def bm25_retrieve(
    query: str,
    chunks: List[Dict],
    bm25_index: BM25Okapi,
    top_k: int = TOP_K_BM25,
) -> List[Dict]:
    """Retrieve top-k chunks by BM25 keyword score."""
    scores = bm25_index.get_scores(query.lower().split())
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    return [
        {"text": chunks[i]["text"], "metadata": {k: v for k, v in chunks[i].items() if k != "text"}, "score": float(scores[i])}
        for i in top_indices
    ]


# ── Reciprocal Rank Fusion ────────────────────────────────────────────────────

def reciprocal_rank_fusion(
    dense_results: List[Dict],
    bm25_results: List[Dict],
    top_k: int = TOP_K_FINAL,
    k: int = 60,
) -> List[Dict]:
    """
    Combine dense and BM25 results using Reciprocal Rank Fusion.
    RRF score = sum(1 / (k + rank)) across retrieval methods.
    k=60 is the standard constant that reduces sensitivity to high-rank outliers.
    """
    scores: Dict[str, float] = {}
    docs: Dict[str, Dict] = {}

    for rank, result in enumerate(dense_results):
        doc_id = _result_id(result)
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
        docs[doc_id] = result

    for rank, result in enumerate(bm25_results):
        doc_id = _result_id(result)
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
        docs[doc_id] = result

    sorted_ids = sorted(scores, key=lambda x: scores[x], reverse=True)[:top_k]
    fused = []
    for doc_id in sorted_ids:
        result = docs[doc_id].copy()
        result["rrf_score"] = round(scores[doc_id], 4)
        fused.append(result)

    return fused


# ── Helpers ───────────────────────────────────────────────────────────────────

def _result_id(result: Dict) -> str:
    meta = result.get("metadata", {})
    return f"{meta.get('source', '')}_{meta.get('chunk_index', '')}"


def _format_chroma_results(chroma_results) -> List[Dict]:
    results = []
    for i, doc in enumerate(chroma_results["documents"][0]):
        results.append({
            "text": doc,
            "metadata": chroma_results["metadatas"][0][i],
            "score": round(1 - chroma_results["distances"][0][i], 4),
        })
    return results
