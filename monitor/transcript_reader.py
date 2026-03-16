"""
monitor/transcript_reader.py
Reads a Claude Code session transcript JSONL file and extracts
the learner's prompts. Called from log_session.py at session end.

Transcript entry types:
  user (userType=external) — the learner's actual messages  ← we want these
  assistant                — Claude's responses
  file-history-snapshot    — IDE state snapshots             ← skip
  progress / system        — internal metadata               ← skip
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.environ.get("REPO_ROOT", str(Path(__file__).parent.parent)))

from monitor.config import (
    PROMPT_TEXT_TRUNCATE_LENGTH,
    PROMPT_SHORT_THRESHOLD,
    PROMPT_DETAILED_THRESHOLD,
)


def read_transcript(transcript_path: str) -> dict:
    """
    Parse a Claude Code transcript and return structured prompt data.
    Returns an empty dict if the file is missing, empty, or unreadable.
    """
    if not transcript_path:
        return {}

    path = Path(transcript_path)
    if not path.exists():
        return {}

    prompts = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Only the learner's own messages
                if entry.get("type") != "user" or entry.get("userType") != "external":
                    continue

                content = entry.get("message", {}).get("content", "")

                # Content can be a plain string or a list of content blocks
                if isinstance(content, list):
                    text = " ".join(
                        part.get("text", "")
                        for part in content
                        if isinstance(part, dict) and part.get("type") == "text"
                    ).strip()
                else:
                    text = str(content).strip()

                if not text:
                    continue

                prompts.append({
                    "text":   text[:PROMPT_TEXT_TRUNCATE_LENGTH],
                    "length": len(text),
                    "ts":     entry.get("timestamp", ""),
                })

    except OSError:
        return {}

    if not prompts:
        return {}

    lengths = [p["length"] for p in prompts]
    return {
        "prompt_count":      len(prompts),
        "avg_prompt_length": round(sum(lengths) / len(lengths)),
        "max_prompt_length": max(lengths),
        "short_prompts":     sum(1 for l in lengths if l < PROMPT_SHORT_THRESHOLD),
        "detailed_prompts":  sum(1 for l in lengths if l >= PROMPT_DETAILED_THRESHOLD),
        # Full prompt texts kept for the future analysis agent
        "prompts":           prompts,
    }
