# 章页面侧边栏导航设计规格

*设计日期：2026-07-12*  
*对应实现：为书籍网站每一章页面增加左侧全局目录与右侧本章小节索引*

---

## 1. 设计目标

在现有 Jekyll / GitHub Pages 站点上，为每一章主页面（`book/part-NN-*/MM-*/README.md`）增加双侧边栏：

- **左侧**：展示全书「篇 → 章」层级导航，帮助读者在不同章节间快速跳转。
- **右侧**：展示当前章的「二级标题 → 三级标题」小节索引，支持展开/收起、点击跳转、滚动高亮。
- **响应式**：宽屏显示双栏，中等屏幕保留左侧目录，小屏幕折叠为顶部汉堡菜单。

实现过程不迁移站点、不引入 GitHub Pages 禁止的自定义 Ruby 插件，只通过 Jekyll 布局、Liquid 包含、`_data` 数据文件、CSS 与客户端 JavaScript 完成。

---

## 2. 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│  顶部标题栏（书名 + 移动端汉堡菜单）                           │
├──────────┬───────────────────────────────┬──────────────────┤
│          │                               │                  │
│ 左侧全局  │                               │  右侧本章        │
│ 章节目录  │      主内容区（Markdown）      │  小节索引        │
│ (Liquid) │                               │ (Client JS)      │
│          │                               │                  │
└──────────┴───────────────────────────────┴──────────────────┘
```

- **左侧数据来源**：`book/SUMMARY.md` 经 `tools/build_navigation.py` 解析，生成 `_data/navigation.yml`，构建时由 Liquid 渲染。
- **右侧数据来源**：页面加载后，JavaScript 扫描 `.book-content` 内的 `h2` / `h3` 标题动态生成。
- **样式与交互**：`assets/css/book-sidebar.css` 负责响应式布局与高亮；`assets/js/book-toc.js` 负责目录生成、展开/收起、滚动监听。

---

## 3. 新增与修改文件

### 3.1 新增文件

| 文件 | 作用 |
|------|------|
| `_layouts/chapter.html` | 章页面 HTML 骨架，包含左右侧栏容器 |
| `_includes/sidebar-left.html` | 用 `_data/navigation.yml` 渲染左侧全局目录 |
| `_includes/sidebar-right.html` | 右侧本章目录的 HTML 容器与标题 |
| `_data/navigation.yml` | 由 `SUMMARY.md` 生成的结构化导航数据（需提交） |
| `assets/css/book-sidebar.css` | 响应式布局、侧栏样式、高亮、折叠动画 |
| `assets/js/book-toc.js` | 扫描标题、生成右侧目录、展开/收起、滚动高亮 |
| `tools/build_navigation.py` | 解析 `book/SUMMARY.md` 并生成 `_data/navigation.yml` |
| `tests/test_build_navigation.py` | 导航生成脚本的单元测试 |

### 3.2 修改文件

| 文件 | 修改内容 |
|------|----------|
| `_config.yml` | 为 `book/part-*/**/README.md` 增加默认 `layout: chapter`；确保 Kramdown 标题 ID 生成开启 |
| `_includes/head-custom.html` | 无需修改；`chapter.html` 直接引入 `book-sidebar.css` |
| `CLAUDE.md` | 在「构建与验证」与「新增章节的检查清单」中补充 `tools/build_navigation.py` 步骤 |
| `README.md`（仓库根） | 可选：说明本地预览或构建顺序 |

---

## 4. 详细设计

### 4.1 `_layouts/chapter.html`

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  {% include head-custom.html %}
  <link rel="stylesheet" href="{{ '/assets/css/book-sidebar.css' | relative_url }}">
</head>
<body class="book-chapter">
  <header class="book-header">
    <button class="nav-toggle" aria-label="打开目录" aria-expanded="false">☰</button>
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

  <script src="{{ '/assets/js/book-toc.js' | relative_url }}"></script>
</body>
</html>
```

**要点**
- 不再继承 Cayman / Minimal 默认布局，因此 `head-custom.html` 必须保留 MathJax、rouge 样式等必要内容。
- 通过 `_config.yml` 的 `defaults` 为所有章 `README.md` 自动应用此布局，无需逐章加 frontmatter。

### 4.2 `_config.yml` 默认布局配置

```yaml
defaults:
  - scope:
      path: "book/part-*/**/README.md"
      type: "pages"
    values:
      layout: "chapter"
```

`book/README.md`、`book/SUMMARY.md`、附录 HTML 等路径不匹配，继续使用 Jekyll 默认布局。

### 4.3 `_data/navigation.yml` 与生成脚本

**数据格式**

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
    ...
```

**`tools/build_navigation.py` 解析规则**
- `## 标题` → 一个 part。
- `- [标题](路径)` → 一个 chapter。
- 链接以 `.md` 结尾时，去掉 `.md` 并转换为目录 URL（`README.md` → `/`）。
- 链接以 `.html` 结尾时保留原 URL。
- 清除标题中的 `**` 等 Markdown 标记。
- 附录结构与正文统一处理。

**运行命令**

```bash
python3 tools/build_navigation.py
```

**集成**
- 每次修改 `book/SUMMARY.md` 后运行，并提交生成的 `_data/navigation.yml`。
- 在 `CLAUDE.md` 构建流程和新增章节检查清单中补充此步骤。

### 4.4 `_includes/sidebar-left.html`

使用 Liquid 遍历 `_data/navigation.yml`：

