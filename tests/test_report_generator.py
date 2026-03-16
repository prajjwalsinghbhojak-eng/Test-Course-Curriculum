"""
Tests for monitor/report_generator.py
Covers: analyze_ai_usage, analyze_notebook_progress, analyze_prompt_patterns,
generate_insights, render_report, bar(), pct().
"""

import datetime
import pytest
from monitor.report_generator import (
    analyze_ai_usage,
    analyze_notebook_progress,
    analyze_prompt_patterns,
    analyze_git_activity,
    analyze_fs_activity,
    generate_insights,
    render_report,
    bar,
    pct,
    events_in_window,
)


# ── Helpers ────────────────────────────────────────────────────────────────

def ts_now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def pre_tool(tool, category, source="claude"):
    return {"event_type": "PreToolUse", "tool": tool, "category": category, "source": source, "ts": ts_now()}


def nb_event(path, day, ratio, errors=0, error_types=None):
    return {
        "event_type": "notebook_execution",
        "path": path,
        "day": day,
        "notebook_name": path.split("/")[-1],
        "execution_ratio": ratio,
        "cells_with_errors": errors,
        "error_types": error_types or [],
        "ts": ts_now(),
    }


def session_event(prompt_count=3, avg_len=80, prompts=None):
    return {
        "event_type": "session_end",
        "ts": ts_now(),
        "prompts": {
            "prompt_count": prompt_count,
            "avg_prompt_length": avg_len,
            "prompts": prompts or [
                {"text": "x" * avg_len, "length": avg_len, "ts": ts_now()}
                for _ in range(prompt_count)
            ],
        },
    }


# ── bar() and pct() ────────────────────────────────────────────────────────

def test_bar_full():
    result = bar(1.0)
    assert "100%" in result
    assert "░" not in result


def test_bar_empty():
    result = bar(0.0)
    assert "0%" in result
    assert "█" not in result


def test_bar_half():
    result = bar(0.5)
    assert "50%" in result


def test_pct_basic():
    assert pct(3, 10) == "30%"


def test_pct_zero_total():
    assert pct(5, 0) == "0%"


# ── analyze_ai_usage ───────────────────────────────────────────────────────

def test_ai_usage_empty():
    result = analyze_ai_usage([], [])
    assert result["total_tool_calls"] == 0


def test_ai_usage_counts_pre_tool_only():
    records = [
        pre_tool("Bash", "execution"),
        {"event_type": "PostToolUse", "tool": "Bash", "ts": ts_now()},
    ]
    result = analyze_ai_usage(records, [])
    assert result["total_tool_calls"] == 1


def test_ai_usage_by_source():
    claude_records = [pre_tool("Bash", "execution", source="claude")]
    gemini_records = [pre_tool("run_shell_command", "execution", source="gemini")]
    result = analyze_ai_usage(claude_records, gemini_records)
    assert result["by_source"]["claude"] == 1
    assert result["by_source"]["gemini"] == 1
    assert result["total_tool_calls"] == 2


def test_ai_usage_top_tools():
    records = [pre_tool("Bash", "execution")] * 5 + [pre_tool("Read", "exploration")] * 2
    result = analyze_ai_usage(records, [])
    assert result["top_tools"]["Bash"] == 5
    assert result["top_tools"]["Read"] == 2


def test_ai_usage_skips_unknown_tool():
    records = [{"event_type": "PreToolUse", "tool": "", "category": "other", "source": "claude", "ts": ts_now()}]
    result = analyze_ai_usage(records, [])
    assert result["total_tool_calls"] == 0


def test_ai_usage_ratios():
    records = [
        pre_tool("Bash",  "execution"),
        pre_tool("Edit",  "code_edit"),
        pre_tool("Read",  "exploration"),
        pre_tool("TodoWrite", "planning"),
    ]
    result = analyze_ai_usage(records, [])
    assert result["execution_ratio"]   == "25%"
    assert result["code_edit_ratio"]   == "25%"
    assert result["exploration_ratio"] == "25%"
    assert result["planning_ratio"]    == "25%"


# ── analyze_notebook_progress ─────────────────────────────────────────────

def test_notebook_empty_returns_empty():
    result = analyze_notebook_progress([])
    assert result == {}


