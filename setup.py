#!/usr/bin/env python3
"""
setup.py — Cross-platform setup for AI Learning Monitor.
Works on Windows, macOS, and Linux.

Usage:
  python setup.py          # Windows / any platform
  bash setup.sh            # macOS / Linux shortcut
"""

import os
import shutil
import signal
import stat
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.resolve()


def main():
    print()
    print("══════════════════════════════════════════════")
    print("  AI Learning Monitor — Environment Setup")
    print("══════════════════════════════════════════════")
    print()

    _load_env_monitor()
    _install_deps()
    _install_git_hooks()
    _set_repo_root()
    _start_daemon()
    _validate_hooks_config()
    _check_monitor_token()
    _check_gemini_key()
    _check_git_identity()

    print()
    print("══════════════════════════════════════════════")
    print("  Setup complete. Monitor is active.")
    print()
    print("  Commands:")
    print("    make report   — generate your progress report")
    print("    make sync     — push logs to the reports branch")
    print("    make status   — check daemon status")
    print("    make stop     — stop the background daemon")
    print()
    print("  No make? Run directly:")
    print("    python monitor/report_generator.py")
    print("    python monitor/push_logs.py")
    print("══════════════════════════════════════════════")
    print()


# ── Steps ──────────────────────────────────────────────────────────────────

def _load_env_monitor():
    """Load .env.monitor if present; set vars in os.environ and persist to system."""
    env_file = REPO_ROOT / ".env.monitor"
    if not env_file.exists():
        print("▶ No .env.monitor found — using environment defaults.")
        print("  (Copy .env.monitor.example → .env.monitor and fill in MONITOR_PUSH_TOKEN")
        print("   to enable log sync to the instructor dashboard.)")
        return

    print("▶ Loading .env.monitor...")
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and value:
                os.environ[key] = value

    # On Windows, persist the monitor vars to the user environment registry
    if sys.platform == "win32":
        _persist_env_vars_windows()

    print("  ✓ Configuration loaded")


def _persist_env_vars_windows():
    """Write monitor env vars into the Windows user environment registry."""
    monitor_vars = [
        "MONITOR_PUSH_TOKEN", "MONITOR_REPO_URL",
        "MONITOR_REPORTS_BRANCH", "GEMINI_API_KEY",
    ]
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE
        )
        for var in monitor_vars:
            val = os.environ.get(var, "")
            if val:
                winreg.SetValueEx(key, var, 0, winreg.REG_SZ, val)
        winreg.CloseKey(key)
        print("  ✓ Monitor vars persisted to Windows user environment")
        print("  ℹ Restart your terminal for the changes to take effect.")
    except Exception as e:
        print(f"  ⚠ Could not write to Windows registry: {e}")


def _check_monitor_token():
    print("▶ Checking monitoring token...")
    token = os.environ.get("MONITOR_PUSH_TOKEN", "").strip()
    repo_url = os.environ.get("MONITOR_REPO_URL", "").strip()
    if token and repo_url:
        print("  ✓ MONITOR_PUSH_TOKEN and MONITOR_REPO_URL are set")
        print(f"    Logs will sync to: {repo_url}")
    else:
        print()
        print("  ⚠  Monitoring token not configured.")
        print("     Your progress logs won't reach the instructor dashboard until this is set up.")
        print()
        print("     Steps:")
        print("       1. Copy .env.monitor.example  →  .env.monitor")
        print("       2. Paste the token from your instructor into MONITOR_PUSH_TOKEN")
        print("       3. Re-run: python setup.py")
        print()


def _check_gemini_key():
    print("▶ Checking Gemini CLI setup...")
    if os.environ.get("GEMINI_API_KEY", "").strip():
        print("  ✓ GEMINI_API_KEY is set")
    else:
        print("  ⚠  GEMINI_API_KEY not set. Gemini CLI won't work until you set it.")
        print("     Add it to .env.monitor under GEMINI_API_KEY, then re-run setup.")


def _install_deps():
    print("▶ Installing Python dependencies...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "watchdog", "--quiet"],
        stdout=subprocess.DEVNULL,
    )
    print("  ✓ watchdog installed")


