"""
03-example-01-basic-stats.py
Generated for book/part-01-feature-extraction/03-statistical-features/README.md

This script generates Figure 3-1: an overview of basic statistical features.
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
    "figure.figsize": (8, 6),
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

print("=== Basic statistics ===")
print(f"Mean:        {mean:.3f}")
print(f"Median:      {median:.3f}")
print(f"Mode:        {mode:.3f}")
print(f"Variance:    {variance:.3f}")
print(f"Std:         {std:.3f}")
print(f"Range:       {range_val:.3f}")
print(f"Q1:          {q1:.3f}")
print(f"Q3:          {q3:.3f}")
print(f"IQR:         {iqr:.3f}")
print(f"Skewness:    {skewness:.3f}")
print(f"Kurtosis:    {kurtosis:.3f}")
print(f"Energy:      {energy:.3f}")
print(f"RMS:         {rms:.3f}")
print(f"Zero-cross:  {zcr:.3f}")

# ---------------------------------------------------------------------------
# 3. Visualize
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(2, 1, figsize=(8, 6), height_ratios=[2, 1])

# Time series with key reference levels
ax = axes[0]
ax.plot(x, label="Original series", color=COLORS["primary"], linewidth=1.2)
ax.axhline(mean, color=COLORS["accent"], linestyle="--", label="Mean")
ax.axhline(median, color=COLORS["secondary"], linestyle="-.", label="Median")
ax.axhline(q1, color=COLORS["neutral"], linestyle=":", label="Q1 / Q3")
ax.axhline(q3, color=COLORS["neutral"], linestyle=":")
ax.set_xlabel("Time step")
ax.set_ylabel("Value")
ax.set_title("Basic Statistical Features Overview")
ax.legend(loc="upper left", fontsize=8)
ax.grid(True, linestyle=":", alpha=0.5)
ax.set_facecolor(COLORS["background"])

# Histogram with central tendency and spread markers
ax = axes[1]
ax.hist(x, bins=20, color=COLORS["primary"], edgecolor="white", alpha=0.7)
ax.axvline(mean, color=COLORS["accent"], linestyle="--", linewidth=1.5, label="Mean")
ax.axvline(median, color=COLORS["secondary"], linestyle="-.", linewidth=1.5, label="Median")
ax.axvline(q1, color=COLORS["neutral"], linestyle=":", linewidth=1.5)
ax.axvline(q3, color=COLORS["neutral"], linestyle=":", linewidth=1.5)
ax.set_xlabel("Value")
ax.set_ylabel("Count")
ax.set_title("Distribution Histogram")
ax.legend(loc="upper right", fontsize=8)
ax.grid(True, linestyle=":", alpha=0.5)
ax.set_facecolor(COLORS["background"])

# Compact statistics table as a text box
stat_text = (
    f"Mean={mean:.2f}\n"
    f"Median={median:.2f}\n"
    f"Std={std:.2f}\n"
    f"Range={range_val:.2f}\n"
    f"IQR={iqr:.2f}\n"
    f"Skew={skewness:.2f}\n"
    f"Kurt={kurtosis:.2f}\n"
    f"Energy={energy:.1f}\n"
    f"RMS={rms:.2f}\n"
    f"ZCR={zcr:.2f}"
)
ax.text(
    0.02,
    0.98,
    stat_text,
    transform=ax.transAxes,
    fontsize=8,
    verticalalignment="top",
    fontfamily="monospace",
    bbox=dict(boxstyle="round", facecolor=COLORS["background"], alpha=0.9),
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
