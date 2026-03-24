"""
Evaluation pipeline for the Customer Support Intelligence Bot.

Metrics
-------
faithfulness  Is the answer grounded in the retrieved context? (0.0 – 1.0)
relevance     Does the answer address what was actually asked?  (0.0 – 1.0)

Results are appended to evaluation/eval_results.jsonl.
The monitoring app reads this file to generate reports.
"""
import csv
import json
import time
from pathlib import Path
from typing import List, Dict


# ── Single-answer scorer ──────────────────────────────────────────────────────

def evaluate_answer(
    query: str,
    answer: str,
    context_chunks: List[str],
    gemini_client,
) -> Dict:
    """
    Score a single answer using LLM-as-judge.

    Returns:
        {
            "faithfulness": float,   # 0.0 = not grounded, 1.0 = fully grounded
            "relevance":    float,   # 0.0 = off-topic,    1.0 = directly answers query
            "reasoning":    str,     # one-sentence justification from the judge
        }

    TODO: Implement using Gemini as the judge.
    Hint: Prompt Gemini CLI —
        "Write an evaluate_answer function that uses Gemini structured output to
        score faithfulness and relevance for a RAG answer. Load the judge prompt
        from prompts/evaluate_prompt.txt. Return a Pydantic model with
        faithfulness (float), relevance (float), and reasoning (str)."
    """
    return {
        "faithfulness": 0.0,
        "relevance": 0.0,
        "reasoning": "TODO: implement evaluate_answer",
    }


# ── Batch evaluation runner ───────────────────────────────────────────────────

def run_evaluation(
    agent,
    gemini_client,
    questions_path: str | Path,
    log_path: str | Path,
) -> Dict:
    """
    Run evaluation over all questions in the CSV and log each result.

    CSV format (columns): query, expected_answer_theme (optional)

    Returns:
        {
            "avg_faithfulness": float,
            "avg_relevance":    float,
            "n":                int,
        }
    """
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    results = []

    with open(questions_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            query = row["query"]

            # Run the agent
            output = agent.invoke({
                "query":            query,
                "chat_history":     [],
                "product_area":     None,
                "retrieved_chunks": [],
                "tool_calls":       [],
                "answer":           "",
                "sources":          [],
                "ticket_id":        None,
                "route":            None,
            })

            context = [c["text"] for c in output.get("retrieved_chunks", [])]
            scores  = evaluate_answer(query, output["answer"], context, gemini_client)

            record = {
                "timestamp":   time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "query":       query,
                "answer":      output["answer"],
                "route":       output.get("route"),
                "faithfulness": scores["faithfulness"],
                "relevance":    scores["relevance"],
                "reasoning":    scores["reasoning"],
                "num_sources":  len(output.get("sources", [])),
            }
            results.append(record)

            # Append to JSONL — one record per line for easy streaming by the monitoring app
            with open(log_path, "a", encoding="utf-8") as log:
                log.write(json.dumps(record) + "\n")

    if not results:
        return {"avg_faithfulness": 0.0, "avg_relevance": 0.0, "n": 0}

    return {
        "avg_faithfulness": round(sum(r["faithfulness"] for r in results) / len(results), 3),
        "avg_relevance":    round(sum(r["relevance"]    for r in results) / len(results), 3),
        "n":                len(results),
    }
