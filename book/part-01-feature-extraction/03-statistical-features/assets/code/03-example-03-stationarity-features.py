"""
03-example-03-stationarity-features.py
Generated for book/part-01-feature-extraction/03-statistical-features/README.md

This script generates Figure 3-3: comparing stationarity features between a
stationary AR(1) series and a non-stationary series with trend and
heteroscedasticity.
"""
import pathlib
import warnings

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tools.sm_exceptions import InterpolationWarning
from statsmodels.tsa.stattools import adfuller, kpss

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
    "figure.figsize": (10, 3.5),
    "figure.autolayout": True,
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
    # KPSS may emit InterpolationWarning when p-values are outside the
    # tabulated range; this is expected and does not affect the statistic.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", InterpolationWarning)
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

print("平稳序列特征:")
print(f"  ADF 统计量 = {feat_stationary['adf_stat']:.4f}")
print(f"  ADF p-value = {feat_stationary['adf_pvalue']:.4f}")
print(f"  ADF 滞后阶数 = {feat_stationary['adf_lags']}")
print(f"  ADF 平稳? {feat_stationary['adf_is_stationary']}")
print(f"  KPSS 统计量 = {feat_stationary['kpss_stat']:.4f}")
print(f"  KPSS p-value = {feat_stationary['kpss_pvalue']:.4f}")
print(f"  KPSS 平稳? {feat_stationary['kpss_is_stationary']}")
print(f"  CV(均值) = {feat_stationary['cv_mean']:.4f}, CV(方差) = {feat_stationary['cv_var']:.4f}")

print("\n非平稳序列特征:")
print(f"  ADF 统计量 = {feat_nonstationary['adf_stat']:.4f}")
print(f"  ADF p-value = {feat_nonstationary['adf_pvalue']:.4f}")
print(f"  ADF 滞后阶数 = {feat_nonstationary['adf_lags']}")
print(f"  ADF 平稳? {feat_nonstationary['adf_is_stationary']}")
print(f"  KPSS 统计量 = {feat_nonstationary['kpss_stat']:.4f}")
print(f"  KPSS p-value = {feat_nonstationary['kpss_pvalue']:.4f}")
print(f"  KPSS 平稳? {feat_nonstationary['kpss_is_stationary']}")
print(f"  CV(均值) = {feat_nonstationary['cv_mean']:.4f}, CV(方差) = {feat_nonstationary['cv_var']:.4f}")

# ---------------------------------------------------------------------------
# 3. Visualize
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, sharex=True, figsize=(10, 3.2))

series_data = [
    (x_stationary, feat_stationary, "平稳 AR(1) 序列"),
    (x_nonstationary, feat_nonstationary, "非平稳序列（趋势 + 异方差）"),
]

for ax, (x, feat, title) in zip(axes, series_data):
    # Primary axis: original series and rolling mean
    ax.plot(x, label="原始序列", color=COLORS["primary"], linewidth=1.0, alpha=0.8)
    ax.plot(
        feat["rolling_mean"],
        label=f"滚动均值 (w={window})",
        color=COLORS["accent"],
        linewidth=1.2,
    )
    ax.set_xlabel("时间步")
    ax.set_ylabel("取值")
    ax.set_title(title)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.set_facecolor(COLORS["background"])

    # Secondary axis: rolling variance
    ax2 = ax.twinx()
    ax2.plot(
        feat["rolling_var"],
        label=f"滚动方差 (w={window})",
        color=COLORS["danger"],
        linewidth=1.0,
        linestyle="--",
        alpha=0.8,
    )
    ax2.set_ylabel("滚动方差", color=COLORS["danger"])
    ax2.tick_params(axis="y", labelcolor=COLORS["danger"])

    # Combine legends without frame
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    # Text annotation (no background box)
    label = "平稳" if feat["adf_is_stationary"] else "非平稳"
    textstr = (
        f"ADF: {feat['adf_stat']:.3f} (p={feat['adf_pvalue']:.3f}, lags={feat['adf_lags']})\n"
        f"KPSS: {feat['kpss_stat']:.3f} (p={feat['kpss_pvalue']:.3f})\n"
        f"CV(均值)={feat['cv_mean']:.3f}, CV(方差)={feat['cv_var']:.3f}\n"
        f"判定: {label}"
    )
    ax.text(
        0.98,
        0.97,
        textstr,
        transform=ax.transAxes,
        fontsize=7,
        verticalalignment="top",
        horizontalalignment="right",
    )

fig.tight_layout()

# ---------------------------------------------------------------------------
# 4. Save figure
# ---------------------------------------------------------------------------
out_dir = pathlib.Path(__file__).parent.parent / "images"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "03-fig-03-stationarity.png"
fig.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"\nSaved figure to {out_path}")
