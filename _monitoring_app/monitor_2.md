# AI Learning Monitor — Boilerplate Repo

> A self-contained, background monitoring agent that tracks learner progress,
> AI tool usage, and development discipline — embedded directly in the dev environment.

---

## How it works

When a learner clones this repo and runs setup, three monitoring layers
activate silently in the background:

| Layer | What it captures |
|---|---|
| **Claude Code hooks** | Every tool call (Bash, Edit, Read, WebSearch…), category, session prompts, session summary |
| **Gemini CLI hooks** | Same as Claude Code — tool calls, categories, session summary |
| **Git hooks** | Every commit: files changed, test presence, test pass/fail |
| **Filesystem daemon** | File creation/modification: planning docs, test files, notebooks, code |

All events are written as append-only JSONL logs in `logs/{learner_id}/`.
At session end, logs are automatically pushed to the `monitoring-reports` branch
of the shared repo, where instructors can review them.

---

## Learner setup (one-time, after cloning)

### Step 1 — Configure your token

Your instructor will provide a `MONITOR_PUSH_TOKEN`. This is how your progress
logs reach the instructor dashboard. Without it, everything else still works —
logs just won't be visible to your instructor.

```bash
# Copy the example config and fill in your token
cp .env.monitor.example .env.monitor
# Open .env.monitor in any editor and paste your token into MONITOR_PUSH_TOKEN
# Also add your GEMINI_API_KEY if you have one
```

### Step 2 — Set your git identity

```bash
git config --global user.name  "Your Name"
git config --global user.email "you@company.com"
```

### Step 3 — Run setup

**Linux / Mac / GitHub Codespaces:**
```bash
bash _monitoring_app/setup.sh
```

**Windows (PowerShell or Git Bash):**
```bash
python _monitoring_app/setup.py
```

Setup installs dependencies, configures git hooks, starts the background daemon,
loads your `.env.monitor`, and tells you if anything is missing.

### Step 4 — Verify

```bash
make -f _monitoring_app/Makefile health    # All checks should show ✓
```

> **Codespaces users:** If your instructor has set org-level secrets, steps 1–2
> above may already be pre-configured. Run `make -f _monitoring_app/Makefile health` first to check.

---

## Learner commands

```bash
make -f _monitoring_app/Makefile health       # Full diagnostic: daemon, hooks, identity, dependencies
make -f _monitoring_app/Makefile report       # Generate your personal progress report (last 7 days)
make -f _monitoring_app/Makefile report-30    # Generate a 30-day report
make -f _monitoring_app/Makefile sync         # Manually push logs to the team reports branch
make -f _monitoring_app/Makefile status       # Check whether the daemon is running
make -f _monitoring_app/Makefile stop         # Stop the daemon
make restart      # Restart the daemon
```

---

## What gets monitored

### AI coding assistant usage (Claude Code + Gemini CLI)

Every tool call is logged with:
- Tool name and category (`execution`, `code_edit`, `exploration`, `planning`, `research`)
- Session summary at end of session (total calls, breakdown by category)
- Prompts typed to Claude (captured from session transcript)

### Jupyter notebook activity (Phase 1 — learning path)

Every time a `.ipynb` file is saved:
- Which cells have been executed and in what order
- Execution ratio (cells run / total code cells)
- Errors encountered (type + message + cell source)
- Whether markdown notes are present

### Git discipline

On every `git commit`:
- Files staged and changed
- Whether test files are present
- Whether tests pass before committing
- Commit message, branch, and author

### Filesystem activity

Continuously (background daemon):
- Planning artifacts created (`prd`, `spec`, `plan`, `design`, `architecture`)
- Test files created
- Python source and notebook activity

---

## Configuration

All behaviour is tunable via environment variables. Copy `.env.monitor.example`
to `.env.monitor` and adjust values as needed — no code changes required.

```bash
cp .env.monitor.example .env.monitor
# Edit .env.monitor to set MONITOR_PUSH_TOKEN, thresholds, etc.
source .env.monitor
```

Key variables:

