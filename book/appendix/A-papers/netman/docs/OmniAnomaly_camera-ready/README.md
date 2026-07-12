# OmniAnomaly: Robust Anomaly Detection for Multivariate Time Series through Stochastic Recurrent Neural Network（KDD 2019）

> 作者：Ya Su、Youjian Zhao、Chenhao Niu、Rong Liu、Wei Sun、Dan Pei（通讯）
> 机构：清华大学；BNRist；Stevens Institute of Technology；北京邮电大学
> 发表年份：2019
> 会议/期刊：ACM SIGKDD 2019（KDD '19, August 4-8, 2019, Anchorage, AK, USA）
> 关联 PDF：同目录下 `OmniAnomaly_camera-ready.pdf`

## 一、文档信息速览

| 字段 | 值 |
|---|---|
| 标题 | Robust Anomaly Detection for Multivariate Time Series through Stochastic Recurrent Neural Network |
| 作者 | Ya Su、Youjian Zhao、Chenhao Niu、Rong Liu、Wei Sun、Dan Pei |
| 机构 | 清华大学；BNRist；Stevens Institute of Technology；北京邮电大学 |
| 发表年份 | 2019 |
| 会议/期刊 | ACM SIGKDD 2019（DOI 10.1145/3292500.3330672） |
| 分类 | 多变量时序异常检测 / 深度生成模型 / 解释性 |
| 核心问题 | 工业实体（服务器、卫星、机器人等）多维传感器时序具有强随机性与复杂时序依赖，传统确定性 RNN / VAE 不能很好捕获，导致异常检测鲁棒性差且难以解释 |
| 主要贡献 | (1) OmniAnomaly：GRU + VAE + Planar Normalizing Flows + 随机变量连接的随机 RNN；(2) 基于重建概率的实体级异常检测；(3) 按 univariate 重建概率做异常解释；(4) 在 3 个真实数据集上 F1 达 0.86，比最佳 baseline 提升 0.09，解释准确率最高 0.89 |

## 二、背景（Background）

工业实体（如服务器、航天器、机器人、引擎）通常被多维时间序列（telemetry / sensor data）持续监控；及时检测这些实体的异常对于服务质量管理至关重要。一个实体通常有 12-55 个 metric（CPU load、network usage、memory usage、radiation、temperature、kinematic 等），需要 entity-level 的多变量联合异常检测，而不能只在每个 metric 上做 univariate 检测。

为什么要在 entity-level 检测？
1. 运维工程师关心整个实体的健康度，而非单个指标；
2. 训练/维护 N 个 univariate 模型代价高（如 Mars 探测器有 27×55=1485 个 metric）；
3. 一个 incident 往往引起多个 metric 同时异常；
4. 建模一个 metric 的期望值时，使用同实体的其他 metric 信息更有效。

但是工业实体受软件控制、外部环境、人类操作、其它系统影响，**行为具有强随机性 + 复杂时序依赖**。论文指出，已有方法在以下两点不足：
- **简单 VAE**：用 VAE 处理时序时，把 feed-forward 网络替换为 LSTM 不足以表达随机性，stochastic 变量之间没有显式时序依赖；
- **简单 stochastic RNN**：虽引入随机变量，但变量之间无连接，无法捕获长程依赖。

另一个挑战是**可解释性**：运维不仅要知道"实体异常了"，还要知道"哪个 metric 最可疑"。基于深度生成模型做解释是公开难题。

论文提出 **OmniAnomaly**：
1. 用 Linear Gaussian State Space Model 连接相邻时刻的 stochastic 变量 + 把 stochastic 变量与 GRU 隐变量拼接（**stochastic variable connection**）；
2. 用 **planar Normalizing Flows** 让 stochastic 变量能拟合复杂非高斯后验；
3. 用 **重建概率**（而非重建误差）做异常判定，对低频异常更鲁棒；
4. 用各 univariate 的重建概率做异常解释。

## 三、目的（Problems Solved）

- **多变量时序异常检测鲁棒性差**：不同实体的统计特性差异大，模型需通用。
- **随机变量无时序依赖**：现有方法用简单 VAE/LSTM 拼接，stochastic 变量在时间步间独立。
- **重建误差 vs 重建概率**：固定阈值重建误差在低频异常上效果差；概率框架更稳。
- **可解释性**：运维需知道"哪个 metric 异常"。
- **少标签 / 无标签**：工业数据极少异常标签，模型应能无监督训练。

