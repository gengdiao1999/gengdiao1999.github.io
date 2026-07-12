"""
tools/build_navigation.py
Parse book/SUMMARY.md and generate _data/navigation.yml.
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SUMMARY_PATH = REPO_ROOT / "book" / "SUMMARY.md"
OUTPUT_PATH = REPO_ROOT / "_data" / "navigation.yml"


def _clean_title(title: str) -> str:
    """Remove markdown bold markers and surrounding whitespace."""
    return title.replace("**", "").strip()


def _convert_url(url: str) -> str:
    """Convert a link relative to book/SUMMARY.md into a site-relative URL."""
    url = url.strip()
    if url.endswith(".md"):
        url = url[:-3]
        if url.endswith("/README"):
            url = url[:-7]
        if not url.startswith("/"):
            url = "/book/" + url
        if not url.endswith("/"):
            url += "/"
    else:
        if not url.startswith("/"):
            url = "/book/" + url
    return url


def parse_summary(text: str) -> list[dict]:
    """Parse SUMMARY.md into a list of parts, each containing chapters."""
    parts = []
    current_part = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        part_match = re.match(r"^##\s+(.*)$", line)
        if part_match:
            if current_part is not None:
                parts.append(current_part)
            current_part = {
                "title": part_match.group(1).strip(),
                "chapters": [],
            }
            continue

        chapter_match = re.match(r"^[-*]\s+\[([^\]]+)\]\(([^)]+)\)$", line)
        if chapter_match and current_part is not None:
            title = chapter_match.group(1)
            url = chapter_match.group(2)
            current_part["chapters"].append({
                "title": _clean_title(title),
                "url": _convert_url(url),
            })

    if current_part is not None:
        parts.append(current_part)

    return parts


def to_yaml(parts: list[dict]) -> str:
    """Serialize parts to a minimal YAML string."""
    lines = []
    for part in parts:
        title = part["title"]
        if ":" in title:
            title = f'"{title}"'
        lines.append(f"- title: {title}")
        lines.append("  chapters:")
        for chapter in part["chapters"]:
            ct = chapter["title"]
            if ":" in ct:
                ct = f'"{ct}"'
            lines.append(f"    - title: {ct}")
            lines.append(f"      url: {chapter['url']}")
    return "\n".join(lines) + "\n"


def main():
    text = SUMMARY_PATH.read_text(encoding="utf-8")
    parts = parse_summary(text)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(to_yaml(parts), encoding="utf-8")
    print(f"Generated {OUTPUT_PATH} with {len(parts)} parts.")


if __name__ == "__main__":
    main()