| Variable | Default | Purpose |
|---|---|---|
| `MONITOR_REPORTS_BRANCH` | `monitoring-reports` | Branch where logs are pushed |
| `MONITOR_PUSH_TOKEN` | _(empty)_ | GitHub PAT for private monitoring repo |
| `MONITOR_NOTEBOOK_COMPLETE_THRESHOLD` | `0.9` | Ratio to mark notebook as completed |
| `MONITOR_PROMPT_SHORT_THRESHOLD` | `50` | Char count below which a prompt is "short" |
| `MONITOR_FS_DEBOUNCE_WINDOW` | `2.0` | Seconds to suppress duplicate file events |

See `.env.monitor.example` for the full list.

---

## Instructor view

All learner logs are pushed to the `monitoring-reports` branch:

```
monitoring-reports/
  logs/
    alice_smith/
      claude_events.jsonl
      gemini_events.jsonl
      git_events.jsonl
      fs_events.jsonl
      sessions.jsonl
      notebook_events.jsonl
    bob_jones/
      ...
  reports/
    alice_smith/
      progress_report_2025-01-27.md
    bob_jones/
      ...
```

A GitHub Action runs every Monday and generates fresh Markdown progress reports
for all learners automatically.

To review manually:
```bash
git fetch origin monitoring-reports
git checkout monitoring-reports
ls reports/
git checkout main
```

---

## Report format

Each learner report covers:

| Section | Contents |
|---|---|
| 📓 Learning Progress | Notebook execution per day, completion rate, errors |
| 🤖 AI Assistant Usage | Tool calls by category, per-source (Claude vs Gemini), top tools |
| 💬 Prompt Patterns | Prompt count, average length, short vs detailed breakdown |
| 📁 File System Activity | Files created/modified, planning docs, test files |
| 🔀 Git Discipline | Commit count, avg files/commit, test discipline rate |
| 💡 Insights | Automated ✅ / ⚠️ flags and recommended next steps |

---

## Architecture

```
.claude/settings.json          ← Claude Code lifecycle hooks
.gemini/settings.json          ← Gemini CLI lifecycle hooks
monitor/
  config.py                    ← All paths, thresholds, and settings (env-configurable)
  event_writer.py              ← Thread-safe JSONL writer (cross-platform)
  log_event.py                 ← PreToolUse / PostToolUse / Notification handler
  log_session.py               ← Session-end handler + sync trigger
  notebook_tracker.py          ← Jupyter notebook execution parser
  transcript_reader.py         ← Claude Code session transcript parser
  daemon.py                    ← Filesystem watcher (background)
  push_logs.py                 ← Pushes logs to monitoring-reports branch
  report_generator.py          ← Generates Markdown progress reports
git-hooks/
  pre-commit                   ← Test detection + git event logging
  post-commit                  ← Commit metadata logging
.github/workflows/
  weekly_reports.yml           ← Auto-generates all learner reports every Monday
setup.sh                       ← One-time bootstrap (Linux/Mac/Codespaces)
setup.py                       ← One-time bootstrap (Windows, cross-platform)
requirements.txt               ← Python dependencies
.env.monitor.example           ← Template for all configurable settings
Makefile                       ← Convenience commands
```

---

## Troubleshooting

**Daemon not running after setup**
```bash
make -f _monitoring_app/Makefile status      # check PID file
make restart     # stop + start
```

**Logs not appearing in `logs/{name}/`**
```bash
# Confirm REPO_ROOT is set
echo $REPO_ROOT

# Re-export if missing
export REPO_ROOT=$(pwd)
```

**Claude Code hooks not firing**
```bash
# Verify settings file is present
cat .claude/settings.json

# Check the hook format — hooks receive data via stdin, not env vars
```

**Git hooks not logging**
```bash
# Verify hooks are executable
ls -la .git/hooks/pre-commit .git/hooks/post-commit

# Re-run setup if missing
bash _monitoring_app/setup.sh
```

**Remote push failing**
```bash
# Test connectivity
git ls-remote origin

# For private monitoring repo, set the token
export MONITOR_PUSH_TOKEN=your-pat-here
make -f _monitoring_app/Makefile sync
```

---

## Privacy note

Logs capture tool types and file paths — **not file contents or code**.
Learners can view their own logs at any time in `logs/{their_name}/`.
Session prompt text from Claude Code transcripts is captured for coaching analysis.
