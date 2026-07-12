"""
03-example-06-periodicity-features.py
Generated for book/part-01-feature-extraction/03-statistical-features/README.md

This script generates Figure 3-6: a synthetic periodic series, estimates its
period via ACF peak detection, periodogram peak detection, and rolling-window
period stability, then visualizes the results.
"""
import pathlib

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import periodogram
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
    "figure.figsize": (5.2, 5.6),
})

# ---------------------------------------------------------------------------
# 1. Generate a synthetic periodic series
# ---------------------------------------------------------------------------
rng = np.random.default_rng(42)
n = 360
true_period = 24
amplitude = 3.0
noise_std = 0.5

t = np.arange(n)
x = amplitude * np.sin(2 * np.pi * t / true_period) + rng.normal(scale=noise_std, size=n)

# ---------------------------------------------------------------------------
# 2. Period estimation via ACF peak
# ---------------------------------------------------------------------------
nlags = n // 2
acf_vals = acf(x, nlags=nlags, fft=True)

# Approximate 95% confidence bound under the white-noise hypothesis.
white_noise_bound = 1.96 / np.sqrt(n)

# The first local maximum that exceeds the confidence bound.
acf_peaks = []
for k in range(1, len(acf_vals) - 1):
    if (
        acf_vals[k] > white_noise_bound
        and acf_vals[k] > acf_vals[k - 1]
        and acf_vals[k] > acf_vals[k + 1]
    ):
        acf_peaks.append(k)
        break

acf_period = acf_peaks[0] if acf_peaks else None

# ---------------------------------------------------------------------------
# Helper: parabolic interpolation around a discrete spectrum peak
# ---------------------------------------------------------------------------
def refined_period(frequencies, power, peak_idx):
    """Return the refined period using parabolic interpolation around peak_idx."""
    alpha = power[peak_idx - 1]
    beta = power[peak_idx]
    gamma = power[peak_idx + 1]
    denom = alpha - 2.0 * beta + gamma
    if abs(denom) < 1e-12:
        return 1.0 / frequencies[peak_idx]
    p = 0.5 * (alpha - gamma) / denom
    refined_freq = frequencies[peak_idx] + p * (frequencies[1] - frequencies[0])
    return 1.0 / refined_freq


# ---------------------------------------------------------------------------
# 3. Period estimation via periodogram (FFT) peak
# ---------------------------------------------------------------------------
freqs, power = periodogram(x, fs=1.0)
# Exclude the zero-frequency component.
dominant_idx = 1 + int(np.argmax(power[1:]))
fft_period = refined_period(freqs, power, dominant_idx)

# ---------------------------------------------------------------------------
# 4. Rolling-window period stability
# ---------------------------------------------------------------------------
window = 96
rolling_periods = np.full(n, np.nan)

for i in range(window - 1, n):
    win = x[i - window + 1 : i + 1]
    f_win, p_win = periodogram(win, fs=1.0)
    idx = 1 + int(np.argmax(p_win[1:]))
    rolling_periods[i] = refined_period(f_win, p_win, idx)

period_stability = float(np.nanstd(rolling_periods))
mean_period = float(np.nanmean(rolling_periods))

print("Periodicity features:")
print(f"  True period          = {true_period}")
print(f"  ACF peak period      = {acf_period}")
print(f"  Periodogram period   = {fft_period:.2f}")
print(f"  Rolling mean period  = {mean_period:.2f}")
print(f"  Period stability     = {period_stability:.2f}")

# ---------------------------------------------------------------------------
# 5. Visualize
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(5.2, 5.6))
gs = fig.add_gridspec(3, 2, hspace=0.40, wspace=0.30)

ax_series = fig.add_subplot(gs[0, :])
ax_acf = fig.add_subplot(gs[1, 0])
ax_periodogram = fig.add_subplot(gs[1, 1])
ax_rolling = fig.add_subplot(gs[2, :])

