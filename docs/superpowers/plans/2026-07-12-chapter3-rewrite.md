# 第 3 章《特征提取》重写实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `book/part-01-feature-extraction/03-statistical-features/README.md` 按 3.1–3.6 特征主题结构重写，每个特征先给定义再讲算法，末尾以“本章小结”收尾；同时修复公式渲染配置。

**Architecture：** 保持现有 7 个 Python 脚本与配图不变，仅重写章主文件 `README.md` 与 `references.md`；新增 `_config.yml` 为 GitHub Pages 启用 MathJax，使 LaTeX 公式可在网页端渲染。

**Tech Stack：** Markdown (GFM)、LaTeX math、Jekyll/GitHub Pages、MathJax、Python（用于脚本复用验证）。

## Global Constraints

- 章节主文件使用一级标题 `# 第 3 章 特征提取`，避免多个一级标题。
- 小节使用 `##`、`###`、`####` 层级。
- 数学公式使用标准 LaTeX：行内 `$...$`，块级 `$$...$$`。
- 中文与英文/数字之间保留一个空格。
- 专有名词首次出现时加粗。
- 图片命名符合 `<chapter>-fig-NN-<short-desc>.png`。
- 代码块必须标注语言且可直接运行。
- 每章末尾必须包含 `## 本章小结`。
- 新增或修改后需通过 `pytest tests/test_build_index.py`。

---

## 文件改动清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `book/part-01-feature-extraction/03-statistical-features/README.md` | 重写 | 按 3.1–3.6 + 本章小结结构组织 |
| `book/part-01-feature-extraction/03-statistical-features/references.md` | 修改 | 调整引用顺序，补充缺失条目 |
| `book/SUMMARY.md` | 修改（如需要） | 确认第 3 章标题为“特征提取” |
| `_config.yml` | 新增 | 配置 Jekyll/MathJax 支持公式渲染 |

**保留不变：**
- `book/part-01-feature-extraction/03-statistical-features/assets/code/03-example-01-basic-stats.py`
- `book/part-01-feature-extraction/03-statistical-features/assets/code/03-example-02-rolling-stats.py`
- `book/part-01-feature-extraction/03-statistical-features/assets/code/03-example-03-stationarity-features.py`
- `book/part-01-feature-extraction/03-statistical-features/assets/code/03-example-04-seasonality-features.py`
- `book/part-01-feature-extraction/03-statistical-features/assets/code/03-example-05-trend-features.py`
- `book/part-01-feature-extraction/03-statistical-features/assets/code/03-example-06-periodicity-features.py`
- `book/part-01-feature-extraction/03-statistical-features/assets/code/03-example-07-frequency-features.py`
- `assets/images/` 下 7 张配图

---

### Task 1: 确认并调整 SUMMARY.md 第 3 章标题

**Files:**
- Read: `book/SUMMARY.md`
- Modify: `book/SUMMARY.md`（如标题不是“特征提取”）

**Interfaces:**
- Consumes: 无
- Produces: 更新后的目录条目

- [ ] **Step 1: 读取 SUMMARY.md**

```bash
cat book/SUMMARY.md
```

- [ ] **Step 2: 检查第 3 章标题**

查找形如 `- [第 3 章 XXX](...)` 的条目。

- [ ] **Step 3: 如需要，将标题改为“特征提取”**

例如将 `- [第 3 章 统计特征](...)` 改为 `- [第 3 章 特征提取](...)`。

- [ ] **Step 4: 提交**

```bash
git add book/SUMMARY.md
git commit -m "docs(chapter/03): update chapter title in SUMMARY to 特征提取"
```

---

### Task 2: 重写 README.md 主体内容

**Files:**
- Read: `docs/superpowers/specs/2026-07-12-chapter3-rewrite-design.md`
- Read: `book/part-01-feature-extraction/03-statistical-features/assets/code/*.py`
- Modify: `book/part-01-feature-extraction/03-statistical-features/README.md`

**Interfaces:**
- Consumes: 现有脚本输出、现有配图、references.md 引用键
- Produces: 新的章主文件

- [ ] **Step 1: 备份当前 README.md**

