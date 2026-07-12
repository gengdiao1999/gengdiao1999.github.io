"""
03-example-02-rolling-stats.py
Generated for book/part-01-feature-extraction/03-statistical-features/README.md

This script generates Figure 3-2: an overview of rolling-window statistical features.
"""
import pathlib

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
    "figure.figsize": (10, 4.2),
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
# 2. Rolling-window statistics
# ---------------------------------------------------------------------------
window = 20
s = pd.Series(x)
rolling_mean = s.rolling(window=window).mean()
rolling_std = s.rolling(window=window).std()
rolling_max = s.rolling(window=window).max()
rolling_min = s.rolling(window=window).min()
rolling_range = rolling_max - rolling_min
rolling_skew = s.rolling(window=window).skew()
rolling_kurt = s.rolling(window=window).kurt()

# ---------------------------------------------------------------------------
# 3. Visualize in a 2x2 panel
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, sharex=True, figsize=(10, 4.2))

# (1) Original series with rolling mean and std
ax = axes[0, 0]
ax.plot(s, label="原始序列", color=COLORS["primary"], linewidth=1.0)
ax.plot(
    rolling_mean,
    label=f"滚动均值 (w={window})",
    color=COLORS["accent"],
    linewidth=1.2,
)
ax.fill_between(
    range(n),
    rolling_mean - rolling_std,
    rolling_mean + rolling_std,
    color=COLORS["accent"],
    alpha=0.2,
    label="±1 滚动标准差",
)
ax.set_ylabel("取值")
ax.set_title("滚动均值与标准差")
ax.legend(loc="upper left")
ax.grid(True, linestyle=":", alpha=0.5)
ax.set_facecolor(COLORS["background"])

# (2) Rolling extrema and range
ax = axes[0, 1]
ax.plot(rolling_max, label="滚动最大值", color=COLORS["secondary"], linewidth=1.0)
ax.plot(rolling_min, label="滚动最小值", color=COLORS["danger"], linewidth=1.0)
ax.plot(
    rolling_range,
    label="滚动极差",
    color=COLORS["accent"],
    linestyle="--",
    linewidth=1.0,
)
ax.set_ylabel("取值")
ax.set_title("滚动最大、最小值与极差")
ax.legend(loc="upper left")
ax.grid(True, linestyle=":", alpha=0.5)
ax.set_facecolor(COLORS["background"])

# (3) Rolling skewness
ax = axes[1, 0]
ax.plot(rolling_skew, color=COLORS["secondary"], linewidth=1.2)
ax.axhline(0, color=COLORS["neutral"], linestyle=":", linewidth=1.0)
ax.set_xlabel("时间步")
ax.set_ylabel("偏度")
ax.set_title("滚动偏度")
ax.grid(True, linestyle=":", alpha=0.5)
ax.set_facecolor(COLORS["background"])

# (4) Rolling kurtosis
ax = axes[1, 1]
ax.plot(rolling_kurt, color=COLORS["danger"], linewidth=1.2)
ax.axhline(0, color=COLORS["neutral"], linestyle=":", linewidth=1.0)
ax.set_xlabel("时间步")
ax.set_ylabel("峰度")
ax.set_title("滚动峰度")
ax.grid(True, linestyle=":", alpha=0.5)
ax.set_facecolor(COLORS["background"])

fig.tight_layout()

# ---------------------------------------------------------------------------
# 4. Save figure
# ---------------------------------------------------------------------------
out_dir = pathlib.Path(__file__).parent.parent / "images"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "03-fig-02-rolling-stats.png"
fig.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"Saved figure to {out_path}")
