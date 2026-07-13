"""Regression tests for Chapter 3 figure generation scripts."""
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CHAPTER_DIR = REPO_ROOT / "book" / "part-01-feature-extraction" / "03-statistical-features"
CODE_DIR = CHAPTER_DIR / "assets" / "code"
IMAGE_DIR = CHAPTER_DIR / "assets" / "images"

SEASONALITY_SCRIPT = CODE_DIR / "03-example-04-seasonality-features.py"
TREND_SCRIPT = CODE_DIR / "03-example-05-trend-features.py"
SEASONALITY_FIG = IMAGE_DIR / "03-fig-04-seasonality.png"
TREND_FIG = IMAGE_DIR / "03-fig-05-trend.png"


def _run_script(script_path: Path):
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(script_path.parent),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Script failed:\n{result.stdout}\n{result.stderr}"
    return result


def test_run_seasonality_script():
    _run_script(SEASONALITY_SCRIPT)
    assert SEASONALITY_FIG.exists()
    assert SEASONALITY_FIG.stat().st_size > 0


def test_run_trend_script():
    _run_script(TREND_SCRIPT)
    assert TREND_FIG.exists()
    assert TREND_FIG.stat().st_size > 0


def _extract_strengths(stdout: str, marker: str):
    """Extract numeric strength values printed by a script."""
    pattern = re.compile(rf"{marker}\s*=\s*([0-9.]+)")
    return [float(m) for m in pattern.findall(stdout)]


def test_seasonal_strength_ranges():
    result = _run_script(SEASONALITY_SCRIPT)
    values = _extract_strengths(result.stdout, "F_s")
    assert len(values) == 3, f"Expected 3 seasonal strength values, got {values}"
    low, mid, high = sorted(values)
    assert 0.10 <= low <= 0.30, f"Weak seasonal strength out of range: {low}"
    assert 0.50 <= mid <= 0.75, f"Medium seasonal strength out of range: {mid}"
    assert 0.88 <= high <= 0.99, f"Strong seasonal strength out of range: {high}"


def test_trend_strength_ranges():
    result = _run_script(TREND_SCRIPT)
    values = _extract_strengths(result.stdout, "F_t")
    assert len(values) == 3, f"Expected 3 trend strength values, got {values}"
    low, mid, high = sorted(values)
    assert 0.10 <= low <= 0.30, f"Weak trend strength out of range: {low}"
    assert 0.50 <= mid <= 0.75, f"Medium trend strength out of range: {mid}"
    assert 0.88 <= high <= 0.99, f"Strong trend strength out of range: {high}"
