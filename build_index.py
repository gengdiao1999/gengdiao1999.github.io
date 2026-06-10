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


def _html_escape(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def render_paper_card(row, doc_fields, doc_dir_name):
    """Render one <article class="card"> for a paper."""
    title = _html_escape(doc_fields["title"])
    etitle = _html_escape(row.get("title", ""))
    venue = _html_escape(row.get("venue", ""))
    summary = _html_escape(doc_fields["summary"])
    year = row.get("year", "")
    topic = doc_fields["topic"]
    pdf_url = row.get("pdf_url", "").strip()
    arxiv_html = ""
    if pdf_url and "arxiv.org" in pdf_url.lower():
        arxiv_id = pdf_url.rstrip("/").split("/")[-1]
        arxiv_html = (
            f'      <a class="arxiv-link" href="{_html_escape(pdf_url)}" '
            f'target="_blank" rel="noopener">arXiv:{_html_escape(arxiv_id)}</a>\n'
        )
    badge = f'<span class="badge badge-{topic}">{_html_escape(topic)}</span>' if topic in {"anomaly","rca","forecast","failure","obs","llm","log"} else ""
    return f"""  <article class="card" data-topic="{topic}" data-year="{year}"
           data-keywords="{title} {etitle} {_html_escape(doc_fields.get('topic',''))}">
    <a class="ctitle" href="./docs/{doc_dir_name}/README.html">{title}</a>
    <p class="etitle">{etitle}</p>
    <div class="meta">
      {badge}
      <span class="year-tag">{year}</span>
{arxiv_html}    </div>
    <p class="venue">{venue}</p>
    <p class="summary">{summary}</p>
    <div class="actions">
      <a class="btn btn-primary" href="./docs/{doc_dir_name}/README.html">阅读方案说明</a>
      <a class="btn" href="./{_html_escape(row.get('pdf_file',''))}" target="_blank">查看 PDF</a>
    </div>
  </article>
"""


def render_patent_card(row, doc_fields, doc_dir_name):
    title = _html_escape(doc_fields["title"])
    etitle = _html_escape(row.get("title", ""))
    pub_date = row.get("publication_date", "")
    year = pub_date.split(".")[0] if pub_date else ""
    assignee = _html_escape(row.get("assignee", ""))
    pub_kind = _html_escape(row.get("pub_kind", ""))
    summary = _html_escape(doc_fields["summary"])
    topic = doc_fields["topic"]
    gp_url = _html_escape(row.get("google_patents_url", ""))
    badge = ""
    if "发明" in pub_kind:
        badge = '<span class="badge badge-llm">发明</span>'
    elif "实用新型" in pub_kind:
        badge = '<span class="badge badge-obs">实用新型</span>'
    return f"""  <article class="card" data-topic="{topic}" data-year="{year}"
           data-keywords="{title} {etitle} {assignee}">
    <a class="ctitle" href="./docs/{doc_dir_name}/README.html">{title}</a>
    <p class="etitle">{etitle}</p>
    <div class="meta">
      {badge}
      <span class="year-tag">{year}</span>
      <a class="arxiv-link" href="{gp_url}" target="_blank" rel="noopener">{_html_escape(row.get('patent_id',''))}</a>
    </div>
    <p class="venue">{assignee} · {pub_kind}</p>
    <p class="summary">{summary}</p>
    <div class="actions">
      <a class="btn btn-primary" href="./docs/{doc_dir_name}/README.html">阅读方案说明</a>
      <a class="btn" href="./{_html_escape(row.get('pdf_file',''))}" target="_blank">查看 PDF</a>
    </div>
  </article>
"""


def _doc_dir_name_from_pdf_file(pdf_file):
    return pdf_file[:-4] if pdf_file.lower().endswith(".pdf") else pdf_file


def _topic_chips_papers():
    return [
        ("all", "全部"),
        ("anomaly", "异常检测"),
        ("rca", "根因分析"),
        ("forecast", "时序预测"),
        ("failure", "故障预测"),
        ("obs", "可观测性"),
        ("llm", "LLM"),
        ("log", "日志"),
        ("other", "其他"),
    ]


def _year_chips_for(years):
    return [("all", "全部")] + [(y, y) for y in sorted(set(years), reverse=True)]


def build_papers_index_html():
    css, js = load_alibaba_template()
    rows = load_papers_csv()
    cards = []
    years = []
    for row in rows:
        doc_dir = _doc_dir_name_from_pdf_file(row.get("pdf_file", ""))
        readme = (PAPERS_DIR / "docs" / doc_dir / "README.html")
        doc_fields = extract_doc_fields(readme.read_text(encoding="utf-8")) if readme.exists() else {"title": row.get("title",""), "summary": "", "topic": "other"}
        cards.append(render_paper_card(row, doc_fields, doc_dir))
        if row.get("year"):
            years.append(row["year"])
    # sort cards: year DESC, then etitle A-Z
    cards_sorted = sorted(
        cards,
        key=lambda c: (
            -int(re.search(r'data-year="(\d+)"', c).group(1)) if re.search(r'data-year="(\d+)"', c) else 0,
            re.search(r'<p class="etitle">([^<]*)</p>', c).group(1) if re.search(r'<p class="etitle">([^<]*)</p>', c) else ""
        )
    )
    topic_chips = _topic_chips_papers()
    year_chips = _year_chips_for(years)
    topic_chips_html = "\n".join(
        f'  <span class="chip{" active" if v=="all" else ""}" data-filter="topic" data-value="{v}">{lbl}</span>'
        for v, lbl in topic_chips
    )
    year_chips_html = "\n".join(
        f'  <span class="chip{" active" if v=="all" else ""}" data-filter="year" data-value="{v}">{lbl}</span>'
        for v, lbl in year_chips
    )
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>清华 NetMan AIOps Lab 论文 176 篇 · 索引</title>
<style>{css}</style>
</head>
<body>

<h1>📚 清华 NetMan AIOps 论文 176 篇</h1>
<p class="lead">清华大学网络管理与网络经济研究组（NetMan Lab）2014–2026 年 AIOps / 时序分析 / 系统可靠性代表性论文合集。</p>
<p class="top-links">
  <a href="../../README.md">⬅ 返回根 README</a>
  <a href="../alibaba/index.html">对比阿里 AIOps 16 篇</a>
  <a href="../pdfs/index.html">对比必示专利 30 件</a>
</p>

<h2>📊 数据速览</h2>
<div class="stats">
  <div class="stat-card"><div class="num">176</div><div class="label">论文总数</div></div>
  <div class="stat-card"><div class="num">2014–2026</div><div class="label">时间跨度</div></div>
  <div class="stat-card"><div class="num">176</div><div class="label">中文方案说明</div></div>
  <div class="stat-card"><div class="num">176 / 176</div><div class="label">PDF 已抓</div></div>
</div>

<h2>🔍 搜索 / 分类筛选</h2>
<div class="search-bar">
  <input type="text" id="search-input" placeholder="搜索论文标题、作者、关键词..." autocomplete="off">
</div>

<div class="chips">
  <span class="chips-label">方向：</span>
{topic_chips_html}
</div>

<div class="chips">
  <span class="chips-label">年份：</span>
{year_chips_html}
</div>

<p class="lead" id="result-count" aria-live="polite">显示全部 176 篇</p>

<h2>📄 176 篇论文（点击标题或按钮访问）</h2>
<div class="grid" id="paper-grid">
{''.join(cards_sorted)}
</div>

<footer>
  <h3>📎 附录：抓取与版权</h3>
  <ul>
    <li><b>抓取日期</b>：2026-06-08</li>
    <li><b>数据来源</b>：<a href="https://netman.aiops.org/publications/" target="_blank" rel="noopener">netman.aiops.org/publications</a></li>
    <li><b>版权说明</b>：所有 PDF 与方案说明仅用于学习研究目的，版权归原作者与出版方所有</li>
  </ul>
</footer>

<script>{js}</script>
</body>
</html>
"""
