"""
Tests for Gemini CLI hook handling in monitor/log_event.py and monitor/log_session.py
Verifies: event name normalisation, tool categorisation, log file routing,
stdout JSON output, and field parsing differences from Claude Code.
"""

import json
import sys
import io
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path


# ── Helpers ────────────────────────────────────────────────────────────────

def run_log_event(stdin_data: dict, source: str = "gemini") -> tuple[list[dict], str]:
    """
    Run monitor/log_event.main() with synthetic stdin and capture:
    - events written to the log file
    - stdout output (must be valid JSON for Gemini)
    """
    import os
    os.environ.setdefault("REPO_ROOT", str(Path(__file__).parent.parent))

    from monitor import log_event  # import once; never reload (breaks patches)

    written = []

    def fake_write(log_file, event_type, payload):
        written.append({"log_file": str(log_file), "event_type": event_type, **payload})

    stdout_capture = io.StringIO()

    with patch.object(log_event, "write_event", side_effect=fake_write), \
         patch("sys.stdin", io.StringIO(json.dumps(stdin_data))), \
         patch("sys.argv", ["log_event.py", "--source", source]), \
         patch("sys.stdout", stdout_capture):
        log_event.main()

    return written, stdout_capture.getvalue()


# ── Event name normalisation ───────────────────────────────────────────────

def test_before_tool_normalised_to_pre_tool_use():
    events, _ = run_log_event({
        "hook_event_name": "BeforeTool",
        "tool_name": "write_file",
        "tool_input": {"file_path": "main.py", "content": "x=1"},
    })
    assert events[0]["event_type"] == "PreToolUse"


def test_after_tool_normalised_to_post_tool_use():
    events, _ = run_log_event({
        "hook_event_name": "AfterTool",
        "tool_name": "run_shell_command",
        "tool_result": {"output": "ok", "is_error": False},
    })
    assert events[0]["event_type"] == "PostToolUse"


def test_claude_pre_tool_use_unchanged():
    events, _ = run_log_event({
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": "ls"},
    }, source="claude")
    assert events[0]["event_type"] == "PreToolUse"


# ── Tool categorisation ────────────────────────────────────────────────────

@pytest.mark.parametrize("tool, expected_category", [
    ("run_shell_command", "execution"),
    ("run_notebook_cell", "execution"),
    ("write_file",        "code_edit"),
    ("edit_file",         "code_edit"),
    ("replace",           "code_edit"),
    ("read_file",         "exploration"),
    ("list_directory",    "exploration"),
    ("search_files",      "exploration"),
    ("web_search",        "research"),
    ("web_fetch",         "research"),
    ("save_memory",       "planning"),
    ("unknown_tool",      "other"),
])
def test_gemini_tool_categories(tool, expected_category):
    events, _ = run_log_event({
        "hook_event_name": "BeforeTool",
        "tool_name": tool,
        "tool_input": {},
    })
    assert events[0]["category"] == expected_category


# ── Log file routing ───────────────────────────────────────────────────────

def test_gemini_writes_to_gemini_log():
    events, _ = run_log_event({
        "hook_event_name": "BeforeTool",
        "tool_name": "write_file",
        "tool_input": {},
    }, source="gemini")
    assert "gemini_events" in events[0]["log_file"]


def test_claude_writes_to_claude_log():
    events, _ = run_log_event({
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {},
    }, source="claude")
    assert "claude_events" in events[0]["log_file"]


# ── Source field in payload ────────────────────────────────────────────────

def test_gemini_source_field():
    events, _ = run_log_event({
        "hook_event_name": "BeforeTool",
        "tool_name": "read_file",
        "tool_input": {"file_path": "app.py"},
    }, source="gemini")
    assert events[0]["source"] == "gemini"


def test_claude_source_field():
    events, _ = run_log_event({
        "hook_event_name": "PreToolUse",
        "tool_name": "Read",
        "tool_input": {"file_path": "app.py"},
    }, source="claude")
    assert events[0]["source"] == "claude"


# ── Gemini AfterTool uses tool_result (not tool_response) ─────────────────

def test_gemini_after_tool_reads_tool_result():
    events, _ = run_log_event({
        "hook_event_name": "AfterTool",
        "tool_name": "run_shell_command",
        "tool_result": {"output": "hello", "is_error": False},
    })
    assert events[0]["success"] is True


def test_gemini_after_tool_detects_error():
    events, _ = run_log_event({
        "hook_event_name": "AfterTool",
        "tool_name": "run_shell_command",
        "tool_result": {"output": "command not found", "is_error": True},
    })
    assert events[0]["success"] is False


def test_claude_post_tool_use_reads_tool_response():
    events, _ = run_log_event({
        "hook_event_name": "PostToolUse",
        "tool_name": "Bash",
        "tool_response": {"content": [{"text": "output"}], "is_error": False},
    }, source="claude")
    assert events[0]["success"] is True


# ── Stdout must be valid JSON (Gemini requirement) ─────────────────────────

def test_stdout_is_valid_json_for_gemini():
    _, stdout = run_log_event({
        "hook_event_name": "BeforeTool",
        "tool_name": "write_file",
        "tool_input": {},
    }, source="gemini")
    parsed = json.loads(stdout.strip())
    assert parsed == {}


def test_stdout_is_valid_json_for_claude():
    _, stdout = run_log_event({
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {},
    }, source="claude")
    parsed = json.loads(stdout.strip())
    assert parsed == {}


# ── AfterAgent captures agent response ────────────────────────────────────

def test_after_agent_logs_response():
    events, _ = run_log_event({
        "hook_event_name": "AfterAgent",
        "agent_response": "Here is the refactored code...",
    })
    assert events[0]["event_type"] == "AgentResponse"
    assert "refactored" in events[0]["agent_response"]


# ── Input truncation ───────────────────────────────────────────────────────

def test_long_input_truncated():
    long_content = "x" * 1000
    events, _ = run_log_event({
        "hook_event_name": "BeforeTool",
        "tool_name": "write_file",
        "tool_input": {"file_path": "big.py", "content": long_content},
    })
    assert len(events[0]["input"]["content"]) == 300