def test_notebook_no_notebook_events():
    result = analyze_notebook_progress([{"event_type": "PreToolUse", "ts": ts_now()}])
    assert result == {}


def test_notebook_counts():
    records = [
        nb_event("day1/nb1.ipynb", "day1", 1.0),
        nb_event("day1/nb2.ipynb", "day1", 0.5),
        nb_event("day2/nb3.ipynb", "day2", 0.0),
        nb_event("day2/nb4.ipynb", "day2", 0.95, errors=1, error_types=["NameError"]),
    ]
    result = analyze_notebook_progress(records)
    assert result["notebooks_opened"]      == 4
    assert result["notebooks_completed"]   == 2   # ratio >= 0.9
    assert result["notebooks_in_progress"] == 1   # 0.1 <= ratio < 0.9
    assert result["notebooks_with_errors"] == 1


def test_notebook_latest_snapshot_wins():
    """Two events for the same notebook path — latest should win."""
    records = [
        {**nb_event("day1/nb1.ipynb", "day1", 0.0), "ts": "2026-03-12T08:00:00Z"},
        {**nb_event("day1/nb1.ipynb", "day1", 1.0), "ts": "2026-03-12T09:00:00Z"},
    ]
    # Sort by ts to ensure order; analyze_notebook_progress uses last entry per path
    result = analyze_notebook_progress(sorted(records, key=lambda r: r["ts"]))
    assert result["notebooks_opened"]    == 1
    assert result["notebooks_completed"] == 1


def test_notebook_grouped_by_day():
    records = [
        nb_event("day1/nb1.ipynb", "day1", 1.0),
        nb_event("day2/nb2.ipynb", "day2", 0.5),
    ]
    result = analyze_notebook_progress(records)
    assert "day1" in result["by_day"]
    assert "day2" in result["by_day"]


# ── analyze_prompt_patterns ───────────────────────────────────────────────

def test_prompt_patterns_empty():
    result = analyze_prompt_patterns([])
    assert result["total_prompts"] == 0


def test_prompt_patterns_no_transcript_sessions():
    """Sessions without prompts should return minimal dict."""
    records = [{"event_type": "session_end", "ts": ts_now(), "prompts": {}}]
    result = analyze_prompt_patterns(records)
    assert result["total_prompts"] == 0


def test_prompt_patterns_counts():
    records = [
        session_event(
            prompt_count=3,
            prompts=[
                {"text": "hi", "length": 2, "ts": ts_now()},           # short
                {"text": "x" * 80, "length": 80, "ts": ts_now()},      # medium
                {"text": "x" * 150, "length": 150, "ts": ts_now()},    # detailed
            ],
        )
    ]
    result = analyze_prompt_patterns(records)
    assert result["total_prompts"] == 3
    assert result["short_prompts"] == 1
    assert result["detailed_prompts"] == 1
    assert result["max_prompt_length"] == 150


def test_prompt_patterns_multiple_sessions():
    records = [
        session_event(prompt_count=2, prompts=[
            {"text": "a", "length": 1, "ts": ts_now()},
            {"text": "b", "length": 1, "ts": ts_now()},
        ]),
        session_event(prompt_count=1, prompts=[
            {"text": "x" * 200, "length": 200, "ts": ts_now()},
        ]),
    ]
    result = analyze_prompt_patterns(records)
    assert result["total_prompts"] == 3
    assert result["sessions_with_transcripts"] == 2


# ── generate_insights ─────────────────────────────────────────────────────

def _defaults():
    """Minimal dicts that pass all guards without triggering warnings."""
    ai = {
        "total_tool_calls": 10,
        "by_category": {"execution": 2, "exploration": 5, "code_edit": 3, "planning": 0, "research": 0},
        "by_source": {"claude": 10},
        "top_tools": {"Bash": 2, "Read": 5, "Edit": 3},
        "execution_ratio": "20%", "code_edit_ratio": "30%",
        "exploration_ratio": "50%", "planning_ratio": "0%", "research_ratio": "0%",
    }
    git = {"commits_missing_tests": 0, "test_discipline_rate": "100%", "total_commits": 5, "avg_files_per_commit": 2.0}
    fs  = {"planning_docs_created": 1, "files_created": 3, "files_modified": 8,
            "test_files_created": 1, "notebooks_created": 0}
    sessions = {"sessions_this_week": 5, "avg_tool_calls_per_session": 2.0, "total_tool_calls_across_sessions": 10}
    notebooks = {}
    prompts   = {}
    return ai, git, fs, sessions, notebooks, prompts


