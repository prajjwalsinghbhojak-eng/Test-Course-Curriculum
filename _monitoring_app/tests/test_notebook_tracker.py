"""
Tests for monitor/notebook_tracker.py
Uses synthetic .ipynb JSON — no real notebook files needed.
"""

import json
import pytest
from monitor.notebook_tracker import parse_notebook, _infer_day_topic


# ── Helpers ────────────────────────────────────────────────────────────────

def make_notebook(cells: list[dict]) -> dict:
    """Build a minimal valid .ipynb structure."""
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {"kernelspec": {"display_name": "Python 3"}},
        "cells": cells,
    }


def code_cell(source: str, execution_count: int | None = None, outputs: list = None) -> dict:
    return {
        "cell_type": "code",
        "source": [source],
        "execution_count": execution_count,
        "outputs": outputs or [],
        "metadata": {},
    }


def error_output(ename: str, evalue: str) -> dict:
    return {
        "output_type": "error",
        "ename": ename,
        "evalue": evalue,
        "traceback": [],
    }


def stream_output(text: str) -> dict:
    return {"output_type": "stream", "name": "stdout", "text": [text]}


def markdown_cell(source: str) -> dict:
    return {"cell_type": "markdown", "source": [source], "metadata": {}}


# ── Tests: parse_notebook ──────────────────────────────────────────────────

def test_unexecuted_notebook(tmp_path):
    nb = make_notebook([
        code_cell("x = 1"),
        code_cell("print(x)"),
    ])
    f = tmp_path / "day_01_intro.ipynb"
    f.write_text(json.dumps(nb))

    result = parse_notebook(str(f), str(tmp_path))

    assert result["cells_code"] == 2
    assert result["cells_executed"] == 0
    assert result["execution_ratio"] == 0.0
    assert result["cells_with_errors"] == 0


def test_fully_executed_notebook(tmp_path):
    nb = make_notebook([
        code_cell("x = 1", execution_count=1, outputs=[stream_output("1")]),
        code_cell("y = 2", execution_count=2, outputs=[stream_output("2")]),
        code_cell("x + y", execution_count=3, outputs=[stream_output("3")]),
    ])
    f = tmp_path / "notebooks" / "day_02" / "basics.ipynb"
    f.parent.mkdir(parents=True)
    f.write_text(json.dumps(nb))

    result = parse_notebook(str(f), str(tmp_path))

    assert result["cells_executed"] == 3
    assert result["execution_ratio"] == 1.0
    assert result["execution_sequential"] is True
    assert result["cells_with_errors"] == 0
    assert result["day"] == "day_02"
    assert result["topic"] == "basics"


def test_partial_execution(tmp_path):
    nb = make_notebook([
        code_cell("import os", execution_count=1),
        code_cell("os.getcwd()", execution_count=2),
        code_cell("# not run yet"),
        code_cell("# also not run"),
    ])
    f = tmp_path / "day_03_paths.ipynb"
    f.write_text(json.dumps(nb))

    result = parse_notebook(str(f), str(tmp_path))

    assert result["cells_code"] == 4
    assert result["cells_executed"] == 2
    assert result["execution_ratio"] == 0.5


def test_notebook_with_errors(tmp_path):
    nb = make_notebook([
        code_cell("import langchain", execution_count=1,
                  outputs=[error_output("ModuleNotFoundError", "No module named 'langchain'")]),
        code_cell("x = 1", execution_count=2, outputs=[stream_output("ok")]),
        code_cell("bad_var", execution_count=3,
                  outputs=[error_output("NameError", "name 'bad_var' is not defined")]),
    ])
    f = tmp_path / "day_04_langchain.ipynb"
    f.write_text(json.dumps(nb))

    result = parse_notebook(str(f), str(tmp_path))

    assert result["cells_with_errors"] == 2
    assert "ModuleNotFoundError" in result["error_types"]
    assert "NameError" in result["error_types"]
    assert len(result["error_details"]) == 2
    # Cell source should be captured for debugging
    assert "langchain" in result["error_details"][0]["cell_source"]


def test_non_sequential_execution(tmp_path):
    """Learner re-ran cells out of order — execution_counts not 1,2,3."""
    nb = make_notebook([
        code_cell("x = 1",  execution_count=3),
        code_cell("y = 2",  execution_count=1),
        code_cell("x + y",  execution_count=2),
    ])
    f = tmp_path / "day_01_rerun.ipynb"
    f.write_text(json.dumps(nb))

    result = parse_notebook(str(f), str(tmp_path))

    assert result["execution_sequential"] is False


def test_markdown_cells_detected(tmp_path):
    nb = make_notebook([
        markdown_cell("## Introduction\nThis notebook covers..."),
        code_cell("x = 1", execution_count=1),
    ])
    f = tmp_path / "day_01_intro.ipynb"
    f.write_text(json.dumps(nb))

    result = parse_notebook(str(f), str(tmp_path))

    assert result["cells_markdown"] == 1
    assert result["has_markdown_notes"] is True


def test_invalid_file_returns_none(tmp_path):
    f = tmp_path / "broken.ipynb"
    f.write_text("not valid json {{{")

    result = parse_notebook(str(f), str(tmp_path))
    assert result is None


def test_missing_file_returns_none(tmp_path):
    result = parse_notebook(str(tmp_path / "ghost.ipynb"), str(tmp_path))
    assert result is None


def test_empty_notebook(tmp_path):
    nb = make_notebook([])
    f = tmp_path / "day_01_empty.ipynb"
    f.write_text(json.dumps(nb))

    result = parse_notebook(str(f), str(tmp_path))

    assert result["cells_code"] == 0
    assert result["execution_ratio"] == 0.0


# ── Tests: _infer_day_topic ────────────────────────────────────────────────

@pytest.mark.parametrize("rel_path, expected_day, expected_topic", [
    # Directory-based day
    ("notebooks/day_03/langchain_basics.ipynb", "day_03", "langchain basics"),
    ("notebooks/day_3/langchain_basics.ipynb",  "day_03", "langchain basics"),
    ("week_01/day_03/topic.ipynb",              "day_03", "topic"),
    # Filename-based day
    ("day03_langchain.ipynb",                   "day_03", "langchain"),
    ("day_3_embeddings.ipynb",                  "day_03", "embeddings"),
    # Leading number convention
    ("03_embeddings_exercise.ipynb",            "day_03", "embeddings exercise"),
    # No day info → unknown
    ("misc/scratch.ipynb",                      "unknown", "scratch"),
])
def test_infer_day_topic(rel_path, expected_day, expected_topic):
    day, topic = _infer_day_topic(rel_path)
    assert day == expected_day
    assert topic == expected_topic
