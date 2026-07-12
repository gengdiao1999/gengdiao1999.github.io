"""
03-example-03-stationarity-features.py
Generated for book/part-01-feature-extraction/03-statistical-features/README.md

This script generates Figure 3-3: comparing stationarity features between a
stationary AR(1) series and a non-stationary series with trend and
heteroscedasticity.
"""
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss

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
    "figure.figsize": (5.3, 6.2),
})

# ---------------------------------------------------------------------------
# 1. Generate example series
# ---------------------------------------------------------------------------
rng = np.random.default_rng(42)
n = 200
t = np.arange(n)

# Stationary series: AR(1) with phi = 0.5, constant variance and positive level
phi = 0.5
level = 10.0
noise_stationary = rng.normal(scale=1.0, size=n)
x_stationary = np.zeros(n)
for i in range(1, n):
    x_stationary[i] = phi * x_stationary[i - 1] + noise_stationary[i]
x_stationary += level  # shift to positive mean so CV is interpretable

# Non-stationary series: deterministic trend + random walk + increasing variance
trend = 0.03 * t
walk = np.cumsum(rng.normal(scale=0.3, size=n))
hetero_scale = 1.0 + 0.02 * t  # variance grows over time
noise_nonstat = rng.normal(scale=hetero_scale, size=n)
x_nonstationary = trend + walk + noise_nonstat

# ---------------------------------------------------------------------------
# 2. Compute stationarity features
# ---------------------------------------------------------------------------
window = 30


def rolling_cv(series, window):
    """Return rolling mean, rolling variance, CV of mean, CV of variance."""
    s = pd.Series(series)
    rolling_mean = s.rolling(window=window).mean()
    rolling_var = s.rolling(window=window).var()
    valid_mean = rolling_mean.dropna()
    valid_var = rolling_var.dropna()
    cv_mean = valid_mean.std() / valid_mean.mean()
    cv_var = valid_var.std() / valid_var.mean()
    return rolling_mean, rolling_var, cv_mean, cv_var


def stationarity_summary(series, window=30):
    """Compute ADF, KPSS and rolling-CV features for a series."""
    adf_res = adfuller(series, autolag="AIC")
    kpss_res = kpss(series, regression="c", nlags="auto")
    rolling_mean, rolling_var, cv_mean, cv_var = rolling_cv(series, window)
    return {
        "adf_stat": adf_res[0],
        "adf_pvalue": adf_res[1],
        "adf_lags": adf_res[2],
        "adf_is_stationary": adf_res[1] < 0.05,
        "kpss_stat": kpss_res[0],
        "kpss_pvalue": kpss_res[1],
        "kpss_is_stationary": kpss_res[1] >= 0.05,
        "cv_mean": cv_mean,
        "cv_var": cv_var,
        "rolling_mean": rolling_mean,
        "rolling_var": rolling_var,
    }


feat_stationary = stationarity_summary(x_stationary, window=window)
feat_nonstationary = stationarity_summary(x_nonstationary, window=window)

print("Stationary series features:")
print(f"  ADF statistic = {feat_stationary['adf_stat']:.4f}")
print(f"  ADF p-value   = {feat_stationary['adf_pvalue']:.4f}")
print(f"  ADF lags      = {feat_stationary['adf_lags']}")
print(f"  ADF stationary? {feat_stationary['adf_is_stationary']}")
print(f"  KPSS statistic = {feat_stationary['kpss_stat']:.4f}")
print(f"  KPSS p-value   = {feat_stationary['kpss_pvalue']:.4f}")
print(f"  KPSS stationary? {feat_stationary['kpss_is_stationary']}")
print(f"  CV(mean) = {feat_stationary['cv_mean']:.4f}, CV(var) = {feat_stationary['cv_var']:.4f}")

print("\nNon-stationary series features:")
print(f"  ADF statistic = {feat_nonstationary['adf_stat']:.4f}")
print(f"  ADF p-value   = {feat_nonstationary['adf_pvalue']:.4f}")
print(f"  ADF lags      = {feat_nonstationary['adf_lags']}")
print(f"  ADF stationary? {feat_nonstationary['adf_is_stationary']}")
print(f"  KPSS statistic = {feat_nonstationary['kpss_stat']:.4f}")
print(f"  KPSS p-value   = {feat_nonstationary['kpss_pvalue']:.4f}")
print(f"  KPSS stationary? {feat_nonstationary['kpss_is_stationary']}")
print(f"  CV(mean) = {feat_nonstationary['cv_mean']:.4f}, CV(var) = {feat_nonstationary['cv_var']:.4f}")

# ---------------------------------------------------------------------------
# 3. Visualize
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(2, 1, sharex=True)

series_data = [
    (x_stationary, feat_stationary, "Stationary AR(1) series"),
    (x_nonstationary, feat_nonstationary, "Non-stationary series (trend + heteroscedasticity)"),
]

for ax, (x, feat, title) in zip(axes, series_data):
    # Primary axis: original series and rolling mean
    ax.plot(x, label="Original series", color=COLORS["primary"], linewidth=1.0, alpha=0.8)
    ax.plot(
        feat["rolling_mean"],
        label=f"Rolling mean (w={window})",
        color=COLORS["accent"],
        linewidth=1.5,
    )
    ax.set_ylabel("Value")
    ax.set_title(title)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.set_facecolor(COLORS["background"])

    # Secondary axis: rolling variance
    ax2 = ax.twinx()
    ax2.plot(
        feat["rolling_var"],
        label=f"Rolling variance (w={window})",
        color=COLORS["danger"],
        linewidth=1.2,
        linestyle="--",
        alpha=0.8,
    )
    ax2.set_ylabel("Rolling variance", color=COLORS["danger"])
    ax2.tick_params(axis="y", labelcolor=COLORS["danger"])

    # Combine legends
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=7)

    # Text annotation box with test results
    label = "stationary" if feat["adf_is_stationary"] else "non-stationary"
    textstr = (
        f"ADF: {feat['adf_stat']:.3f} (p={feat['adf_pvalue']:.3f}, lags={feat['adf_lags']})\n"
        f"KPSS: {feat['kpss_stat']:.3f} (p={feat['kpss_pvalue']:.3f})\n"
        f"CV(mean)={feat['cv_mean']:.3f}, CV(var)={feat['cv_var']:.3f}\n"
        f"Decision: {label}"
    )
    ax.text(
        0.98,
        0.97,
        textstr,
        transform=ax.transAxes,
        fontsize=8,
        verticalalignment="top",
        horizontalalignment="right",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=COLORS["neutral"], alpha=0.9),
    )

axes[-1].set_xlabel("Time step")
fig.tight_layout()

# ---------------------------------------------------------------------------
# 4. Save figure
# ---------------------------------------------------------------------------
out_dir = pathlib.Path(__file__).parent.parent / "images"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "03-fig-03-stationarity.png"
fig.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"\nSaved figure to {out_path}")