def test_insights_positive_signals():
    ai, git, fs, sessions, notebooks, prompts = _defaults()
    insights = generate_insights(ai, git, fs, sessions, notebooks, prompts)
    text = " ".join(insights)
    assert "✅" in text


def test_insights_no_planning_docs_flag():
    ai, git, fs, sessions, notebooks, prompts = _defaults()
    fs["planning_docs_created"] = 0
    insights = generate_insights(ai, git, fs, sessions, notebooks, prompts)
    assert any("planning" in i.lower() for i in insights)


def test_insights_high_execution_ratio_flag():
    ai, git, fs, sessions, notebooks, prompts = _defaults()
    ai["by_category"]["execution"] = 8
    ai["total_tool_calls"] = 10
    insights = generate_insights(ai, git, fs, sessions, notebooks, prompts)
    assert any("execution" in i.lower() for i in insights)


def test_insights_low_sessions_flag():
    ai, git, fs, sessions, notebooks, prompts = _defaults()
    sessions["sessions_this_week"] = 1
    insights = generate_insights(ai, git, fs, sessions, notebooks, prompts)
    assert any("session" in i.lower() for i in insights)


def test_insights_notebook_errors_flagged():
    ai, git, fs, sessions, _, prompts = _defaults()
    notebooks = {
        "notebooks_opened": 3, "notebooks_completed": 2, "notebooks_in_progress": 0,
        "notebooks_with_errors": 1, "completion_rate": "67%", "days_active": ["day1"],
        "by_day": {},
    }
    insights = generate_insights(ai, git, fs, sessions, notebooks, prompts)
    assert any("error" in i.lower() for i in insights)


# ── render_report ─────────────────────────────────────────────────────────

def test_render_report_contains_sections():
    ai, git, fs, sessions, notebooks, prompts = _defaults()
    insights = generate_insights(ai, git, fs, sessions, notebooks, prompts)
    report = render_report(ai, git, fs, sessions, notebooks, prompts, insights, days=7)

    assert "AI Coding Assistant Usage" in report
    assert "Git Discipline" in report
    assert "File System Activity" in report
    assert "Insights" in report


def test_render_report_no_tool_calls_omits_ai_section():
    ai, git, fs, sessions, notebooks, prompts = _defaults()
    ai["total_tool_calls"] = 0
    insights = generate_insights(ai, git, fs, sessions, notebooks, prompts)
    report = render_report(ai, git, fs, sessions, notebooks, prompts, insights, days=7)
    assert "AI Coding Assistant Usage" not in report


def test_render_report_notebook_section_shown():
    ai, git, fs, sessions, _, prompts = _defaults()
    notebooks = {
        "notebooks_opened": 2, "notebooks_completed": 1, "notebooks_in_progress": 1,
        "notebooks_with_errors": 0, "completion_rate": "50%", "days_active": ["day1"],
        "by_day": {"day1": [
            {"notebook_name": "intro.ipynb", "execution_ratio": 1.0, "cells_with_errors": 0, "error_types": []}
        ]},
    }
    insights = generate_insights(ai, git, fs, sessions, notebooks, prompts)
    report = render_report(ai, git, fs, sessions, notebooks, prompts, insights, days=7)
    assert "Learning Progress" in report
    assert "intro.ipynb" in report


def test_render_report_prompt_section_shown():
    ai, git, fs, sessions, notebooks, _ = _defaults()
    prompts = {
        "total_prompts": 5,
        "sessions_with_transcripts": 2,
        "avg_prompt_length": 85,
        "max_prompt_length": 200,
        "short_prompts": 1,
        "detailed_prompts": 3,
    }
    insights = generate_insights(ai, git, fs, sessions, notebooks, prompts)
    report = render_report(ai, git, fs, sessions, notebooks, prompts, insights, days=7)
    assert "Prompt Patterns" in report
