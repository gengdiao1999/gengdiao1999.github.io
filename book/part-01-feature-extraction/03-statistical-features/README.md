# 第 3 章 特征提取

特征提取是时间序列分析的首要步骤。好的特征能够以少量标量或向量刻画序列的核心模式，为后续的分类、异常检测、预测与因果分析提供可解释且稳定的输入。本章从统计特征、时域特征与频域特征三个层面展开，并讨论特征组合与工程实践中的常见问题。

## 本章目标

- 掌握常用的全局与局部统计特征：均值、方差、偏度、峰度、分位数、滑动窗口统计量等。
- 理解平稳性、季节性、趋势性与周期性等时域特征的刻画方法。
- 能够使用傅里叶变换与功率谱密度提取频域特征，并解释频带能量的物理意义。
- 了解特征组合、缩放与选择在时序工程实践中的典型流程。
- 能够使用 Python（`numpy`、`pandas`、`scipy`、`statsmodels`）计算并可视化上述特征。

## 1. 引言

## 2. 统计特征

统计特征用少量标量刻画整条序列或局部窗口的数值特性，是后续建模最直接、最可解释的特征来源。下面按全局基本量、分布形态、能量与计数、滑动窗口四个层面展开。

### 2.1 基本统计量

基本统计量描述序列的中心位置与离散程度，是所有特征工程的基础。

| 特征 | 直观含义 |
|------|----------|
| 均值（Mean） | 序列的算术平均中心 |
| 中位数（Median） | 排序后位于中间位置的值，对异常值更稳健 |
| 众数（Mode） | 出现频率最高的值，适合离散或近似重复的序列 |
| 方差（Variance） / 标准差（Std） | 序列偏离均值的平均幅度 |
| 极差（Range） | 最大值与最小值之差，反映整体波动范围 |
| 四分位距（IQR） | 第三四分位数与第一四分位数之差，反映中间 50% 数据的离散程度 |

常用公式如下：

$$
\bar{x} = \frac{1}{N}\sum_{i=1}^{N}x_i
$$

$$
\sigma = \sqrt{\frac{1}{N}\sum_{i=1}^{N}(x_i - \bar{x})^2}
$$

$$
\text{Range} = \max(\mathbf{x}) - \min(\mathbf{x})
$$

$$
\text{IQR} = Q_3 - Q_1
$$

其中 $Q_1$ 与 $Q_3$ 分别为第 25% 与第 75% 分位数。

使用 `numpy`/`pandas` 可一行计算：

```python
import numpy as np

mean = np.mean(x)
median = np.median(x)
std = np.std(x)
q1, q3 = np.percentile(x, [25, 75])
iqr = q3 - q1
range_val = np.ptp(x)  # np.max(x) - np.min(x)
```

完整脚本见 [`assets/code/03-example-01-basic-stats.py`](./assets/code/03-example-01-basic-stats.py)。

![图 3-1 基本统计量概览](./assets/images/03-fig-01-basic-stats.png)

**图 3-1** 基本统计量概览。

### 2.2 分布形态特征

分布形态特征刻画序列取值分布的不对称性与尾部厚度，对异常检测与模型假设检验尤为重要。

**偏度（Skewness）**衡量分布的不对称程度：

$$
\gamma_1 = \frac{1}{N}\sum_{i=1}^{N}\left(\frac{x_i-\bar{x}}{\sigma}\right)^3
$$

- $\gamma_1 = 0$ 表示大致对称；
- $\gamma_1 > 0$ 表示右偏（长尾在右）；
- $\gamma_1 < 0$ 表示左偏（长尾在左）。

**峰度（Kurtosis）**衡量分布尾部的厚重程度，工程上常用超额峰度：

$$
\gamma_2 = \frac{1}{N}\sum_{i=1}^{N}\left(\frac{x_i-\bar{x}}{\sigma}\right)^4 - 3
$$

- $\gamma_2 = 0$ 接近正态分布尾部；
- $\gamma_2 > 0$ 尾部更厚、极端值更多；
- $\gamma_2 < 0$ 尾部更轻、取值更集中。

