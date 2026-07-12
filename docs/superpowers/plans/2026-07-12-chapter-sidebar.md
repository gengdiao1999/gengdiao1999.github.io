# 章页面侧边栏导航实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在现有 Jekyll / GitHub Pages 站点上为每一章主页面增加左侧全局目录与右侧本章小节索引，并实现响应式折叠。

**Architecture：** 新增 Jekyll 布局 `_layouts/chapter.html` 包裹章 `README.md`；左侧导航数据由 `tools/build_navigation.py` 从 `book/SUMMARY.md` 生成并写入 `_data/navigation.yml`，构建时用 Liquid 渲染；右侧目录由 `assets/js/book-toc.js` 在页面加载后扫描 `h2`/`h3` 动态生成；布局与交互样式由 `assets/css/book-sidebar.css` 控制。

**Tech Stack：** Jekyll (GitHub Pages), Liquid, Python 3, YAML, HTML, CSS, JavaScript (ES6).

## Global Constraints

- 不引入 GitHub Pages 禁止的自定义 Ruby 插件。
- `book/SUMMARY.md` 保持唯一手写目录数据源。
- 所有新增文件路径遵循仓库现有约定（`_layouts/`、`_includes/`、`_data/`、`assets/`、`tools/`、`tests/`）。
- 提交信息使用语义化前缀，例如 `feat(sidebar): ...`、`docs(claude): ...`、`test(sidebar): ...`。
- 修改 `SUMMARY.md` 后必须重新运行 `tools/build_navigation.py` 并提交 `_data/navigation.yml`。
- 图片、代码、数据目录不受本次改动影响。

---

## 文件结构总览

### 新增文件

- `tools/build_navigation.py`：解析 `book/SUMMARY.md` 生成 `_data/navigation.yml`。
- `tests/test_build_navigation.py`：`build_navigation.py` 的单元测试。
- `_data/navigation.yml`：构建产物，由脚本生成。
- `_layouts/chapter.html`：章页面布局骨架。
- `_includes/sidebar-left.html`：左侧全局目录 Liquid 片段。
- `_includes/sidebar-right.html`：右侧本章目录容器。
- `assets/css/book-sidebar.css`：响应式布局与侧栏样式。
- `assets/js/book-toc.js`：客户端目录生成、展开/收起、滚动高亮、移动端菜单。

### 修改文件

- `_config.yml`：为 `book/part-*/**/README.md` 增加默认 `layout: chapter`。
- `CLAUDE.md`：在「构建与验证」和「新增章节的检查清单」中补充导航生成步骤。

---

## Task 1：导航数据生成脚本（TDD）

**Files：**
- Create: `tests/test_build_navigation.py`
- Create: `tools/build_navigation.py`

**Interfaces：**
- Consumes: `book/SUMMARY.md`（现有文件）
- Produces: `_data/navigation.yml`（Task 2 生成）

- [ ] **Step 1：编写失败的测试**

  创建 `tests/test_build_navigation.py`：

  ```python
  import sys
  from pathlib import Path

  sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

  from build_navigation import parse_summary, _convert_url, _clean_title

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
  ```

- [ ] **Step 2：运行测试以确认失败**

  Run: `python3 -m pytest tests/test_build_navigation.py -v`
  Expected: `ModuleNotFoundError: No module named 'build_navigation'`（因为脚本尚未创建）

- [ ] **Step 3：实现最小脚本**

  创建 `tools/build_navigation.py`：

  ```python
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

          chapter_match = re.match(r"^[-*]\s+\[([^\]]+)\]\(([^)]+)\)$", line.strip())
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
  ```

- [ ] **Step 4：运行测试以确认通过**

  Run: `python3 -m pytest tests/test_build_navigation.py -v`
  Expected: `4 passed`

- [ ] **Step 5：提交**

  ```bash
  git add tests/test_build_navigation.py tools/build_navigation.py
  git commit -m "feat(sidebar): add navigation data generator with tests"
  ```

---

## Task 2：生成并提交 `_data/navigation.yml`

**Files：**
- Create: `_data/navigation.yml`

**Interfaces：**
- Consumes: `tools/build_navigation.py` from Task 1
- Produces: `_data/navigation.yml` consumed by `_includes/sidebar-left.html` in Task 4

