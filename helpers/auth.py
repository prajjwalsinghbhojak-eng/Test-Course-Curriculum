# helpers/auth.py
import base64
import hashlib
import os
from cryptography.fernet import Fernet
import getpass

_cached_key = None

def get_api_key():
    global _cached_key
    if _cached_key:
        return _cached_key

    passphrase = os.environ.get("COURSE_PASSPHRASE")
    if not passphrase:
        # Use getpass to hide input if running in an interactive environment
        passphrase = getpass.getpass("Enter course passphrase: ")

    key = base64.urlsafe_b64encode(hashlib.sha256(passphrase.encode()).digest())
    f = Fernet(key)

    # Resolve secrets.enc location dynamically relative to this auth.py file
    # Assuming auth.py is in AI_CoE_L-D/helpers/auth.py and secrets.enc is in AI_CoE_L-D/secrets.enc
    current_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(current_dir)
    secrets_path = os.path.join(repo_root, "secrets.enc")

    if not os.path.exists(secrets_path):
        raise FileNotFoundError(f"Could not find {secrets_path}. Please ensure it is present in the repo root.")

    try:
        with open(secrets_path, "rb") as file:
            encrypted_data = file.read()
            _cached_key = f.decrypt(encrypted_data).decode()
    except Exception as e:
        raise ValueError("Failed to decrypt the secret. Incorrect passphrase or corrupted secrets.enc file.") from e

    return _cached_key