## 四、核心原理（Principles）

**系统总览**：OmniAnomaly 在每个时间步用 GRU 编码器 + 随机变量 $z_t$ 表达输入 $x_t$；$z_t$ 通过 Linear Gaussian State Space Model 关联到 $z_{t-1}$；用 Planar Normalizing Flows 让后验 $q(z_t|\cdot)$ 表达非高斯分布；用重建概率 $p(x_t|z_t)$ 作为异常分数；判定异常后，按各 univariate 的 $p(x_{t,d}|z_t)$ 排序给出解释。

**关键概念**：

- **Multivariate Time Series**：多变量时间序列 $x_{1..T} \in \mathbb{R}^{T \times D}$。
- **Entity-level Anomaly**：整个实体的异常，而非单个 metric。
- **Stochastic Variable**：随机隐变量 $z_t$。
- **GRU**：Gated Recurrent Unit。
- **VAE**：Variational Autoencoder。
- **Planar NF**：Planar Normalizing Flows。
- **Linear Gaussian State Space Model (LG-SSM)**：线性高斯状态空间模型。
- **Reconstruction Probability**：重建概率，作为异常分数。
- **Interpretation**：按各 univariate 重建概率排序。

**数学原理**：

- **GRU 编码器**：给定 $x_t$ 和 $h_{t-1}$，输出 $h_t$。

$$
h_t = \text{GRU}(x_t, h_{t-1})
$$

- **变分后验（带时序依赖）**：

$$
q(z_t | x_{1..t}, z_{1..t-1}) = \mathcal{N}\big(\mu_t, \text{diag}(\sigma_t^2)\big)
$$

其中均值 $\mu_t$ 由 $h_t$ 与 $z_{t-1}$ 共同决定（这就是 stochastic variable connection 的核心）：

$$
\mu_t = W_{zh} h_t + W_{zz} z_{t-1} + b_z
$$