- [ ] **Step 1：运行生成脚本**

  Run: `python3 tools/build_navigation.py`
  Expected: `Generated /app/study/gengdiao1999.github.io/_data/navigation.yml with 9 parts.`

- [ ] **Step 2：验证生成文件内容**

  Run: `head -n 15 _data/navigation.yml`
  Expected:
  ```yaml
  - title: 基础篇：绪论与基础
    chapters:
      - title: 第 1 章 绪论
        url: /book/part-00-fundamentals/01-introduction/
      - title: 第 2 章 时间序列基础
        url: /book/part-00-fundamentals/02-time-series-basics/
  - title: 第一篇：特征提取
    chapters:
      - title: 第 3 章 特征提取
        url: /book/part-01-feature-extraction/03-statistical-features/
  ```

- [ ] **Step 3：提交**

  ```bash
  git add _data/navigation.yml
  git commit -m "chore(sidebar): generate navigation data from SUMMARY.md"
  ```

---

## Task 3：创建章页面布局与侧栏包含片段

**Files：**
- Create: `_layouts/chapter.html`
- Create: `_includes/sidebar-left.html`
- Create: `_includes/sidebar-right.html`

**Interfaces：**
- Consumes: `_data/navigation.yml` from Task 2
- Produces: HTML layout used by all chapter pages

- [ ] **Step 1：创建 `_layouts/chapter.html`**

  ```html
  ---
  ---
  <!DOCTYPE html>
  <html lang="zh-CN">
  <head>
    {% include head-custom.html %}
    <link rel="stylesheet" href="{{ '/assets/css/book-sidebar.css' | relative_url }}">
  </head>
  <body class="book-chapter">
    <header class="book-header">
      <button class="nav-toggle" id="nav-toggle" aria-label="打开目录" aria-expanded="false">☰</button>
      <a class="book-title" href="{{ '/' | relative_url }}">时间序列分析：从特征到因果</a>
    </header>

    <div class="book-frame">
      <aside class="sidebar-left" id="sidebar-left">
        {% include sidebar-left.html %}
      </aside>

      <main class="book-main">
        <article class="book-content">
          {{ content }}
        </article>
      </main>

      <aside class="sidebar-right" id="sidebar-right">
        {% include sidebar-right.html %}
      </aside>
    </div>

    <div class="overlay" id="overlay"></div>
    <script src="{{ '/assets/js/book-toc.js' | relative_url }}"></script>
  </body>
  </html>
  ```

- [ ] **Step 2：创建 `_includes/sidebar-left.html`**

  ```html
  <nav class="nav-global" aria-label="全书目录">
    {% for part in site.data.navigation %}
      <div class="nav-part">
        <p class="nav-part-title">{{ part.title }}</p>
        <ul class="nav-chapter-list">
          {% for chapter in part.chapters %}
            <li class="nav-chapter-item{% if page.url == chapter.url %} active{% endif %}">
              <a href="{{ chapter.url | relative_url }}">{{ chapter.title }}</a>
            </li>
          {% endfor %}
        </ul>
      </div>
    {% endfor %}
  </nav>
  ```

- [ ] **Step 3：创建 `_includes/sidebar-right.html`**

  ```html
  <nav class="toc-nav" aria-label="本章目录">
    <p class="toc-title">本章目录</p>
    <div id="toc-root"></div>
  </nav>
  ```

- [ ] **Step 4：验证文件存在**

  Run:
  ```bash
  test -f _layouts/chapter.html && echo "chapter.html OK"
  test -f _includes/sidebar-left.html && echo "sidebar-left OK"
  test -f _includes/sidebar-right.html && echo "sidebar-right OK"
  ```
  Expected:
  ```
  chapter.html OK
  sidebar-left OK
  sidebar-right OK
  ```

- [ ] **Step 5：提交**

  ```bash
  git add _layouts/chapter.html _includes/sidebar-left.html _includes/sidebar-right.html
  git commit -m "feat(sidebar): add chapter layout and sidebar includes"
  ```

---

## Task 4：编写响应式样式

**Files：**
- Create: `assets/css/book-sidebar.css`

