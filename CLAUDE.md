# CLAUDE.md — 时间序列书籍编写规范

本文件是《时间序列分析：从特征到因果》一书的编写规范。所有贡献者在新增或修改章节前应阅读并遵守本规范。

---

## 1. 项目目标

将本仓库重构为一部**面向工程与研究人员的中文技术书籍**，覆盖时间序列分析的核心主题：

- 特征提取
- 时域分析
- 频域分析
- 时序分类
- 时序异常检测
- 时序预测（单指标 / 多指标）
- 时序因果分析

原仓库中的论文与专利作为附录 A、B 保留，供正文引用与延伸阅读。

---

## 2. 目录结构

```
/
├── README.md                 # 仓库入口：书籍总览与阅读路线
├── CLAUDE.md                 # 本文件：编写规范
├── book/                     # 书籍正文
│   ├── README.md             # 前言
│   ├── SUMMARY.md            # 全书目录
│   ├── part-NN-<name>/       # 篇
│   │   └── MM-<chapter>/     # 章
│   │       ├── README.md     # 章主文件
│   │       ├── sections/     # 细分小节（可选）
│   │       ├── assets/
│   │       │   ├── images/   # 章图片
│   │       │   ├── code/     # 可运行 Python 脚本
│   │       │   └── data/     # 示例数据
│   │       ├── exercises.md  # 习题
│   │       └── references.md # 引用
│   └── appendix/             # 附录
│       ├── A-papers/         # 附录 A：论文
│       └── B-patents/        # 附录 B：专利
├── tools/                    # 构建与辅助脚本
│   ├── build_index.py        # 生成论文/专利 HTML 索引
│   └── generate_figures.py   # 批量生成图片（预留）
└── tests/                    # 测试
    └── test_build_index.py
```

### 2.1 命名约定

- **Part 文件夹**：`part-NN-<kebab-case-name>/`，例如 `part-01-feature-extraction/`。
- **Chapter 文件夹**：`<NN>-<kebab-case-name>/`，例如 `03-statistical-features/`。
- **章主文件**：必须命名为 `README.md`。
- **图片文件**：`<chapter>-fig-NN-<short-desc>.png`，例如 `03-fig-01-mean-std-ts.png`。
- **代码文件**：`<chapter>-example-NN-<short-desc>.py`，例如 `03-example-01-rolling-stats.py`。
- **数据文件**：`<chapter>-data-NN.<ext>`，例如 `03-data-01-synthetic.csv`。

---

## 3. Markdown 风格

### 3.1 通用规则

- 使用 **GFM（GitHub Flavored Markdown）**。
- 章节主文件使用一级标题 `# 章标题`，避免多个一级标题。
- 小节使用 `##`、`###`、`####` 层级。
- 数学公式使用 **LaTeX**：
  - 行内公式：`$...$`
  - 块级公式：`$$...$$`
- 中文与英文/数字之间保留一个空格（Markdown 源码中）。
- 专有名词首次出现时加粗，例如 **动态时间规整（Dynamic Time Warping, DTW）**。

### 3.2 章节内容组织

每章 `README.md` 应围绕一个核心主题展开，由若干相互关联的小节组成。每个小节聚焦一个具体知识点、方法或问题，避免把过多内容塞进单个小节。

- 章节主文件使用一级标题 `# 第 N 章 章标题`。
- 一级标题下按主题划分若干二级小节，使用 `##`。
- 每个二级小节可进一步使用 `###`、`####` 展开细节。
- 小节标题应准确概括该节内容，编号或不编号均可，但同一本书内宜保持一致。
- 每章末尾必须包含一个 `## 本章小结` 小节，用于回顾本章核心内容、梳理关键结论，并指出与后续章节的衔接。

示例结构：

```markdown
# 第 N 章 章标题

## 主题一：问题背景与核心概念

## 主题二：方法原理

### 2.1 基本假设

### 2.2 推导过程

## 主题三：算法实现与 Python 实践

## 主题四：结果可视化与解读

## 本章小结

- 回顾 ...
- 关键结论 ...
- 下一章将介绍 ...
```

编写时应注意：

- 小节之间逻辑连贯，过渡自然。
- 避免为追求统一模板而生搬硬套无关章节。
- 代码、公式、图片应嵌入到与其内容对应的小节中，而非集中到固定位置。

---

## 4. 图片规范

### 4.1 图片生成

- 优先使用 Python + `matplotlib` / `seaborn` 生成。
- 图片脚本放在 `assets/code/`，图片输出到 `assets/images/`。
- 脚本头部必须包含：`# Generated for book/part-NN/MM/README.md`。
- 使用统一的调色板（见下方）。
- 推荐输出格式：`PNG`，分辨率 `300 dpi`，宽不超过 1600 px。
- 图片标题、坐标轴标签、刻度文字、图例（legend）等能用中文的尽可能使用中文，保持全书风格统一。
- 必须正确配置中文字体，避免中文乱码。例如 `matplotlib` 中可设置：
  ```python
  plt.rcParams["font.sans-serif"] = ["SimHei", "WenQuanYi Micro Hei", "Noto Sans CJK SC", "DejaVu Sans"]
  plt.rcParams["axes.unicode_minus"] = False
  ```
  脚本运行前应检测系统可用字体，优先选择支持中文的字体，确保保存的 PNG 中文字正常显示。
- 整体排版应紧凑丰满：标题、坐标轴标签、刻度文字、图例字体均适当缩小；图例与标签不使用边框、不使用背景色。
- 图片应尽量扁平、加宽，以充分利用 Markdown 页面宽度；内容较丰富的图在 Markdown 中宜独占一行展示，避免与文字混排。
- 推荐通过 `fig.tight_layout()` 或 `bbox_inches="tight"` 减少空白边距。

