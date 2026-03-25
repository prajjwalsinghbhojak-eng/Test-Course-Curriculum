"""
Dataset setup for Project 1 — Customer Support Intelligence Bot.

Downloads the Bitext Customer Support dataset from HuggingFace and prepares:
    data/support_docs/      Markdown support articles (one per intent category)
    data/sample_queries.csv 50 evaluation queries with expected categories

Run automatically by .devcontainer/project1/setup.sh on Codespace creation.
Can also be run manually: python data/setup_data.py
"""
import csv
import random
from pathlib import Path

DATA_DIR  = Path(__file__).parent
DOCS_DIR  = DATA_DIR / "support_docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

DATASET_NAME  = "bitext/Bitext-customer-support-llm-chatbot-training-dataset"
EVAL_QUERIES  = 50
RANDOM_SEED   = 42

# Maps Bitext category names to friendlier product area labels
CATEGORY_MAP = {
    "ACCOUNT":          "Account Management",
    "CANCELLATION_FEE": "Billing",
    "DELIVERY":         "Orders & Delivery",
    "FEEDBACK":         "General",
    "INVOICE":          "Billing",
    "ORDER":            "Orders & Delivery",
    "PAYMENT":          "Payments",
    "REFUND":           "Payments",
    "SUBSCRIPTION":     "Billing",
    "SHIPPING_ADDRESS": "Orders & Delivery",
    "CONTACT":          "General",
    "NEWSLETTER":       "General",
}


def build_support_articles(dataset) -> None:
    """
    Group Q&A pairs by category and write one markdown article per category.
    Each article contains the top 10 representative Q&A pairs as sections.
    """
    from collections import defaultdict
    grouped = defaultdict(list)

    for row in dataset["train"]:
        category = row.get("category", "GENERAL").upper()
        grouped[category].append({
            "question": row["instruction"],
            "answer":   row["response"],
        })

    for category, pairs in grouped.items():
        product_area = CATEGORY_MAP.get(category, "General")
        title        = category.replace("_", " ").title()
        filename     = category.lower() + ".md"

        # Take up to 10 representative pairs
        sample = pairs[:10]

        lines = [
            "---",
            f"title: {title} Support Guide",
            f"product_area: {product_area}",
            "---",
            "",
            f"# {title} Support Guide",
            "",
            f"This article covers common questions about {title.lower()}.",
            "",
        ]

        for i, pair in enumerate(sample, 1):
            lines += [
                f"## Q{i}: {pair['question']}",
                "",
                pair["answer"],
                "",
            ]

        (DOCS_DIR / filename).write_text("\n".join(lines), encoding="utf-8")

    print(f"Created {len(grouped)} support articles in {DOCS_DIR}")


def build_sample_queries(dataset) -> None:
    """
    Select 50 diverse queries from the dataset for evaluation.
    Ensures coverage across multiple categories.
    """
    random.seed(RANDOM_SEED)

    # Collect one query per category first, then fill remaining slots randomly
    by_category = {}
    for row in dataset["train"]:
        cat = row.get("category", "GENERAL").upper()
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(row["instruction"])

    selected = []
    categories = list(by_category.keys())

    # Round-robin across categories until we have EVAL_QUERIES
    i = 0
    while len(selected) < EVAL_QUERIES:
        cat = categories[i % len(categories)]
        pool = by_category[cat]
        if pool:
            selected.append({
                "query":                   pool.pop(0),
                "expected_category":       cat,
                "expected_product_area":   CATEGORY_MAP.get(cat, "General"),
            })
        i += 1

    out_path = DATA_DIR / "sample_queries.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["query", "expected_category", "expected_product_area"])
        writer.writeheader()
        writer.writerows(selected)

    print(f"Saved {len(selected)} evaluation queries to {out_path}")


def main():
    try:
        from datasets import load_dataset
    except ImportError:
        print("ERROR: 'datasets' library not installed. Run: pip install datasets")
        return

    print(f"Downloading dataset: {DATASET_NAME}")
    ds = load_dataset(DATASET_NAME, trust_remote_code=True)

    build_support_articles(ds)
    build_sample_queries(ds)

    print("\nDataset setup complete.")
    print(f"  Support articles : {DOCS_DIR}")
    print(f"  Eval queries     : {DATA_DIR / 'sample_queries.csv'}")


if __name__ == "__main__":
    main()
