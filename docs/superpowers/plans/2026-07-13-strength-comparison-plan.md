# 第 3 章趋势/季节性强度可视化对比实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为第 3 章的季节性强度 $F_s$ 与趋势强度 $F_t$ 增加“弱 / 中 / 强”强度阶梯对比图，并同步更新正文图注。

**Architecture:** 保持现有示例脚本作为可执行入口，重写 `03-example-04-seasonality-features.py` 与 `03-example-05-trend-features.py` 的绘图部分，生成纵向三行对比图；新增 `tests/test_chapter3_figures.py` 以脚本运行 + 输出文件校验作为回归测试；最后更新 `README.md` 图注文字。

**Tech Stack:** Python 3, numpy, pandas, matplotlib, statsmodels (STL), pytest.

## Global Constraints

- 输出 PNG 分辨率 300 dpi，宽度不超过 1600 px。
- 中文字体优先使用 bundled `wqy-microhei.ttc`，回退系统中文字体。
- 使用 `CLAUDE.md` 统一调色板：`primary`/`secondary`/`accent`/`danger`/`neutral`/`background`。
- 图例无边框、无背景色；坐标轴与标题使用中文。
- 仅修改 `03-example-04-seasonality-features.py`、`03-example-05-trend-features.py`、对应 PNG 与 `README.md`。
- 不新增特征指标，不修改现有公式与定义。
- 提交前运行 `pytest tests/ -v` 并确保通过。

---

## File Structure

| 文件 | 职责 |
|------|------|
| `book/part-01-feature-extraction/03-statistical-features/assets/code/03-example-04-seasonality-features.py` | 生成新的图 3-4：弱/中/强季节性强度对比。 |
| `book/part-01-feature-extraction/03-statistical-features/assets/code/03-example-05-trend-features.py` | 生成新的图 3-5：弱/中/强趋势强度对比。 |
| `book/part-01-feature-extraction/03-statistical-features/assets/images/03-fig-04-seasonality.png` | 由脚本重新生成。 |
| `book/part-01-feature-extraction/03-statistical-features/assets/images/03-fig-05-trend.png` | 由脚本重新生成。 |
| `book/part-01-feature-extraction/03-statistical-features/README.md` | 更新图 3-4 / 图 3-5 的 caption 与必要解释文字。 |
| `tests/test_chapter3_figures.py` | 新增回归测试：运行脚本并校验输出文件存在且非空；校验强度值落在目标区间。 |

---

### Task 1: 新增回归测试骨架

**Files:**
- Create: `tests/test_chapter3_figures.py`
- Modify: 无

**Interfaces:**
- Consumes: 无
- Produces: `test_run_seasonality_script`、`test_run_trend_script`、`test_seasonal_strength_ranges`、`test_trend_strength_ranges`

- [ ] **Step 1: 编写失败测试（脚本输出文件存在性）**

```python
"""Regression tests for Chapter 3 figure generation scripts."""
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CHAPTER_DIR = REPO_ROOT / "book" / "part-01-feature-extraction" / "03-statistical-features"
CODE_DIR = CHAPTER_DIR / "assets" / "code"
IMAGE_DIR = CHAPTER_DIR / "assets" / "images"

SEASONALITY_SCRIPT = CODE_DIR / "03-example-04-seasonality-features.py"
TREND_SCRIPT = CODE_DIR / "03-example-05-trend-features.py"
SEASONALITY_FIG = IMAGE_DIR / "03-fig-04-seasonality.png"
TREND_FIG = IMAGE_DIR / "03-fig-05-trend.png"


def _run_script(script_path: Path):
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(script_path.parent),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Script failed:\n{result.stdout}\n{result.stderr}"
    return result


def test_run_seasonality_script():
    _run_script(SEASONALITY_SCRIPT)
    assert SEASONALITY_FIG.exists()
    assert SEASONALITY_FIG.stat().st_size > 0


def test_run_trend_script():
    _run_script(TREND_SCRIPT)
    assert TREND_FIG.exists()
    assert TREND_FIG.stat().st_size > 0
```

- [ ] **Step 2: 运行测试，确认失败**

Run: `pytest tests/test_chapter3_figures.py -v`

Expected: FAIL，因为目标脚本尚未生成新图（或旧图已存在但后续步骤会重写）。

- [ ] **Step 3: 提交测试骨架**

```bash
git add tests/test_chapter3_figures.py
git commit -m "test(chapter3): add regression tests for figure generation scripts"
```

---

### Task 2: 重写季节性强度示例脚本

**Files:**
- Modify: `book/part-01-feature-extraction/03-statistical-features/assets/code/03-example-04-seasonality-features.py`
- Create: `book/part-01-feature-extraction/03-statistical-features/assets/images/03-fig-04-seasonality.png`（脚本生成）