**Interfaces：**
- Consumes: `_layouts/chapter.html` selectors (`.book-chapter`, `.book-frame`, etc.)
- Produces: Styles applied to all chapter pages

- [ ] **Step 1：创建 `assets/css/book-sidebar.css`**

  ```css
  :root {
    --header-height: 56px;
    --sidebar-left-width: 260px;
    --sidebar-right-width: 240px;
    --content-max-width: 900px;
    --primary-color: #0b5394;
    --accent-color: #e69138;
    --bg-color: #f8f9fa;
    --border-color: #e1e4e8;
    --text-color: #24292f;
    --muted-color: #6e7781;
  }

  * {
    box-sizing: border-box;
  }

  html {
    scroll-behavior: smooth;
  }

  body.book-chapter {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans CJK SC", "PingFang SC", "Microsoft YaHei", sans-serif;
    color: var(--text-color);
    line-height: 1.6;
    background: #fff;
  }

  .book-header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: var(--header-height);
    display: flex;
    align-items: center;
    padding: 0 1rem;
    background: #fff;
    border-bottom: 1px solid var(--border-color);
    z-index: 100;
  }

  .nav-toggle {
    display: none;
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    margin-right: 0.75rem;
    padding: 0;
    color: var(--text-color);
  }

  .book-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-color);
    text-decoration: none;
  }

  .book-title:hover {
    color: var(--primary-color);
  }

  .book-frame {
    display: grid;
    grid-template-columns: var(--sidebar-left-width) 1fr var(--sidebar-right-width);
    margin-top: var(--header-height);
    min-height: calc(100vh - var(--header-height));
  }

  .sidebar-left,
  .sidebar-right {
    position: sticky;
    top: var(--header-height);
    height: calc(100vh - var(--header-height));
    overflow-y: auto;
    padding: 1.5rem 1rem;
    background: var(--bg-color);
    border-right: 1px solid var(--border-color);
  }

  .sidebar-right {
    border-right: none;
    border-left: 1px solid var(--border-color);
  }

  .book-main {
    display: flex;
    justify-content: center;
    padding: 2rem 2.5rem;
  }

  .book-content {
    width: 100%;
    max-width: var(--content-max-width);
  }

  /* Left navigation */
  .nav-global {
    font-size: 0.875rem;
  }

  .nav-part {
    margin-bottom: 1.25rem;
  }

  .nav-part-title {
    font-weight: 600;
    color: var(--muted-color);
    margin: 0 0 0.5rem 0;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.02em;
  }

  .nav-chapter-list {
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .nav-chapter-item {
    margin: 0.25rem 0;
  }

  .nav-chapter-item a {
    display: block;
    padding: 0.35rem 0.5rem;
    color: var(--text-color);
    text-decoration: none;
    border-radius: 4px;
  }

  .nav-chapter-item a:hover {
    background: rgba(11, 81, 148, 0.08);
    color: var(--primary-color);
  }

  .nav-chapter-item.active a {
    background: rgba(11, 81, 148, 0.12);
    color: var(--primary-color);
    font-weight: 500;
  }

  /* Right TOC */
  .toc-nav {
    font-size: 0.8125rem;
  }

  .toc-title {
    font-weight: 600;
    margin: 0 0 0.75rem 0;
    color: var(--text-color);
    font-size: 0.875rem;
  }

  .toc-list {
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .toc-h2 {
    margin: 0.5rem 0;
  }

  .toc-h2 > a {
    display: inline-block;
    padding: 0.25rem 0;
    color: var(--text-color);
    text-decoration: none;
    border-left: 3px solid transparent;
    padding-left: 0.5rem;
  }

  .toc-h2 > a:hover {
    color: var(--primary-color);
  }

  .toc-h2.active > a {
    color: var(--primary-color);
    font-weight: 500;
    border-left-color: var(--accent-color);
  }

  .toc-toggle {
    display: inline-block;
    width: 1rem;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    margin-right: 0.25rem;
    color: var(--muted-color);
    font-size: 0.75rem;
  }

  .toc-h3-list {
    list-style: none;
    margin: 0;
    padding: 0 0 0 1.25rem;
    display: none;
  }

  .toc-h2.expanded .toc-h3-list {
    display: block;
  }

  .toc-h3-list li {
    margin: 0.25rem 0;
  }

  .toc-h3-list a {
    display: block;
    padding: 0.2rem 0;
    color: var(--muted-color);
    text-decoration: none;
    border-left: 3px solid transparent;
    padding-left: 0.5rem;
  }

  .toc-h3-list a:hover,
  .toc-h3-list li.active a {
    color: var(--primary-color);
  }

  .toc-h3-list li.active a {
    border-left-color: var(--accent-color);
  }

  /* Overlay for mobile */
  .overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    z-index: 150;
  }

  /* Responsive */
  @media (max-width: 1399px) {
    .book-frame {
      grid-template-columns: 240px 1fr 220px;
    }
  }

  @media (max-width: 1199px) {
    .book-frame {
      grid-template-columns: 240px 1fr;
    }
    .sidebar-right {
      display: none;
    }
  }

  @media (max-width: 991px) {
    .nav-toggle {
      display: block;
    }

    .book-frame {
      grid-template-columns: 1fr;
    }

    .sidebar-left {
      position: fixed;
      top: var(--header-height);
      left: 0;
      width: 260px;
      transform: translateX(-100%);
      transition: transform 0.2s ease;
      z-index: 200;
    }

    .sidebar-left.open {
      transform: translateX(0);
    }

    .overlay.show {
      display: block;
    }
  }

  @media (max-width: 767px) {
    .book-main {
      padding: 1.25rem 1rem;
    }
  }

  /* Print */
  @media print {
    .book-header,
    .sidebar-left,
    .sidebar-right,
    .nav-toggle,
    .overlay {
      display: none !important;
    }

    .book-frame {
      display: block;
      margin-top: 0;
    }

    .book-main {
      padding: 0;
    }
  }
  ```