```python
from scipy import stats

skewness = stats.skew(x)      # 偏度
kurtosis = stats.kurtosis(x)  # 超额峰度（已减去 3）
```

完整脚本见 [`assets/code/03-example-01-basic-stats.py`](./assets/code/03-example-01-basic-stats.py)。

![图 3-1 基本统计量概览](./assets/images/03-fig-01-basic-stats.png)

**图 3-1** 基本统计量概览。

### 2.3 能量与计数特征

能量特征反映序列整体的“强度”，计数特征则关注序列穿越某一参考水平的频繁程度。

**绝对能量（Absolute Energy）**是序列平方和：

$$
E = \sum_{t=1}^{N}x_t^2
$$

**均方根（Root Mean Square, RMS）**是能量的平均开方：

$$
\text{RMS} = \sqrt{\frac{1}{N}\sum_{t=1}^{N}x_t^2}
$$

**过零率（Zero Crossing Rate, ZCR）**统计相邻样本符号变化的次数，常用于信号处理与振动分析：

$$
\text{ZCR} = \frac{1}{N-1}\sum_{t=1}^{N-1}\mathbb{1}\{x_t \cdot x_{t+1} < 0\}
$$

```python
energy = np.sum(x ** 2)
rms = np.sqrt(np.mean(x ** 2))
zcr = np.sum((x[:-1] * x[1:]) < 0) / (len(x) - 1)
```

完整脚本见 [`assets/code/03-example-01-basic-stats.py`](./assets/code/03-example-01-basic-stats.py)。

![图 3-1 基本统计量概览](./assets/images/03-fig-01-basic-stats.png)

**图 3-1** 基本统计量概览。

### 2.4 滑动窗口统计特征

全局统计量会抹平时序的局部变化。滑动窗口统计特征在固定长度的窗口内重复计算上述指标，从而捕捉序列的局部平稳性、趋势转折与异常段。

给定窗口长度 $w$，在时刻 $t$ 的窗口为 $\{x_{t-w+1}, \dots, x_t\}$，其滚动均值、标准差与极值可写为：

$$
\bar{x}_t^{(w)} = \frac{1}{w}\sum_{k=t-w+1}^{t}x_k
$$

$$
\sigma_t^{(w)} = \sqrt{\frac{1}{w}\sum_{k=t-w+1}^{t}(x_k - \bar{x}_t^{(w)})^2}
$$

$$
\text{Range}_t^{(w)} = \max_{k\in w}(x_k) - \min_{k\in w}(x_k)
$$

同理可定义滚动偏度与滚动峰度。`pandas` 的 `rolling` 对象已经封装了这些计算：

```python
import pandas as pd

s = pd.Series(x)
w = 20

rolling_mean = s.rolling(window=w).mean()
rolling_std = s.rolling(window=w).std()
rolling_max = s.rolling(window=w).max()
rolling_min = s.rolling(window=w).min()
rolling_range = rolling_max - rolling_min
rolling_skew = s.rolling(window=w).skew()
rolling_kurt = s.rolling(window=w).kurt()
```

完整脚本见 [`assets/code/03-example-02-rolling-stats.py`](./assets/code/03-example-02-rolling-stats.py)。

![图 3-2 滑动窗口统计量概览](./assets/images/03-fig-02-rolling-stats.png)

**图 3-2** 滑动窗口统计量概览。

## 3. 时域特征

### 3.1 平稳性特征

**平稳性（Stationarity）** 是指时间序列的统计特性（均值、方差、自相关结构）不随时间推移而显著变化。它是许多经典时序模型（如 ARMA、ARIMA ）的重要前提：非平稳序列的均值或方差漂移会让参数估计失去意义，而平稳序列更易于建模与预测。

#### 3.1.1 ADF 检验

**ADF（Augmented Dickey-Fuller）检验** 是最常用的单位根检验，其回归模型可写为：

$$
\Delta x_t = \alpha + \beta t + \gamma x_{t-1} + \sum_{i=1}^{p}\delta_i \Delta x_{t-i} + \varepsilon_t
$$

