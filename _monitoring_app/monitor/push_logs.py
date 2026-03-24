"""
monitor/push_logs.py
Pushes logs to monitoring-reports branch using a temp directory.
Never touches or switches the learner's current working branch.
"""

import subprocess
import sys
import os
import datetime
import tempfile
import shutil
from urllib.parse import urlparse, urlunparse

sys.path.insert(0, os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from monitor.config import (
    REPO_ROOT, REPORTS_BRANCH, REMOTE_NAME,
    LEARNER_ID, LOGS_DIR, REPORTS_DIR,
)


def run(cmd, cwd=None, check=True):
    return subprocess.run(
        cmd, cwd=str(cwd or REPO_ROOT),
        capture_output=True, text=True, check=check,
    )


def branch_exists_on_remote():
    result = run(["git", "ls-remote", "--heads", REMOTE_NAME, REPORTS_BRANCH], check=False)
    return bool(result.stdout.strip())


def _build_remote_url() -> str:
    """
    Resolve the push URL.

    Priority:
      1. MONITOR_REPO_URL + MONITOR_PUSH_TOKEN  → private monitoring repo (production)
      2. MONITOR_PUSH_TOKEN alone               → inject token into origin URL
      3. Neither                                → plain origin URL (testing / Codespaces with ssh)
    """
    token    = os.environ.get("MONITOR_PUSH_TOKEN", "").strip()
    repo_url = os.environ.get("MONITOR_REPO_URL", "").strip()

    base_url = repo_url or run(["git", "remote", "get-url", REMOTE_NAME]).stdout.strip()

    if token and base_url.startswith("https://"):
        parsed   = urlparse(base_url)
        netloc   = f"x-access-token:{token}@{parsed.hostname}"
        if parsed.port:
            netloc += f":{parsed.port}"
        return urlunparse(parsed._replace(netloc=netloc))

    return base_url


def push_logs_to_remote():
    remote_url = _build_remote_url()

    with tempfile.TemporaryDirectory() as tmpdir:

        if branch_exists_on_remote():
            run(["git", "clone", "--branch", REPORTS_BRANCH,
                 "--depth", "1", remote_url, tmpdir], cwd=None)
        else:
            run(["git", "init", tmpdir], cwd=None)
            run(["git", "remote", "add", REMOTE_NAME, remote_url], cwd=tmpdir)
            run(["git", "checkout", "--orphan", REPORTS_BRANCH], cwd=tmpdir)
            run(["git", "commit", "--allow-empty",
                 "-m", "chore: init monitoring-reports branch"], cwd=tmpdir)

        # Copy logs and reports into temp clone
        dest_logs    = os.path.join(tmpdir, "logs", LEARNER_ID)
        dest_reports = os.path.join(tmpdir, "reports", LEARNER_ID)
        os.makedirs(dest_logs, exist_ok=True)
        os.makedirs(dest_reports, exist_ok=True)

        if LOGS_DIR.exists():
            for f in LOGS_DIR.glob("*.jsonl"):
                shutil.copy2(str(f), os.path.join(dest_logs, f.name))

        if REPORTS_DIR.exists():
            for f in REPORTS_DIR.glob("*.md"):
                shutil.copy2(str(f), os.path.join(dest_reports, f.name))

        # Commit and push from temp dir — main branch untouched
        run(["git", "config", "user.name",  LEARNER_ID], cwd=tmpdir)
        run(["git", "config", "user.email", f"{LEARNER_ID}@monitor"], cwd=tmpdir)
        run(["git", "add", "-A"], cwd=tmpdir)

        status = run(["git", "status", "--porcelain"], cwd=tmpdir)
        if not status.stdout.strip():
            print("[monitor] No new log data to push.")
            return

        ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        run(["git", "commit", "-m", f"monitor: {LEARNER_ID} logs @ {ts}"], cwd=tmpdir)
        run(["git", "push", REMOTE_NAME, REPORTS_BRANCH], cwd=tmpdir)
        print(f"[monitor] Logs pushed to {REMOTE_NAME}/{REPORTS_BRANCH}")


if __name__ == "__main__":
    push_logs_to_remote()
