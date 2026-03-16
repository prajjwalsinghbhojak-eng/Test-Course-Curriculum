# Makefile — AI Learning Monitor convenience commands

REPO_ROOT := $(shell pwd)
export REPO_ROOT

.PHONY: setup report sync status stop restart health

## Bootstrap the monitoring agent (run once after cloning)
setup:
	@bash setup.sh

## Generate a progress report for the current learner
report:
	@REPO_ROOT=$(REPO_ROOT) python3 monitor/report_generator.py

## Generate a 30-day report
report-30:
	@REPO_ROOT=$(REPO_ROOT) python3 monitor/report_generator.py --days 30

## Push logs and reports to the remote monitoring-reports branch
sync:
	@REPO_ROOT=$(REPO_ROOT) python3 monitor/push_logs.py

## Check whether the filesystem daemon is running
status:
	@if [ -f .monitor.pid ]; then \
	  PID=$$(cat .monitor.pid); \
	  if kill -0 $$PID 2>/dev/null; then \
	    echo "✓ Monitor daemon is running (PID $$PID)"; \
	  else \
	    echo "✗ Daemon PID file exists but process is dead. Run 'make setup' to restart."; \
	  fi \
	else \
	  echo "✗ Monitor daemon is not running. Run 'make setup' to start."; \
	fi

## Stop the filesystem daemon
stop:
	@if [ -f .monitor.pid ]; then \
	  kill $$(cat .monitor.pid) 2>/dev/null && echo "✓ Daemon stopped." || echo "Daemon was not running."; \
	  rm -f .monitor.pid; \
	else \
	  echo "No daemon PID file found."; \
	fi

## Restart the daemon
restart: stop setup

## Verify all three monitoring layers are active
health:
	@echo "── AI Learning Monitor Health Check ──"
	@python3 -c "import os; print('✓ REPO_ROOT:', os.environ.get('REPO_ROOT', '✗ NOT SET'))"
	@if [ -f .monitor.pid ]; then \
	  PID=$$(cat .monitor.pid); \
	  if kill -0 $$PID 2>/dev/null; then \
	    echo "✓ Daemon running (PID $$PID)"; \
	  else \
	    echo "✗ Daemon PID file stale — run make setup"; \
	  fi \
	else \
	  echo "✗ Daemon not running — run make setup"; \
	fi
	@[ -f .git/hooks/pre-commit  ] && echo "✓ pre-commit hook installed"  || echo "✗ pre-commit hook missing"
	@[ -f .git/hooks/post-commit ] && echo "✓ post-commit hook installed" || echo "✗ post-commit hook missing"
	@[ -f .claude/settings.json  ] && echo "✓ .claude/settings.json present" || echo "✗ .claude/settings.json missing"
	@python3 -c "import watchdog; print('✓ watchdog installed')" 2>/dev/null || echo "✗ watchdog not installed — run make setup"
	@python3 -c "import subprocess; n=subprocess.check_output(['git','config','user.name'],text=True).strip(); print('✓ Learner identity:', n)" 2>/dev/null || echo "✗ git user.name not set"
	@[ -f .gemini/settings.json ] && echo "✓ .gemini/settings.json present" || echo "⚠ .gemini/settings.json missing (Gemini CLI won't be monitored)"
	@[ -n "$$GEMINI_API_KEY" ] && echo "✓ GEMINI_API_KEY is set" || echo "⚠ GEMINI_API_KEY not set (needed for capstone Gemini usage)"
