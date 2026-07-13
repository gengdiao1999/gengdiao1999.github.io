"""
03-example-04-seasonality-features.py
Generated for book/part-01-feature-extraction/03-statistical-features/README.md

This script generates Figure 3-4: a comparison of weak, medium, and strong
seasonality by varying the seasonal amplitude and noise level.
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
    "figure.figsize": (10, 5.5),
    "figure.autolayout": True,
})

# ---------------------------------------------------------------------------
# 1. Seasonality strength
# ---------------------------------------------------------------------------


def seasonal_strength(trend, seasonal, residual):
    """Seasonal strength based on STL decomposition.

    F_s = 1 - Var(R_t) / Var(S_t + R_t)
    """
    signal = seasonal + residual
    var_residual = np.var(residual, ddof=1)
    var_signal = np.var(signal, ddof=1)
    if var_signal < 1e-12:
        return 0.0
    return 1.0 - var_residual / var_signal


# ---------------------------------------------------------------------------
# 2. Generate weak / medium / strong seasonal series and plot
# ---------------------------------------------------------------------------
rng = np.random.default_rng(42)
n = 240
period = 24
t = np.arange(n)
base_trend = 0.02 * t
season_signal = 3.0 * np.sin(2 * np.pi * t / period) + 1.5 * np.cos(4 * np.pi * t / period)

# Amplitudes were tuned so that the resulting STL-based F_s falls inside the
# target intervals below. The default STL seasonal smoother is too flexible for
# the weak case and overfits noise, so we use a longer seasonal window (23) to
# keep the three levels well separated.
configs = [
    {"label": "弱季节性", "amp": 0.05, "noise": 1.6, "target_low": 0.10, "target_high": 0.30},
    {"label": "中季节性", "amp": 0.42, "noise": 1.0, "target_low": 0.50, "target_high": 0.75},
    {"label": "强季节性", "amp": 1.10, "noise": 0.4, "target_low": 0.88, "target_high": 0.99},
]

fig, axes = plt.subplots(3, 1, sharex=True, figsize=(10, 5.5))
stl_period = period if period % 2 == 1 else period + 1
results = []

for ax, cfg in zip(axes, configs):
    x = base_trend + cfg["amp"] * season_signal + rng.normal(scale=cfg["noise"], size=n)
    s = pd.Series(x)
    res = STL(s, period=stl_period, seasonal=23, robust=False).fit()
    fs = seasonal_strength(res.trend.values, res.seasonal.values, res.resid.values)
    results.append({"label": cfg["label"], "F_s": fs})
    ax.plot(t, x, color=COLORS["primary"], linewidth=0.9, label="原始序列")
    ax.set_ylabel("取值")
    ax.set_title(f"{cfg['label']}  $F_s$ = {fs:.3f}")
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.set_facecolor(COLORS["background"])
    ax.axvspan(0, period, color=COLORS["accent"], alpha=0.08, label=f"一个周期={period}")

axes[-1].set_xlabel("时间步")
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper right", bbox_to_anchor=(0.98, 0.98))
fig.tight_layout()

# ---------------------------------------------------------------------------
# 3. Save figure
# ---------------------------------------------------------------------------
out_dir = pathlib.Path(__file__).parent.parent / "images"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "03-fig-04-seasonality.png"
fig.savefig(out_path, dpi=300, bbox_inches="tight")

# ---------------------------------------------------------------------------
# 4. Validate and report seasonal strength values
# ---------------------------------------------------------------------------
for r, cfg in zip(results, configs):
    print(f"{r['label']}: F_s = {r['F_s']:.4f} (目标区间 [{cfg['target_low']:.2f}, {cfg['target_high']:.2f}])")
    assert cfg["target_low"] <= r["F_s"] <= cfg["target_high"], (
        f"{cfg['label']} 的 F_s {r['F_s']:.4f} 不在目标区间 "
        f"[{cfg['target_low']:.2f}, {cfg['target_high']:.2f}] 内"
    )

print(f"\nSaved figure to {out_path}")
