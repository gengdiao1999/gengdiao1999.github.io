"""
03-example-05-trend-features.py
Generated for book/part-01-feature-extraction/03-statistical-features/README.md

This script generates Figure 3-5: a comparison of weak, medium, and strong
trend strength using STL decomposition and the trend-strength metric $F_t$.
"""
import pathlib

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL

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
    "figure.figsize": (5.2, 5.5),
    "figure.autolayout": True,
})

# ---------------------------------------------------------------------------
# 1. Generate base components: piecewise trend + low-frequency fluctuation + noise
# ---------------------------------------------------------------------------
rng = np.random.default_rng(42)
n = 240
t = np.arange(n)

base_trend = np.where(t < n // 2, 0.04 * t, 0.04 * (n // 2) - 0.02 * (t - n // 2))
low_freq = 0.3 * np.sin(2 * np.pi * t / 60)
noise = rng.normal(scale=0.8, size=n)

# ---------------------------------------------------------------------------
# 2. Trend-strength metric
# ---------------------------------------------------------------------------
def trend_strength(trend, residual):
    """Trend strength based on STL decomposition.

    F_t = 1 - Var(R_t) / Var(T_t + R_t)
    """
    signal = trend + residual
    var_residual = np.var(residual, ddof=1)
    var_signal = np.var(signal, ddof=1)
    if var_signal < 1e-12:
        return 0.0
    return 1.0 - var_residual / var_signal


# ---------------------------------------------------------------------------
# 3. Weak / medium / strong trend comparison
# ---------------------------------------------------------------------------
configs = [
    {"label": "弱趋势性", "factor": 0.15, "target_low": 0.10, "target_high": 0.30},
    {"label": "中趋势性", "factor": 0.60, "target_low": 0.50, "target_high": 0.75},
    {"label": "强趋势性", "factor": 2.00, "target_low": 0.88, "target_high": 0.99},
]

period = 11
series_list = []
results = []

for cfg in configs:
    x = cfg["factor"] * base_trend + low_freq + noise
    series_list.append(x)
    s = pd.Series(x)
    res = STL(s, period=period, robust=False).fit()
    ft = trend_strength(res.trend.values, res.resid.values)
    results.append({"label": cfg["label"], "F_t": ft, "trend": res.trend.values})

# Use the same y-axis range across all panels for easier comparison.
all_values = np.concatenate(series_list + [r["trend"] for r in results])
y_min, y_max = np.min(all_values), np.max(all_values)
y_margin = 0.05 * (y_max - y_min)

fig, axes = plt.subplots(3, 1, sharex=True, figsize=(5.2, 5.5))

for ax, cfg, x, res in zip(axes, configs, series_list, results):
    ax.plot(t, x, color=COLORS["primary"], linewidth=0.9, label="原始序列")
    ax.plot(t, res["trend"], color=COLORS["accent"], linewidth=1.2, label="STL 趋势项")
    ax.set_ylabel("取值")
    ax.set_title(f"{cfg['label']}  $F_t$ = {res['F_t']:.3f}")
    ax.set_ylim(y_min - y_margin, y_max + y_margin)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.set_facecolor(COLORS["background"])

axes[-1].set_xlabel("时间步")
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper right", bbox_to_anchor=(0.98, 0.98))

# ---------------------------------------------------------------------------
# 4. Save figure
# ---------------------------------------------------------------------------
out_dir = pathlib.Path(__file__).parent.parent / "images"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "03-fig-05-trend.png"
fig.tight_layout()
fig.savefig(out_path, dpi=300, bbox_inches="tight")

# ---------------------------------------------------------------------------
# 5. Print results and validate target ranges
# ---------------------------------------------------------------------------
all_in_range = True
for cfg, r in zip(configs, results):
    in_range = cfg["target_low"] <= r["F_t"] <= cfg["target_high"]
    status = "OK" if in_range else "OUT OF RANGE"
    print(f"{r['label']}: F_t = {r['F_t']:.4f}  (target [{cfg['target_low']:.2f}, {cfg['target_high']:.2f}]) {status}")
    all_in_range = all_in_range and in_range

print(f"\nSaved figure to {out_path}")

if not all_in_range:
    raise RuntimeError("One or more trend-strength values fell outside the target ranges.")