### 4.2 统一调色板

```python
import matplotlib.pyplot as plt

COLORS = {
    "primary": "#0b5394",      # 主色
    "secondary": "#6aa84f",    # 辅助绿
    "accent": "#e69138",       # 强调橙
    "danger": "#cc0000",       # 异常/危险
    "neutral": "#999999",      # 中性灰
    "background": "#f8f9fa",   # 背景
}

plt.rcParams.update({
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "font.size": 8,
    "axes.labelsize": 8,
    "axes.titlesize": 9,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7,
    "legend.frameon": False,
    "legend.facecolor": "none",
    "legend.edgecolor": "none",
    "figure.figsize": (10, 3.5),
    "figure.autolayout": True,
})
```

### 4.3 图片引用

```markdown
![图 3-1 滚动均值与标准差示例](./assets/images/03-fig-01-rolling-mean-std.png)

**图 3-1** 滚动均值与标准差示例。
```

---

## 5. 代码规范

### 5.1 代码块

- 所有代码块必须标注语言：
  ````markdown
  ```python
  # code
  ```
  ````
- 代码应可直接运行（除非示例明确说明为伪代码）。
- 复杂算法提供注释与分步说明。

### 5.2 依赖管理

- 每章 `assets/code/` 下可放置 `requirements.txt`，列出该章特殊依赖。
- 通用依赖（numpy, pandas, matplotlib, scipy, scikit-learn）不重复列出。

### 5.3 代码模板

```python
"""
03-example-01-rolling-stats.py
Generated for book/part-01-feature-extraction/03-statistical-features/README.md
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. 构造示例序列
rng = np.random.default_rng(42)
n = 200
x = np.cumsum(rng.normal(size=n))

# 2. 计算滚动统计量
s = pd.Series(x)
rolling_mean = s.rolling(window=20).mean()
rolling_std = s.rolling(window=20).std()

# 3. 可视化
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(s, label="Original", color="#0b5394")
ax.plot(rolling_mean, label="Rolling Mean", color="#e69138")
ax.fill_between(
    range(n),
    rolling_mean - rolling_std,
    rolling_mean + rolling_std,
    color="#e69138",
    alpha=0.2,
    label="±1 Std",
)
ax.legend()
ax.set_title("Rolling Mean and Standard Deviation")
fig.tight_layout()
fig.savefig("../images/03-fig-01-rolling-mean-std.png", dpi=300)
```

---

## 6. 引用规范

### 6.1 文内引用

- 使用 `[^key]` 形式的脚注引用，例如：
  ```markdown
  动态时间规整（DTW）是一种经典的时序相似度度量方法 [^berndt1994dtw]。
  ```
- 章节 `references.md` 中给出完整条目：
  ```markdown
  [^berndt1994dtw]: Berndt, D. J., & Clifford, J. (1994). Using dynamic time warping to find patterns in time series. *KDD Workshop*, 359–370.
  ```

### 6.2 论文/专利附录引用

- 正文中引用论文时，链接到附录 A 的对应条目：
  ```markdown
  相关实现可参考 [附录 A：ROCKET 论文](../appendix/A-papers/classification/ROCKET/README.html)。
  ```

---

## 7. 附录规范

### 7.1 附录 A：论文

位于 `book/appendix/A-papers/`，包含：
- `netman/`：清华 NetMan Lab 论文 176 篇
- `alibaba/`：阿里 AIOps 论文 16 篇
- `classification/`：时序分类代表论文 22 篇

索引由 `tools/build_index.py` 生成，输出到 `book/appendix/A-papers/index.html`。

### 7.2 附录 B：专利

位于 `book/appendix/B-patents/`，包含：
- `pdfs/`：30 件专利 PDF
- `docs/`：每件专利的中文方案说明

索引由 `tools/build_index.py` 生成，输出到 `book/appendix/B-patents/index.html`。

---

## 8. 构建与验证

### 8.1 生成索引与导航

```bash
python3 tools/build_navigation.py      # 生成章节目录数据
python3 tools/build_index.py           # 论文 + 专利
python3 tools/build_index.py papers    # 仅论文
python3 tools/build_index.py pdfs      # 仅专利
```

### 8.2 运行测试

```bash
python3 -m pytest tests/ -v
```

### 8.3 生成图片

```bash
python3 tools/generate_figures.py       # 批量生成（预留）
# 或进入具体章节运行单张图片脚本
python3 book/part-01-feature-extraction/03-statistical-features/assets/code/03-example-01-rolling-stats.py
```

---

## 9. Git 与提交规范

- 提交信息使用语义化前缀：
  - `feat(chapter/03): ...`
  - `fix(build_index): ...`
  - `docs(readme): ...`
  - `refactor(tools): ...`
- 新增章节时，同步更新 `book/SUMMARY.md`。
- 修改索引脚本后，重新运行 `tools/build_index.py` 并提交生成的 HTML。

---

## 10. 新增章节的检查清单

- [ ] 目录命名符合 `part-NN-<name>/<MM>-<chapter>/`
- [ ] 已创建 `README.md`、`exercises.md`、`references.md`
- [ ] 已创建 `assets/images/`、`assets/code/`、`assets/data/`
- [ ] `README.md` 围绕核心主题组织，包含若干小节与 `## 本章小结`
- [ ] 图片由 Python 脚本生成并保存到 `assets/images/`
- [ ] 代码块标注语言且可运行
- [ ] 已更新 `book/SUMMARY.md`
- [ ] 已运行 `tools/build_navigation.py` 并提交 `_data/navigation.yml`
- [ ] 已通过 `pytest tests/test_build_navigation.py`
- [ ] 已通过 `pytest tests/test_build_index.py`

---

*最后更新：2026-07-12*
