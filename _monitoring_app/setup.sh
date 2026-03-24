#!/usr/bin/env bash
# setup.sh
# Bootstraps the AI Learning Monitor agent.
# Run once after cloning the repo: bash setup.sh
# Idempotent — safe to re-run.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export REPO_ROOT

echo ""
echo "══════════════════════════════════════════════"
echo "  AI Learning Monitor — Environment Setup"
echo "══════════════════════════════════════════════"
echo ""

# ── 0. Load .env.monitor ───────────────────────────────────────────────────
ENV_FILE="$REPO_ROOT/.env.monitor"
if [ -f "$ENV_FILE" ]; then
    echo "▶ Loading .env.monitor..."
    set -a
    # shellcheck disable=SC1090
    source "$ENV_FILE"
    set +a
    echo "  ✓ Configuration loaded"
else
    echo "▶ No .env.monitor found — using environment defaults."
    echo "  (Copy .env.monitor.example → .env.monitor and fill in MONITOR_PUSH_TOKEN"
    echo "   to enable log sync to the instructor dashboard.)"
fi

# ── 1. Python dependencies ─────────────────────────────────────────────────
echo "▶ Installing Python dependencies..."
pip install watchdog --quiet --break-system-packages 2>/dev/null || \
  pip install watchdog --quiet

# ── 2. Git hooks ───────────────────────────────────────────────────────────
echo "▶ Installing git hooks..."
GIT_HOOKS_DIR="$REPO_ROOT/.git/hooks"
mkdir -p "$GIT_HOOKS_DIR"

for hook in pre-commit post-commit; do
    src="$REPO_ROOT/git-hooks/$hook"
    dst="$GIT_HOOKS_DIR/$hook"
    cp "$src" "$dst"
    chmod +x "$dst"
    echo "  ✓ $hook installed"
done

# ── 3. Set REPO_ROOT in shell profile ─────────────────────────────────────
echo "▶ Setting REPO_ROOT environment variable..."
SHELL_RC=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [ -n "$SHELL_RC" ]; then
    if ! grep -q "REPO_ROOT" "$SHELL_RC"; then
        echo "" >> "$SHELL_RC"
        echo "# AI Learning Monitor" >> "$SHELL_RC"
        echo "export REPO_ROOT=\"$REPO_ROOT\"" >> "$SHELL_RC"
        echo "  ✓ REPO_ROOT added to $SHELL_RC"
    else
        echo "  ✓ REPO_ROOT already set in $SHELL_RC"
    fi
fi

# Also export for current session
export REPO_ROOT="$REPO_ROOT"

# ── 4. Start the filesystem watcher daemon ────────────────────────────────
echo "▶ Starting filesystem watcher daemon..."
mkdir -p "$REPO_ROOT/logs"
PID_FILE="$REPO_ROOT/.monitor.pid"

if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        echo "  ✓ Daemon already running (PID $OLD_PID)"
    else
        rm -f "$PID_FILE"
        REPO_ROOT="$REPO_ROOT" nohup python3 "$REPO_ROOT/monitor/daemon.py" \
            >> "$REPO_ROOT/logs/daemon.log" 2>&1 &
        echo "  ✓ Daemon started (PID $!)"
    fi
else
    REPO_ROOT="$REPO_ROOT" nohup python3 "$REPO_ROOT/monitor/daemon.py" \
        >> "$REPO_ROOT/logs/daemon.log" 2>&1 &
    echo "  ✓ Daemon started (PID $!)"
fi

# ── 5. Validate Claude Code hooks config ─────────────────────────────────
echo "▶ Validating Claude Code hooks..."
HOOKS_FILE="$REPO_ROOT/.claude/settings.json"
if [ -f "$HOOKS_FILE" ]; then
    echo "  ✓ .claude/settings.json present"
else
    echo "  ✗ WARNING: .claude/settings.json not found. Claude Code hooks won't fire."
fi

# ── 6. Persist monitor env vars to shell profile ─────────────────────────
echo "▶ Persisting monitor settings to shell profile..."
if [ -n "$SHELL_RC" ]; then
    VARS_TO_PERSIST=(MONITOR_PUSH_TOKEN MONITOR_REPO_URL MONITOR_REPORTS_BRANCH GEMINI_API_KEY)
    for VAR in "${VARS_TO_PERSIST[@]}"; do
        VAL="${!VAR:-}"
        if [ -n "$VAL" ] && ! grep -q "^export $VAR=" "$SHELL_RC" 2>/dev/null; then
            echo "export $VAR=\"$VAL\"" >> "$SHELL_RC"
            echo "  ✓ $VAR added to $SHELL_RC"
        fi
    done
fi

# ── 7. Check monitoring token ─────────────────────────────────────────────
echo "▶ Checking monitoring token..."
if [ -n "${MONITOR_PUSH_TOKEN:-}" ] && [ -n "${MONITOR_REPO_URL:-}" ]; then
    echo "  ✓ MONITOR_PUSH_TOKEN and MONITOR_REPO_URL are set"
    echo "    Logs will sync to: $MONITOR_REPO_URL"
else
    echo ""
    echo "  ⚠  Monitoring token not configured."
    echo "     Your progress logs won't reach the instructor dashboard until this is set up."
    echo ""
    echo "     Steps:"
    echo "       1. cp .env.monitor.example .env.monitor"
    echo "       2. Open .env.monitor and paste the token from your instructor"
    echo "          into MONITOR_PUSH_TOKEN"
    echo "       3. Re-run: bash _monitoring_app/setup.sh"
    echo ""
fi

# ── 8. Check Gemini CLI API key ───────────────────────────────────────────
echo "▶ Checking Gemini CLI setup..."
if [ -n "${GEMINI_API_KEY:-}" ]; then
    echo "  ✓ GEMINI_API_KEY is set"
else
    echo "  ⚠  GEMINI_API_KEY not set. Gemini CLI won't work until you set it."
    echo "     Add it to .env.monitor under GEMINI_API_KEY, then re-run setup."
fi

# ── 9. Verify learner identity ────────────────────────────────────────────
echo "▶ Checking learner identity (git config)..."
GIT_NAME=$(git config user.name 2>/dev/null || echo "")
GIT_EMAIL=$(git config user.email 2>/dev/null || echo "")

if [ -z "$GIT_NAME" ] || [ -z "$GIT_EMAIL" ]; then
    echo ""
    echo "  ⚠  Git identity not configured. Please set it now:"
    echo "     git config --global user.name  \"Your Name\""
    echo "     git config --global user.email \"you@example.com\""
    echo ""
else
    echo "  ✓ Learner: $GIT_NAME <$GIT_EMAIL>"
fi

# ── Done ───────────────────────────────────────────────────────────────────
echo ""
echo "══════════════════════════════════════════════"
echo "  Setup complete. Monitor is active."
echo ""
echo "  Commands:"
echo "    make report    — generate your progress report"
echo "    make sync      — push logs to the reports branch"
echo "    make status    — check daemon status"
echo "    make stop      — stop the background daemon"
echo "══════════════════════════════════════════════"
echo ""
