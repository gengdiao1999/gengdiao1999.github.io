"""
03-example-07-frequency-features.py
Generated for book/part-01-feature-extraction/03-statistical-features/README.md

This script generates Figure 3-7: a synthetic series composed of multiple
frequency components, then extracts FFT amplitude features, Welch PSD features,
and low/mid/high frequency band energy ratios.
"""
import pathlib

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.signal import welch

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
    "figure.figsize": (5.2, 6.0),
})

# ---------------------------------------------------------------------------
# 1. Generate a synthetic multi-frequency series
# ---------------------------------------------------------------------------
rng = np.random.default_rng(42)
fs = 1000.0          # Sampling frequency (Hz)
n = 2048             # Number of samples
t = np.arange(n) / fs

# Three sinusoidal components + trend-like low-frequency drift + noise
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

# Exclude the DC component (index 0) for dominant-frequency estimation.
dominant_idx = 1 + int(np.argmax(fft_magnitude[1:]))
dominant_freq = fft_freqs[dominant_idx]
dominant_amp = fft_magnitude[dominant_idx]

# Low/high frequency energy ratio (using squared amplitudes / power).
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

# Normalized spectral distribution
p_f = psd_power / (np.sum(psd_power) + 1e-12)

# Spectral entropy
spectral_entropy = float(-np.sum(p_f * np.log(p_f + 1e-12)))

# Spectral centroid
spectral_centroid = float(np.sum(psd_freqs * p_f))

# Spectral bandwidth
spectral_bandwidth = float(np.sqrt(np.sum(p_f * (psd_freqs - spectral_centroid) ** 2)))

# ---------------------------------------------------------------------------
# 4. Band energy ratios based on PSD
# ---------------------------------------------------------------------------
bands = {
    "low":  (0.0, 30.0),
    "mid":  (30.0, 100.0),
    "high": (100.0, fs / 2.0),
}
band_energies = {name: band_energy(psd_freqs, psd_power, *b) for name, b in bands.items()}
total_energy = sum(band_energies.values()) + 1e-12
band_ratios = {name: energy / total_energy for name, energy in band_energies.items()}

print("Frequency-domain features:")
print(f"  Dominant frequency        = {dominant_freq:.2f} Hz")
print(f"  Dominant amplitude        = {dominant_amp:.4f}")
print(f"  Low/high energy ratio     = {low_high_ratio:.4f}")
print(f"  Spectral entropy          = {spectral_entropy:.4f}")
print(f"  Spectral centroid         = {spectral_centroid:.2f} Hz")
print(f"  Spectral bandwidth        = {spectral_bandwidth:.2f} Hz")
print("  Band energy ratios (PSD):")
for name in ("low", "mid", "high"):
    print(f"    {name:5s}: {band_ratios[name]:.4f} ({band_energies[name]:.2f})")

# ---------------------------------------------------------------------------
# 5. Visualize
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(3, 1, figsize=(5.2, 6.0))

# Panel 1: time series
axes[0].plot(t, x, color=COLORS["primary"], linewidth=0.8, alpha=0.9)
axes[0].set_xlabel("Time (s)")
axes[0].set_ylabel("Value")
axes[0].set_title("Synthetic Multi-Frequency Series")
axes[0].grid(True, linestyle=":", alpha=0.5)
axes[0].set_facecolor(COLORS["background"])

# Panel 2: FFT amplitude spectrum
axes[1].plot(fft_freqs, fft_magnitude, color=COLORS["primary"], linewidth=0.9)
axes[1].axvline(
    dominant_freq,
    color=COLORS["danger"],
    linestyle="--",
    linewidth=1.2,
    label=f"Dominant = {dominant_freq:.1f} Hz",
)
axes[1].axvspan(*low_band, color=COLORS["secondary"], alpha=0.15, label="Low band")
axes[1].axvspan(*high_band, color=COLORS["accent"], alpha=0.15, label="High band")
axes[1].set_xlabel("Frequency (Hz)")
axes[1].set_ylabel("Amplitude")
axes[1].set_title("FFT Amplitude Spectrum")
axes[1].set_xlim(0, fs / 2.0)
axes[1].grid(True, linestyle=":", alpha=0.5)
axes[1].set_facecolor(COLORS["background"])
axes[1].legend(loc="upper right", fontsize=8)

# Panel 3: Welch PSD with band shading
axes[2].fill_between(psd_freqs, psd_power, color=COLORS["primary"], alpha=0.3)
axes[2].plot(psd_freqs, psd_power, color=COLORS["primary"], linewidth=1.0)
axes[2].axvspan(*bands["low"], color=COLORS["secondary"], alpha=0.15, label="Low")
axes[2].axvspan(*bands["mid"], color=COLORS["accent"], alpha=0.15, label="Mid")
axes[2].axvspan(*bands["high"], color=COLORS["danger"], alpha=0.10, label="High")
axes[2].set_xlabel("Frequency (Hz)")
axes[2].set_ylabel("Power / Hz")
axes[2].set_title("Welch Power Spectral Density")
axes[2].set_xlim(0, fs / 2.0)
axes[2].grid(True, linestyle=":", alpha=0.5)
axes[2].set_facecolor(COLORS["background"])
axes[2].legend(loc="upper right", fontsize=8)

# Annotation box with key features
textstr = (
    f"Dominant freq = {dominant_freq:.1f} Hz\n"
    f"Dominant amp = {dominant_amp:.3f}\n"
    f"Low/high ratio = {low_high_ratio:.2f}\n"
    f"Spectral entropy = {spectral_entropy:.2f}\n"
    f"Spectral centroid = {spectral_centroid:.1f} Hz\n"
    f"Bandwidth = {spectral_bandwidth:.1f} Hz"
)
axes[2].text(
    0.02,
    0.98,
    textstr,
    transform=axes[2].transAxes,
    fontsize=8,
    verticalalignment="top",
    horizontalalignment="left",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=COLORS["neutral"], alpha=0.9),
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