```html
<nav class="nav-part" aria-label="全书目录">
  {% for part in site.data.navigation %}
    <div class="nav-part-item">
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

**要点**
- 当前章高亮通过 `page.url == chapter.url` 判断。
- 当前所在 part 可额外加 `expanded` 类（可选）。

### 4.5 `_includes/sidebar-right.html`

仅提供容器与标题：

```html
<nav class="toc-nav" aria-label="本章目录">
  <p class="toc-title">本章目录</p>
  <div id="toc-root">
    <!-- 由 book-toc.js 填充 -->
  </div>
</nav>
```

### 4.6 `assets/js/book-toc.js`

**执行时机**
- DOMContentLoaded 触发；若页面存在 `window.MathJax`，等待 `MathJax.typesetPromise()` 完成后再扫描标题，避免公式改变标题文本。

**扫描规则**
- 在 `.book-content` 内查找 `h2`、`h3`。
- 跳过 `h1`（页面主标题）。
- 为没有 `id` 的标题按文本生成稳定的 slug（Kramdown 通常会生成，此为兜底）。

**层级构建**
- `h2` 为一级节点，默认展开。
- 紧跟在 `h2` 后的 `h3` 作为该 `h2` 的子节点，默认折叠。
- 渲染结构示例：

```html
<ul class="toc-list">
  <li class="toc-h2 active">
    <button class="toc-toggle" aria-expanded="true">▾</button>
    <a href="#section-1">3.1 统计特征</a>
    <ul class="toc-h3-list">
      <li><a href="#section-1-1">3.1.1 基本统计量</a></li>
      ...
    </ul>
  </li>
</ul>
```

**交互**
- 点击 `h2` 旁的切换按钮：展开/收起其下的 `h3`。
- 点击目录项：平滑滚动到对应标题。
- 滚动监听（throttle/requestAnimationFrame）：高亮当前进入视口的标题，并自动展开其父 `h2`。

**降级**
- 若 JS 被禁用或执行失败，右侧栏保留「本章目录」标题，正文阅读不受影响。

### 4.7 `assets/css/book-sidebar.css`

**基础网格**

```css
.book-frame {
  display: grid;
  grid-template-columns: 260px 1fr 240px;
  min-height: calc(100vh - var(--header-height));
}
```

**断点策略**

| 断点 | 行为 |
|------|------|
| `≥1400px` | 左 260px + 主内容最大 900px + 右 240px |
| `1200px–1399px` | 左 240px + 主内容自适应 + 右 220px |
| `992px–1199px` | 隐藏右侧目录，保留左侧目录 |
| `768px–991px` | 左侧目录变为抽屉，通过汉堡按钮展开 |
| `<768px` | 双栏均隐藏，主内容全宽；汉堡菜单控制左侧抽屉 |

**关键样式**
- 侧栏 `position: sticky; top: var(--header-height); height: calc(100vh - var(--header-height)); overflow-y: auto;`
- 当前章高亮：左侧加 `3px` 主题色 `#0b5394` 竖线。
- 当前小节高亮：右侧文本加粗、左侧加强调色竖线。
- 三级标题默认 `display: none`，父级 `expanded` 后 `display: block`。
- 打印媒体查询隐藏侧栏与顶部按钮。

---

## 5. 构建与验证流程更新

在 `CLAUDE.md` 中补充：

```bash
# 生成章节目录数据
python3 tools/build_navigation.py

# 生成论文/专利索引
python3 tools/build_index.py

# 运行测试
python3 -m pytest tests/ -v
```

新增章节检查清单增加：

- [ ] 已运行 `tools/build_navigation.py` 并提交 `_data/navigation.yml`。
- [ ] 已通过 `pytest tests/test_build_navigation.py`。

---

## 6. 验收标准

- [ ] 所有章 `README.md` 页面渲染时带有左侧全局目录与右侧本章目录。
- [ ] 左侧目录结构与 `book/SUMMARY.md` 一致，当前章高亮正确。
- [ ] 右侧目录正确列出当前页所有 `h2` 与 `h3`，默认 `h2` 展开、`h3` 折叠。
- [ ] 点击右侧目录项可平滑滚动到对应小节。
- [ ] 滚动页面时，右侧目录自动高亮当前小节并展开其父 `h2`。
- [ ] 在 `1200px` 及以上屏幕显示双栏；在 `992px–1199px` 隐藏右侧栏；在 `<768px` 双栏隐藏并通过汉堡菜单展开左侧栏。
- [ ] `tools/build_navigation.py` 可由 `SUMMARY.md` 正确生成 `_data/navigation.yml`。
- [ ] `pytest tests/test_build_navigation.py` 全部通过。
- [ ] 修改 `SUMMARY.md` 后重新运行脚本并提交，导航数据保持同步。

---

## 7. 风险与回滚

| 风险 | 缓解措施 |
|------|----------|
| Jekyll 默认主题样式与新布局冲突 | 新布局不继承默认布局，CSS 从零控制主内容区基础样式 |
| 右侧目录依赖 JS | JS 失败时不阻塞正文；可考虑未来增加 Jekyll 插件方案作为 fallback |
| 作者忘记运行 `build_navigation.py` | 在 `CLAUDE.md` 检查清单与构建流程中强制要求；测试回归 |
| 移动端汉堡菜单遮挡内容 | 抽屉使用 `transform: translateX` + 遮罩层，点击外部关闭 |

---

## 8. 后续可扩展

- 在左侧目录增加搜索框，过滤章标题。
- 为右侧目录增加「返回顶部」按钮。
- 支持暗色模式切换，CSS 变量化管理颜色。
- 如未来迁移到文档生成器（VitePress / MkDocs），本设计的导航数据结构可直接复用。
