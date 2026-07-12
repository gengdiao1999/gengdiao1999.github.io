"""
03-example-06-periodicity-features.py
Generated for book/part-01-feature-extraction/03-statistical-features/README.md

This script generates Figure 3-6: a synthetic periodic series, estimates its
period via ACF peak detection, periodogram peak detection, and rolling-window
period stability, then visualizes the results.
"""
import pathlib

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import periodogram
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

white_noise_bound = 1.96 / np.sqrt(n)

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

print("周期性特征:")
print(f"  真实周期          = {true_period}")
print(f"  ACF 峰值周期      = {acf_period}")
print(f"  周期图峰值周期    = {fft_period:.2f}")
print(f"  滚动平均周期      = {mean_period:.2f}")
print(f"  周期稳定性        = {period_stability:.2f}")

# ---------------------------------------------------------------------------
# 5. Visualize in a flat 2x2 layout
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(10, 4.2))

# Panel 1: original series
axes[0, 0].plot(t, x, color=COLORS["primary"], linewidth=0.9, alpha=0.8, label="合成序列")
axes[0, 0].axvline(
    true_period,
    color=COLORS["accent"],
    linestyle="--",
    linewidth=1.0,
    label=f"真实周期 = {true_period}",
)
axes[0, 0].set_ylabel("取值")
axes[0, 0].set_xlabel("时间步")
axes[0, 0].set_title("合成周期序列")
axes[0, 0].grid(True, linestyle=":", alpha=0.5)
axes[0, 0].set_facecolor(COLORS["background"])
axes[0, 0].legend(loc="upper right")

# Panel 2: ACF with confidence band and first significant peak
lags = np.arange(len(acf_vals))
axes[0, 1].plot(lags, acf_vals, color=COLORS["primary"], linewidth=1.0)
axes[0, 1].axhline(0, color=COLORS["neutral"], linewidth=0.8, linestyle="-", alpha=0.6)
axes[0, 1].axhline(
    white_noise_bound,
    color=COLORS["accent"],
    linewidth=1.0,
    linestyle="--",
    label=f"95% 置信界 = {white_noise_bound:.3f}",
)
axes[0, 1].axhline(
    -white_noise_bound,
    color=COLORS["accent"],
    linewidth=1.0,
    linestyle="--",
)
if acf_period is not None:
    axes[0, 1].scatter(
        [acf_period],
        [acf_vals[acf_period]],
        color=COLORS["danger"],
        s=30,
        zorder=3,
        label=f"峰值 = {acf_period}",
    )
axes[0, 1].set_xlabel("滞后阶数")
axes[0, 1].set_ylabel("ACF")
axes[0, 1].set_title("ACF 峰值法")
axes[0, 1].grid(True, linestyle=":", alpha=0.5)
axes[0, 1].set_facecolor(COLORS["background"])
axes[0, 1].legend(loc="upper right")

# Panel 3: periodogram with dominant frequency
axes[1, 0].plot(freqs, power, color=COLORS["primary"], linewidth=1.0)
axes[1, 0].axvline(
    freqs[dominant_idx],
    color=COLORS["danger"],
    linestyle="--",
    linewidth=1.0,
    label=f"f = {freqs[dominant_idx]:.3f}",
)
axes[1, 0].set_xlabel("频率")
axes[1, 0].set_ylabel("功率")
axes[1, 0].set_title("周期图峰值法")
axes[1, 0].grid(True, linestyle=":", alpha=0.5)
axes[1, 0].set_facecolor(COLORS["background"])
axes[1, 0].legend(loc="upper right")

# Panel 4: rolling-window period estimates and stability
valid_idx = ~np.isnan(rolling_periods)
axes[1, 1].plot(
    t[valid_idx],
    rolling_periods[valid_idx],
    color=COLORS["secondary"],
    linewidth=1.0,
    label="滚动周期估计",
)
axes[1, 1].axhline(
    mean_period,
    color=COLORS["accent"],
    linestyle="--",
    linewidth=1.0,
    label=f"均值 = {mean_period:.1f}",
)
axes[1, 1].axhline(
    true_period,
    color=COLORS["neutral"],
    linestyle=":",
    linewidth=1.0,
    label=f"真实 = {true_period}",
)
axes[1, 1].set_xlabel("时间步")
axes[1, 1].set_ylabel("估计周期")
axes[1, 1].yaxis.get_major_formatter().set_useOffset(False)
axes[1, 1].set_title("滚动周期稳定性")
axes[1, 1].grid(True, linestyle=":", alpha=0.5)
axes[1, 1].set_facecolor(COLORS["background"])
axes[1, 1].legend(loc="upper right")

# Annotation (no box)
textstr = (
    f"ACF 周期 = {acf_period}\n"
    f"周期图周期 = {fft_period:.1f}\n"
    f"滚动稳定性 = {period_stability:.2f}"
)
axes[1, 1].text(
    0.02,
    0.98,
    textstr,
    transform=axes[1, 1].transAxes,
    fontsize=7,
    verticalalignment="top",
    horizontalalignment="left",
)

fig.tight_layout()

# ---------------------------------------------------------------------------
# 6. Save figure
# ---------------------------------------------------------------------------
out_dir = pathlib.Path(__file__).parent.parent / "images"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "03-fig-06-periodicity.png"
fig.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"\nSaved figure to {out_path}")
