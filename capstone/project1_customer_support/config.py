"""
Central configuration for the Customer Support Intelligence Bot.
All constants, model names, and file paths are defined here.
"""
import os
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent
DATA_DIR   = BASE_DIR / "data"
DOCS_DIR   = DATA_DIR / "support_docs"
PROMPTS_DIR = BASE_DIR / "prompts"

# ── Gemini ────────────────────────────────────────────────────────────────────
GEMINI_API_KEY   = os.environ.get("GEMINI_API_KEY", "")
CHAT_MODEL       = "gemini-2.0-flash"
EMBEDDING_MODEL  = "models/text-embedding-004"

# ── ChromaDB ──────────────────────────────────────────────────────────────────
CHROMA_PERSIST_DIR = str(BASE_DIR / ".chroma")
CHROMA_COLLECTION  = "support_docs"

# ── Retrieval ─────────────────────────────────────────────────────────────────
CHUNK_SIZE      = 512
CHUNK_OVERLAP   = 64
TOP_K_DENSE     = 5
TOP_K_BM25      = 5
TOP_K_FINAL     = 3   # chunks passed to the LLM after fusion

# ── Evaluation ────────────────────────────────────────────────────────────────
EVAL_QUESTIONS_PATH = DATA_DIR / "sample_queries.csv"
EVAL_LOG_PATH       = BASE_DIR / "evaluation" / "eval_results.jsonl"
