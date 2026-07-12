"""
03-example-04-seasonality-features.py
Generated for book/part-01-feature-extraction/03-statistical-features/README.md

This script generates Figure 3-4: STL decomposition of a synthetic seasonal
series and visualizes seasonality strength, intra-period statistics, and
seasonal-lag autocorrelation features.
"""
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.stattools import acf

# ---------------------------------------------------------------------------
# Palette (see CLAUDE.md)
# ---------------------------------------------------------------------------
COLORS = {
    "primary": "#0b5394",
    "secondary": "#6aa84f",
    "accent": "#e69138",
    "danger": "#cc0000",
    "neutral": "#999999",
    "background": "#f8f9fa",
}

# Width <= 5.3 in at 300 dpi keeps the PNG width <= 1600 px.
plt.rcParams.update({
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "font.size": 9,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "figure.figsize": (5.2, 6.5),
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
    # Guard against numerical issues when there is no seasonal variation
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

print(f"Seasonal strength F_s = {F_s:.4f}")
print(f"Intra-period mean  = {intra_stats['mean'][:5].round(4)} ...")
print(f"Intra-period std   = {intra_stats['std'][:5].round(4)} ...")
print(f"Intra-period skew  = {intra_stats['skew'][:5].round(4)} ...")
print(f"Intra-period kurt  = {intra_stats['kurt'][:5].round(4)} ...")
for k, v in seasonal_acf.items():
    print(f"{k} = {v:.4f}")

# ---------------------------------------------------------------------------
# 4. Visualize STL decomposition
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(4, 1, sharex=True)

components = [
    ("Observed", s.values, COLORS["primary"]),
    ("Trend", res.trend.values, COLORS["accent"]),
    ("Seasonal", res.seasonal.values, COLORS["secondary"]),
    ("Residual", res.resid.values, COLORS["neutral"]),
]

for ax, (name, values, color) in zip(axes, components):
    ax.plot(t, values, color=color, linewidth=1.0)
    ax.set_ylabel(name, fontsize=9)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.set_facecolor(COLORS["background"])

axes[0].set_title(f"STL Decomposition (period={period})")

# Annotate seasonal strength on the observed subplot
textstr = f"Seasonal strength $F_s$ = {F_s:.3f}"
axes[0].text(
    0.02,
    0.97,
    textstr,
    transform=axes[0].transAxes,
    fontsize=9,
    verticalalignment="top",
    horizontalalignment="left",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=COLORS["neutral"], alpha=0.9),
)

axes[-1].set_xlabel("Time step")
fig.tight_layout()

# ---------------------------------------------------------------------------
# 5. Save figure
# ---------------------------------------------------------------------------
out_dir = pathlib.Path(__file__).parent.parent / "images"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "03-fig-04-seasonality.png"
fig.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"\nSaved figure to {out_path}")