def _install_git_hooks():
    print("▶ Installing git hooks...")
    hooks_src = REPO_ROOT / "git-hooks"
    hooks_dst = REPO_ROOT / ".git" / "hooks"
    hooks_dst.mkdir(parents=True, exist_ok=True)

    for hook in ("pre-commit", "post-commit"):
        src = hooks_src / hook
        dst = hooks_dst / hook
        shutil.copy2(src, dst)
        if sys.platform != "win32":
            dst.chmod(dst.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
        print(f"  ✓ {hook} installed")


def _set_repo_root():
    print("▶ Setting REPO_ROOT environment variable...")
    repo_str = str(REPO_ROOT)

    if sys.platform == "win32":
        _set_repo_root_windows(repo_str)
    else:
        _set_repo_root_unix(repo_str)

    # Export for the current process so the daemon launch below can inherit it
    os.environ["REPO_ROOT"] = repo_str


def _set_repo_root_windows(repo_str: str):
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, "REPO_ROOT", 0, winreg.REG_SZ, repo_str)
        winreg.CloseKey(key)
        print(f"  ✓ REPO_ROOT set in Windows user environment")
        print("  ℹ Restart your terminal for the change to take effect.")
    except Exception as e:
        print(f"  ⚠ Could not write to Windows registry: {e}")
        print(f"  Set it manually in PowerShell:")
        print(f"    [System.Environment]::SetEnvironmentVariable('REPO_ROOT', '{repo_str}', 'User')")


def _set_repo_root_unix(repo_str: str):
    home = Path.home()
    for rc in (home / ".zshrc", home / ".bashrc"):
        if rc.exists():
            if "REPO_ROOT" not in rc.read_text():
                with open(rc, "a") as f:
                    f.write(f'\n# AI Learning Monitor\nexport REPO_ROOT="{repo_str}"\n')
                print(f"  ✓ REPO_ROOT added to {rc}")
            else:
                print(f"  ✓ REPO_ROOT already set in {rc}")
            return
    print("  ⚠ Could not find ~/.zshrc or ~/.bashrc — set REPO_ROOT manually.")


def _start_daemon():
    print("▶ Starting filesystem watcher daemon...")
    logs_dir = REPO_ROOT / "logs"
    logs_dir.mkdir(exist_ok=True)

    pid_file = REPO_ROOT / ".monitor.pid"
    if pid_file.exists():
        try:
            old_pid = int(pid_file.read_text().strip())
            os.kill(old_pid, 0)  # raises if process is gone
            print(f"  ✓ Daemon already running (PID {old_pid})")
            return
        except (OSError, ValueError):
            pid_file.unlink(missing_ok=True)

    daemon_script = str(REPO_ROOT / "monitor" / "daemon.py")
    log_file = str(logs_dir / "daemon.log")
    env = {**os.environ, "REPO_ROOT": str(REPO_ROOT)}

    with open(log_file, "a") as log_out:
        if sys.platform == "win32":
            DETACHED = 0x00000008
            NEW_GROUP = 0x00000200
            proc = subprocess.Popen(
                [sys.executable, daemon_script],
                stdout=log_out, stderr=log_out,
                env=env,
                creationflags=DETACHED | NEW_GROUP,
            )
        else:
            proc = subprocess.Popen(
                [sys.executable, daemon_script],
                stdout=log_out, stderr=log_out,
                env=env,
                start_new_session=True,
            )

    print(f"  ✓ Daemon started (PID {proc.pid})")


def _validate_hooks_config():
    print("▶ Validating Claude Code hooks...")
    hooks_file = REPO_ROOT / ".claude" / "settings.json"
    if hooks_file.exists():
        print("  ✓ .claude/settings.json present")
    else:
        print("  ✗ WARNING: .claude/settings.json not found. Claude Code hooks won't fire.")


def _check_git_identity():
    print("▶ Checking learner identity (git config)...")
    try:
        name = subprocess.check_output(
            ["git", "config", "user.name"], text=True, stderr=subprocess.DEVNULL
        ).strip()
        email = subprocess.check_output(
            ["git", "config", "user.email"], text=True, stderr=subprocess.DEVNULL
        ).strip()
        if name and email:
            print(f"  ✓ Learner: {name} <{email}>")
            return
    except Exception:
        pass
    print()
    print("  ⚠  Git identity not configured. Please set it now:")
    print('     git config --global user.name  "Your Name"')
    print('     git config --global user.email "you@example.com"')
    print()


if __name__ == "__main__":
    main()
