"""Generate timeseries/papers/index.html and timeseries/pdfs/index.html from CSV + docs.

Reuses CSS/JS skeleton from timeseries/alibaba/index.html. Does NOT read PDFs.
"""
import csv
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).parent.resolve()
ALIBABA_INDEX = REPO_ROOT / "timeseries" / "alibaba" / "index.html"
PAPERS_DIR = REPO_ROOT / "timeseries" / "papers"
PDFS_DIR = REPO_ROOT / "timeseries" / "pdfs"


def load_alibaba_template():
    """Extract <style>...</style> and <script>...</script> from alibaba index."""
    text = ALIBABA_INDEX.read_text(encoding="utf-8")
    m_css = re.search(r"<style>(.*?)</style>", text, re.DOTALL)
    m_js = re.search(r"<script>(.*?)</script>", text, re.DOTALL)
    if not m_css or not m_js:
        raise RuntimeError("alibaba template missing <style> or <script>")
    return m_css.group(1), m_js.group(1)
