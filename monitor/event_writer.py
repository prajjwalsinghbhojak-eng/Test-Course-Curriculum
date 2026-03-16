"""
monitor/event_writer.py
Thread-safe JSONL event writer used by all monitoring layers.
"""

import json
import datetime
from pathlib import Path
from monitor.config import LEARNER_ID

try:
    import fcntl
    def _lock(f):   fcntl.flock(f, fcntl.LOCK_EX)
    def _unlock(f): fcntl.flock(f, fcntl.LOCK_UN)
except ImportError:
    # Windows: fcntl unavailable; hooks are sequential so races are rare
    def _lock(f):   pass
    def _unlock(f): pass


def write_event(log_file: Path, event_type: str, payload: dict) -> None:
    """Append a structured event to a JSONL log file (file-lock safe)."""
    record = {
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "learner": LEARNER_ID,
        "event_type": event_type,
        **payload,
    }
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a") as f:
        _lock(f)
        try:
            f.write(json.dumps(record) + "\n")
        finally:
            _unlock(f)
