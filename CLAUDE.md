# CLAUDE.md — AI Learning Monitor

> Read before acting. This is the single source of truth for architecture,
> conventions, and decisions. For feature status see docs/FEATURES.md.

---

## What this project is

Background telemetry agent embedded in a repo that learners clone as part of
an AI engineering training program. Monitors three layers silently:

1. **Claude Code hooks** — every AI tool call during capstone
2. **Git hooks** — commit discipline, test presence, test results
3. **Filesystem daemon** — file activity, notebook execution signals

All signals are written as append-only JSONL logs and pushed to a
`monitoring-reports` branch. A GitHub Action generates weekly Markdown
reports per learner for instructor review.

---

## Two-phase learning model

| Phase | Duration | What happens | What we monitor |
|---|---|---|---|
| **Phase 1** | Days 1–12 | Learners work through Jupyter notebooks | Notebook execution (cells run, errors, completion) |
| **Phase 2** | Capstone | Learners build a project using AI coding assistants | Gemini CLI (primary) + Claude Code (exception) tool use, prompts, git discipline |

Learners do **not** use AI coding assistants during Phase 1.

---

## Repo structure

```
ai-learning-path-tracker/
├── .claude/settings.json        # Claude Code hooks config
├── .gemini/settings.json        # Gemini CLI hooks config  ← planned
├── monitor/
│   ├── config.py                # Paths, learner identity, settings
│   ├── event_writer.py          # Thread-safe JSONL writer (cross-platform)
│   ├── log_event.py             # PreToolUse/PostToolUse/Notification handler
│   ├── log_session.py           # Stop hook → session summary → sync trigger
│   ├── daemon.py                # Filesystem watcher (watchdog)
│   ├── notebook_tracker.py      # Parses .ipynb on save → execution signals
│   ├── push_logs.py             # Pushes logs to monitoring-reports via tempdir
│   └── report_generator.py      # Generates per-learner Markdown reports
├── git-hooks/
│   ├── pre-commit               # Logs staged files, test detection, pytest
│   └── post-commit              # Logs hash, message, files changed
├── .github/workflows/
│   └── weekly_reports.yml       # Runs every Monday + manual trigger
├── docs/
│   └── FEATURES.md              # Feature tracker (completed / planned)
├── setup.sh                     # Unix/Mac bootstrap (idempotent)
├── setup.py                     # Windows + universal Python bootstrap
└── Makefile                     # setup / report / sync / status / health / stop
```

---

## Log files per learner

All under `logs/{learner_id}/`:

| File | Written by | Contains |
|---|---|---|
| `claude_events.jsonl` | Claude Code hooks | PreToolUse, PostToolUse, Notification events |
| `gemini_events.jsonl` | Gemini CLI hooks | Same schema, `source: "gemini"` |
| `git_events.jsonl` | Git hooks | pre_commit, commit events |
| `fs_events.jsonl` | Filesystem daemon | file_created, file_modified events |
| `notebook_events.jsonl` | Daemon → notebook_tracker | Notebook execution snapshots |
| `sessions.jsonl` | Stop hook | Session-end summaries |

---

## Hook architecture

### Claude Code (`.claude/settings.json`)
### Gemini CLI (`.gemini/settings.json`) ← planned

Both call the same Python scripts. The `--source` flag distinguishes them:

```
PreToolUse   → python3 monitor/log_event.py --source claude
PostToolUse  → python3 monitor/log_event.py --source claude
Stop         → python3 monitor/log_session.py --source claude
Notification → python3 monitor/log_event.py --source claude
```

Hook data arrives via **stdin as JSON** (not env vars — confirmed via debug
capture). Key stdin fields:
```json
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {"command": "...", "description": "..."},
  "tool_response": {"content": [...], "is_error": false},
  "session_id": "...",
  "transcript_path": "...",
  "cwd": "..."
}
```

### Git hooks (`.git/hooks/`)
Source in `git-hooks/`, copied by setup. Python scripts, `#!/usr/bin/env python3`.
`post-commit` uses `git diff-tree HEAD` (not `git diff --cached` — that's
always empty after a commit).

### Filesystem daemon
`nohup` background process. PID in `.monitor.pid`. Watches repo root
recursively, debounces 2 seconds per path.

For `.ipynb` files: `notebook_tracker.parse_notebook()` runs on every save,
emits a rich `notebook_execution` event to `notebook_events.jsonl`.

---

## Learner identity

Resolved from `git config user.name` → lowercased, spaces → underscores.
Falls back to `socket.gethostname()`. All log paths namespaced under this ID.

---

## Remote sync

`push_logs.py` uses a `tempfile.TemporaryDirectory()` — never touches the
learner's working branch.

Env var overrides:
- `MONITOR_PUSH_TOKEN` — PAT for authenticated push (production: private monitoring repo)
- `MONITOR_REPO_URL` — URL of separate private monitoring repo
- Neither set → pushes to `origin/monitoring-reports` (fine for testing)

---

## Code conventions

- All logs: **append-only JSONL**, one object per line
- Timestamps: **UTC ISO 8601** with trailing `Z`
- Learner IDs: **lowercase_with_underscores**
- File paths in events: **relative to REPO_ROOT**
- Hook scripts: always `sys.exit(0)` — never block git or AI operations
- Cross-platform: no `fcntl` at top level (wrapped in try/except), no `SIGTERM` assumption

---

## Key commands

```bash
export REPO_ROOT=$(pwd)      # required before any monitor script

make setup                   # full bootstrap (idempotent)
make health                  # 6-point system check
make report                  # generate 7-day progress report
make sync                    # push logs to monitoring-reports
make status / stop / restart # daemon control
```

---

## Confirmed decisions (don't re-open without cause)

| Decision | Rationale |
|---|---|
| Hook data via stdin, not env vars | Confirmed via debug capture — env vars were always empty |
| No shell history watcher | Adds noise, not signal for this use case |
| Gemini CLI (not Aider) for capstone | Company uses Google apps; Aider adds abstraction layer |
| Separate log files per AI source | `claude_events.jsonl` vs `gemini_events.jsonl` — same schema, `source` field |
| Defer proficiency scoring | A separate agent will process raw logs into reports later |
| Defer private monitoring repo | Do before cohort rollout; origin branch fine for testing |
