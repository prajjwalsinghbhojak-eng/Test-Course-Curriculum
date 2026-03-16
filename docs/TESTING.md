# Testing Guide — AI Learning Monitor

This document is in two parts:

- **Part A — GitHub Setup** (done once by the team member setting up the org)
- **Part B — End-to-End Testing** (done to verify everything works)

Follow Part A completely before starting Part B.

---

# Part A — Initial GitHub Setup

## A1. Create the central monitoring repo

This is the private repo where all learner logs will land. Instructors read from here.

1. Go to `https://github.com/organizations/LatentviewIT/repositories/new`
2. Repository name: `learning-monitor-reports`
3. Set to **Private**
4. **Do not** initialise with README, .gitignore, or licence — leave it completely empty
5. Click **Create repository**

---

## A2. Push the monitor code into `AI_CoE_L-D`

The monitor code lives in your local clone. Merge it into the org repo.

```bash
# In your local clone of this project
cd /path/to/ai-learning-path-tracker

# Add the org repo as a remote
git remote add company https://github.com/LatentviewIT/AI_CoE_L-D.git

# Fetch what's already there
git fetch company

# Merge — allow unrelated histories because the two repos started independently
git merge company/main --allow-unrelated-histories
```

If there are merge conflicts (most likely in README.md):
```bash
# Open the conflicted file, keep whichever content makes sense, then:
git add README.md
git commit -m "merge: integrate AI Learning Monitor into AI_CoE_L-D"
```

Push to the org repo:
```bash
git push company main
```

Verify it landed:
```bash
# You should see monitor/ setup.sh setup.py .env.monitor.example etc.
git ls-tree company/main --name-only
```

---

## A3. Create a fine-grained PAT for log sync

This token allows any learner's machine to push logs into `learning-monitor-reports`.
It has write access to that one repo only — safe to share with all learners.

1. Go to `https://github.com/settings/personal-access-tokens/new`
   *(log in as the org owner or a service account)*
2. Token name: `ai-monitor-push-token`
3. Expiration: set to the length of your cohort + 1 month
4. Resource owner: `LatentviewIT`
5. Repository access: **Only select repositories** → choose `learning-monitor-reports`
6. Permissions → **Contents**: Read and write *(all other permissions: No access)*
7. Click **Generate token** — copy it immediately, you won't see it again

Store it somewhere secure (e.g. a 1Password shared vault or internal Notion page).
You will paste this into `.env.monitor` for each learner during onboarding.

---

## A4. Set org-level Codespace secrets (for company-account learners)

Learners using GitHub Codespaces with their **company account** will receive these
secrets automatically — no `.env.monitor` required.

1. Go to `https://github.com/organizations/LatentviewIT/settings/secrets/codespaces`
2. Add the following secrets:

| Secret name | Value |
|---|---|
| `MONITOR_PUSH_TOKEN` | the PAT from A3 |
| `MONITOR_REPO_URL` | `https://github.com/LatentviewIT/learning-monitor-reports` |
| `ANTHROPIC_API_KEY` | your Anthropic API key |
| `GEMINI_API_KEY` | your Google Gemini API key |

3. For each secret, set **Repository access** to `AI_CoE_L-D` (or all repositories if preferred)

> **Personal account or local users** will use `.env.monitor` instead — see Part B prerequisites.

---

## A5. Make `AI_CoE_L-D` a template repository

Learners will click "Use this template" to create their own private copy.

1. Go to `https://github.com/LatentviewIT/AI_CoE_L-D`
2. Click **Settings**
3. Under the **General** section, check **Template repository**
4. Click **Save**

You should now see a green **"Use this template"** button on the repo homepage.

---

## A6. Set up the GitHub Action secret

The weekly report Action needs permission to push generated reports back to
`learning-monitor-reports`.

1. Go to `https://github.com/LatentviewIT/AI_CoE_L-D/settings/secrets/actions`
2. Add a new repository secret:

| Secret name | Value |
|---|---|
| `MONITOR_PUSH_TOKEN` | the PAT from A3 |

> `GITHUB_TOKEN` is provided automatically by GitHub Actions — no setup needed for that.

---

## A7. Verify the repo is ready

```bash
# From your local clone with the company remote added
git fetch company

# Check main branch has the monitor code
git ls-tree company/main --name-only
# Expected: monitor/ setup.sh setup.py .env.monitor.example Makefile ...

# Check the monitoring-reports repo exists and is accessible with your token
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: token YOUR_PAT_HERE" \
  https://api.github.com/repos/LatentviewIT/learning-monitor-reports
# Expected: 200
```