**Interfaces:**
- Consumes: `setup_chinese_font()`、统一调色板 `COLORS`、现有 `seasonal_strength()` 函数
- Produces: 新生成的 `03-fig-04-seasonality.png`；打印三条序列的 $F_s$ 值

- [ ] **Step 1: 修改脚本，生成弱/中/强三条季节性序列并绘图**

保留字体设置、调色板与 `seasonal_strength()` 函数，替换数据生成与绘图部分。关键实现要求：

```python
# 参数
rng = np.random.default_rng(42)
n = 240
period = 24
t = np.arange(n)
base_trend = 0.02 * t
season_signal = 3.0 * np.sin(2 * np.pi * t / period) + 1.5 * np.cos(4 * np.pi * t / period)

# 三个等级：通过调整季节振幅与噪声标准差得到目标 F_s 区间
configs = [
    {"label": "弱季节性", "amp": 0.4, "noise": 1.6, "target_low": 0.10, "target_high": 0.30},
    {"label": "中季节性", "amp": 1.2, "noise": 1.0, "target_low": 0.50, "target_high": 0.75},
    {"label": "强季节性", "amp": 4.0, "noise": 0.4, "target_low": 0.88, "target_high": 0.99},
]

# 计算并绘图
fig, axes = plt.subplots(3, 1, sharex=True, figsize=(10, 5.5))
stl_period = period if period % 2 == 1 else period + 1
results = []

for ax, cfg in zip(axes, configs):
    x = base_trend + cfg["amp"] * season_signal + rng.normal(scale=cfg["noise"], size=n)
    s = pd.Series(x)
    res = STL(s, period=stl_period, robust=False).fit()
    fs = seasonal_strength(res.trend.values, res.seasonal.values, res.resid.values)
    results.append({"label": cfg["label"], "F_s": fs})
    ax.plot(t, x, color=COLORS["primary"], linewidth=0.9, label="原始序列")
    ax.set_ylabel("取值")
    ax.set_title(f"{cfg['label']}  $F_s$ = {fs:.3f}")
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.set_facecolor(COLORS["background"])
    # 标出一个周期
    ax.axvspan(0, period, color=COLORS["accent"], alpha=0.08, label=f"一个周期={period}")

axes[-1].set_xlabel("时间步")
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper right", bbox_to_anchor=(0.98, 0.98))
fig.tight_layout()
fig.savefig(out_path, dpi=300, bbox_inches="tight")
```

- [ ] **Step 2: 运行脚本并验证输出**

Run:
```bash
cd book/part-01-feature-extraction/03-statistical-features/assets/code
python3 03-example-04-seasonality-features.py
```

Expected: 生成 `../images/03-fig-04-seasonality.png`，终端打印三个 $F_s$ 值，且均在目标区间。

- [ ] **Step 3: 运行测试，确认通过**

Run: `pytest tests/test_chapter3_figures.py::test_run_seasonality_script -v`

Expected: PASS

- [ ] **Step 4: 提交**

```bash
git add book/part-01-feature-extraction/03-statistical-features/assets/code/03-example-04-seasonality-features.py
# 不直接 add PNG；等 Task 4 一起提交或单独提交
```

---

### Task 3: 扩展测试覆盖强度值区间

**Files:**
- Modify: `tests/test_chapter3_figures.py`

**Interfaces:**
- Consumes: 脚本运行后打印到 stdout 的 $F_s$ / $F_t$ 值
- Produces: 区间断言测试

- [ ] **Step 1: 新增强度值区间断言**

在 `tests/test_chapter3_figures.py` 末尾追加：

```python
import re


def _extract_strengths(stdout: str, marker: str):
    """Extract numeric strength values printed by a script."""
    pattern = re.compile(rf"{marker}\s*=\s*([0-9.]+)")
    return [float(m) for m in pattern.findall(stdout)]


def test_seasonal_strength_ranges():
    result = _run_script(SEASONALITY_SCRIPT)
    values = _extract_strengths(result.stdout, "F_s")
    assert len(values) == 3, f"Expected 3 seasonal strength values, got {values}"
    low, mid, high = sorted(values)
    assert 0.10 <= low <= 0.30, f"Weak seasonal strength out of range: {low}"
    assert 0.50 <= mid <= 0.75, f"Medium seasonal strength out of range: {mid}"
    assert 0.88 <= high <= 0.99, f"Strong seasonal strength out of range: {high}"
```

- [ ] **Step 2: 运行测试，确认失败**

Run: `pytest tests/test_chapter3_figures.py::test_seasonal_strength_ranges -v`

Expected: FAIL，因为当前 stdout 格式可能不匹配（或旧脚本未打印三行）。

- [ ] **Step 3: 提交测试扩展**

