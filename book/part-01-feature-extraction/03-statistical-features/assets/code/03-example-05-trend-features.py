"""
03-example-05-trend-features.py
Generated for book/part-01-feature-extraction/03-statistical-features/README.md

This script generates Figure 3-5: a synthetic series with trend and noise, and
visualizes linear trend, STL trend strength, Mann-Kendall S statistic, and
local rolling slope signs.
"""
import pathlib

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.seasonal import STL

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
    "figure.figsize": (10, 3.2),
    "figure.autolayout": True,
})

# ---------------------------------------------------------------------------
# 1. Generate synthetic series with trend and noise
# ---------------------------------------------------------------------------
rng = np.random.default_rng(42)
n = 240
t = np.arange(n)

# Piecewise linear trend + low-frequency fluctuation + noise
trend = np.where(t < n // 2, 0.04 * t, 0.04 * (n // 2) - 0.02 * (t - n // 2))
low_freq = 1.5 * np.sin(2 * np.pi * t / 60)
noise = rng.normal(scale=0.8, size=n)
x = trend + low_freq + noise

s = pd.Series(x, index=pd.RangeIndex(start=0, stop=n, step=1))

# ---------------------------------------------------------------------------
# 2. Linear trend (OLS via numpy polyfit)
# ---------------------------------------------------------------------------
coefs = np.polyfit(t, x, 1)  # [slope, intercept]
slope_linear, intercept_linear = coefs
linear_trend = slope_linear * t + intercept_linear
r2_linear = 1.0 - np.sum((x - linear_trend) ** 2) / np.sum((x - np.mean(x)) ** 2)

# ---------------------------------------------------------------------------
# 3. STL decomposition and trend strength
# ---------------------------------------------------------------------------
# STL period must be odd for the default seasonal smoother.
# Here we use a small dummy period to separate low-frequency trend from noise.
period = 11
stl = STL(s, period=period, robust=False)
res = stl.fit()


def trend_strength(trend, residual):
    """Trend strength based on STL decomposition.

    F_t = 1 - Var(R_t) / Var(T_t + R_t)
    """
    signal = trend + residual
    var_residual = np.var(residual, ddof=1)
    var_signal = np.var(signal, ddof=1)
    if var_signal < 1e-12:
        return 0.0
    return 1.0 - var_residual / var_signal


F_t = trend_strength(res.trend.values, res.resid.values)

# ---------------------------------------------------------------------------
# 4. Mann-Kendall S statistic
# ---------------------------------------------------------------------------
def mann_kendall_s(series):
    """Compute Kendall's S statistic for monotonic trend detection.

    S = sum_{i < j} sign(x_j - x_i)
    """
    x_arr = np.asarray(series)
    n_val = len(x_arr)
    s = 0
    for i in range(n_val - 1):
        s += np.sum(np.sign(x_arr[i + 1:] - x_arr[i]))
    return int(s)


mk_s = mann_kendall_s(x)
# Cross-check with scipy.stats.kendalltau against time index
tau, tau_pvalue = stats.kendalltau(t, x)
mk_s_scipy = int(tau * n * (n - 1) / 2)

# ---------------------------------------------------------------------------
# 5. Local trend changes via rolling window slope signs
# ---------------------------------------------------------------------------
window = 30


def rolling_slope(series, window):
    """Return slope of OLS fit in each rolling window; first window-1 values are NaN."""
    s_arr = np.asarray(series)
    n_val = len(s_arr)
    slopes = np.full(n_val, np.nan)
    for i in range(window - 1, n_val):
        y = s_arr[i - window + 1 : i + 1]
        x_win = np.arange(window) - (window - 1) / 2.0
        slopes[i] = np.sum((x_win - np.mean(x_win)) * (y - np.mean(y))) / np.sum(
            (x_win - np.mean(x_win)) ** 2
        )
    return slopes


rolling_slopes = rolling_slope(s, window)
rolling_signs = np.sign(rolling_slopes)

valid_signs = pd.Series(rolling_signs).dropna().values
sign_changes = int(np.sum(np.abs(np.diff(valid_signs)) > 1e-12))

print("线性趋势:")
print(f"  斜率 beta_1 = {slope_linear:.6f}")
print(f"  截距 beta_0 = {intercept_linear:.4f}")
print(f"  R^2 = {r2_linear:.4f}")
print(f"\nSTL 趋势强度 F_t = {F_t:.4f}")
print(f"\nMann-Kendall S 统计量 = {mk_s} (scipy 校验: {mk_s_scipy})")
print(f"Kendall tau = {tau:.4f}, p-value = {tau_pvalue:.4e}")
print(f"\n滚动斜率符号 (window={window}):")
print(f"  正窗口数: {int(np.sum(valid_signs > 0))}")
print(f"  负窗口数: {int(np.sum(valid_signs < 0))}")
print(f"  符号变化次数: {sign_changes}")

# ---------------------------------------------------------------------------
# 6. Visualize in a flat 1x2 layout
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, sharex=True, figsize=(10, 3.2))

# Panel 1: original series with linear and STL trends
axes[0].plot(t, x, label="原始序列", color=COLORS["primary"], linewidth=0.9, alpha=0.8)
axes[0].plot(
    t,
    linear_trend,
    label=f"线性趋势 ($\\beta_1$={slope_linear:.4f})",
    color=COLORS["accent"],
    linewidth=1.2,
    linestyle="--",
)
axes[0].plot(
    t,
    res.trend.values,
    label="STL 趋势",
    color=COLORS["secondary"],
    linewidth=1.2,
)
axes[0].set_ylabel("取值")
axes[0].set_xlabel("时间步")
axes[0].set_title("趋势特征示例")
axes[0].grid(True, linestyle=":", alpha=0.5)
axes[0].set_facecolor(COLORS["background"])
axes[0].legend(loc="upper left")

# Annotation (no box)
textstr = (
    f"线性 $R^2$ = {r2_linear:.3f}\n"
    f"趋势强度 $F_t$ = {F_t:.3f}\n"
    f"Mann-Kendall $S$ = {mk_s}\n"
    f"滚动符号变化 = {sign_changes}"
)
axes[0].text(
    0.98,
    0.97,
    textstr,
    transform=axes[0].transAxes,
    fontsize=7,
    verticalalignment="top",
    horizontalalignment="right",
)

# Panel 2: rolling window slope and its sign
axes[1].axhline(0, color=COLORS["neutral"], linewidth=0.8, linestyle="-", alpha=0.6)
axes[1].plot(t, rolling_slopes, label=f"滚动斜率 (w={window})", color=COLORS["accent"], linewidth=1.0)
axes[1].scatter(
    t[window - 1:],
    rolling_slopes[window - 1:],
    c=np.where(rolling_signs[window - 1:] > 0, COLORS["secondary"], COLORS["danger"]),
    s=10,
    zorder=3,
    label="斜率符号 (+/−)",
)
axes[1].set_ylabel("斜率")
axes[1].set_xlabel("时间步")
axes[1].set_title("局部滚动斜率符号")
axes[1].grid(True, linestyle=":", alpha=0.5)
axes[1].set_facecolor(COLORS["background"])
axes[1].legend(loc="upper left")

fig.tight_layout()

# ---------------------------------------------------------------------------
# 7. Save figure
# ---------------------------------------------------------------------------
out_dir = pathlib.Path(__file__).parent.parent / "images"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "03-fig-05-trend.png"
fig.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"\nSaved figure to {out_path}")
