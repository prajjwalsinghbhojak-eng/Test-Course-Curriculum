"""
monitor/log_session.py
Called by Claude Code (Stop) and Gemini CLI (SessionEnd) hooks.
Writes a session summary and triggers a log push to the reports branch.

Usage:
  python3 monitor/log_session.py --source claude   # Claude Code Stop hook
  python3 monitor/log_session.py --source gemini   # Gemini CLI SessionEnd hook
"""

import argparse
import contextlib
import datetime
import io
import json
import sys
import os

sys.path.insert(0, os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(__file__))))

from monitor.config import SESSION_LOG_FILE, CLAUDE_LOG_FILE, GEMINI_LOG_FILE, LEARNER_ID
from monitor.event_writer import write_event
from monitor.push_logs import push_logs_to_remote
from monitor.transcript_reader import read_transcript


def summarize_session(source: str) -> dict:
    """Read today's events for the given source and compute a session summary."""
    log_file = GEMINI_LOG_FILE if source == "gemini" else CLAUDE_LOG_FILE
    today    = datetime.date.today().isoformat()
    summary  = {
        "date":            today,
        "source":          source,
        "total_tool_calls": 0,
        "by_category":     {},
        "tool_breakdown":  {},
        "errors":          0,
    }

    if not log_file.exists():
        return summary

    with open(log_file) as f:
        for line in f:
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue

            if not ev.get("ts", "").startswith(today):
                continue
            if ev.get("event_type") != "PreToolUse":
                continue

            summary["total_tool_calls"] += 1
            cat  = ev.get("category", "other")
            tool = ev.get("tool", "unknown")
            summary["by_category"][cat]     = summary["by_category"].get(cat, 0) + 1
            summary["tool_breakdown"][tool] = summary["tool_breakdown"].get(tool, 0) + 1
            if not ev.get("success", True):
                summary["errors"] += 1

    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="claude",
                        choices=["claude", "gemini"],
                        help="Which AI tool fired this hook")
    args = parser.parse_args()
    source = args.source

    # Read hook context from stdin
    hook_data = {}
    try:
        raw = sys.stdin.read()
        if raw.strip():
            hook_data = json.loads(raw)
    except Exception:
        pass

    session_summary = summarize_session(source)

    # Read transcript to capture what the learner actually typed
    transcript_data = {}
    if source == "claude":
        transcript_path = hook_data.get("transcript_path", "")
        transcript_data = read_transcript(transcript_path)

    write_event(SESSION_LOG_FILE, "session_end", {
        "source":          source,
        "session_id":      hook_data.get("session_id", ""),
        "session_summary": session_summary,
        "prompts":         transcript_data,
    })

    print(
        f"[monitor] {source} session logged for {LEARNER_ID}: "
        f"{session_summary['total_tool_calls']} tool calls today.",
        file=sys.stderr,
    )

    # Push logs — redirect stdout so it doesn't corrupt Gemini's JSON channel
    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            push_logs_to_remote()
        print(buf.getvalue().strip(), file=sys.stderr)
    except Exception as e:
        print(f"[monitor] Warning: could not push logs: {e}", file=sys.stderr)

    # Gemini CLI reads stdout and expects valid JSON.
    # Claude Code ignores stdout, so this is safe for both.
    print("{}", flush=True)


if __name__ == "__main__":
    main()