```bash
git add tests/test_chapter3_figures.py
git commit -m "test(chapter3): assert seasonal strength values fall in expected ranges"
```

---

### Task 4: 重写趋势强度示例脚本

**Files:**
- Modify: `book/part-01-feature-extraction/03-statistical-features/assets/code/03-example-05-trend-features.py`
- Create: `book/part-01-feature-extraction/03-statistical-features/assets/images/03-fig-05-trend.png`（脚本生成）

**Interfaces:**
- Consumes: `setup_chinese_font()`、统一调色板 `COLORS`、现有 `trend_strength()` 函数
- Produces: 新生成的 `03-fig-05-trend.png`；打印三条序列的 $F_t$ 值

- [ ] **Step 1: 修改脚本，生成弱/中/强三条趋势序列并绘图**

保留字体设置、调色板与 `trend_strength()` 函数，替换数据生成与绘图部分。关键实现要求：

```python
# 参数
rng = np.random.default_rng(42)
n = 240
t = np.arange(n)

# 基础成分：分段线性趋势 + 低频波动 + 噪声
base_trend = np.where(t < n // 2, 0.04 * t, 0.04 * (n // 2) - 0.02 * (t - n // 2))
low_freq = 1.5 * np.sin(2 * np.pi * t / 60)
noise = rng.normal(scale=0.8, size=n)

configs = [
    {"label": "弱趋势性", "factor": 0.15, "target_low": 0.10, "target_high": 0.30},
    {"label": "中趋势性", "factor": 0.80, "target_low": 0.50, "target_high": 0.75},
    {"label": "强趋势性", "factor": 2.50, "target_low": 0.88, "target_high": 0.99},
]

fig, axes = plt.subplots(3, 1, sharex=True, figsize=(10, 5.5))
period = 11
results = []

for ax, cfg in zip(axes, configs):
    x = cfg["factor"] * base_trend + low_freq + noise
    s = pd.Series(x)
    res = STL(s, period=period, robust=False).fit()
    ft = trend_strength(res.trend.values, res.resid.values)
    results.append({"label": cfg["label"], "F_t": ft})
    ax.plot(t, x, color=COLORS["primary"], linewidth=0.9, label="原始序列")
    ax.plot(t, res.trend.values, color=COLORS["accent"], linewidth=1.2, label="STL 趋势项")
    ax.set_ylabel("取值")
    ax.set_title(f"{cfg['label']}  $F_t$ = {ft:.3f}")
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.set_facecolor(COLORS["background"])

axes[-1].set_xlabel("时间步")
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper right", bbox_to_anchor=(0.98, 0.98))
fig.tight_layout()
fig.savefig(out_path, dpi=300, bbox_inches="tight")
```

- [ ] **Step 2: 运行脚本并验证输出**

Run:
```bash
cd book/part-01-feature-extraction/03-statistical-features/assets/code
python3 03-example-05-trend-features.py
```

Expected: 生成 `../images/03-fig-05-trend.png`，终端打印三个 $F_t$ 值，且均在目标区间。

- [ ] **Step 3: 运行测试，确认通过**

Run: `pytest tests/test_chapter3_figures.py -v`

Expected: PASS

- [ ] **Step 4: 提交**

```bash
git add book/part-01-feature-extraction/03-statistical-features/assets/code/03-example-05-trend-features.py
git commit -m "feat(chapter3): add weak/medium/strong trend strength comparison figure"
```

---

### Task 5: 扩展测试覆盖趋势强度区间

**Files:**
- Modify: `tests/test_chapter3_figures.py`

**Interfaces:**
- Consumes: 趋势脚本 stdout
- Produces: `test_trend_strength_ranges`

- [ ] **Step 1: 新增趋势强度区间断言**

在 `tests/test_chapter3_figures.py` 末尾追加：

```python
def test_trend_strength_ranges():
    result = _run_script(TREND_SCRIPT)
    values = _extract_strengths(result.stdout, "F_t")
    assert len(values) == 3, f"Expected 3 trend strength values, got {values}"
    low, mid, high = sorted(values)
    assert 0.10 <= low <= 0.30, f"Weak trend strength out of range: {low}"
    assert 0.50 <= mid <= 0.75, f"Medium trend strength out of range: {mid}"
    assert 0.88 <= high <= 0.99, f"Strong trend strength out of range: {high}"
```

- [ ] **Step 2: 运行测试，确认通过**

Run: `pytest tests/test_chapter3_figures.py -v`

Expected: PASS

- [ ] **Step 3: 提交**

```bash
git add tests/test_chapter3_figures.py
git commit -m "test(chapter3): assert trend strength values fall in expected ranges"
```

---

### Task 6: 更新 README.md 图注与说明文字

**Files:**
- Modify: `book/part-01-feature-extraction/03-statistical-features/README.md`

