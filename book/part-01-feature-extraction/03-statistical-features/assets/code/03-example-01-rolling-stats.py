"""
03-example-01-rolling-stats.py
Generated for book/part-01-feature-extraction/03-statistical-features/README.md

This script generates Figure 3-1: an example of rolling mean and standard deviation.
"""
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

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
    "figure.figsize": (8, 4.5),
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
print("=== Global statistics ===")
print(f"Mean:        {np.mean(x):.3f}")
print(f"Std:         {np.std(x):.3f}")
print(f"Skewness:    {stats.skew(x):.3f}")
print(f"Kurtosis:    {stats.kurtosis(x):.3f}")
print(f"Range:       {np.ptp(x):.3f}")
print(f"Median:      {np.median(x):.3f}")

# ---------------------------------------------------------------------------
# 3. Rolling-window statistics
# ---------------------------------------------------------------------------
window = 20
s = pd.Series(x)
rolling_mean = s.rolling(window=window).mean()
rolling_std = s.rolling(window=window).std()

# ---------------------------------------------------------------------------
# 4. Visualize
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.5))

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

ax.set_xlabel("Time step")
ax.set_ylabel("Value")
ax.set_title("Rolling Mean and Standard Deviation")
ax.legend(loc="upper left")
ax.grid(True, linestyle=":", alpha=0.5)
ax.set_facecolor(COLORS["background"])
fig.tight_layout()

# ---------------------------------------------------------------------------
# 5. Save figure
# ---------------------------------------------------------------------------
out_dir = pathlib.Path(__file__).parent.parent / "images"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "03-fig-01-rolling-mean-std.png"
fig.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"Saved figure to {out_path}")