其中 $\Delta x_t = x_t - x_{t-1}$ 为一阶差分，$p$ 为滞后阶数。原假设为序列存在单位根（非平稳）；当 p-value 小于显著性水平（通常取 0.05）时，拒绝原假设，认为序列平稳。

从 ADF 检验可提取以下特征：

- `adf_statistic`：ADF 统计量（越负越倾向于平稳）。
- `adf_pvalue`：对应 p-value。
- `adf_is_stationary`：布尔值，p-value < 0.05 时为 `True`。
- `adf_lags`：检验时自动选择的滞后阶数。

`statsmodels` 中的调用方式如下：

```python
import numpy as np
from statsmodels.tsa.stattools import adfuller

# x 为已加载的时间序列，例如：x = np.array([...])
x = np.random.randn(100)  # 占位示例序列，请替换为实际数据

adf_res = adfuller(x, autolag="AIC")
adf_stat, adf_pvalue, used_lags = adf_res[0], adf_res[1], adf_res[2]
is_stationary = adf_pvalue < 0.05
```

#### 3.1.2 KPSS 检验

**KPSS（Kwiatkowski-Phillips-Schmidt-Shin）检验** 与 ADF 检验的假设正好相反：原假设为序列平稳，备择假设为序列存在单位根。因此解读时需要注意 p-value 的方向：

- `kpss_statistic`：LM 统计量。
- `kpss_pvalue`：对应 p-value。
- `kpss_is_stationary`：布尔值，p-value >= 0.05 时为 `True`。

```python
import numpy as np
from statsmodels.tsa.stattools import kpss

# x 为已加载的时间序列，例如：x = np.array([...])
x = np.random.randn(100)  # 占位示例序列，请替换为实际数据

kpss_res = kpss(x, regression="c", nlags="auto")
kpss_stat, kpss_pvalue = kpss_res[0], kpss_res[1]
is_stationary = kpss_pvalue >= 0.05
```

实际工程中，通常同时报告 ADF 与 KPSS 结果。当两者结论冲突时，可结合滚动统计量的稳定性进一步判断。

#### 3.1.3 滚动统计量稳定性特征

全局检验只能给出整条序列是否平稳的结论，而滚动统计量可以刻画平稳性随时间的局部变化。给定窗口长度 $w$，时刻 $t$ 的滚动均值与滚动方差分别为：

$$
m_t^{(w)} = \frac{1}{w}\sum_{k=t-w+1}^{t}x_k
$$

$$
v_t^{(w)} = \frac{1}{w}\sum_{k=t-w+1}^{t}\left(x_k - m_t^{(w)}\right)^2
$$

为了用单个标量衡量滚动均值或滚动方差自身的波动程度，可计算其**变异系数（Coefficient of Variation, CV）**：

$$
CV_m = \frac{\sigma\left(m_t^{(w)}\right)}{\bar{m}_t^{(w)}}, \quad
CV_v = \frac{\sigma\left(v_t^{(w)}\right)}{\bar{v}_t^{(w)}}
$$

$CV_m$ 与 $CV_v$ 越大，说明序列的局部均值或局部方差随时间变化越剧烈，平稳性越差。需要注意，当序列均值或方差接近零时，CV 可能不稳定，此时可改用绝对标准差或 MAD。

```python
import numpy as np
import pandas as pd

# x 为已加载的时间序列，例如：x = np.array([...])
x = np.random.randn(100)  # 占位示例序列，请替换为实际数据

s = pd.Series(x)
window = 30
rolling_mean = s.rolling(window=window).mean()
rolling_var = s.rolling(window=window).var()

cv_mean = rolling_mean.std() / rolling_mean.mean()
cv_var = rolling_var.std() / rolling_var.mean()
```

完整脚本见 [`assets/code/03-example-03-stationarity-features.py`](./assets/code/03-example-03-stationarity-features.py)。

![图 3-3 平稳序列与非平稳序列的 ADF/KPSS 检验与滚动统计量对比](./assets/images/03-fig-03-stationarity.png)

