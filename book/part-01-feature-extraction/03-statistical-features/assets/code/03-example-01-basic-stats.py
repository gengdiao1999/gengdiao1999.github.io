"""
03-example-01-basic-stats.py
Generated for book/part-01-feature-extraction/03-statistical-features/README.md

This script generates Figure 3-1: an overview of basic statistical features.
"""
import pathlib

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# ---------------------------------------------------------------------------
# Palette and Chinese font setup (see CLAUDE.md)
# ---------------------------------------------------------------------------
COLORS = {
    "primary": "#0b5394",
    "secondary": "#6aa84f",
    "accent": "#e69138",
    "danger": "#cc0000",
    "neutral": "#999999",
    "background": "#f8f9fa",
}


def setup_chinese_font():
    """Use bundled WenQuanYi Micro Hei or a system Chinese font."""
    font_path = pathlib.Path(__file__).parent.parent / "fonts" / "wqy-microhei.ttc"
    if font_path.exists():
        fm.fontManager.addfont(str(font_path))
        prop = fm.FontProperties(fname=str(font_path))
        plt.rcParams["font.sans-serif"] = [prop.get_name(), "DejaVu Sans"]
    else:
        candidates = [
            "SimHei",
            "WenQuanYi Micro Hei",
            "Noto Sans CJK SC",
            "Source Han Sans SC",
            "Microsoft YaHei",
            "DejaVu Sans",
        ]
        available = {f.name for f in fm.fontManager.ttflist}
        chosen = next((f for f in candidates if f in available), "DejaVu Sans")
        plt.rcParams["font.sans-serif"] = [chosen, "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False


setup_chinese_font()

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

# ---------------------------------------------------------------------------
# 1. Generate example series: trend + random walk + noise
# ---------------------------------------------------------------------------
rng = np.random.default_rng(42)
n = 200
trend = np.linspace(0, 5, n)
walk = np.cumsum(rng.normal(scale=0.3, size=n))
noise = rng.normal(scale=0.5, size=n)
x = trend + walk + noise

# ---------------------------------------------------------------------------
# 2. Compute global statistics
# ---------------------------------------------------------------------------
mean = np.mean(x)
median = np.median(x)
mode = float(stats.mode(x, keepdims=True).mode[0])
variance = np.var(x)
std = np.std(x)
q1, q3 = np.percentile(x, [25, 75])
iqr = q3 - q1
range_val = np.ptp(x)
skewness = stats.skew(x)
kurtosis = stats.kurtosis(x)
energy = np.sum(x ** 2)
rms = np.sqrt(np.mean(x ** 2))
zcr = np.sum((x[:-1] * x[1:]) < 0) / (n - 1)

print("=== 基本统计量 ===")
print(f"均值:        {mean:.3f}")
print(f"中位数:      {median:.3f}")
print(f"众数:        {mode:.3f}")
print(f"方差:        {variance:.3f}")
print(f"标准差:      {std:.3f}")
print(f"极差:        {range_val:.3f}")
print(f"Q1:          {q1:.3f}")
print(f"Q3:          {q3:.3f}")
print(f"IQR:         {iqr:.3f}")
print(f"偏度:        {skewness:.3f}")
print(f"峰度:        {kurtosis:.3f}")
print(f"绝对能量:    {energy:.3f}")
print(f"RMS:         {rms:.3f}")
print(f"过零率:      {zcr:.3f}")

# ---------------------------------------------------------------------------
# 3. Visualize
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10, 3.2))

# Time series with key reference levels
ax = axes[0]
ax.plot(x, label="原始序列", color=COLORS["primary"], linewidth=1.0)
ax.axhline(mean, color=COLORS["accent"], linestyle="--", label="均值")
ax.axhline(median, color=COLORS["secondary"], linestyle="-.", label="中位数")
ax.axhline(q1, color=COLORS["neutral"], linestyle=":", label="Q1 / Q3")
ax.axhline(q3, color=COLORS["neutral"], linestyle=":")
ax.set_xlabel("时间步")
ax.set_ylabel("取值")
ax.set_title("基本统计量概览")
ax.legend(loc="upper left")
ax.grid(True, linestyle=":", alpha=0.5)
ax.set_facecolor(COLORS["background"])

# Histogram with central tendency and spread markers
ax = axes[1]
ax.hist(x, bins=20, color=COLORS["primary"], edgecolor="white", alpha=0.7)
ax.axvline(mean, color=COLORS["accent"], linestyle="--", linewidth=1.5, label="均值")
ax.axvline(median, color=COLORS["secondary"], linestyle="-.", linewidth=1.5, label="中位数")
ax.axvline(q1, color=COLORS["neutral"], linestyle=":", linewidth=1.5)
ax.axvline(q3, color=COLORS["neutral"], linestyle=":", linewidth=1.5)
ax.set_xlabel("取值")
ax.set_ylabel("频数")
ax.set_title("分布直方图")
ax.legend(loc="upper right")
ax.grid(True, linestyle=":", alpha=0.5)
ax.set_facecolor(COLORS["background"])

# Compact statistics table as a text box (no background border)
stat_text = (
    f"均值={mean:.2f}\n"
    f"中位数={median:.2f}\n"
    f"标准差={std:.2f}\n"
    f"极差={range_val:.2f}\n"
    f"IQR={iqr:.2f}\n"
    f"偏度={skewness:.2f}\n"
    f"峰度={kurtosis:.2f}\n"
    f"能量={energy:.1f}\n"
    f"RMS={rms:.2f}\n"
    f"过零率={zcr:.2f}"
)
ax.text(
    0.02,
    0.98,
    stat_text,
    transform=ax.transAxes,
    fontsize=7,
    verticalalignment="top",
)

fig.tight_layout()

# ---------------------------------------------------------------------------
# 4. Save figure
# ---------------------------------------------------------------------------
out_dir = pathlib.Path(__file__).parent.parent / "images"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "03-fig-01-basic-stats.png"
fig.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"Saved figure to {out_path}")
