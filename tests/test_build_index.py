"""Tests for build_index.py helpers used to generate papers/pdfs index pages."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from build_index import load_alibaba_template


def test_load_alibaba_template_returns_css_and_js():
    css, js = load_alibaba_template()
    assert ":root" in css
    assert "--c-primary" in css
    assert "function applyFilter" in js
    assert "card.style.display" in js