$$
\sigma_t = \text{softplus}(W_{zh}' h_t + W_{zz}' z_{t-1} + b_z')
$$

- **Planar Normalizing Flows**（$L$ 步可逆映射）：

$$
z_t^{(0)} = \mu_t + \sigma_t \odot \epsilon,\quad
z_t^{(l+1)} = z_t^{(l)} + u_l \cdot h(w_l^\top z_t^{(l)} + b_l),\quad l = 0..L-1
$$

$$
z_t = z_t^{(L)}
$$

其中 $h$ 是 $\tanh$，$u_l, w_l, b_l$ 是可学习参数。最终后验 $q(z_t)$ 不再被限制为高斯。

- **重建模型**：

$$
p(x_t | z_t) = \prod_{d=1}^{D} p(x_{t,d} | z_t)
$$

通常 $p(x_{t,d} | z_t) = \mathcal{N}(\hat{x}_{t,d}, \sigma_{x,d}^2)$，$\hat{x}_t$ 由 decoder $f_\theta(z_t)$ 产生。

- **Evidence Lower Bound (ELBO)**：

$$
\mathcal{L} = \mathbb{E}_{q}\big[\sum_{t=1}^T \log p(x_t | z_t)\big] - \text{KL}\big(q(z_{1..T} | x_{1..T}) \,\|\, p(z_{1..T})\big)
$$

- **异常分数**（对每个观测的负重建概率）：

$$
s_t = -\sum_{d=1}^{D} \log p(x_{t,d} | z_t)
$$

- **解释得分**（每个 univariate 单独的概率）：

$$
s_{t,d} = -\log p(x_{t,d} | z_t)
$$

排序得到 top-k 可疑 metric。

- **阈值选择**：训练集上用 POT（Peaks-Over-Threshold）方法自适应选阈值。

**与现有方法的差异**：与 Donut（VAE 但无 NF、无时序 stochastic 变量）、LSTM-VAE（feed-forward 替换为 LSTM 但无 NF）相比，OmniAnomaly 同时引入时序随机变量连接 + 非高斯后验；与 DAGMM、USAD、LSTM-VAE 等相比，重建概率分数更鲁棒。

## 五、算法详解（Algorithm）

1. **输入 / 输出**：
   - 输入：多变量时序 $x_{1..T} \in \mathbb{R}^{T \times D}$；窗口大小 $W$。
   - 输出：实体级异常分数序列 $s_{1..T}$；异常区间；top-k 可疑 metric（解释）。

2. **核心模块**：
   - **窗口化**：用滑窗生成训练样本。
   - **GRU 编码器**：$h_t = \text{GRU}(x_t, h_{t-1})$。
   - **Stochastic Variable Connection**：把 $z_{t-1}$ 与 $h_t$ 拼接后映射到 $z_t$ 的均值和方差。
   - **Planar Normalizing Flows**：$L$ 步可逆映射得到 $z_t$。
   - **GRU 解码器**：用 $z_{1..t}$ 重构 $x_{1..t}$。
   - **重建概率**：$p(x_t | z_t)$。
   - **异常检测**：滑动窗口上聚合重建概率 → POT 阈值 → 异常区间。
   - **异常解释**：按各 univariate 重建概率排序，给出 top-k 可疑 metric。

3. **伪代码**：

```python
class OmniAnomaly(nn.Module):
    def __init__(self, d_in, d_hid, d_z, n_flows=8):
        super().__init__()
        self.gru_enc = nn.GRU(d_in, d_hid, batch_first=True)
        self.fc_mu = nn.Linear(d_hid + d_z, d_z)
        self.fc_logvar = nn.Linear(d_hid + d_z, d_z)
        self.flows = nn.ModuleList([PlanarFlow(d_z) for _ in range(n_flows)])
        self.gru_dec = nn.GRU(d_z, d_hid, batch_first=True)
        self.fc_x = nn.Linear(d_hid, d_in)
        self.log_sigma_x = nn.Parameter(torch.zeros(d_in))

    def encode(self, x):
        h, _ = self.gru_enc(x)
        return h

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        return mu + std * torch.randn_like(mu)

    def planar_flow(self, z):
        for flow in self.flows:
            z = flow(z)
        return z

    def forward(self, x):
        h = self.encode(x)                       # (B, T, H)
        T = h.size(1)
        zs = []
        z_prev = torch.zeros(x.size(0), d_z)    # z_0 = 0
        for t in range(T):
            mu = self.fc_mu(torch.cat([h[:, t, :], z_prev], dim=-1))
            logvar = self.fc_logvar(torch.cat([h[:, t, :], z_prev], dim=-1))
            z0 = self.reparameterize(mu, logvar)
            z = self.planar_flow(z0)
            zs.append(z)
            z_prev = z
        z_seq = torch.stack(zs, dim=1)
        x_hat, _ = self.gru_dec(z_seq)
        x_hat = self.fc_x(x_hat)
        return x_hat, z_seq, mu, logvar

def loss_function(x, x_hat, mu, logvar, sigma_x):
    recon = -0.5 * ((x - x_hat) ** 2 / sigma_x ** 2 + 2 * torch.log(sigma_x)).sum()
    kld = -0.5 * (1 + logvar - mu ** 2 - logvar.exp()).sum()
    return recon - kld

def anomaly_score(x, model):
    """Per-time-step reconstruction probability. 越大越异常。"""
    x_hat, z, mu, logvar = model(x)
    sigma_x = model.log_sigma_x
    log_px = -0.5 * ((x - x_hat) ** 2 / sigma_x ** 2 + 2 * torch.log(sigma_x))
    s = -log_px.sum(dim=-1)            # sum over metrics
    return s

def detect_anomalies(scores, q=0.999):
    """POT-based adaptive threshold."""
    th = pot_threshold(scores, q=q)
    return scores > th

def interpret(x, model, topk=3):
    """按 univariate 重建概率给 top-k 可疑 metric。"""
    x_hat, *_ = model(x)
    sigma_x = model.log_sigma_x
    log_px = -0.5 * ((x - x_hat) ** 2 / sigma_x ** 2)
    score = -log_px.squeeze(0)              # (T, D)
    return score.topk(topk, dim=-1).indices

def train_omnianomaly(X_train, epochs=50, batch_size=128, lr=1e-3):
    model = OmniAnomaly(d_in=X_train.shape[-1], d_hid=128, d_z=32)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    for ep in range(epochs):
        for batch in dataloader(X_train, batch_size):
            x_hat, z, mu, logvar = model(batch)
            loss = loss_function(batch, x_hat, mu, logvar, model.log_sigma_x)
            opt.zero_grad(); loss.backward(); opt.step()
    return model
```

4. **关键数学**：见 §四。

5. **复杂度分析**：
   - 训练：$O(T \cdot D \cdot H \cdot L)$ per batch，$L$ 为 planar flow 步数；
   - 推理：$O(T \cdot D \cdot H \cdot L)$；
   - 内存：$O(B \cdot T \cdot (H + D + Z \cdot L))$。

6. **训练与推理**：
   - 训练：ELBO 最大化，Adam / RMSProp；
   - 推理：滑窗 → 重建概率 → POT 阈值 → 异常区间 → 解释 top-k。

7. **示例**：服务器集群 28 台机器 × 38 个 metric（CPU load、network usage、memory usage 等），2 天数据。某台机器 12:00-12:30 CPU load、network inflow 飙高，其他 metric 正常。OmniAnomaly 在该窗口给出高异常分数；解释给出 top-1 = network_inflow、top-2 = cpu_load。

## 六、系统架构图（Architecture）

```mermaid
graph TB
    A[多变量时序 X_1..T] --> B[窗口化]
    B --> C[GRU 编码器 h_t]
    C --> D[拼接 h_t + z_{t-1}]
    D --> E[FC -> mu, logvar]
    E --> F[重参数化 z_0]
    F --> G[Planar Normalizing Flow 8 步]
    G --> G1[u1 h w1 z + b1]
    G --> G2[u2 h w2 z + b2]
    G --> G3[uL h wL z + bL]
    G1 --> H[z_t]
    G2 --> H
    G3 --> H
    H --> I[GRU 解码器]
    I --> J[FC x_hat]
    J --> K[重建概率 log p x_t | z_t]
    K --> L[负对数 -> 异常分数 s_t]
    L --> M[POT 阈值]
    M --> N{超阈值?}
    N -->|是| O[异常区间]
    N -->|否| P[正常]
    O --> Q[按各 univariate 重建概率排序]
    Q --> R[Top-k 可疑 metric 解释]
    H --> I
```

## 七、流程图（Process Flow）

```mermaid
flowchart TD
    S1[多变量时序采集] --> S2[归一化 + 滑窗]
    S2 --> S3[GRU 编码]
    S3 --> S4[随机变量连接: h_t + z_{t-1} -> mu, logvar]
    S4 --> S5[重参数化 z_0]
    S5 --> S6[Planar NF L 步 z_t]
    S6 --> S7[GRU 解码 x_hat]
    S7 --> S8[ELBO 损失: 重建 + KL]
    S8 --> S9[反向传播 + Adam]
    S9 --> S10{收敛?}
    S10 -->|否| S4
    S10 -->|是| S11[保存模型]
    S11 --> S12[在线 滑窗 输入]
    S12 --> S13[计算重建概率 s_t]
    S13 --> S14[POT 自适应阈值]
    S14 --> S15[异常区间]
    S15 --> S16[按 metric 重建概率排序]
    S16 --> S17[Top-k 可疑 metric 解释]
```

## 八、关键创新点（Key Innovations）

- **+ 随机变量连接（LG-SSM + 拼接）**：让 $z_t$ 显式依赖 $z_{t-1}$ 与 $h_t$。
- **+ Planar Normalizing Flows**：让后验 $q(z_t)$ 拟合复杂非高斯分布。
- **+ 重建概率作异常分数**：比固定阈值重建误差更鲁棒。
- **+ 按 univariate 重建概率做解释**：top-k 可疑 metric。
- **+ POT 自适应阈值**：不依赖人工调阈值。
- **+ 跨领域鲁棒**：在航天 + 互联网服务器两类截然不同的数据上 F1 全部 > 0.84。

## 九、实验与结果（Experiments）

- **数据集**（Table 1）：
  - **Server machine dataset**（本论文新发布）：28 台服务器 × 38 个 metric。
  - **Soil Moisture Active Passive (SMAP) satellite**：55 个 entity × 25 metric。
  - **Mars Science Laboratory (MSL) rover**：27 × 55 metric。
- **Baseline**：传统时序异常检测（OC-SVM、IF、PCA、AE）、Donut、Bagel、LSTM-VAE、USAD、DAGMM、THOC 等。
- **主要指标**：Precision、Recall、F1-Score（官方协议下整体）。
- **关键结果数字**：
  - 3 个数据集 F1-Score 平均 **0.86**，相对最佳 baseline 提升 **+0.09**；
  - 3 个数据集 F1-Score **全部 > 0.84**；
  - 异常解释准确率最高 **0.89**；
  - 论文同时公开代码 + server machine dataset。
- **消融实验**：
  - 去掉 LG-SSM：F1 下降约 0.05；
  - 去掉 Planar NF：F1 下降约 0.03-0.05；
  - 去掉 stochastic 变量连接：F1 显著下降；
  - 重建误差 vs 重建概率：重建概率更稳。
- **效率**：GPU 上训练分钟级到小时级；推理毫秒级。
- **可视化**：异常区间 vs ground truth；top-k 解释热力图。

## 十、应用场景（Use Cases）

- **服务器集群监控**：CPU / 内存 / 网络 / 磁盘多 metric 联合异常。
- **航天器遥测**：辐射 / 温度 / 功率 / 计算活动联合监测。
- **机器人系统**：kinematic / visual / haptic / auditory 异常。
- **工业引擎**：accelerator / torque / temperature 异常。
- **智能制造产线**：多 sensor 联合异常检测 + 故障定位。

## 十一、相关论文（Related Papers in this set）

- `TraceSieve_ISSRE23`（追踪异常检测 / 微服务）
- `liu_imc15_Opprentice`（KPI 异常检测 / 无监督）
- `label-less-v3`（日志异常检测 / 无监督）
- `LogAnomaly`（日志异常检测）
- `FluxInfer`（指标异常检测 + 解释）
- `08723601`（KPI 周期自适应）
- `chenwenxiao_infocom2019`（多源指标故障定位）
- `www2018`（KPI 异常检测）

## 十二、术语表（Glossary）

- **Multivariate Time Series**：多变量时间序列。
- **Entity-level Anomaly**：实体级异常。
- **Metric-level Anomaly**：单 metric 异常。
- **Stochastic Variable**：随机隐变量 $z_t$。
- **GRU**：Gated Recurrent Unit。
- **VAE**：Variational Autoencoder。
- **Planar NF**：Planar Normalizing Flow。
- **LG-SSM**：Linear Gaussian State Space Model。
- **ELBO**：Evidence Lower Bound。
- **KL Divergence**：Kullback-Leibler 散度。
- **Reconstruction Probability**：重建概率。
- **POT**：Peaks-Over-Threshold（自适应阈值）。
- **SMAP**：Soil Moisture Active Passive satellite。
- **MSL**：Mars Science Laboratory rover。
- **Telemetry**：遥测数据。
- **OC-SVM / IF / PCA / AE**：经典异常检测 baseline。
- **DAGMM / USAD / THOC / Donut / Bagel / LSTM-VAE**：深度异常检测 baseline。

## 十三、参考与延伸阅读

- Paper: GRU, *Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation*（Cho et al., 2014）。
- Paper: VAE, *Auto-Encoding Variational Bayes*（Kingma & Welling, 2014）。
- Paper: Planar NF, *Variational Inference with Normalizing Flows*（Rezende & Mohamed, 2015）。
- Paper: Stochastic RNN, *Stochastic Recurrent Neural Network*（Bayer & Osendorfer, 2014 / Chung et al., 2015）。
- Paper: Donut, *Unsupervised Anomaly Detection for Seasonal KPIs in Web Applications*（Xu et al., WWW 2018）。
- 数据集：SMAP / MSL（NASA）、Server machine（本文发布）。
- 相关论文：`TraceSieve_ISSRE23`、`liu_imc15_Opprentice`、`label-less-v3`、`LogAnomaly`、`FluxInfer`、`08723601`、`chenwenxiao_infocom2019`、`www2018`。