---

# Part B — End-to-End Testing

Once Part A is complete, run through these tests to verify every layer works.

---

## Prerequisites

```bash
# 1. Create your test copy of the repo
#    Go to https://github.com/LatentviewIT/AI_CoE_L-D
#    Click "Use this template" → Create a new private repository
#    Name it: ai-learning-monitor-test (or similar)
#    Clone it locally:
git clone https://github.com/<your-account>/ai-learning-monitor-test
cd ai-learning-monitor-test

# 2. Set git identity
git config --global user.name  "Test User"
git config --global user.email "test@example.com"

# 3. Configure .env.monitor (skip if using Codespaces with org secrets set)
cp .env.monitor.example .env.monitor
# Open .env.monitor and fill in:
#   MONITOR_PUSH_TOKEN=<the PAT from A3>
#   GEMINI_API_KEY=<your Gemini key>
# MONITOR_REPO_URL is already pre-filled — do not change it

# 4. Run setup
bash setup.sh        # Mac/Linux/Codespaces
# python setup.py    # Windows

# 5. Verify
make health
```

Expected `make health` output — all lines should show ✓:

```
── AI Learning Monitor Health Check ──
✓ REPO_ROOT: /path/to/repo
✓ Daemon running (PID 12345)
✓ pre-commit hook installed
✓ post-commit hook installed
✓ .claude/settings.json present
✓ watchdog installed
✓ Learner identity: test_user
```

---

## B1. Unit tests

Runs in under 1 second. All 82 tests must pass before proceeding.

```bash
python -m pytest tests/ -q
```

Expected:
```
82 passed in 0.3s
```

---

## B2. Filesystem daemon

**Goal:** Confirm file events are written to `fs_events.jsonl`.

Open two terminals. In terminal 1:
```bash
tail -f logs/test_user/fs_events.jsonl
```

In terminal 2:
```bash
touch test_signal.py
sleep 3
```

Expected in terminal 1:
```json
{"ts": "...", "event_type": "file_created", "path": "test_signal.py", "tags": ["python_source"], "ext": ".py"}
```

Cleanup: `rm test_signal.py`

**Notebook test:**
```bash
python3 -c "
import json, pathlib
nb = {'nbformat': 4, 'nbformat_minor': 5, 'metadata': {},
      'cells': [{'cell_type': 'code', 'source': ['print(1)'],
                 'execution_count': 1, 'outputs': []}]}
pathlib.Path('test_nb.ipynb').write_text(json.dumps(nb))
"
sleep 3
tail -1 logs/test_user/notebook_events.jsonl | python3 -m json.tool
```

Expected: JSON with `execution_ratio`, `cells_executed`, `day`, `topic`.

Cleanup: `rm test_nb.ipynb`

---

## B3. Git hooks

**Goal:** Confirm `pre_commit` and `commit` events appear in `git_events.jsonl`.

```bash
echo "# test" >> README.md
git add README.md
git commit -m "test: verify git hooks"
tail -5 logs/test_user/git_events.jsonl | python3 -m json.tool
```

Expected — two events:
1. `pre_commit` — has `files_staged`, `has_tests`, `tests_passed`
2. `commit` — has `hash`, `message`, `author`, `files_changed`

Verify `files_changed` is not 0:
```bash
python3 -c "
import json
events = [json.loads(l) for l in open('logs/test_user/git_events.jsonl')]
commits = [e for e in events if e['event_type'] == 'commit']
assert commits[-1]['files_changed'] > 0, 'FAIL: files_changed is 0'
print('OK — files_changed:', commits[-1]['files_changed'])
"
```

---

## B4. Claude Code hooks

**Goal:** Confirm tool-call events appear in `claude_events.jsonl`.

Terminal 1:
```bash
tail -f logs/test_user/claude_events.jsonl
```

Terminal 2:
```bash
export REPO_ROOT=$(pwd)
claude
```

Inside Claude, type: `list the files in this directory`

Expected in terminal 1:
```json
{"ts": "...", "event_type": "PreToolUse", "source": "claude", "tool": "Bash", "category": "execution"}
{"ts": "...", "event_type": "PostToolUse", "source": "claude", "tool": "Bash", "success": true}
```

Exit Claude (`/exit`). Check session summary:
```bash
tail -1 logs/test_user/sessions.jsonl | python3 -m json.tool
```

