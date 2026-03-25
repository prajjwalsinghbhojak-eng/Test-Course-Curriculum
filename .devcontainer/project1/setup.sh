#!/bin/bash
set -e

echo ""
echo "=========================================="
echo "  Capstone Project 1 — Environment Setup  "
echo "=========================================="
echo ""

# ── 1. Python dependencies ────────────────────────────────────────────────────
echo "▶ Installing Python dependencies..."
pip install -q -r .devcontainer/project1/requirements.txt
echo "  ✓ Python dependencies installed"

# ── 2. Gemini CLI ─────────────────────────────────────────────────────────────
echo "▶ Installing Gemini CLI..."
npm install -g @google/gemini-cli --silent
echo "  ✓ Gemini CLI installed ($(gemini --version 2>/dev/null || echo 'version unknown'))"

# ── 3. Decrypt API key and export to shell ────────────────────────────────────
echo "▶ Decrypting API key..."
python3 - <<'PYEOF'
import os, sys, base64, hashlib

passphrase = os.environ.get("COURSE_PASSPHRASE", "")
if not passphrase:
    print("  ✗ COURSE_PASSPHRASE is not set.")
    print("    Go to: github.com → Settings → Codespaces → Secrets")
    print("    Add secret: COURSE_PASSPHRASE = (value provided by your instructor)")
    sys.exit(0)

try:
    from cryptography.fernet import Fernet
    key = base64.urlsafe_b64encode(hashlib.sha256(passphrase.encode()).digest())
    f = Fernet(key)
    with open("secrets.enc", "rb") as file:
        api_key = f.decrypt(file.read()).decode()

    # Export to both .bashrc and .profile so it's available in all shell sessions
    export_line = f'\nexport GEMINI_API_KEY="{api_key}"\n'
    for rc_file in ["~/.bashrc", "~/.profile"]:
        path = os.path.expanduser(rc_file)
        with open(path, "a") as rc:
            rc.write(export_line)

    print("  ✓ GEMINI_API_KEY exported to shell environment")
except Exception as e:
    print(f"  ✗ Failed to decrypt: {e}")
    print("    Check that your COURSE_PASSPHRASE is correct.")
PYEOF

# Make GEMINI_API_KEY available for the rest of this script (data download)
export GEMINI_API_KEY=$(python3 -c "
import os, base64, hashlib
from cryptography.fernet import Fernet
p = os.environ.get('COURSE_PASSPHRASE', '')
if not p: exit()
k = base64.urlsafe_b64encode(hashlib.sha256(p.encode()).digest())
f = Fernet(k)
print(f.decrypt(open('secrets.enc','rb').read()).decode())
" 2>/dev/null || echo "")

# ── 4. Download and prepare dataset ──────────────────────────────────────────
echo "▶ Setting up project dataset..."
python3 capstone/project1_customer_support/data/setup_data.py
echo "  ✓ Dataset ready"

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo "=========================================="
echo "  Setup complete! Here's how to start:    "
echo "                                          "
echo "  Run the app:                            "
echo "    streamlit run app.py                  "
echo "                                          "
echo "  Use Gemini CLI:                         "
echo "    gemini                                "
echo "=========================================="
echo ""
