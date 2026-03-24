# Getting Started

This guide gets you up and running with the AI CoE Level 1 curriculum.

**Recommended path: GitHub Codespaces** — runs entirely in your browser, no local installs required.
Local VS Code is fully supported as an alternative if you prefer to work on your machine.

---

## Option 1 — GitHub Codespaces (Recommended)

**What you need:** A GitHub account. Nothing else.

### Step 1 — Create your copy of the repo

1. Go to the course repo on GitHub
2. Click **"Use this template"** → **"Create a new repository"**
3. Set it to **Private**, give it a name, click **"Create repository"**

### Step 2 — Add your course passphrase

Your instructor will give you a course passphrase. This unlocks the API key embedded in the repo.

1. Go to your new repo on GitHub
2. Click **Settings** → **Secrets and variables** → **Codespaces**
3. Click **"New repository secret"**
4. Name: `COURSE_PASSPHRASE`
5. Value: *(paste the passphrase from your instructor)*
6. Click **"Add secret"**

> You only do this once. The secret is injected automatically into every Codespace you open from this repo.

### Step 3 — Open in Codespace

1. Click **"Code"** → **"Codespaces"** tab → **"Create codespace on main"**
2. The environment builds (~2 minutes on first launch, faster after)
3. VS Code opens in your browser — all packages are pre-installed

### Step 4 — Open a notebook and start learning

1. In the file explorer, navigate to `AI_CoE_Curriculum/Level_1_Beginner/`
2. Open `Day_01_Introduction_to_AI_and_LLMs/01_What_is_GenAI.ipynb`
3. Click **"Run All"** or run cells one by one
4. The first cell that calls `get_api_key()` will authenticate silently using your secret

That's it — no terminal, no installs, no configuration.

---

## Option 2 — Local VS Code

Use this if you prefer to work locally or can't access Codespaces.

**What you need:**
- [Python 3.10+](https://www.python.org/downloads/) (user-level install, no admin required)
- [VS Code](https://code.visualstudio.com/) (user-level install, no admin required)
- VS Code extensions: **Python** and **Jupyter** (install from the Extensions panel)

> No Docker required. No devcontainer. Just Python and VS Code.

### Step 1 — Clone your repo

```bash
git clone https://github.com/<your-username>/<your-repo-name>
cd <your-repo-name>
```

### Step 2 — Set your course passphrase

Set the `COURSE_PASSPHRASE` environment variable to the value your instructor gave you.

**Mac / Linux:**
```bash
export COURSE_PASSPHRASE="your passphrase here"
```
Add it to `~/.zshrc` or `~/.bashrc` to make it permanent.

**Windows (PowerShell):**
```powershell
$env:COURSE_PASSPHRASE = "your passphrase here"
```
To make it permanent, set it in System → Environment Variables.

### Step 3 — Open in VS Code and select a kernel

```bash
code .
```

Open any notebook, click **"Select Kernel"** → **"Python Environments"** → choose your Python 3.10+ interpreter.

### Step 4 — Run a notebook

Open `AI_CoE_Curriculum/Level_1_Beginner/Day_01_Introduction_to_AI_and_LLMs/01_What_is_GenAI.ipynb`.

Each notebook has a `%pip install` cell at the top — run it once and the required packages install automatically. Subsequent runs skip the install.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `Enter course passphrase:` prompt appears | `COURSE_PASSPHRASE` secret/env var is not set — follow Step 2 above |
| `ValueError: Failed to decrypt` | Wrong passphrase — check with your instructor |
| `FileNotFoundError: secrets.enc` | You're not running the notebook from the repo root — reopen the folder, not just the file |
| Codespace takes long to open | Normal on first launch (~2 min); subsequent opens are faster |
| Kernel not found (local) | Select the kernel manually: click "Select Kernel" in the top-right of the notebook |
