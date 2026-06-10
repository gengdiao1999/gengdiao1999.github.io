"""Tests for build_index.py helpers used to generate papers/pdfs index pages."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from build_index import (
    build_papers_index_html,
    build_pdfs_index_html,
    extract_doc_fields,
    load_alibaba_template,
    load_papers_csv,
    load_patents_csv,
    render_paper_card,
    render_patent_card,
)


def test_load_alibaba_template_returns_css_and_js():
    css, js = load_alibaba_template()
    assert ":root" in css
    assert "--c-primary" in css
    assert "function applyFilter" in js
    assert "card.style.display" in js


SAMPLE_README = """<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>一种基于日志的运维分析方法（ICSE 2024）</title></head>
<body>
<h1>一种基于日志的运维分析方法</h1>
<p>本文提出基于深度学习的日志分析方案,在公开数据集上 F1 达到 0.95。</p>
</body></html>
"""


def test_extract_doc_fields_returns_title_and_summary():
    fields = extract_doc_fields(SAMPLE_README)
    assert fields["title"] == "一种基于日志的运维分析方法（ICSE 2024）"
    assert "深度学习" in fields["summary"]
    assert fields["topic"] == "log"  # 关键词 日志 命中 log


def test_load_papers_csv_returns_176_rows():
    rows = load_papers_csv()
    assert len(rows) == 176
    assert "year" in rows[0]
    assert "title" in rows[0]
    assert "pdf_file" in rows[0]


def test_load_patents_csv_returns_30_rows():
    rows = load_patents_csv()
    assert len(rows) == 30
    assert "publication_date" in rows[0]
    assert "patent_id" in rows[0]


def test_render_paper_card_contains_title_year_and_links():
    csv_row = {
        "year": "2024",
        "title": "Smart Eye: A Log Anomaly Detector",
        "authors": "Pei et al.",
        "venue": "WWW 2026",
        "pdf_url": "https://arxiv.org/abs/2510.04710",
        "pdf_file": "2510.04710v1_11.pdf",
        "size_bytes": "7632909",
    }
    doc_fields = {
        "title": "Smart Eye: 日志异常检测框架",
        "summary": "本文提出 LLM-Guided 工业级日志异常检测方案。",
        "topic": "log",
    }
    html = render_paper_card(csv_row, doc_fields, "2510.04710v1_11")
    assert 'class="card"' in html
    assert 'data-topic="log"' in html
    assert 'data-year="2024"' in html
    assert "Smart Eye" in html
    assert "arxiv.org/abs/2510.04710" in html
    assert "./docs/2510.04710v1_11/README.html" in html
    assert "./2510.04710v1_11.pdf" in html


def test_render_patent_card_contains_patent_id_and_links():
    row = {
        "patent_id": "CN110532550A",
        "title": "一种基于日志词频树的智能系统日志解析处理方法",
        "application_no": "201910742035.5",
        "publication_date": "2019.12.03",
        "assignee": "北京必示科技有限公司",
        "pub_kind": "发明专利申请",
        "pdf_file": "CN110532550A.pdf",
        "google_patents_url": "https://patents.google.com/patent/CN110532550A/zh",
    }
    doc_fields = {"title": "一种日志词频树方法", "summary": "基于词频树的日志解析方案。", "topic": "log"}
    html = render_patent_card(row, doc_fields, "CN110532550A")
    assert 'data-topic="log"' in html
    assert 'CN110532550A' in html
    assert './docs/CN110532550A/README.html' in html
    assert './CN110532550A.pdf' in html
    assert 'patents.google.com/patent/CN110532550A' in html


def test_build_papers_index_html_has_176_cards():
    html = build_papers_index_html()
    assert html.count('<article class="card"') == 176
    assert 'class="chip"' in html
    assert 'id="paper-grid"' in html
    assert 'id="search-input"' in html
    assert 'function applyFilter' in html


def test_build_pdfs_index_html_has_30_cards():
    html = build_pdfs_index_html()
    assert html.count('<article class="card"') == 30
    assert 'id="paper-grid"' in html
    assert "必示科技" in html