**Interfaces:**
- Consumes: 新生成的图 3-4 / 图 3-5
- Produces: 更新的 caption 与正文解释

- [ ] **Step 1: 更新图 3-4 caption**

定位到行 472–474：

```markdown
![图 3-4 不同季节性强度的序列形态对比](./assets/images/03-fig-04-seasonality.png)

**图 3-4** 不同季节性强度的序列形态对比。从上到下依次为弱、中、强季节性示例，标题中标注了对应的季节性强度 $F_s$。$F_s$ 越接近 1，季节波形越清晰；越接近 0，序列越接近噪声。
```

- [ ] **Step 2: 更新图 3-5 caption**

定位到行 617–619：

```markdown
![图 3-5 不同趋势强度的序列形态对比](./assets/images/03-fig-05-trend.png)

**图 3-5** 不同趋势强度的序列形态对比。从上到下依次为弱、中、强趋势性示例，橙色曲线为 STL 提取的趋势项，标题中标注了对应的趋势强度 $F_t$。$F_t$ 越接近 1，趋势项对序列波动的解释程度越高。
```

- [ ] **Step 3: 在公式后补充解释（可选，如需要）**

在 3.3.2 节 $F_s$ 公式之后、3.4.3 节 $F_t$ 公式之后，各增加一句：

```markdown
> 图 3-4 展示了不同季节性强度下序列的典型形态，读者可据此判断实际数据中 $F_s$ 的相对强弱。
```

```markdown
> 图 3-5 展示了不同趋势强度下序列的典型形态，读者可据此判断实际数据中 $F_t$ 的相对强弱。
```

- [ ] **Step 4: 运行 Markdown 相关检查（如 tests/test_build_navigation.py）**

Run: `pytest tests/test_build_navigation.py -v`

Expected: PASS

- [ ] **Step 5: 提交**

```bash
git add book/part-01-feature-extraction/03-statistical-features/README.md
git commit -m "docs(chapter3): update captions for strength comparison figures"
```

---

### Task 7: 最终验证与图片提交

**Files:**
- Add: `book/part-01-feature-extraction/03-statistical-features/assets/images/03-fig-04-seasonality.png`
- Add: `book/part-01-feature-extraction/03-statistical-features/assets/images/03-fig-05-trend.png`

**Interfaces:**
- Consumes: 前述所有任务结果
- Produces: 可提交的工作树

- [ ] **Step 1: 运行完整测试套件**

Run: `pytest tests/ -v`

Expected: 全部通过。

- [ ] **Step 2: 检查生成的图片**

Run:
```bash
file book/part-01-feature-extraction/03-statistical-features/assets/images/03-fig-04-seasonality.png
file book/part-01-feature-extraction/03-statistical-features/assets/images/03-fig-05-trend.png
```

Expected: 均为 PNG 图片，大小大于 0。

- [ ] **Step 3: 提交图片与最终变更**

```bash
git add book/part-01-feature-extraction/03-statistical-features/assets/images/03-fig-04-seasonality.png
# 如 Task 2 未提交，此时一并提交脚本变更
git add book/part-01-feature-extraction/03-statistical-features/assets/code/03-example-04-seasonality-features.py
git add book/part-01-feature-extraction/03-statistical-features/assets/images/03-fig-05-trend.png
# 如 Task 4 未提交，此时一并提交脚本变更
git add book/part-01-feature-extraction/03-statistical-features/assets/code/03-example-05-trend-features.py
git commit -m "feat(chapter3): regenerate strength comparison figures"
```

- [ ] **Step 4: 最终状态检查**

Run: `git status`

Expected: 工作树干净，或仅留下未跟踪的无关文件。

---

## Self-Review Checklist

- [ ] **Spec coverage**: 每个 spec 要求（弱/中/强对比、目标区间、统一风格、README 更新、测试）均有对应任务。
- [ ] **Placeholder scan**: 计划中没有 TBD/TODO/“后续补充”。
- [ ] **Type consistency**: 测试与脚本之间通过文件路径和 stdout 正则交互，签名一致。
- [ ] **可测试性**: 每个任务结束都有明确的运行命令与期望结果。

---

## Notes for Implementers

1. 若实际生成的 $F_s$ / $F_t$ 值略微超出目标区间，优先微调 `amp`/`noise`/`factor` 参数，而不是放宽测试区间。参数应在同一次提交中调整。
2. 图例统一放在图右上角（`bbox_to_anchor=(0.98, 0.98)`），避免与子图标题重叠。
3. 季节性子图可用半透明 `axvspan` 标出第一个周期；趋势子图则不需要周期标注。
4. 如 `wqy-microhei.ttc` 字体不存在，脚本中的回退逻辑会自动选择系统字体，测试不应因此失败。
