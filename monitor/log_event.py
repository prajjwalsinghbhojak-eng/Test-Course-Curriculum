"""
monitor/log_event.py
Called by Claude Code and Gemini CLI lifecycle hooks.
Receives event data via stdin as JSON. Writes to the correct log file
based on --source flag passed by the hook command in settings.json.

Claude Code events  → claude_events.jsonl
Gemini CLI events   → gemini_events.jsonl

Both use the same schema; the `source` field identifies the tool.
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(__file__))))

from monitor.config import (
    CLAUDE_LOG_FILE, GEMINI_LOG_FILE,
    STRING_TRUNCATE_LENGTH, AGENT_RESPONSE_TRUNCATE_LENGTH,
)
from monitor.event_writer import write_event

# ── Tool → category mappings ───────────────────────────────────────────────

# Claude Code tool names
CLAUDE_CATEGORIES = {
    "Bash":      "execution",
    "Edit":      "code_edit",
    "Write":     "code_edit",
    "Read":      "exploration",
    "Glob":      "exploration",
    "Grep":      "exploration",
    "LS":        "exploration",
    "Task":      "agentic",
    "WebSearch": "research",
    "WebFetch":  "research",
    "TodoWrite": "planning",
    "TodoRead":  "planning",
}

# Gemini CLI tool names
GEMINI_CATEGORIES = {
    "run_shell_command":   "execution",
    "run_notebook_cell":  "execution",
    "write_file":         "code_edit",
    "edit_file":          "code_edit",
    "replace":            "code_edit",
    "create_file":        "code_edit",
    "read_file":          "exploration",
    "list_directory":     "exploration",
    "search_files":       "exploration",
    "glob":               "exploration",
    "web_search":         "research",
    "web_fetch":          "research",
    "browser":            "research",
    "save_memory":        "planning",
    "read_memory":        "planning",
}

# Gemini hook event names → normalised names (matches Claude Code convention)
GEMINI_EVENT_MAP = {
    "BeforeTool":   "PreToolUse",
    "AfterTool":    "PostToolUse",
    "Notification": "Notification",
    "AfterAgent":   "AgentResponse",
}


def classify_tool(tool_name: str, source: str) -> str:
    table = GEMINI_CATEGORIES if source == "gemini" else CLAUDE_CATEGORIES
    return table.get(tool_name, "other")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="claude",
                        choices=["claude", "gemini"],
                        help="Which AI tool fired this hook")
    args = parser.parse_args()
    source = args.source

    # ── Read stdin JSON (Claude Code and Gemini CLI both use this) ─────────
    hook_data = {}
    try:
        raw = sys.stdin.read()
        if raw.strip():
            hook_data = json.loads(raw)
    except Exception:
        pass

    raw_event = hook_data.get("hook_event_name", "unknown")

    # Normalise Gemini event names to match Claude Code convention
    if source == "gemini":
        event_type = GEMINI_EVENT_MAP.get(raw_event, raw_event)
    else:
        event_type = raw_event

    tool_name = hook_data.get("tool_name", "unknown")
    category  = classify_tool(tool_name, source)

    payload = {
        "source":   source,
        "tool":     tool_name,
        "category": category,
    }

    if event_type == "PreToolUse":
        tool_input = hook_data.get("tool_input", {})
        if isinstance(tool_input, dict):
            payload["input"] = {
                k: (str(v)[:STRING_TRUNCATE_LENGTH] if isinstance(v, str) and len(str(v)) > STRING_TRUNCATE_LENGTH else v)
                for k, v in tool_input.items()
            }
        else:
            payload["input"] = str(tool_input)[:STRING_TRUNCATE_LENGTH]

    elif event_type == "PostToolUse":
        # Claude uses tool_response; Gemini uses tool_result
        resp = hook_data.get("tool_response") or hook_data.get("tool_result") or {}
        if isinstance(resp, dict):
            payload["success"] = not resp.get("is_error", False)
            content = resp.get("content", [])
            if isinstance(content, list):
                text = " ".join(
                    c.get("text", "") for c in content if isinstance(c, dict)
                )
            else:
                text = str(content)
            payload["result_summary"] = text[:STRING_TRUNCATE_LENGTH]
        else:
            payload["success"] = True
            payload["result_summary"] = str(resp)[:STRING_TRUNCATE_LENGTH]

    elif event_type == "Notification":
        payload["message"] = hook_data.get("message", "")[:STRING_TRUNCATE_LENGTH]

    elif event_type == "AgentResponse":
        # Gemini AfterAgent — the AI's final response text for this turn
        payload["agent_response"] = hook_data.get("agent_response", "")[:AGENT_RESPONSE_TRUNCATE_LENGTH]

    log_file = GEMINI_LOG_FILE if source == "gemini" else CLAUDE_LOG_FILE
    write_event(log_file, event_type, payload)

    # Gemini CLI requires valid JSON on stdout to confirm the hook succeeded.
    # Claude Code ignores stdout, so this is safe for both.
    print("{}", flush=True)


if __name__ == "__main__":
    main()
