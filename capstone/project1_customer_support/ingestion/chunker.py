"""
Text chunking utilities.
Splits documents into smaller chunks for embedding and retrieval.
"""
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_documents(documents: List[Dict]) -> List[Dict]:
    """
    Split a list of documents into chunks. All metadata fields are preserved.

    Returns a list of chunk dicts with keys:
        text, source, title, product_area, chunk_index
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " "],
    )

    chunks = []
    for doc in documents:
        splits = splitter.split_text(doc["text"])
        for i, split in enumerate(splits):
            chunks.append({
                "text": split,
                "source": doc["source"],
                "title": doc["title"],
                "product_area": doc["product_area"],
                "chunk_index": i,
            })

    print(f"Created {len(chunks)} chunks from {len(documents)} documents")
    return chunks
