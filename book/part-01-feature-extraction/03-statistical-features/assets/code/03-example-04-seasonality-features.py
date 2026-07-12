"""
03-example-04-seasonality-features.py
Generated for book/part-01-feature-extraction/03-statistical-features/README.md

This script generates Figure 3-4: STL decomposition of a synthetic seasonal
series and visualizes seasonality strength.
"""
import pathlib

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.stattools import acf

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
# 1. Generate synthetic seasonal series
# ---------------------------------------------------------------------------
rng = np.random.default_rng(42)
n = 240
period = 24  # e.g. hourly data over one day
t = np.arange(n)

# Trend + deterministic seasonality + noise
trend = 0.02 * t
seasonality = 3.0 * np.sin(2 * np.pi * t / period) + 1.5 * np.cos(4 * np.pi * t / period)
noise = rng.normal(scale=0.8, size=n)
x = trend + seasonality + noise

s = pd.Series(x, index=pd.RangeIndex(start=0, stop=n, step=1))

# ---------------------------------------------------------------------------
# 2. STL decomposition
# ---------------------------------------------------------------------------
# period must be odd for the default seasonal smoother; use period + 1 if even
stl_period = period if period % 2 == 1 else period + 1
stl = STL(s, period=stl_period, robust=False)
res = stl.fit()

# ---------------------------------------------------------------------------
# 3. Seasonality features
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


def intra_period_stats(series, period):
    """Compute mean/std/skew/kurt for each period position p = t mod period."""
    df = pd.DataFrame({"value": np.asarray(series), "pos": np.arange(len(series)) % period})
    grouped = df.groupby("pos")["value"]
    return {
        "mean": grouped.mean().values,
        "std": grouped.std(ddof=1).values,
        "skew": grouped.apply(lambda g: stats.skew(g, bias=False)).values,
        "kurt": grouped.apply(lambda g: stats.kurtosis(g, bias=False)).values,
    }


def seasonal_acf_features(series, period, max_lag_order=3):
    """Return ACF values at lags k = m, 2m, ..., max_lag_order * m."""
    max_lag = max_lag_order * period
    acf_values = acf(series, nlags=max_lag, fft=True, missing="drop")
    return {f"acf_lag_{(i + 1) * period}": acf_values[(i + 1) * period] for i in range(max_lag_order)}


F_s = seasonal_strength(res.trend.values, res.seasonal.values, res.resid.values)
intra_stats = intra_period_stats(s, period)
seasonal_acf = seasonal_acf_features(s, period, max_lag_order=3)

print(f"季节性强度 F_s = {F_s:.4f}")
print(f"周期内均值  = {intra_stats['mean'][:5].round(4)} ...")
print(f"周期内标准差 = {intra_stats['std'][:5].round(4)} ...")
print(f"周期内偏度  = {intra_stats['skew'][:5].round(4)} ...")
print(f"周期内峰度  = {intra_stats['kurt'][:5].round(4)} ...")
for k, v in seasonal_acf.items():
    print(f"{k} = {v:.4f}")

# ---------------------------------------------------------------------------
# 4. Visualize STL decomposition in a flat 2x2 layout
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, sharex=True, figsize=(10, 4.2))

components = [
    ("原始序列", s.values, COLORS["primary"]),
    ("趋势项", res.trend.values, COLORS["accent"]),
    ("季节项", res.seasonal.values, COLORS["secondary"]),
    ("残差项", res.resid.values, COLORS["neutral"]),
]

for ax, (name, values, color) in zip(axes.flat, components):
    ax.plot(t, values, color=color, linewidth=1.0)
    ax.set_ylabel(name)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.set_facecolor(COLORS["background"])

axes[0, 0].set_title(f"STL 分解 (周期={period})")

# Annotate seasonal strength on the observed subplot (no box)
textstr = f"季节性强度 $F_s$ = {F_s:.3f}"
axes[0, 0].text(
    0.02,
    0.97,
    textstr,
    transform=axes[0, 0].transAxes,
    fontsize=8,
    verticalalignment="top",
    horizontalalignment="left",
)

axes[1, 0].set_xlabel("时间步")
axes[1, 1].set_xlabel("时间步")
fig.tight_layout()

# ---------------------------------------------------------------------------
# 5. Save figure
# ---------------------------------------------------------------------------
out_dir = pathlib.Path(__file__).parent.parent / "images"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "03-fig-04-seasonality.png"
fig.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"\nSaved figure to {out_path}")