# Panel 1: original series
ax_series.plot(t, x, color=COLORS["primary"], linewidth=0.9, alpha=0.8, label="Synthetic series")
ax_series.axvline(
    true_period,
    color=COLORS["accent"],
    linestyle="--",
    linewidth=1.2,
    label=f"True period = {true_period}",
)
ax_series.set_ylabel("Value")
ax_series.set_title("Synthetic Periodic Series")
ax_series.grid(True, linestyle=":", alpha=0.5)
ax_series.set_facecolor(COLORS["background"])
ax_series.legend(loc="upper right", fontsize=8)

# Panel 2: ACF with confidence band and first significant peak
lags = np.arange(len(acf_vals))
ax_acf.plot(lags, acf_vals, color=COLORS["primary"], linewidth=1.0)
ax_acf.axhline(0, color=COLORS["neutral"], linewidth=0.8, linestyle="-", alpha=0.6)
ax_acf.axhline(
    white_noise_bound,
    color=COLORS["accent"],
    linewidth=1.0,
    linestyle="--",
    label=f"95% bound = {white_noise_bound:.3f}",
)
ax_acf.axhline(
    -white_noise_bound,
    color=COLORS["accent"],
    linewidth=1.0,
    linestyle="--",
)
if acf_period is not None:
    ax_acf.scatter(
        [acf_period],
        [acf_vals[acf_period]],
        color=COLORS["danger"],
        s=40,
        zorder=3,
        label=f"Peak = {acf_period}",
    )
ax_acf.set_xlabel("Lag")
ax_acf.set_ylabel("ACF")
ax_acf.set_title("ACF Peak Method")
ax_acf.grid(True, linestyle=":", alpha=0.5)
ax_acf.set_facecolor(COLORS["background"])
ax_acf.legend(loc="upper right", fontsize=8)

# Panel 3: periodogram with dominant frequency
ax_periodogram.plot(freqs, power, color=COLORS["primary"], linewidth=1.0)
ax_periodogram.axvline(
    freqs[dominant_idx],
    color=COLORS["danger"],
    linestyle="--",
    linewidth=1.2,
    label=f"f = {freqs[dominant_idx]:.3f}",
)
ax_periodogram.set_xlabel("Frequency")
ax_periodogram.set_ylabel("Power")
ax_periodogram.set_title("Periodogram Peak Method")
ax_periodogram.grid(True, linestyle=":", alpha=0.5)
ax_periodogram.set_facecolor(COLORS["background"])
ax_periodogram.legend(loc="upper right", fontsize=8)

# Panel 4: rolling-window period estimates and stability
valid_idx = ~np.isnan(rolling_periods)
ax_rolling.plot(
    t[valid_idx],
    rolling_periods[valid_idx],
    color=COLORS["secondary"],
    linewidth=1.2,
    label="Rolling period estimate",
)
ax_rolling.axhline(
    mean_period,
    color=COLORS["accent"],
    linestyle="--",
    linewidth=1.2,
    label=f"Mean = {mean_period:.1f}",
)
ax_rolling.axhline(
    true_period,
    color=COLORS["neutral"],
    linestyle=":",
    linewidth=1.0,
    label=f"True = {true_period}",
)
ax_rolling.set_xlabel("Time step")
ax_rolling.set_ylabel("Estimated period")
ax_rolling.set_title("Rolling-Window Period Stability")
ax_rolling.grid(True, linestyle=":", alpha=0.5)
ax_rolling.set_facecolor(COLORS["background"])
ax_rolling.legend(loc="upper right", fontsize=8)

# Annotation box with estimated periods and stability
textstr = (
    f"ACF period = {acf_period}\n"
    f"Periodogram period = {fft_period:.1f}\n"
    f"Rolling stability = {period_stability:.2f}"
)
ax_rolling.text(
    0.02,
    0.98,
    textstr,
    transform=ax_rolling.transAxes,
    fontsize=9,
    verticalalignment="top",
    horizontalalignment="left",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=COLORS["neutral"], alpha=0.9),
)

# ---------------------------------------------------------------------------
# 6. Save figure
# ---------------------------------------------------------------------------
out_dir = pathlib.Path(__file__).parent.parent / "images"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "03-fig-06-periodicity.png"
fig.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"\nSaved figure to {out_path}")