**图 3-3** 平稳序列与非平稳序列的 ADF/KPSS 检验与滚动统计量对比。

### 3.2 季节性特征

**季节性（Seasonality）** 是指时间序列在固定时间间隔（如小时、天、周、年）上重复出现的模式。与趋势性不同，季节性通常围绕一个相对稳定的周期波动，例如电力负荷的日内峰谷、零售销量的周末效应等。刻画季节性不仅有助于理解业务规律，还能为后续的去季节、预测与异常检测提供结构化特征。

#### 3.2.1 季节性强度

给定序列的 STL 分解 $x_t = T_t + S_t + R_t$，其中 $T_t$ 为趋势项、$S_t$ 为季节项、$R_t$ 为残差项，**季节性强度（Seasonal Strength）** 可定义为：

$$
F_s = 1 - \frac{\text{Var}(R_t)}{\text{Var}(S_t + R_t)}
$$

$F_s$ 越接近 1，说明序列的波动主要由季节性解释；越接近 0，则季节性越弱。该指标在 `statsmodels.tsa.seasonal.STL` 分解后可直接计算。

#### 3.2.2 周期内统计量

将序列按周期位置 $p = t \bmod m$ 分组（$m$ 为周期长度），可计算每个位置上的均值、标准差、偏度与峰度：

$$
\bar{x}^{(p)} = \frac{1}{n_p}\sum_{t: t \bmod m = p} x_t
$$

$$
\sigma^{(p)} = \sqrt{\frac{1}{n_p}\sum_{t: t \bmod m = p}(x_t - \bar{x}^{(p)})^2}
$$

同理可计算位置 $p$ 上的偏度 $\gamma_1^{(p)}$ 与峰度 $\gamma_2^{(p)}$。这些向量特征可以捕捉季节性波形在不同相位上的形态差异。

#### 3.2.3 季节滞后自相关特征

若序列存在周期为 $m$ 的季节性，则在滞后 $k = m, 2m, \dots$ 处的自相关系数通常显著为正。取前几个季节滞后的 ACF 值作为标量特征：

$$
\rho_{m}, \rho_{2m}, \rho_{3m}, \dots
$$

它们既可作为季节性强度的补充指标，也可直接输入下游模型。

```python
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.stattools import acf
import numpy as np
import pandas as pd
from scipy import stats

# x 为已加载的时间序列，m 为已知周期
m = 24
s = pd.Series(x)
res = STL(s, period=m).fit()

# 季节性强度
F_s = 1 - np.var(res.resid, ddof=1) / np.var(res.seasonal + res.resid, ddof=1)

# 周期内统计量
df = pd.DataFrame({"value": x, "pos": np.arange(len(x)) % m})
grouped = df.groupby("pos")["value"]
intra_mean = grouped.mean().values
intra_std = grouped.std(ddof=1).values
intra_skew = grouped.apply(lambda g: stats.skew(g, bias=False)).values
intra_kurt = grouped.apply(lambda g: stats.kurtosis(g, bias=False)).values

# 季节滞后 ACF
acf_vals = acf(x, nlags=3 * m, fft=True)
seasonal_acf = [acf_vals[m], acf_vals[2 * m], acf_vals[3 * m]]
```

完整脚本见 [`assets/code/03-example-04-seasonality-features.py`](./assets/code/03-example-04-seasonality-features.py)。

![图 3-4 STL 分解与季节性强度示例](./assets/images/03-fig-04-seasonality.png)

**图 3-4** STL 分解与季节性强度示例。

### 3.3 趋势性特征

### 3.4 周期性特征

## 4. 频域特征

### 4.1 傅里叶变换特征

### 4.2 功率谱密度特征

### 4.3 频带能量特征

## 5. 特征组合与工程实践

## 6. 本章小结

## 参考与延伸阅读

- [本章引用](./references.md)
- [本章习题](./exercises.md)
- [附录 A：特征提取相关论文](../appendix/A-papers/README.md)

---

*本章图片由 Python 脚本生成，详见 `assets/code/` 目录。*
