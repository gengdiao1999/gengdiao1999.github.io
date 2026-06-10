"""Tests for build_index.py helpers used to generate papers/pdfs index pages."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from build_index import extract_doc_fields, load_alibaba_template


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
