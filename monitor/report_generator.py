"""
monitor/report_generator.py
Reads all local JSONL logs and generates a Markdown progress report.

Sections (shown only when data exists):
  📓 Learning Progress     — Phase 1: notebook execution by day
  🤖 AI Assistant Usage    — Phase 2: unified Claude + Gemini tool calls
  💬 Prompt Patterns       — what the learner typed to Claude
  📁 File System Activity  — files created/modified
  🔀 Git Discipline        — commits, test discipline
  💡 Insights              — coaching flags and positive signals

Output: reports/{learner_id}/progress_report_{date}.md
"""

import collections
import datetime
import json
import os
import sys

sys.path.insert(0, os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(__file__))))

from monitor.config import (
    LEARNER_ID,
    CLAUDE_LOG_FILE,
    GEMINI_LOG_FILE,
    GIT_LOG_FILE,
    FS_LOG_FILE,
    SESSION_LOG_FILE,
    NOTEBOOK_LOG_FILE,
    REPORTS_DIR,
    NOTEBOOK_COMPLETION_THRESHOLD,
    NOTEBOOK_IN_PROGRESS_MIN,
    PROMPT_SHORT_THRESHOLD,
    PROMPT_DETAILED_THRESHOLD,
)


# ── Helpers ────────────────────────────────────────────────────────────────

