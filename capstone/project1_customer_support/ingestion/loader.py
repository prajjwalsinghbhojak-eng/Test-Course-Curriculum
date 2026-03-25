"""
Document loading utilities.
Reads support articles from data/support_docs/ and returns them as dicts.
"""
from pathlib import Path
from typing import List, Dict


def load_support_docs(docs_dir: str | Path) -> List[Dict]:
    """
    Load all markdown support articles from docs_dir.

    Each article is expected to have optional YAML-style frontmatter:
        ---
        title: How to set up webhooks
        product_area: Payments
        ---

    Returns a list of dicts with keys:
        text, source, title, product_area
    """
    docs_dir = Path(docs_dir)
    documents = []

    for file in sorted(docs_dir.glob("*.md")):
        text = file.read_text(encoding="utf-8")
        metadata = _parse_frontmatter(text, file.stem)
        documents.append({
            "text": text,
            "source": file.name,
            "title": metadata.get("title", file.stem.replace("_", " ").title()),
            "product_area": metadata.get("product_area", "General"),
        })

    print(f"Loaded {len(documents)} support articles from {docs_dir}")
    return documents


def _parse_frontmatter(text: str, filename: str) -> Dict:
    """Extract key: value frontmatter from the top of a markdown file."""
    metadata = {}
    lines = text.strip().splitlines()

    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            if line.strip() == "---":
                break
            if ":" in line:
                key, _, value = line.partition(":")
                metadata[key.strip()] = value.strip()

    return metadata
