"""
Tests for monitor/transcript_reader.py
Covers: missing file, empty file, string content, list content blocks,
non-user entries filtered, stats computed correctly, text capped at 1000.
"""

import json
import pytest
from pathlib import Path
from monitor.transcript_reader import read_transcript


# ── Helpers ────────────────────────────────────────────────────────────────

def make_entry(text, user_type="external", entry_type="user", ts="2026-03-12T10:00:00Z"):
    return {
        "type": entry_type,
        "userType": user_type,
        "timestamp": ts,
        "message": {"content": text},
    }


def write_transcript(tmp_path, entries):
    path = tmp_path / "transcript.jsonl"
    path.write_text("\n".join(json.dumps(e) for e in entries))
    return str(path)


# ── Edge cases ─────────────────────────────────────────────────────────────

def test_missing_path_returns_empty():
    assert read_transcript("") == {}


def test_nonexistent_file_returns_empty():
    assert read_transcript("/tmp/does_not_exist_xyz.jsonl") == {}


def test_empty_file_returns_empty(tmp_path):
    path = tmp_path / "empty.jsonl"
    path.write_text("")
    assert read_transcript(str(path)) == {}


def test_malformed_json_lines_skipped(tmp_path):
    path = tmp_path / "bad.jsonl"
    path.write_text('not json\n{"type":"user","userType":"external","message":{"content":"hi"},"timestamp":"2026-03-12T00:00:00Z"}\n')
    result = read_transcript(str(path))
    assert result["prompt_count"] == 1


# ── Filtering ──────────────────────────────────────────────────────────────

def test_only_external_user_messages_captured(tmp_path):
    entries = [
        make_entry("learner prompt", user_type="external"),
        make_entry("tool message",   user_type="tool"),
        {"type": "assistant", "message": {"content": "response"}, "timestamp": "2026-03-12T00:00:00Z"},
        {"type": "system",    "message": {"content": "system"}, "timestamp": "2026-03-12T00:00:00Z"},
    ]
    path = write_transcript(tmp_path, entries)
    result = read_transcript(path)
    assert result["prompt_count"] == 1
    assert result["prompts"][0]["text"] == "learner prompt"


def test_empty_text_skipped(tmp_path):
    entries = [
        make_entry(""),           # empty string — should skip
        make_entry("  "),         # whitespace only — should skip
        make_entry("real prompt"),
    ]
    path = write_transcript(tmp_path, entries)
    result = read_transcript(path)
    assert result["prompt_count"] == 1


# ── Content formats ────────────────────────────────────────────────────────

def test_string_content(tmp_path):
    entries = [make_entry("plain string prompt")]
    path = write_transcript(tmp_path, entries)
    result = read_transcript(path)
    assert result["prompts"][0]["text"] == "plain string prompt"


def test_list_content_blocks(tmp_path):
    content = [
        {"type": "text", "text": "Hello"},
        {"type": "image", "data": "..."},   # non-text block — ignored
        {"type": "text", "text": "World"},
    ]
    entry = {
        "type": "user",
        "userType": "external",
        "timestamp": "2026-03-12T00:00:00Z",
        "message": {"content": content},
    }
    path = tmp_path / "t.jsonl"
    path.write_text(json.dumps(entry))
    result = read_transcript(str(path))
    assert result["prompts"][0]["text"] == "Hello World"


# ── Statistics ─────────────────────────────────────────────────────────────

def test_stats_computed_correctly(tmp_path):
    entries = [
        make_entry("hi"),                             # length 2  — short
        make_entry("medium length prompt here"),      # length 26 — short
        make_entry("x" * 120),                        # length 120 — detailed
    ]
    path = write_transcript(tmp_path, entries)
    result = read_transcript(path)

    assert result["prompt_count"] == 3
    assert result["max_prompt_length"] == 120
    assert result["short_prompts"] == 2      # < 50
    assert result["detailed_prompts"] == 1   # >= 100
    assert result["avg_prompt_length"] == round((2 + 26 + 120) / 3)


def test_text_capped_at_1000_chars(tmp_path):
    entries = [make_entry("z" * 2000)]
    path = write_transcript(tmp_path, entries)
    result = read_transcript(path)
    # text stored in log is capped, but length records the original
    assert len(result["prompts"][0]["text"]) == 1000
    assert result["prompts"][0]["length"] == 2000


def test_timestamp_preserved(tmp_path):
    entries = [make_entry("hello", ts="2026-03-12T09:30:00Z")]
    path = write_transcript(tmp_path, entries)
    result = read_transcript(path)
    assert result["prompts"][0]["ts"] == "2026-03-12T09:30:00Z"
