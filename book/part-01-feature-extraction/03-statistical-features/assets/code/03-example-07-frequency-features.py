"""
03-example-07-frequency-features.py
Generated for book/part-01-feature-extraction/03-statistical-features/README.md

This script generates Figure 3-7: a synthetic series composed of multiple
frequency components, then extracts FFT amplitude features, Welch PSD features,
and low/mid/high frequency band energy ratios.
"""
import pathlib

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import welch

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
    "figure.figsize": (12, 3.0),
    "figure.autolayout": True,
})

# ---------------------------------------------------------------------------
# 1. Generate a synthetic multi-frequency series
# ---------------------------------------------------------------------------
rng = np.random.default_rng(42)
fs = 1000.0          # Sampling frequency (Hz)
n = 2048             # Number of samples
t = np.arange(n) / fs

components = {
    "low":    {"freq": 5.0,  "amp": 2.0},
    "mid":    {"freq": 50.0, "amp": 1.5},
    "high":   {"freq": 120.0, "amp": 1.0},
}
x = 0.3 * np.sin(2 * np.pi * 0.5 * t)  # very slow drift
for comp in components.values():
    x += comp["amp"] * np.sin(2 * np.pi * comp["freq"] * t)
x += rng.normal(scale=0.2, size=n)

# ---------------------------------------------------------------------------
# 2. FFT amplitude features
# ---------------------------------------------------------------------------
fft_vals = np.fft.rfft(x)
fft_freqs = np.fft.rfftfreq(n, d=1.0 / fs)
fft_power = np.abs(fft_vals) ** 2 / n
fft_magnitude = np.abs(fft_vals) / n

dominant_idx = 1 + int(np.argmax(fft_magnitude[1:]))
dominant_freq = fft_freqs[dominant_idx]
dominant_amp = fft_magnitude[dominant_idx]


def band_energy(freqs, power, fmin, fmax):
    mask = (freqs >= fmin) & (freqs < fmax)
    return float(np.sum(power[mask]))


low_band = (0.0, 30.0)
high_band = (100.0, fs / 2.0)
energy_low = band_energy(fft_freqs, fft_power, *low_band)
energy_high = band_energy(fft_freqs, fft_power, *high_band)
low_high_ratio = energy_low / (energy_high + 1e-12)

# ---------------------------------------------------------------------------
# 3. Welch PSD features
# ---------------------------------------------------------------------------
psd_freqs, psd_power = welch(x, fs=fs, nperseg=256, noverlap=128, window="hann")

p_f = psd_power / (np.sum(psd_power) + 1e-12)

spectral_entropy = float(-np.sum(p_f * np.log(p_f + 1e-12)))
spectral_centroid = float(np.sum(psd_freqs * p_f))
spectral_bandwidth = float(np.sqrt(np.sum(p_f * (psd_freqs - spectral_centroid) ** 2)))

# ---------------------------------------------------------------------------
# 4. Band energy ratios based on PSD
# ---------------------------------------------------------------------------
bands = {
    "低频":  (0.0, 30.0),
    "中频":  (30.0, 100.0),
    "高频":  (100.0, fs / 2.0),
}
band_energies = {name: band_energy(psd_freqs, psd_power, *b) for name, b in bands.items()}
total_energy = sum(band_energies.values()) + 1e-12
band_ratios = {name: energy / total_energy for name, energy in band_energies.items()}

print("频域特征:")
print(f"  主导频率        = {dominant_freq:.2f} Hz")
print(f"  主导幅值        = {dominant_amp:.4f}")
print(f"  低/高频能量比   = {low_high_ratio:.4f}")
print(f"  谱熵            = {spectral_entropy:.4f}")
print(f"  谱质心          = {spectral_centroid:.2f} Hz")
print(f"  谱带宽          = {spectral_bandwidth:.2f} Hz")
print("  频带能量占比:")
for name in ("低频", "中频", "高频"):
    print(f"    {name:4s}: {band_ratios[name]:.4f} ({band_energies[name]:.2f})")

# ---------------------------------------------------------------------------
# 5. Visualize in a flat 1x3 layout
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(12, 3.0))

# Panel 1: time series
axes[0].plot(t, x, color=COLORS["primary"], linewidth=0.8, alpha=0.9)
axes[0].set_xlabel("时间 (s)")
axes[0].set_ylabel("取值")
axes[0].set_title("合成多频序列")
axes[0].grid(True, linestyle=":", alpha=0.5)
axes[0].set_facecolor(COLORS["background"])

# Panel 2: FFT amplitude spectrum
axes[1].plot(fft_freqs, fft_magnitude, color=COLORS["primary"], linewidth=0.9)
axes[1].axvline(
    dominant_freq,
    color=COLORS["danger"],
    linestyle="--",
    linewidth=1.0,
    label=f"主导 = {dominant_freq:.1f} Hz",
)
axes[1].axvspan(*low_band, color=COLORS["secondary"], alpha=0.15, label="低频带")
axes[1].axvspan(*high_band, color=COLORS["accent"], alpha=0.15, label="高频带")
axes[1].set_xlabel("频率 (Hz)")
axes[1].set_ylabel("幅值")
axes[1].set_title("FFT 幅频谱")
axes[1].set_xlim(0, fs / 2.0)
axes[1].grid(True, linestyle=":", alpha=0.5)
axes[1].set_facecolor(COLORS["background"])
axes[1].legend(loc="upper right")

# Panel 3: Welch PSD with band shading
axes[2].fill_between(psd_freqs, psd_power, color=COLORS["primary"], alpha=0.3)
axes[2].plot(psd_freqs, psd_power, color=COLORS["primary"], linewidth=1.0)
axes[2].axvspan(*bands["低频"], color=COLORS["secondary"], alpha=0.15, label="低频")
axes[2].axvspan(*bands["中频"], color=COLORS["accent"], alpha=0.15, label="中频")
axes[2].axvspan(*bands["高频"], color=COLORS["danger"], alpha=0.10, label="高频")
axes[2].set_xlabel("频率 (Hz)")
axes[2].set_ylabel("功率 / Hz")
axes[2].set_title("Welch 功率谱密度")
axes[2].set_xlim(0, fs / 2.0)
axes[2].grid(True, linestyle=":", alpha=0.5)
axes[2].set_facecolor(COLORS["background"])
axes[2].legend(loc="upper right")

# Annotation (no box)
textstr = (
    f"主导频率 = {dominant_freq:.1f} Hz\n"
    f"主导幅值 = {dominant_amp:.3f}\n"
    f"低/高频比 = {low_high_ratio:.2f}\n"
    f"谱熵 = {spectral_entropy:.2f}\n"
    f"谱质心 = {spectral_centroid:.1f} Hz\n"
    f"谱带宽 = {spectral_bandwidth:.1f} Hz"
)
axes[2].text(
    0.02,
    0.98,
    textstr,
    transform=axes[2].transAxes,
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
out_path = out_dir / "03-fig-07-frequency.png"
fig.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"\nSaved figure to {out_path}")
