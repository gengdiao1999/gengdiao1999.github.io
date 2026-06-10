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


TOPIC_KEYWORDS = [
    ("anomaly", ["anomaly", "异常检测", "异常"]),
    ("rca", ["root cause", "rca", "根因"]),
    ("forecast", ["forecast", "predict", "预测"]),
    ("failure", ["failure", "mce", "故障预测"]),
    ("obs", ["observability", "可观测", "可视化"]),
    ("llm", ["llm", "agent", "大模型"]),
    ("log", ["log", "日志"]),
]


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)

    def get_text(self):
        s = " ".join(self.parts)
        s = re.sub(r"\s+", " ", s).strip()
        return s


def _first_p_text(html_text):
    """Return plain text of the first <p>...</p> in html_text, capped at 120 chars."""
    m = re.search(r"<p\b[^>]*>(.*?)</p>", html_text, re.DOTALL | re.IGNORECASE)
    if not m:
        return ""
    inner = m.group(1)
    ext = _TextExtractor()
    ext.feed(inner)
    text = ext.get_text()
    if len(text) > 120:
        text = text[:120].rstrip() + "…"
    return text


def _title_from_html(html_text):
    m = re.search(r"<title>(.*?)</title>", html_text, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else ""


def _infer_topic(haystack):
    h = haystack.lower()
    for topic, kws in TOPIC_KEYWORDS:
        for kw in kws:
            if kw in h:
                return topic
    return "other"


def extract_doc_fields(html_text):
    """Extract title, summary, topic from a docs/<dir>/README.html string."""
    title = _title_from_html(html_text)
    summary = _first_p_text(html_text)
    topic = _infer_topic(html_text + " " + title)
    return {"title": title, "summary": summary, "topic": topic}


def load_papers_csv():
    """Return list of dicts from timeseries/papers/papers_index.csv."""
    with (PAPERS_DIR / "papers_index.csv").open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_patents_csv():
    """Return list of dicts from timeseries/pdfs/patents_index.csv."""
    with (PDFS_DIR / "patents_index.csv").open(encoding="utf-8") as f:
        return list(csv.DictReader(f))
