"""
monitor/daemon.py
Background filesystem watcher daemon.
Monitors the repo for planning artifacts, test files, and code activity.
Started automatically by setup.sh; runs as a detached background process.

Requires: pip install watchdog
"""

import sys
import os
import time
import signal
import logging

sys.path.insert(0, os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from monitor.config import (
    REPO_ROOT,
    FS_LOG_FILE,
    NOTEBOOK_LOG_FILE,
    WATCH_EXTENSIONS,
    WATCH_IGNORE_DIRS,
    PLANNING_PATTERNS,
    TEST_PATTERNS,
    FS_EVENT_DEBOUNCE_WINDOW,
)
from monitor.event_writer import write_event
from monitor.notebook_tracker import parse_notebook

logging.basicConfig(
    level=logging.INFO,
    format="[monitor-daemon] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

PID_FILE = REPO_ROOT / ".monitor.pid"


def classify_file(filepath: str) -> list[str]:
    """Return a list of learning signal tags for a given file path."""
    tags = []
    name = filepath.lower()

    if any(p in name for p in PLANNING_PATTERNS):
        tags.append("planning_artifact")
    if any(p in name for p in TEST_PATTERNS):
        tags.append("test_file")
    if name.endswith(".ipynb"):
        tags.append("notebook")
    if name.endswith(".py"):
        tags.append("python_source")
    if name.endswith((".yaml", ".yml")):
        tags.append("config")
    if name.endswith(".md"):
        tags.append("documentation")

    return tags or ["other"]


def should_ignore(path: str) -> bool:
    parts = Path(path).parts
    return any(d in parts for d in WATCH_IGNORE_DIRS)


class LearningActivityHandler(FileSystemEventHandler):
    def __init__(self):
        self._debounce: dict[str, float] = {}

    def _debounced(self, path: str, window: float = FS_EVENT_DEBOUNCE_WINDOW) -> bool:
        """Suppress duplicate events within `window` seconds for same path."""
        now = time.time()
        if now - self._debounce.get(path, 0) < window:
            return True
        self._debounce[path] = now
        return False

    def on_created(self, event):
        if event.is_directory:
            return
        self._handle(event.src_path, "file_created")

    def on_modified(self, event):
        if event.is_directory:
            return
        self._handle(event.src_path, "file_modified")

    def _handle(self, path: str, action: str):
        if should_ignore(path):
            return
        ext = Path(path).suffix
        if ext not in WATCH_EXTENSIONS:
            return
        if self._debounced(path):
            return

        rel_path = str(Path(path).relative_to(REPO_ROOT))
        tags = classify_file(path)

        write_event(FS_LOG_FILE, action, {
            "path": rel_path,
            "tags": tags,
            "ext": ext,
        })

        # Notebooks get a second, richer event with execution data
        if ext == ".ipynb":
            nb_data = parse_notebook(path, str(REPO_ROOT))
            if nb_data:
                write_event(NOTEBOOK_LOG_FILE, "notebook_execution", nb_data)
                log.info(
                    f"notebook: {nb_data['notebook_name']} "
                    f"[{nb_data['cells_executed']}/{nb_data['cells_code']} cells executed, "
                    f"{nb_data['cells_with_errors']} errors]"
                )

        log.info(f"{action}: {rel_path} [{', '.join(tags)}]")


def write_pid():
    PID_FILE.write_text(str(os.getpid()))


def clear_pid():
    try:
        PID_FILE.unlink()
    except FileNotFoundError:
        pass


def main():
    write_pid()
    log.info(f"Starting filesystem watcher on {REPO_ROOT}")

    handler = LearningActivityHandler()
    observer = Observer()
    observer.schedule(handler, str(REPO_ROOT), recursive=True)
    observer.start()

    def shutdown(sig, frame):
        log.info("Stopping filesystem watcher.")
        observer.stop()
        clear_pid()
        sys.exit(0)

    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
    clear_pid()


if __name__ == "__main__":
    main()