- [ ] **Step 2：验证 CSS 文件存在**

  Run: `test -f assets/css/book-sidebar.css && echo "CSS OK"`
  Expected: `CSS OK`

- [ ] **Step 3：提交**

  ```bash
  git add assets/css/book-sidebar.css
  git commit -m "feat(sidebar): add responsive sidebar styles"
  ```

---

## Task 5：编写客户端目录脚本

**Files：**
- Create: `assets/js/book-toc.js`

**Interfaces：**
- Consumes: `.book-content` headings (`h2`, `h3`) and `#toc-root` container
- Produces: Populated right-hand table of contents with scroll spy

- [ ] **Step 1：创建 `assets/js/book-toc.js`**

  ```javascript
  (function () {
    "use strict";

    const TOC_ROOT_ID = "toc-root";
    const CONTENT_SELECTOR = ".book-content";
    const HEADING_SELECTORS = "h2, h3";

    function slugify(text) {
      return text
        .toLowerCase()
        .replace(/\s+/g, "-")
        .replace(/[^\w\-]/g, "")
        .replace(/-+/g, "-")
        .substring(0, 64);
    }

    function ensureHeadingId(heading) {
      if (!heading.id) {
        const text = heading.textContent.trim();
        heading.id = "section-" + slugify(text);
      }
      return heading.id;
    }

    function buildTree(headings) {
      const root = [];
      let currentH2 = null;

      headings.forEach(function (heading) {
        const level = parseInt(heading.tagName[1], 10);
        const node = {
          level: level,
          text: heading.textContent.trim(),
          id: ensureHeadingId(heading),
        };

        if (level === 2) {
          currentH2 = Object.assign({}, node, { children: [] });
          root.push(currentH2);
        } else if (level === 3 && currentH2) {
          currentH2.children.push(node);
        }
      });

      return root;
    }

    function renderToc(tree) {
      const rootEl = document.getElementById(TOC_ROOT_ID);
      if (!rootEl || tree.length === 0) return;

      const ul = document.createElement("ul");
      ul.className = "toc-list";

      tree.forEach(function (h2) {
        const li = document.createElement("li");
        li.className = "toc-h2 expanded";
        li.dataset.target = h2.id;

        const toggle = document.createElement("button");
        toggle.className = "toc-toggle";
        toggle.setAttribute("aria-expanded", "true");
        toggle.textContent = "▾";
        toggle.addEventListener("click", function (e) {
          e.preventDefault();
          const isExpanded = li.classList.contains("expanded");
          li.classList.toggle("expanded", !isExpanded);
          toggle.setAttribute("aria-expanded", String(!isExpanded));
          toggle.textContent = isExpanded ? "▸" : "▾";
        });

        const link = document.createElement("a");
        link.href = "#" + h2.id;
        link.textContent = h2.text;

        li.appendChild(toggle);
        li.appendChild(link);

        if (h2.children.length > 0) {
          const subUl = document.createElement("ul");
          subUl.className = "toc-h3-list";

          h2.children.forEach(function (h3) {
            const subLi = document.createElement("li");
            subLi.dataset.target = h3.id;

            const subLink = document.createElement("a");
            subLink.href = "#" + h3.id;
            subLink.textContent = h3.text;

            subLi.appendChild(subLink);
            subUl.appendChild(subLi);
          });

          li.appendChild(subUl);
        }

        ul.appendChild(li);
      });

      rootEl.appendChild(ul);
    }

    function setupScrollSpy(headings) {
      const tocItems = document.querySelectorAll("[data-target]");
      if (tocItems.length === 0) return;

      const observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              const id = entry.target.id;
              tocItems.forEach(function (item) {
                item.classList.toggle("active", item.dataset.target === id);
              });

              const activeH3 = document.querySelector(
                '.toc-h3-list li[data-target="' + id + '"]'
              );
              if (activeH3) {
                const h2Li = activeH3.closest(".toc-h2");
                if (h2Li && !h2Li.classList.contains("expanded")) {
                  h2Li.classList.add("expanded");
                  const toggle = h2Li.querySelector(".toc-toggle");
                  if (toggle) {
                    toggle.setAttribute("aria-expanded", "true");
                    toggle.textContent = "▾";
                  }
                }
              }
            }
          });
        },
        {
          rootMargin: "-80px 0px -60% 0px",
          threshold: 0,
        }
      );

      headings.forEach(function (heading) {
        observer.observe(heading);
      });
    }

    function setupMobileNav() {
      const toggle = document.getElementById("nav-toggle");
      const sidebar = document.getElementById("sidebar-left");
      const overlay = document.getElementById("overlay");

      if (!toggle || !sidebar || !overlay) return;

      function open() {
        sidebar.classList.add("open");
        overlay.classList.add("show");
        toggle.setAttribute("aria-expanded", "true");
      }

      function close() {
        sidebar.classList.remove("open");
        overlay.classList.remove("show");
        toggle.setAttribute("aria-expanded", "false");
      }

      toggle.addEventListener("click", function () {
        if (sidebar.classList.contains("open")) {
          close();
        } else {
          open();
        }
      });

      overlay.addEventListener("click", close);
    }

    function init() {
      if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise().then(run).catch(run);
      } else {
        run();
      }
    }

    function run() {
      const content = document.querySelector(CONTENT_SELECTOR);
      if (!content) return;

      const headings = Array.from(content.querySelectorAll(HEADING_SELECTORS));
      const tree = buildTree(headings);
      renderToc(tree);
      setupScrollSpy(headings);
      setupMobileNav();
    }

    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", init);
    } else {
      init();
    }
  })();
  ```

