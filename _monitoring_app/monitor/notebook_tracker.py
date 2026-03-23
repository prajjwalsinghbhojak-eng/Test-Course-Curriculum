"""
monitor/notebook_tracker.py
Parses a Jupyter notebook file on every save and extracts execution signals.
Called by the filesystem daemon whenever a .ipynb file is modified or created.

Logs to notebook_events.jsonl — kept separate from fs_events.jsonl so the
future reporting agent has a clean, dedicated feed to reason over.
"""

import json
import os
import re
from pathlib import Path

import sys
sys.path.insert(0, os.environ.get("REPO_ROOT", str(Path(__file__).parent.parent.parent)))

from monitor.config import STRING_TRUNCATE_LENGTH, NOTEBOOK_CELL_TRUNCATE_LENGTH


def parse_notebook(abs_path: str, repo_root: str) -> dict | None:
    """
    Parse a .ipynb file and return structured execution data.
    Returns None if the file cannot be read or parsed.
    """
    try:
        with open(abs_path, encoding="utf-8") as f:
            nb = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None

    cells = nb.get("cells", [])
    code_cells     = [c for c in cells if c.get("cell_type") == "code"]
    markdown_cells = [c for c in cells if c.get("cell_type") == "markdown"]

    # ── Execution counts ───────────────────────────────────────────────────
    executed = [c for c in code_cells if c.get("execution_count") is not None]
    exec_counts = [c["execution_count"] for c in executed]

    # Sequential means 1, 2, 3 ... with no gaps or re-runs
    is_sequential = (
        exec_counts == list(range(1, len(exec_counts) + 1))
    ) if exec_counts else False

    # ── Error analysis ─────────────────────────────────────────────────────
    error_cells   = []
    error_types   = []
    error_details = []

    for cell in code_cells:
        for output in cell.get("outputs", []):
            if output.get("output_type") == "error":
                error_cells.append(cell)
                ename = output.get("ename", "UnknownError")
                evalue = output.get("evalue", "")
                error_types.append(ename)
                error_details.append({
                    "error_type": ename,
                    "message":    evalue[:STRING_TRUNCATE_LENGTH],
                    # Include the cell source so the future agent knows WHAT code failed
                    "cell_source": "".join(cell.get("source", []))[:NOTEBOOK_CELL_TRUNCATE_LENGTH],
                })
                break  # one error entry per cell

    # ── Outputs ────────────────────────────────────────────────────────────
    cells_with_output = [c for c in code_cells if c.get("outputs")]

    # ── Path metadata ──────────────────────────────────────────────────────
    rel_path = str(Path(abs_path).relative_to(repo_root))
    day, topic = _infer_day_topic(rel_path)

    # ── Kernel ─────────────────────────────────────────────────────────────
    kernel = (
        nb.get("metadata", {})
          .get("kernelspec", {})
          .get("display_name", "unknown")
    )

    total_code = len(code_cells)
    total_executed = len(executed)

    return {
        # Identity
        "path":          rel_path,
        "notebook_name": Path(abs_path).stem,
        "day":           day,
        "topic":         topic,
        "kernel":        kernel,

        # Structure
        "cells_total":    len(cells),
        "cells_code":     total_code,
        "cells_markdown": len(markdown_cells),

        # Execution state
        "cells_executed":      total_executed,
        "cells_with_output":   len(cells_with_output),
        "cells_with_errors":   len(error_cells),
        "execution_ratio":     round(total_executed / total_code, 2) if total_code else 0.0,
        "execution_sequential": is_sequential,

        # Error details — kept for the agent to reason over
        "error_types":   list(dict.fromkeys(error_types)),  # deduplicated, order preserved
        "error_details": error_details[:10],                # cap at 10 errors

        # Notes signal — are learners adding their own markdown?
        "has_markdown_notes": len(markdown_cells) > 0,
    }


def _infer_day_topic(rel_path: str) -> tuple[str, str]:
    """
    Infer day label and topic name from the notebook's path.

    Handles common conventions:
      notebooks/day_03/langchain_basics.ipynb  → ("day_03", "langchain_basics")
      day03_langchain.ipynb                    → ("day_03", "langchain")
      week_01/day_3/topic.ipynb                → ("day_03", "topic")
      03_embeddings.ipynb                      → ("day_03", "embeddings")
    """
    parts = Path(rel_path).parts
    stem  = Path(rel_path).stem

    # Search directory components first, then filename
    day = "unknown"
    for part in list(parts[:-1]) + [stem]:
        m = re.search(r"day[_\-]?(\d+)", part.lower())
        if m:
            day = f"day_{int(m.group(1)):02d}"
            break

    # If still unknown, try a bare leading number: "03_embeddings"
    if day == "unknown":
        m = re.match(r"^(\d+)[_\-]", stem)
        if m:
            day = f"day_{int(m.group(1)):02d}"

    # Topic = stem with day prefix stripped, underscores → spaces
    topic = re.sub(r"^(day[_\-]?\d+[_\-]?|\d+[_\-])", "", stem.lower()).strip("_-")
    topic = topic.replace("_", " ").replace("-", " ") or stem

    return day, topic
