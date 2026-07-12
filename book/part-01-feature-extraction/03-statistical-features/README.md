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

### 3.2 季节性特征

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