- [ ] **Step 2：验证 JS 语法**

  Run: `node --check assets/js/book-toc.js`
  Expected: 无输出且退出码为 0（表示语法检查通过）

- [ ] **Step 3：提交**

  ```bash
  git add assets/js/book-toc.js
  git commit -m "feat(sidebar): add client-side chapter TOC script"
  ```

---

## Task 6：更新 `_config.yml` 应用布局

**Files：**
- Modify: `_config.yml`

**Interfaces：**
- Consumes: `_layouts/chapter.html` from Task 3
- Produces: All chapter READMEs use the chapter layout by default

- [ ] **Step 1：在 `_config.yml` 末尾添加 defaults**

  修改 `_config.yml`，在文件末尾追加：

  ```yaml
  defaults:
    - scope:
        path: "book/part-*/**/README.md"
        type: "pages"
      values:
        layout: "chapter"
  ```

- [ ] **Step 2：验证 YAML 语法**

  Run: `python3 -c "import yaml; yaml.safe_load(open('_config.yml'))" && echo "YAML OK"`
  Expected: `YAML OK`

- [ ] **Step 3：提交**

  ```bash
  git add _config.yml
  git commit -m "feat(sidebar): apply chapter layout to all part READMEs"
  ```

---

## Task 7：更新 `CLAUDE.md` 构建流程与检查清单