```bash
cp book/part-01-feature-extraction/03-statistical-features/README.md /tmp/README-chapter3-backup.md
```

- [ ] **Step 2: 写入新结构**

使用 `# 第 3 章 特征提取` 作为一级标题，随后按顺序写入：

```markdown
# 第 3 章 特征提取

特征提取是时间序列分析的首要步骤……

## 3.1 统计特征

### 3.1.1 基本统计量

### 3.1.2 分布形态特征

### 3.1.3 能量与计数特征

### 3.1.4 滑动窗口统计特征

## 3.2 平稳性特征

### 3.2.1 平稳性的定义与解释

### 3.2.2 ADF 检验

### 3.2.3 KPSS 检验

### 3.2.4 滚动统计量稳定性

## 3.3 季节性特征

### 3.3.1 季节性的定义与解释

### 3.3.2 季节性强度

### 3.3.3 周期内统计量

### 3.3.4 季节滞后自相关特征

## 3.4 趋势性特征

### 3.4.1 趋势性的定义与解释

### 3.4.2 线性趋势特征

### 3.4.3 趋势强度

### 3.4.4 Mann-Kendall 趋势检验

### 3.4.5 局部趋势变化特征

## 3.5 周期性特征

### 3.5.1 周期性的定义与解释

### 3.5.2 ACF 峰值法

### 3.5.3 周期图峰值法

### 3.5.4 滚动周期稳定性

## 3.6 频域特征

### 3.6.1 傅里叶变换特征

### 3.6.2 功率谱密度特征

### 3.6.3 频带能量特征

## 本章小结

## 参考与延伸阅读

- [](./references.md)
- [附录 A：相关论文](../appendix/A-papers/README.md)
```

- [ ] **Step 3: 填充 3.1 统计特征内容**

从现有 README 的“6. 统计特征”小节迁移内容，保留公式、代码、图片引用，仅调整标题层级。

- [ ] **Step 4: 填充 3.2 平稳性特征内容**

先写定义与解释（严平稳、宽平稳、工程意义），再迁移 ADF/KPSS/滚动统计量内容。

- [ ] **Step 5: 填充 3.3 季节性特征内容**

先写定义与解释（固定时间间隔重复模式，与周期性的区别），再迁移 STL/周期内统计量/季节滞后 ACF 内容。

- [ ] **Step 6: 填充 3.4 趋势性特征内容**

先写定义与解释（长期上升/下降/稳定倾向，与季节性的区别），再迁移线性趋势/趋势强度/Mann-Kendall/局部趋势内容。

- [ ] **Step 7: 填充 3.5 周期性特征内容**

先写定义与解释（重复波动模式，周期可与日历无关，与季节性的区别），再迁移 ACF 峰值法/周期图法/滚动周期稳定性内容。

- [ ] **Step 8: 填充 3.6 频域特征内容**

迁移现有频域特征内容（FFT、Welch PSD、频带能量）。

- [ ] **Step 9: 撰写“本章小结”**

回顾 3.1–3.6 核心思想，指出特征组合与任务适配的重要性，提示后续章节。

- [ ] **Step 10: 检查并修正 LaTeX 公式**

重点检查：
- 行内公式用 `$...$`，块级用 `$$...$$`。
- 多行公式 `aligned` 环境中 `\\` 正确转义。
- 避免使用非标准宏。
- 检查 `	ext{Var}`、`mod` 等标准宏。

- [ ] **Step 11: 提交**

```bash
git add book/part-01-feature-extraction/03-statistical-features/README.md
git commit -m "docs(chapter/03): rewrite README with 3.1-3.6 topic-based structure"
```

---

### Task 3: 更新 references.md

**Files:**
- Read: `book/part-01-feature-extraction/03-statistical-features/references.md`
- Modify: `book/part-01-feature-extraction/03-statistical-features/references.md`

**Interfaces:**
- Consumes: 新 README.md 中使用的引用键
- Produces: 更新后的引用条目列表

- [ ] **Step 1: 读取当前 references.md**

```bash
cat book/part-01-feature-extraction/03-statistical-features/references.md
```