Expected: `session_summary.total_tool_calls > 0` and `prompts.prompt_count > 0`.

---

## B5. Gemini CLI hooks

**Goal:** Confirm tool-call events appear in `gemini_events.jsonl`.

Terminal 1:
```bash
tail -f logs/test_user/gemini_events.jsonl
```

Terminal 2:
```bash
export REPO_ROOT=$(pwd)
gemini
```

Inside Gemini, type: `list the files here`

Expected in terminal 1 — events with `"source": "gemini"` and Gemini tool names
(`run_shell_command`, `list_directory`, etc.).

Exit the session. Check:
```bash
tail -1 logs/test_user/sessions.jsonl | python3 -m json.tool
```

Expected: `source: "gemini"`, `session_summary.total_tool_calls > 0`.

---

## B6. Report generation

```bash
make report
cat reports/test_user/progress_report_$(date +%Y-%m-%d).md
```

Verify these sections appear (depending on what activity you generated above):
- `## 🤖 AI Coding Assistant Usage`
- `## 📁 File System Activity`
- `## 🔀 Git Discipline`
- `## 💡 Insights & Recommended Next Steps`

---

## B7. Remote sync

**Goal:** Confirm logs land in `learning-monitor-reports`.

```bash
make sync
```

Expected output:
```
[monitor] Pushing logs for test_user to monitoring-reports...
[monitor] Pushed successfully.
```

Verify on GitHub — go to:
`https://github.com/LatentviewIT/learning-monitor-reports`

You should see:
```
logs/
  test_user/
    claude_events.jsonl
    git_events.jsonl
    fs_events.jsonl
    sessions.jsonl
```

Or verify from the command line:
```bash
git clone https://github.com/LatentviewIT/learning-monitor-reports /tmp/monitor-check
ls /tmp/monitor-check/logs/
# Expected: test_user/
ls /tmp/monitor-check/logs/test_user/
# Expected: claude_events.jsonl  gemini_events.jsonl  git_events.jsonl  fs_events.jsonl  sessions.jsonl
rm -rf /tmp/monitor-check
```

---

## B8. GitHub Action (weekly reports)

**Goal:** Confirm the Action generates reports for all learners automatically.

1. Go to `https://github.com/LatentviewIT/AI_CoE_L-D/actions`
2. Click **Weekly Learning Progress Reports**
3. Click **Run workflow** → **Run workflow**
4. Wait for completion (typically < 2 minutes)
5. Check the run logs — look for `[monitor] Report written to ...` lines

After success:
```bash
git clone https://github.com/LatentviewIT/learning-monitor-reports /tmp/monitor-check
ls /tmp/monitor-check/reports/test_user/
# Expected: progress_report_YYYY-MM-DD.md
cat /tmp/monitor-check/reports/test_user/progress_report_*.md
rm -rf /tmp/monitor-check
```

---

## B9. Multi-learner isolation

**Goal:** Confirm a second learner's logs are stored in a separate folder.

```bash
# Switch to a second identity
git config user.name "Second Learner"
git config user.email "second@example.com"

# Generate activity
echo "# second learner test" >> README.md
git add README.md
git commit -m "test: second learner isolation"
make sync
```

Verify both learner folders exist in `learning-monitor-reports`:
```bash
git clone https://github.com/LatentviewIT/learning-monitor-reports /tmp/monitor-check
ls /tmp/monitor-check/logs/
# Expected: second_learner/  test_user/
rm -rf /tmp/monitor-check
```

Restore original identity:
```bash
git config user.name "Test User"
git config user.email "test@example.com"
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `make health` shows daemon not running | setup.sh failed silently | `make restart` or check `logs/daemon.log` |
| No events in `claude_events.jsonl` | `REPO_ROOT` not set | `export REPO_ROOT=$(pwd)` before starting Claude |
| `files_changed: 0` in commit events | Old hook version installed | Re-run `bash setup.sh` to reinstall hooks |
| `make sync` fails with 401/403 | Token wrong or expired | Check `MONITOR_PUSH_TOKEN` in `.env.monitor` |
| `make sync` fails with 404 | `learning-monitor-reports` repo doesn't exist | Complete step A1 |
| Gemini hooks not firing | `GEMINI_API_KEY` not set | Check `.env.monitor` and re-run setup |
| GitHub Action fails with permission error | `MONITOR_PUSH_TOKEN` secret not set on `AI_CoE_L-D` | Complete step A6 |
| Tests failing | Import error | Run `python -m pytest tests/ -v` for details |
