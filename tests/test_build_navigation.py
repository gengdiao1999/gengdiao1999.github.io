import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from build_navigation import parse_summary, _convert_url, _clean_title, to_yaml

try:
    import yaml
except ImportError:
    yaml = None

SAMPLE_SUMMARY = """# 全书目录

## 基础篇：绪论与基础

- [第 1 章 绪论](part-00-fundamentals/01-introduction/README.md)
- [第 2 章 时间序列基础](part-00-fundamentals/02-time-series-basics/README.md)

## 附录

- [附录 A：论文](appendix/A-papers/README.md)
  - [清华 NetMan Lab 论文 176 篇](appendix/A-papers/netman/index.html)
"""


def test_clean_title_removes_bold():
    assert _clean_title("**第 3 章 特征提取**") == "第 3 章 特征提取"
    assert _clean_title("第 1 章 绪论") == "第 1 章 绪论"


def test_convert_url_md_to_directory():
    assert _convert_url("part-00-fundamentals/01-introduction/README.md") == "/book/part-00-fundamentals/01-introduction/"
    assert _convert_url("part-01-feature-extraction/03-statistical-features/README.md") == "/book/part-01-feature-extraction/03-statistical-features/"


def test_convert_url_html_keeps_filename():
    assert _convert_url("appendix/A-papers/netman/index.html") == "/book/appendix/A-papers/netman/index.html"


def test_parse_summary_structure():
    parts = parse_summary(SAMPLE_SUMMARY)
    assert len(parts) == 2
    assert parts[0]["title"] == "基础篇：绪论与基础"
    assert len(parts[0]["chapters"]) == 2
    assert parts[0]["chapters"][0] == {
        "title": "第 1 章 绪论",
        "url": "/book/part-00-fundamentals/01-introduction/",
    }
    assert parts[1]["title"] == "附录"
    assert len(parts[1]["chapters"]) == 1
    assert parts[1]["chapters"][0]["title"] == "附录 A：论文"


def test_to_yaml_is_valid_yaml():
    parts = [
        {
            "title": '附录：带"引号"和：冒号的篇',
            "chapters": [
                {"title": '第 1 章："特殊"标题', "url": "/book/chapter/"},
            ],
        }
    ]
    output = to_yaml(parts)
    if yaml is not None:
        parsed = yaml.safe_load(output)
        assert parsed == parts
    else:
        assert output  # Fallback path produces non-empty string.