- [ ] **Step 2: 检查新 README 中使用的引用键**

从 README.md 中提取所有 `[^key]`。

- [ ] **Step 3: 补充缺失引用条目**

确保以下关键引用存在：
- `[^christ2018tsfresh]`
- `[^mckinney2011pandas]`
- `[^dickey1979adf]`
- `[^kwiatkowski1992kpss]`
- `[^cleveland1990stl]`
- `[^mann1945trend]`

- [ ] **Step 4: 调整引用顺序**

可按 README.md 中首次出现顺序排列。

- [ ] **Step 5: 提交**

```bash
git add book/part-01-feature-extraction/03-statistical-features/references.md
git commit -m "docs(chapter/03): update references order and add missing entries"
```

---

### Task 4: 添加 MathJax 公式渲染配置

**Files:**
- Create: `_config.yml`
- Create: `assets/js/mathjax-config.js`（可选）
- Modify: 无

**Interfaces:**
- Consumes: 无
- Produces: GitHub Pages MathJax 渲染能力

- [ ] **Step 1: 检查是否已存在 _config.yml**

```bash
ls -la _config.yml 2>/dev/null || echo "not exists"
```

- [ ] **Step 2: 创建 _config.yml**

```yaml
title: 时间序列分析：从特征到因果
description: 面向工程与研究人员的中文技术书籍
markdown: kramdown
kramdown:
  math_engine: mathjax
  syntax_highlighter: rouge
```

若 kramdown 的 `math_engine: mathjax` 不足以让 GitHub Pages 自动加载 MathJax JS，则追加 include 配置：

```yaml
head_scripts:
  - https://polyfill.io/v3/polyfill.min.js?features=es6
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js
```

或创建包含 MathJax 配置的 include 文件 `_includes/head-custom.html`。

- [ ] **Step 3: 创建 head-custom.html（如需要）**

```html
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<script>
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']]
  }
};
</script>
```

- [ ] **Step 4: 提交**

```bash
git add _config.yml
git commit -m "docs(site): add Jekyll/MathJax config for LaTeX formula rendering"
```

---

### Task 5: 验证测试与构建

**Files:**
- Run: `pytest tests/test_build_index.py`
- Run: `python3 tools/build_index.py`

**Interfaces:**
- Consumes: 修改后的 Markdown 文件
- Produces: 测试结果

- [ ] **Step 1: 运行索引构建测试**

```bash
python3 -m pytest tests/test_build_index.py -v
```

Expected: all tests pass.

- [ ] **Step 2: 重新生成论文/专利索引**

```bash
python3 tools/build_index.py
```

Expected: 无报错，HTML 文件更新。

- [ ] **Step 3: 检查 README.md 渲染**

本地可用任意 Markdown 预览器查看公式是否正常显示；重点检查 `$$...$$` 块级公式和 `$...$` 行内公式。

- [ ] **Step 4: 提交（如索引有更新）**

```bash
git add book/appendix/A-papers/index.html book/appendix/B-patents/index.html
git commit -m "chore: rebuild paper and patent indexes"
```

---

## 自我审查

**1. Spec coverage:**
- 3.1–3.6 结构 → Task 2
- 每个特征定义与解释 → Task 2 Step 4–8
- 本章小结 → Task 2 Step 9
- 公式正确性 → Task 2 Step 10
- 网页公式渲染 → Task 4
- references.md 更新 → Task 3
- SUMMARY.md 确认 → Task 1
- 测试通过 → Task 5

**2. Placeholder scan:** 无 TBD/TODO/实现稍后。

**3. Type consistency:** 不适用（纯 Markdown/文档任务）。

---

## 执行方式

计划已完成并保存到 `docs/superpowers/plans/2026-07-12-chapter3-rewrite.md`。

**两种执行方式：**

1. **Subagent-Driven（推荐）**：每个 Task 派一个独立子代理执行，我负责审阅。
2. **Inline Execution**：在当前会话中顺序执行，适合内容写作类任务，可保持上下文连贯。

**建议采用 Inline Execution**，因为本任务主要是单文件 Markdown 重写，上下文连贯性更重要。
