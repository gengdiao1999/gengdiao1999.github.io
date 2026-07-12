"""
03-example-02-rolling-stats.py
Generated for book/part-01-feature-extraction/03-statistical-features/README.md

This script generates Figure 3-2: an overview of rolling-window statistical features.
"""
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

plt.rcParams.update({
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "figure.figsize": (4.8, 3.8),
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
fig, axes = plt.subplots(2, 2, sharex=True)

# (1) Original series with rolling mean and std
ax = axes[0, 0]
ax.plot(s, label="Original series", color=COLORS["primary"], linewidth=1.2)
ax.plot(
    rolling_mean,
    label=f"Rolling mean (w={window})",
    color=COLORS["accent"],
    linewidth=1.5,
)
ax.fill_between(
    range(n),
    rolling_mean - rolling_std,
    rolling_mean + rolling_std,
    color=COLORS["accent"],
    alpha=0.2,
    label="±1 rolling std",
)
ax.set_ylabel("Value")
ax.set_title("Rolling Mean and Standard Deviation")
ax.legend(loc="upper left", fontsize=8)
ax.grid(True, linestyle=":", alpha=0.5)
ax.set_facecolor(COLORS["background"])

# (2) Rolling extrema and range
ax = axes[0, 1]
ax.plot(rolling_max, label="Rolling max", color=COLORS["secondary"], linewidth=1.2)
ax.plot(rolling_min, label="Rolling min", color=COLORS["danger"], linewidth=1.2)
ax.plot(
    rolling_range,
    label="Rolling range",
    color=COLORS["accent"],
    linestyle="--",
    linewidth=1.2,
)
ax.set_ylabel("Value")
ax.set_title("Rolling Max, Min and Range")
ax.legend(loc="upper left", fontsize=8)
ax.grid(True, linestyle=":", alpha=0.5)
ax.set_facecolor(COLORS["background"])

# (3) Rolling skewness
ax = axes[1, 0]
ax.plot(rolling_skew, color=COLORS["secondary"], linewidth=1.5)
ax.axhline(0, color=COLORS["neutral"], linestyle=":", linewidth=1.0)
ax.set_xlabel("Time step")
ax.set_ylabel("Skewness")
ax.set_title("Rolling Skewness")
ax.grid(True, linestyle=":", alpha=0.5)
ax.set_facecolor(COLORS["background"])

# (4) Rolling kurtosis
ax = axes[1, 1]
ax.plot(rolling_kurt, color=COLORS["danger"], linewidth=1.5)
ax.axhline(0, color=COLORS["neutral"], linestyle=":", linewidth=1.0)
ax.set_xlabel("Time step")
ax.set_ylabel("Kurtosis")
ax.set_title("Rolling Kurtosis")
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
