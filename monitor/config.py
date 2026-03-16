"""
monitor/config.py
Central configuration for the AI Learning Monitor agent.
All paths, identities, remote settings, and analysis thresholds live here.

Every tunable value is overridable via environment variable so that
operators can adjust behaviour without touching code.
See .env.monitor.example for the full list of supported variables.
"""

import os
import socket
import subprocess
from pathlib import Path

# ── Repo root ──────────────────────────────────────────────────────────────
REPO_ROOT = Path(os.environ.get("REPO_ROOT", Path(__file__).parent.parent))

# ── Learner identity ───────────────────────────────────────────────────────
def get_learner_id() -> str:
    """Resolve learner identity from git config, fallback to hostname."""
    try:
        name = subprocess.check_output(
            ["git", "config", "user.name"], text=True
        ).strip()
        email = subprocess.check_output(
            ["git", "config", "user.email"], text=True
        ).strip()
        if name and email:
            safe = name.lower().replace(" ", "_")
            return f"{safe}"
    except Exception:
        pass
    return socket.gethostname()

LEARNER_ID = get_learner_id()

# ── Local log paths ────────────────────────────────────────────────────────
LOGS_DIR = REPO_ROOT / "logs" / LEARNER_ID
LOGS_DIR.mkdir(parents=True, exist_ok=True)

CLAUDE_LOG_FILE    = LOGS_DIR / "claude_events.jsonl"
GEMINI_LOG_FILE    = LOGS_DIR / "gemini_events.jsonl"
GIT_LOG_FILE       = LOGS_DIR / "git_events.jsonl"
FS_LOG_FILE        = LOGS_DIR / "fs_events.jsonl"
SESSION_LOG_FILE   = LOGS_DIR / "sessions.jsonl"
NOTEBOOK_LOG_FILE  = LOGS_DIR / "notebook_events.jsonl"

# ── Reports path ───────────────────────────────────────────────────────────
REPORTS_DIR = REPO_ROOT / "reports" / LEARNER_ID
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Remote sync settings ───────────────────────────────────────────────────
# The branch where all learner logs and reports are pushed centrally.
# Instructors pull from this branch to review progress.
REPORTS_BRANCH = os.environ.get("MONITOR_REPORTS_BRANCH", "monitoring-reports")

# Optional: remote name (default 'origin'). Override in .env.monitor
REMOTE_NAME = os.environ.get("MONITOR_REMOTE", "origin")

# ── File system watch targets ──────────────────────────────────────────────
WATCH_EXTENSIONS = {".py", ".md", ".txt", ".yaml", ".yml", ".json", ".ipynb"}
WATCH_IGNORE_DIRS = {".git", "__pycache__", ".venv", "node_modules", "logs", "reports"}

# ── Planning artifact patterns ─────────────────────────────────────────────
PLANNING_PATTERNS = ["prd", "spec", "plan", "design", "architecture", "readme"]
TEST_PATTERNS     = ["test_", "_test", "tests/", "spec/"]

# ── Event payload truncation lengths ───────────────────────────────────────
# Controls how much text is stored per event to keep JSONL files manageable.
STRING_TRUNCATE_LENGTH        = int(os.environ.get("MONITOR_STRING_TRUNCATE",        "300"))
AGENT_RESPONSE_TRUNCATE_LENGTH = int(os.environ.get("MONITOR_AGENT_RESPONSE_TRUNCATE", "500"))
NOTEBOOK_CELL_TRUNCATE_LENGTH = int(os.environ.get("MONITOR_NOTEBOOK_CELL_TRUNCATE",  "500"))
PROMPT_TEXT_TRUNCATE_LENGTH   = int(os.environ.get("MONITOR_PROMPT_TEXT_TRUNCATE",    "1000"))
TEST_OUTPUT_TRUNCATE_LENGTH   = int(os.environ.get("MONITOR_TEST_OUTPUT_TRUNCATE",    "200"))

# ── Analysis thresholds ────────────────────────────────────────────────────
# Notebook completion: ratio >= COMPLETE → "completed", >= IN_PROGRESS_MIN → "in-progress"
NOTEBOOK_COMPLETION_THRESHOLD = float(os.environ.get("MONITOR_NOTEBOOK_COMPLETE_THRESHOLD", "0.9"))
NOTEBOOK_IN_PROGRESS_MIN      = float(os.environ.get("MONITOR_NOTEBOOK_IN_PROGRESS_MIN",    "0.1"))

# Prompt quality bands: length < SHORT → "short", length >= DETAILED → "detailed"
PROMPT_SHORT_THRESHOLD    = int(os.environ.get("MONITOR_PROMPT_SHORT_THRESHOLD",    "50"))
PROMPT_DETAILED_THRESHOLD = int(os.environ.get("MONITOR_PROMPT_DETAILED_THRESHOLD", "100"))

# ── Filesystem watcher ─────────────────────────────────────────────────────
# Seconds to suppress duplicate events for the same file path.
FS_EVENT_DEBOUNCE_WINDOW = float(os.environ.get("MONITOR_FS_DEBOUNCE_WINDOW", "2.0"))
