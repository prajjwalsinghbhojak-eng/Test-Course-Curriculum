# Feature Tracker — AI Learning Monitor

Tracks every feature: what's built, what's in progress, and what's planned.
Update this file when features are completed or priorities change.

---

## ✅ Completed

### Core monitoring infrastructure
- **Filesystem daemon** — watchdog-based background process, debounced, PID-tracked, auto-tags file types (test, notebook, planning artifact, python source, config, docs)
- **Append-only JSONL event writer** — thread-safe, cross-platform (fcntl on Unix, no-op fallback on Windows)
- **Learner identity resolution** — from `git config user.name`, falls back to hostname
- **`setup.sh`** — idempotent Unix/Mac bootstrap: deps, git hooks, daemon, identity check
- **`setup.py`** — cross-platform Python bootstrap for Windows learners (registry REPO_ROOT, DETACHED_PROCESS daemon)
- **`make health`** — 6-point system check across all three monitoring layers

### Claude Code hooks
- **`.claude/settings.json`** — hooks wired for PreToolUse, PostToolUse, Stop, Notification
- **`monitor/log_event.py`** — reads hook data from stdin JSON (confirmed format via debug capture), classifies tools into categories (execution, code_edit, exploration, planning, research, agentic)
- **`monitor/log_session.py`** — session-end summary, triggers remote sync

### Git hooks
- **`git-hooks/pre-commit`** — logs staged files, test file detection, pytest result (non-blocking)
- **`git-hooks/post-commit`** — logs commit hash, message, author, branch, files changed (uses `git diff-tree HEAD`, not `git diff --cached`)

### Notebook execution tracker
- **`monitor/notebook_tracker.py`** — parses `.ipynb` JSON on every save; captures cells executed, execution ratio, sequential vs non-sequential execution, per-cell error details with cell source, markdown notes presence, day/topic inferred from path
- **Daemon integration** — notebook saves trigger both a basic `fs_events` entry and a rich `notebook_events` entry
- **16 tests** covering all cell states, error types, partial execution, path conventions

### Remote sync and reporting
- **`monitor/push_logs.py`** — tempdir strategy (never switches working branch), `MONITOR_PUSH_TOKEN` support for private monitoring repo, `MONITOR_REPO_URL` override
- **`monitor/report_generator.py`** — full rewrite: 📓 Learning Progress (notebook execution by day, ASCII progress bars), 🤖 AI Coding Assistant Usage (unified Claude + Gemini, per-source breakdown), 💬 Prompt Patterns (avg/short/detailed), 📁 FS activity, 🔀 Git discipline, 💡 Insights
- **`monitoring-reports` branch** — logs + reports pushed here, separate from main
- **GitHub Action (`weekly_reports.yml`)** — runs every Monday + manual trigger, generates reports for all learners found in `logs/`, pushes back to `monitoring-reports`

### Gemini CLI hooks
- **`.gemini/settings.json`** — hooks for BeforeTool, AfterTool, AfterAgent, SessionEnd, Notification
- **`monitor/log_event.py`** — `--source gemini` flag; normalises Gemini event names (BeforeTool→PreToolUse); handles `tool_result` vs `tool_response`; prints `{}` to stdout (Gemini JSON requirement); separate category mapping for Gemini tool names
- **`monitor/log_session.py`** — `--source` flag; stdout redirected through contextlib to keep Gemini's JSON channel clean
- **26 tests** in `tests/test_gemini_hooks.py`

### Claude Code transcript reader
- **`monitor/transcript_reader.py`** — parses session transcript JSONL, extracts `type=user, userType=external` entries; returns prompt_count, avg/max length, short/detailed prompt counts, full prompt list for agent analysis
- **`monitor/log_session.py`** integration — reads `transcript_path` from hook stdin, stores prompt stats in `session_end` event under `"prompts"` key
- **10 tests** in `tests/test_transcript_reader.py`

---

## 📋 Planned

### `make health` — Gemini CLI binary check
- **What:** Add `which gemini` check to health output (currently checks `.gemini/settings.json` and `GEMINI_API_KEY` but not the binary itself)
- **Effort:** Trivial

### Setup — Gemini API key guidance
- **What:** `setup.sh` and `setup.py` should print onboarding instructions if `GEMINI_API_KEY` is missing
- **Effort:** Trivial

---

## 🔮 Future (post-cohort-1)

### Separate private monitoring repo
- **What:** Move `monitoring-reports` to a separate private GitHub repo owned by instructors; learners get a write-only fine-grained PAT as `MONITOR_PUSH_TOKEN`
- **Why:** Currently learners can technically fetch and read each other's logs from the `monitoring-reports` branch
- **When:** Before cohort rollout; `MONITOR_PUSH_TOKEN` support is already implemented in `push_logs.py`

### AI-powered report agent
- **What:** An LLM agent that reads all raw JSONL logs and produces qualitative assessments: prompt quality scores, learning progression narrative, coaching recommendations per learner
- **Why:** Raw logs have rich data; current report generator only does counts — an agent can reason about patterns, struggles, and growth
- **Note:** Log format has been kept verbose deliberately to feed this agent

### Proficiency dimension scoring
- **Dimensions:** Problem decomposition, planning before coding, test-first thinking, AI prompt quality, speed of iteration, notebook completion rate
- **Depends on:** AI report agent (above)

### Instructor dashboard
- **What:** HTML page on GitHub Pages from `monitoring-reports` branch: per-learner activity heatmap, cohort tool usage breakdown, learners with no activity flagged
- **When:** After first cohort completes, once reporting patterns are understood

### Multi-learner testing
- **What:** End-to-end test with two different git identities to verify `logs/` namespacing and report isolation
- **When:** Before cohort rollout

---

## ❌ Decided Against

| Feature | Reason |
|---|---|
| Shell history watcher | Adds noise, not signal; interactive prompts not captured anyway |
| Aider (instead of Gemini CLI) | Company uses Google apps; direct Gemini CLI preferred |
| VS Code extension monitoring | High effort, limited additional signal given hooks already capture tool use |
| Local HTTPS proxy | Too invasive; requires certificate install; disproportionate to benefit |
| Browser extension for web AI chats | Fragile (DOM changes), privacy-invasive, out of scope |