**Files：**
- Modify: `CLAUDE.md`

**Interfaces：**
- Consumes: `tools/build_navigation.py` from Task 1
- Produces: Updated project conventions

- [ ] **Step 1：更新「构建与验证」小节**

  找到 `CLAUDE.md` 中第 8.1 节「生成索引」部分，替换为：

  ```markdown
  ### 8.1 生成索引与导航

  ```bash
  python3 tools/build_navigation.py      # 生成章节目录数据
  python3 tools/build_index.py           # 论文 + 专利
  python3 tools/build_index.py papers    # 仅论文
  python3 tools/build_index.py pdfs      # 仅专利
  ```
  ```

  （注意保留代码块语法，即外层使用 ````markdown` 包裹时内部代码块使用 ```。）

- [ ] **Step 2：更新「运行测试」小节**

  将 8.2 节：
  ```markdown
  ### 8.2 运行测试

  ```bash
  python3 -m pytest tests/test_build_index.py -v
  ```
  ```
  替换为：
  ```markdown
  ### 8.2 运行测试

  ```bash
  python3 -m pytest tests/ -v
  ```
  ```
  ```

- [ ] **Step 3：更新「新增章节的检查清单」**

  在第 10 节清单末尾增加两项：

  ```markdown
  - [ ] 已运行 `tools/build_navigation.py` 并提交 `_data/navigation.yml`。
  - [ ] 已通过 `pytest tests/test_build_navigation.py`。
  ```

- [ ] **Step 4：提交**

  ```bash
  git add CLAUDE.md
  git commit -m "docs(claude): add sidebar navigation to build workflow and checklist"
  ```

---

## Task 8：集成验证

**Files：**
- All files created/modified in Tasks 1–7

**Interfaces：**
- Consumes: Complete sidebar implementation
- Produces: Verified working feature

- [ ] **Step 1：运行全部 Python 测试**

  Run: `python3 -m pytest tests/ -v`
  Expected: `tests/test_build_index.py` 与 `tests/test_build_navigation.py` 均通过。

- [ ] **Step 2：重新生成导航数据**

  Run: `python3 tools/build_navigation.py`
  Expected: 成功生成 `_data/navigation.yml`。

- [ ] **Step 3：检查文件清单**

  Run:
  ```bash
  for f in _data/navigation.yml _layouts/chapter.html _includes/sidebar-left.html _includes/sidebar-right.html assets/css/book-sidebar.css assets/js/book-toc.js; do
    test -f "$f" && echo "OK $f" || echo "MISSING $f"
  done
  ```
  Expected：全部输出 `OK ...`

- [ ] **Step 4：可选本地 Jekyll 构建验证**

  如果本地已安装 Jekyll：
  Run: `bundle exec jekyll build --destination _site`
  Expected: 构建成功，`_site/book/part-01-feature-extraction/03-statistical-features/index.html` 包含侧栏相关 HTML。

  如果未安装 Jekyll，跳过此步骤并在提交信息中注明未做本地构建验证。

- [ ] **Step 5：最终提交或完成标记**

  如果还有未提交的改动：
  ```bash
  git add -A
  git commit -m "feat(sidebar): complete chapter sidebar navigation"
  ```

---

## 自我检查清单

- [ ] Spec coverage：`book/SUMMARY.md` 解析、`_data/navigation.yml` 生成、布局模板、Liquid 包含片段、CSS、JS、`_config.yml` 默认布局、`CLAUDE.md` 更新均有对应任务。
- [ ] 每个任务都有明确的文件创建/修改清单与验证命令。
- [ ] 每个代码任务都包含可运行的完整代码。
- [ ] 无 TBD/TODO/占位符。
- [ ] 文件路径与命名符合仓库规范。
- [ ] 提交信息符合 CLAUDE.md 的语义化前缀。