def load_jsonl(path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    with open(path) as f:
        for line in f:
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def events_in_window(records: list[dict], days: int) -> list[dict]:
    cutoff = (
        datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
        - datetime.timedelta(days=days)
    )
    result = []
    for r in records:
        try:
            ts = datetime.datetime.fromisoformat(r["ts"].rstrip("Z"))
            if ts >= cutoff:
                result.append(r)
        except (KeyError, ValueError):
            continue
    return result


def pct(n: int, total: int) -> str:
    if total == 0:
        return "0%"
    return f"{100 * n // total}%"


def bar(ratio: float, width: int = 10) -> str:
    """Simple ASCII progress bar: ████░░░░░░  78%"""
    filled = round(ratio * width)
    return "█" * filled + "░" * (width - filled) + f"  {round(ratio * 100)}%"


# ── Analysis ───────────────────────────────────────────────────────────────

def analyze_ai_usage(claude_records: list[dict], gemini_records: list[dict]) -> dict:
    """Unified tool-call analysis across Claude Code and Gemini CLI."""
    all_pre = [
        r for r in (claude_records + gemini_records)
        if r.get("event_type") == "PreToolUse"
        and r.get("tool") not in ("", None, "unknown")
    ]
    total = len(all_pre)

    by_source   = collections.Counter(r.get("source", "claude") for r in all_pre)
    by_category = collections.Counter(r.get("category", "other") for r in all_pre)
    by_tool     = collections.Counter(r.get("tool", "unknown") for r in all_pre)

    return {
        "total_tool_calls":  total,
        "by_source":         dict(by_source),
        "by_category":       dict(by_category.most_common()),
        "top_tools":         dict(by_tool.most_common(5)),
        "execution_ratio":   pct(by_category.get("execution", 0),  total),
        "code_edit_ratio":   pct(by_category.get("code_edit", 0),  total),
        "exploration_ratio": pct(by_category.get("exploration", 0), total),
        "planning_ratio":    pct(by_category.get("planning", 0),   total),
        "research_ratio":    pct(by_category.get("research", 0),   total),
    }


def analyze_notebook_progress(records: list[dict]) -> dict:
    """
    Phase 1: latest execution snapshot per notebook, grouped by day.
    Uses the most recent event per notebook path so the report reflects
    the current state, not an accumulation of all saves.
    """
    nb_events = [r for r in records if r.get("event_type") == "notebook_execution"]
    if not nb_events:
        return {}

    # Latest snapshot per notebook (later lines overwrite earlier ones)
    by_path: dict[str, dict] = {}
    for r in nb_events:
        path = r.get("path", "")
        if path:
            by_path[path] = r

    notebooks = list(by_path.values())

    completed   = [n for n in notebooks if n.get("execution_ratio", 0) >= NOTEBOOK_COMPLETION_THRESHOLD]
    in_progress = [n for n in notebooks if NOTEBOOK_IN_PROGRESS_MIN <= n.get("execution_ratio", 0) < NOTEBOOK_COMPLETION_THRESHOLD]
    with_errors = [n for n in notebooks if n.get("cells_with_errors", 0) > 0]

    # Group by day for the per-day breakdown table
    by_day: dict[str, list[dict]] = {}
    for nb in notebooks:
        day = nb.get("day", "unknown")
        by_day.setdefault(day, []).append(nb)

    return {
        "notebooks_opened":    len(notebooks),
        "notebooks_completed": len(completed),
        "notebooks_in_progress": len(in_progress),
        "notebooks_with_errors": len(with_errors),
        "completion_rate":     pct(len(completed), len(notebooks)),
        "days_active":         sorted(by_day.keys()),
        "by_day": {
            day: sorted(nbs, key=lambda x: x.get("notebook_name", ""))
            for day, nbs in sorted(by_day.items())
        },
    }


def analyze_git_activity(records: list[dict]) -> dict:
    commits     = [r for r in records if r.get("event_type") == "commit"]
    pre_commits = [r for r in records if r.get("event_type") == "pre_commit"]

    tests_passed  = sum(1 for r in pre_commits if r.get("tests_passed") is True)
    tests_missing = sum(1 for r in pre_commits if not r.get("has_tests"))

    return {
        "total_commits":             len(commits),
        "tests_passed_before_commit": tests_passed,
        "commits_missing_tests":     tests_missing,
        "test_discipline_rate":      pct(tests_passed, max(len(pre_commits), 1)),
        "avg_files_per_commit":      round(
            sum(r.get("files_changed", 0) for r in commits) / max(len(commits), 1), 1
        ),
    }


def analyze_fs_activity(records: list[dict]) -> dict:
    created  = [r for r in records if r.get("event_type") == "file_created"]
    modified = [r for r in records if r.get("event_type") == "file_modified"]

    return {
        "files_created":        len(created),
        "files_modified":       len(modified),
        "planning_docs_created": len([r for r in created if "planning_artifact" in r.get("tags", [])]),
        "test_files_created":   len([r for r in created if "test_file"          in r.get("tags", [])]),
        "notebooks_created":    len([r for r in created if "notebook"           in r.get("tags", [])]),
    }


def analyze_sessions(records: list[dict]) -> dict:
    sessions = [r for r in records if r.get("event_type") == "session_end"]
    total_calls = sum(
        r.get("session_summary", {}).get("total_tool_calls", 0) for r in sessions
    )
    return {
        "sessions_this_week":             len(sessions),
        "total_tool_calls_across_sessions": total_calls,
        "avg_tool_calls_per_session":     round(total_calls / max(len(sessions), 1), 1),
    }


def analyze_prompt_patterns(session_records: list[dict]) -> dict:
    """Aggregate prompt statistics from session transcripts."""
    sessions_with_prompts = [
        r for r in session_records
        if r.get("event_type") == "session_end"
        and r.get("prompts", {}).get("prompt_count", 0) > 0
    ]
    if not sessions_with_prompts:
        return {"total_prompts": 0, "sessions_with_transcripts": 0}

    all_prompts = []
    for r in sessions_with_prompts:
        all_prompts.extend(r.get("prompts", {}).get("prompts", []))

    if not all_prompts:
        return {"total_prompts": 0, "sessions_with_transcripts": len(sessions_with_prompts)}

    lengths = [p["length"] for p in all_prompts]
    return {
        "total_prompts":          len(all_prompts),
        "sessions_with_transcripts": len(sessions_with_prompts),
        "avg_prompt_length":      round(sum(lengths) / len(lengths)),
        "max_prompt_length":      max(lengths),
        "short_prompts":          sum(1 for l in lengths if l < PROMPT_SHORT_THRESHOLD),
        "detailed_prompts":       sum(1 for l in lengths if l >= PROMPT_DETAILED_THRESHOLD),
    }


# ── Insights ───────────────────────────────────────────────────────────────

def generate_insights(
    ai: dict, git: dict, fs: dict, sessions: dict,
    notebooks: dict, prompts: dict,
) -> list[str]:
    insights = []

    # ── Notebook progress ──────────────────────────────────────────────────
    if notebooks:
        opened    = notebooks["notebooks_opened"]
        completed = notebooks["notebooks_completed"]
        errors    = notebooks["notebooks_with_errors"]

        if opened == 0:
            insights.append("⚠️ No notebook activity detected this period.")
        elif completed / max(opened, 1) < 0.5:
            insights.append(
                f"⚠️ Only {completed}/{opened} notebooks fully executed — "
                "learner may be reading without running code."
            )
        else:
            insights.append(
                f"✅ {completed}/{opened} notebooks completed "
                f"({notebooks['completion_rate']}) — good execution discipline."
            )
        if errors > 0:
            insights.append(
                f"🔍 {errors} notebook(s) contain unresolved errors — "
                "review error_details in notebook_events.jsonl for coaching."
            )

    # ── Planning discipline ────────────────────────────────────────────────
    if fs["planning_docs_created"] == 0:
        insights.append(
            "⚠️ **No planning artifacts detected** — encourage writing a PRD or "
            "spec before jumping into code."
        )
    else:
        insights.append(
            f"✅ {fs['planning_docs_created']} planning document(s) created — "
            "good habit of thinking before coding."
        )

    # ── Test discipline ────────────────────────────────────────────────────
    if git["commits_missing_tests"] > 0:
        insights.append(
            f"⚠️ {git['commits_missing_tests']} commit(s) had no test files. "
            "Reinforce TDD practices."
        )
    if git["test_discipline_rate"] not in ("0%", ""):
        insights.append(
            f"✅ Tests passed before commit in {git['test_discipline_rate']} of commits."
        )

    # ── AI usage patterns ─────────────────────────────────────────────────
    total = ai["total_tool_calls"]
    by_cat = ai["by_category"]

    if total > 0:
        exec_ratio = by_cat.get("execution", 0) / total
        explore_ratio = by_cat.get("exploration", 0) / total

        if exec_ratio > 0.5:
            insights.append(
                "🔍 **High execution tool usage** — learner may be running code "
                "rather than understanding it. Consider a pairing session."
            )
        if explore_ratio > 0.4:
            insights.append(
                "✅ Strong exploration pattern (reads, greps) — "
                "learner is navigating and understanding the codebase."
            )
        if by_cat.get("planning", 0) > 0:
            insights.append(
                "✅ Learner is using AI for task planning — structured approach observed."
            )

        sources = ai.get("by_source", {})
        if len(sources) > 1:
            insights.append(
                f"📊 Learner used multiple AI tools this period: "
                + ", ".join(f"{s} ({n} calls)" for s, n in sources.items()) + "."
            )

    # ── Prompt quality ────────────────────────────────────────────────────
    if prompts.get("total_prompts", 0) > 0:
        short_pct = prompts["short_prompts"] / prompts["total_prompts"]
        if short_pct > 0.6:
            insights.append(
                f"⚠️ {round(short_pct*100)}% of prompts are under 50 chars — "
                "learner may not be giving enough context to the AI."
            )
        elif prompts["avg_prompt_length"] >= 100:
            insights.append(
                f"✅ Average prompt length {prompts['avg_prompt_length']} chars — "
                "learner is providing detailed context."
            )

    # ── Session frequency ─────────────────────────────────────────────────
    n = sessions["sessions_this_week"]
    if n == 0:
        insights.append("⚠️ No AI coding assistant sessions detected this week.")
    elif n < 3:
        insights.append(
            f"📅 Only {n} session(s) this week — encourage more consistent practice."
        )
    else:
        insights.append(f"✅ {n} sessions this week — good engagement cadence.")

    return insights


# ── Renderer ───────────────────────────────────────────────────────────────

def render_report(
    ai: dict, git: dict, fs: dict, sessions: dict,
    notebooks: dict, prompts: dict,
    insights: list[str], days: int,
) -> str:
    today = datetime.date.today().isoformat()
    period = f"Last {days} days"
    lines = [
        f"# Learning Progress Report — {LEARNER_ID}",
        f"**Generated:** {today}  |  **Period:** {period}",
        "",
        "---",
        "",
    ]

    # ── Phase 1: Notebook progress ────────────────────────────────────────
    if notebooks:
        lines += [
            "## 📓 Learning Progress (Notebooks)",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Notebooks opened      | {notebooks['notebooks_opened']} |",
            f"| Notebooks completed   | {notebooks['notebooks_completed']} ({notebooks['completion_rate']}) |",
            f"| Notebooks in progress | {notebooks['notebooks_in_progress']} |",
            f"| Notebooks with errors | {notebooks['notebooks_with_errors']} |",
            f"| Days active           | {', '.join(notebooks['days_active']) or '—'} |",
            "",
        ]

        for day, nbs in notebooks["by_day"].items():
            lines.append(f"**{day}**")
            lines.append("")
            lines.append("| Notebook | Progress | Errors |")
            lines.append("|----------|----------|--------|")
            for nb in nbs:
                ratio  = nb.get("execution_ratio", 0)
                errs   = nb.get("cells_with_errors", 0)
                etypes = ", ".join(nb.get("error_types", [])) or "—"
                lines.append(
                    f"| {nb.get('notebook_name')} | {bar(ratio)} | "
                    f"{'⚠️ ' + etypes if errs else '✅ none'} |"
                )
            lines.append("")

        lines += ["---", ""]

    # ── Phase 2: AI assistant usage ───────────────────────────────────────
    if ai["total_tool_calls"] > 0:
        lines += [
            "## 🤖 AI Coding Assistant Usage",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total tool calls      | {ai['total_tool_calls']} |",
            f"| Avg calls/session     | {sessions['avg_tool_calls_per_session']} |",
        ]

        # Per-source breakdown if both tools used
        for source, count in sorted(ai.get("by_source", {}).items()):
            lines.append(f"| ↳ {source.capitalize()} calls | {count} |")

        lines += [
            f"| Execution (run code)  | {ai['execution_ratio']} |",
            f"| Code editing          | {ai['code_edit_ratio']} |",
            f"| Exploration (read/search) | {ai['exploration_ratio']} |",
            f"| Planning (todo)       | {ai['planning_ratio']} |",
            f"| Research (web)        | {ai['research_ratio']} |",
            "",
            "**Top tools used:**",
        ]
        for tool, count in ai["top_tools"].items():
            lines.append(f"- `{tool}`: {count} calls")

        lines += ["", "---", ""]

    # ── Prompt patterns ───────────────────────────────────────────────────
    if prompts.get("total_prompts", 0) > 0:
        lines += [
            "## 💬 Prompt Patterns",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total prompts         | {prompts['total_prompts']} |",
            f"| Sessions with data    | {prompts['sessions_with_transcripts']} |",
            f"| Avg prompt length     | {prompts['avg_prompt_length']} chars |",
            f"| Max prompt length     | {prompts['max_prompt_length']} chars |",
            f"| Short prompts (<50)   | {prompts['short_prompts']} |",
            f"| Detailed prompts (≥100) | {prompts['detailed_prompts']} |",
            "",
            "---",
            "",
        ]

    # ── File system activity ──────────────────────────────────────────────
    lines += [
        "## 📁 File System Activity",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Files created         | {fs['files_created']} |",
        f"| Files modified        | {fs['files_modified']} |",
        f"| Planning docs created | {fs['planning_docs_created']} |",
        f"| Test files created    | {fs['test_files_created']} |",
        f"| Notebooks created     | {fs['notebooks_created']} |",
        "",
        "---",
        "",
        "## 🔀 Git Discipline",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total commits         | {git['total_commits']} |",
        f"| Avg files/commit      | {git['avg_files_per_commit']} |",
        f"| Commits with tests    | {git['test_discipline_rate']} |",
        f"| Commits missing tests | {git['commits_missing_tests']} |",
        "",
        "---",
        "",
        "## 💡 Insights & Recommended Next Steps",
        "",
    ]
    for insight in insights:
        lines.append(f"- {insight}")

    lines += [
        "",
        "---",
        "",
        "_Report auto-generated by the AI Learning Monitor._",
    ]

    return "\n".join(lines)


# ── Entry point ────────────────────────────────────────────────────────────

def generate(days: int = 7) -> str:
    claude_events   = events_in_window(load_jsonl(CLAUDE_LOG_FILE),   days)
    gemini_events   = events_in_window(load_jsonl(GEMINI_LOG_FILE),   days)
    git_events      = events_in_window(load_jsonl(GIT_LOG_FILE),      days)
    fs_events       = events_in_window(load_jsonl(FS_LOG_FILE),       days)
    session_events  = events_in_window(load_jsonl(SESSION_LOG_FILE),  days)
    notebook_events = events_in_window(load_jsonl(NOTEBOOK_LOG_FILE), days)

    ai        = analyze_ai_usage(claude_events, gemini_events)
    git       = analyze_git_activity(git_events)
    fs        = analyze_fs_activity(fs_events)
    sessions  = analyze_sessions(session_events)
    notebooks = analyze_notebook_progress(notebook_events)
    prompts   = analyze_prompt_patterns(session_events)
    insights  = generate_insights(ai, git, fs, sessions, notebooks, prompts)

    report = render_report(ai, git, fs, sessions, notebooks, prompts, insights, days)

    today    = datetime.date.today().isoformat()
    out_path = REPORTS_DIR / f"progress_report_{today}.md"
    out_path.write_text(report)
    print(f"[monitor] Report written to {out_path}", file=sys.stderr)
    return report


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()
    print(generate(days=args.days))
