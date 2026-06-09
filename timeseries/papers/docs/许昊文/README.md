# Shallow VAEs with RealNVP Prior Can Perform as Well as Deep Hierarchical VAEs（许昊文等）

> 作者：Haowen Xu, Wenxiao Chen, Jinlin Lai, Zhihan Li, Youjian Zhao, Dan Pei
> 机构：清华大学计算机科学与技术系；北京国家信息科学与技术研究中心（BNRist）
> 发表年份：约 2019–2020（附录引用 2019 年 5 月 arXiv 1905.13452）
> 会议/期刊：ICML 2020 Workshop / NeurIPS 2020 Workshop 系列
> 关联 PDF：同目录下 `许昊文.pdf`

## 一、文档信息速览

| 字段 | 值 |
|---|---|
| 标题 | Shallow VAEs with RealNVP Prior Can Perform as Well as Deep Hierarchical VAEs |
| 作者 | Haowen Xu（许昊文）, Wenxiao Chen, Jinlin Lai, Zhihan Li, Youjian Zhao, Dan Pei |
| 机构 | 清华大学 CS；BNRist |
| 发表年份 | 2019–2020（arXiv 1905.13452） |
| 类别 | 深度生成模型 / VAE 改进 / 可学习先验 / 标准化流（Normalizing Flow） |
| 核心问题 | 现有 SOTA 连续潜变量 VAE 全部依赖深度层次潜变量；学习先验能否让"浅层 VAE"达到甚至超过深层次 VAE 的测试负对数似然（NLL）？ |
| 关键数据集 | 静态二值化 MNIST、动态二值化 MNIST、FashionMNIST、Omniglot |
| 关键模型 | DenseVAE、ConvVAE、ResnetVAE、PixelVAE |
| 关键创新 | (1) 用 RealNVP 先验 + 单个潜变量让浅层 VAE 达到 BIVA 等深层次 VAE 同等 NLL；(2) 给出 Bernoulli p(x|z) 理论最优 decoder；(3) β-VAE 在 RealNVP 先验下获得更好的率失真（RD）曲线 |
| 关键数字 | StaticMNIST 上 ResnetVAE + RNVP p(z) NLL=79.84（仅次于 BIVA 78.59）；MNIST 上 78.49（接近 BIVA 78.41） |
| 致谢 | 国家重点研发计划 2019YFB1802504、BNRist 关键项目 |

## 二、背景（Background）

变分自编码器（VAE, Kingma & Welling 2014 [12]）是一种强大的深度生成模型，通过变分推断训练，需要用学到的分布近似难解的真实后验，因此有许多不同的变分后验被提出 [12], [16], [11]。

与变分后验的工作并行的，还有另一条通过学习先验（prior）来改进变分下界（ELBO）的研究路线 [9], [10], [17], [2]。

尽管这些工作在变分后验和先验上都取得了进展，但当前 SOTA 连续潜变量 VAE 全部依赖深度层次潜变量（hierarchical latent variables），尽管其中一些可能使用复杂的变分后验/先验作为架构组件。在这些深度层次 VAE 中，许多潜变量没有明确的语义意义，只是为了达到较好下界而采用的技术手段。

因此，论文提出并回答一个问题：**在可学习先验的帮助下，浅层 VAE（shallow VAEs）能否达到与深层次 VAE（deep hierarchical VAEs）相当甚至更好的性能？**这个问题之所以重要，是因为浅层 VAE 相比深层次 VAE 更具扩展到更复杂数据集的潜力。

## 三、目的（Problems Solved）

论文要解决的核心问题是：

- **复杂先验与简单潜变量是否足以替代深层次潜变量？** 通过综合实验展示，使用 RealNVP 先验 + 单个潜变量（z），浅层 VAE 在四个数据集上能够达到与深层次 SOTA 层次 VAE（如 BIVA）相当的测试 NLL，并超过许多使用复杂层次 VAE 配备丰富先验/后验的先前工作。
- **Bernoulli 重建分布下 decoder 理论最优解**：证明对有限训练样本，$p_\theta(x|z) = \text{Bernoulli}(\mu_\theta(z))$，当 $0 < \mu^k_\theta(z) < 1$ 时，最优 decoder 是 $\mu_\theta(z)$ 关于训练样本的加权平均。
- **可学习先验能否改善 β-VAE 的率失真曲线**：证明使用可学习 RealNVP 先验，β-VAE 在四个数据集上具有更好的率失真（RD）曲线。

## 四、核心原理（Principles）

**VAE 基本原理**（Eq. 1–4）：

设潜变量 $z$ 服从先验 $p_\lambda(z)$，条件分布 $p_\theta(x|z)$ 由参数为 $\theta$ 的神经网络给出，则：

$$
\log p_\theta(x) \geq L(x; \lambda, \theta, \phi) = E_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_{KL}(q_\phi(z|x) \| p_\lambda(z)) \quad (1)
$$

加入 $\beta$（如 β-VAE [8], [1]）：

$$
L_\beta(\lambda, \theta, \phi) = E_{p^*(x)} E_{q_\phi(z|x)}[\log p_\theta(x|z) + \beta(\log p_\lambda(z) - \log q_\phi(z|x))] \quad (3)
$$

ELBO surgery 分解（[9]）：

$$
L(\lambda, \theta, \phi) = E_{p^*(x)} E_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_{KL}(q_\phi(z) \| p_\lambda(z)) - I_\phi[Z; X] \quad (4)
$$

其中 $I_\phi[Z;X] = \int\int q_\phi(z, x) \log \frac{q_\phi(z, x)}{q_\phi(z) p^*(x)} dz dx$ 是互信息。

**RealNVP 先验**（Eq. 5）：

RealNVP [6] 是一种通用密度估计器，可以从简单先验 $p_\xi(w)$（例如单位高斯）得到可学习先验 $p_\lambda(z)$：

$$
p_\lambda(z) = p_\xi(w) \det \left| \frac{\partial f_\lambda(z)}{\partial z} \right|, \quad z = f_\lambda^{-1}(w) \quad (5)
$$

其中 $\det(\partial f_\lambda(z)/\partial z)$ 是 $f_\lambda(z) = (f_K \circ \cdots \circ f_1)(z)$ 的 Jacobian 行列式，每个 $f_k$ 是可逆的。仿射耦合层 [6] 提供 $f_k$；actnorm 和可逆 1×1 卷积 [13] 进一步增强。

**Proposition 1（Bernoulli 重建下的理论最优 decoder）**：

给定有限离散训练数据 $p^*(x) = \frac{1}{N} \sum_{i=1}^{N} \delta(x - x^{(i)})$，若 $p_\theta(x|z) = \text{Bernoulli}(\mu_\theta(z))$ 且 $\mu_\theta(z)$ 的每个第 $k$ 维输出满足 $0 < \mu^k_\theta(z) < 1$，则最优 decoder 为：

$$
\mu_\theta(z) = \sum_i w_i(z) x^{(i)}, \quad w_i(z) = \frac{q_\phi(z|x^{(i)})}{\sum_j q_\phi(z|x^{(j)})}, \quad \sum_i w_i(z) = 1 \quad (6)
$$

即最优 decoder 是训练样本关于变分后验 $q_\phi(z|x)$ 的加权平均。

**关键概念**：

- **VAE（Variational Auto-Encoder）**：变分自编码器 [12]；
- **ELBO（Evidence Lower Bound）**：证据下界；
- **β-VAE**：通过 $\beta$ 调节重建损失和 KL 散度的 VAE [8]，[1]；
- **RealNVP**：Real-valued Non-Volume Preserving flow [6]；
- **可学习先验 / Learned Prior**：通过标准化流学习得到的先验；
- **聚集后验（aggregated posterior）$q_\phi(z)$**：所有 $x$ 在 $q_\phi(z|x)$ 下的边缘；
- **BIVA（Very Deep Hierarchy of Latent Variables）**：深层次 VAE [14]；
- **VampPrior**：变分混合后验先验 [17]；
- **Lars prior**：可重采样先验 [2]；
- **IAF（Inverse Autoregressive Flow）**：逆自回归流 [11]；
- **PixelCNN / PixelVAE**：PixelCNN 解码器 VAE [7]；
- **Rate-Distortion Curve**：率失真曲线 [1]；
- **Active Units**：活跃潜变量维度数 [3]。

## 五、算法详解（Algorithm）

**实验设置**：

- **数据集**：StaticMNIST、动态二值化 MNIST、FashionMNIST、Omniglot；
- **模型**：DenseVAE（密集层）、ConvVAE（卷积层）、ResnetVAE（ResNet 层）、PixelVAE（ResnetVAE 解码器 + 多层 PixelCNN [7]）；
- **RealNVP 配置**：K 块可逆映射（flow depth K），每块包含可逆密集层、密集耦合层、actnorm [13]；
- **潜变量维度**：StaticMNIST 和 MNIST 用 40，FashionMNIST 和 Omniglot 用 64；
- **训练与评估**：所有实验重复 3 次取均值；在 StaticMNIST 与所有 PixelVAE 上用 NLL 早停；测试集用 1,000 样本计算指标。

**关键结果**（Table 1, 2）：

StaticMNIST 测试 NLL（越低越好）：

| 模型 | NLL |
|---|---|
| ConvHVAE + Lars prior† | 81.70 |
| ConvHVAE + VampPrior† | 81.09 |
| ResConv + RealNVP prior [10] | 81.44 |
| VAE + IAF‡ [11] | 79.88 |
| BIVA‡ [14] | 78.59 |
| Our ConvVAE + RNVP p(z) | 80.09 |
| **Our ResnetVAE + RNVP p(z)** | **79.84** |
| VLAE‡ [4] | 79.03 |
| PixelHVAE + VampPrior† [17] | 79.78 |
| Our PixelVAE + RNVP p(z) | 79.01 |

MNIST 上 Our ResnetVAE + RNVP p(z) NLL=78.49（仅次 BIVA 的 78.41，且 BIVA 使用 6 个潜变量和非常复杂的架构）。

**消融研究**（Table 3）：RealNVP 先验持续优于标准 VAE 和 RealNVP 后验，在 ResnetVAE 上最大提升约 2 nats。

**关键观察**（Table 4）：仅用 RealNVP 先验（p(z)）就比同时用 RealNVP 先验+后验或仅 RealNVP 后验更好。

**Active Units**（Table 5）：RealNVP 先验和后验都能让 ResnetVAE 的所有单元活跃，与标准 VAE 形成鲜明对比。

**重建损失与 ELBO**（Table 6）：ResnetVAE + RealNVP 先验的重建损失和 ELBO 显著高于标准 ResnetVAE；这表明改进主要来自重建损失（1 in Eq. 4）。

**率失真曲线**（Fig. 4）：用 RealNVP 先验的 β-ResnetVAE 越接近边界（x & y 轴 + 绿色线）越好，表明可学习先验能带来"更好"的重建-KL 权衡。

**Rate / Distortion 权衡**（Fig. 5）：可学习先验可在各种 β 下鼓励后验重叠小于单位高斯先验。

**伪代码**：

```python
import torch
import torch.nn as nn
from realnvp import RealNVP


def train_shallow_vae_with_learned_prior(data_loader, vae, optimizer, K_flow=20):
    """浅层 VAE + RealNVP 先验的训练循环"""
    flow = RealNVP(num_blocks=K_flow)  # K 块可逆映射
    for x in data_loader:
        # 1) 编码
        mu, logvar = vae.encoder(x)
        z = vae.reparameterize(mu, logvar)
        # 2) 计算 q(z|x) 的 ELBO 第一项
        recon = vae.decoder(z)
        recon_loss = -vae.bernoulli_log_prob(x, recon)  # log p_theta(x|z)
        # 3) RealNVP 先验 log p_lambda(z)
        w, log_det = flow.inverse(z)
        log_pz = flow.base_log_prob(w) + log_det  # log p_lambda(z)
        # 4) 后验 log q_phi(z|x)
        log_qz_x = -0.5 * ((z - mu) ** 2 / logvar.exp() + logvar).sum(dim=1)
        # 5) ELBO
        elbo = recon_loss - (log_qz_x - log_pz)
        loss = -elbo.mean()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    return vae, flow


def test_nll(vae, flow, test_loader, n_samples=1000):
    """测试 NLL 估计（多采样重要采样）"""
    nlls = []
    for x in test_loader:
        mu, logvar = vae.encoder(x)
        log_ws = []
        for _ in range(n_samples):
            z = vae.reparameterize(mu, logvar)
            w, log_det = flow.inverse(z)
            log_pz = flow.base_log_prob(w) + log_det
            recon = vae.decoder(z)
            log_px_z = vae.bernoulli_log_prob(x, recon)
            log_pz_x = -0.5 * ((z - mu) ** 2 / logvar.exp() + logvar).sum(dim=1)
            log_w = log_px_z + log_pz - log_pz_x
            log_ws.append(log_w)
        log_ws = torch.stack(log_ws)
        nll = -torch.logsumexp(log_ws, dim=0) + torch.log(torch.tensor(float(n_samples)))
        nlls.append(nll.mean().item())
    return sum(nlls) / len(nlls)
```

**关键数学**：见 §四。

**复杂度分析**：

- RealNVP 先验在每个 VAE 训练步上增加 $O(K d)$ 计算（$K$ = flow 深度，$d$ = z 维度）；
- 单个潜变量（d=40 / 64）使后验推断远快于 BIVA（6 个潜变量）；
- 训练时间与标准 VAE + RealNVP 后验相当或更少，因为可学习先验有可逆 Jacobian 但不需要对每个 x 重新计算后验聚合。

**示例**：ResnetVAE + RealNVP p(z) 在 MNIST 上 NLL=78.49，与 BIVA 的 78.41 几乎持平，但 BIVA 使用 6 个潜变量 + 极复杂架构；浅层 + 可学习先验证明了简化架构 + 丰富先验的潜力。

## 六、系统架构图（Architecture）

```mermaid
graph TB
    A[输入 x 二值化图像] --> B[Encoder]
    B --> B1[均值 mu]
    B --> B2[对数方差 logvar]
    B1 --> C[重参数化 z 采样]
    B2 --> C
    C --> D[Decoder]
    D --> E[重建 x_hat]
    C --> F[RealNVP 先验]
    F --> F1[K 块可逆映射]
    F1 --> F2[actnorm + 1x1 conv + 仿射耦合层]
    F2 --> G[基础先验 p_xi 单位高斯]
    F --> H[log p_lambda z]
    C --> I[后验 q_phi z|x 高斯]
    I --> J[log q_phi z|x]
    H --> K[ELBO 重建 - KL]
    J --> K
    E --> K
    K --> L[损失反传]
    L --> M[Adam 优化]
    M --> N[浅层 VAE 训练完成]
    N --> O[测试 NLL 重要采样 1000 样本]
    O --> P[NLL 越低越好]
```

## 七、流程图（Process Flow）

```mermaid
flowchart TD
    S1[数据集：StaticMNIST/MNIST/FashionMNIST/Omniglot] --> S2[模型选择：DenseVAE/ConvVAE/ResnetVAE/PixelVAE]
    S2 --> S3[构建 RealNVP 先验 K=20 或 50 块可逆映射]
    S3 --> S4[训练循环]
    S4 --> S5[Encoder mu logvar]
    S5 --> S6[重参数化 z]
    S6 --> S7[Decoder 重建 x_hat]
    S6 --> S8[RealNVP 先验计算 log p_lambda z]
    S6 --> S9[后验 log q_phi z|x]
    S7 --> S10[重建损失 log p_theta x|z]
    S8 --> S10
    S9 --> S10
    S10 --> S11[ELBO = 重建 - KL]
    S11 --> S12[Adam 优化]
    S12 --> S13[Early Stopping NLL]
    S13 --> S14[模型训练完成]
    S14 --> S15[测试 NLL 1000 样本重要采样]
    S15 --> S16[比较 BIVA/VLAE 等深层次 VAE]
    S16 --> S17[RealNVP p z 与 BIVA 相当]
```

## 八、关键创新点（Key Innovations）

- **+ RealNVP 先验 + 单个潜变量让浅层 VAE 达到 BIVA 同等 NLL**：在四个二值化数据集上展示，证明可学习先验可替代深层次潜变量；
- **+ 给出 Bernoulli p(x|z) 理论最优 decoder 公式**（Proposition 1）：最优 decoder 是训练样本关于 $q_\phi(z|x)$ 的加权平均；
- **+ β-VAE 在 RealNVP 先验下获得更好的率失真曲线**：可学习先验引导"更好"的重建-KL 权衡（Fig. 4）；
- **+ RealNVP 先验能提升 Active Units**：让所有潜变量维度都活跃（Table 5）；
- **+ 改进主要来自重建损失而非 KL 散度**：Table 6 表明改进主要源于第 1 项；
- **+ 用 4 种 VAE 架构 × 4 个数据集系统控制变量**：综合实验设计充分。

## 九、实验与结果（Experiments）

- **数据集**：静态二值化 MNIST（StaticMNIST）、动态二值化 MNIST、FashionMNIST、Omniglot；
- **基线**：ConvHVAE + Lars prior / VampPrior、ResConv + RealNVP prior [10]、VAE + IAF [11]、BIVA [14]、VLAE [4]、PixelHVAE + VampPrior [17]、PixelVAE [7]；
- **评估指标**：测试 NLL（越低越好）、Active Units、ELBO 拆解（recon、kl、klz|x）、率失真曲线、归一化距离、生成样本质量；
- **关键结果数字**：
  - StaticMNIST：ResnetVAE + RNVP p(z) NLL=79.84，PixelVAE + RNVP p(z) NLL=79.01；
  - MNIST：ConvVAE + RNVP p(z) NLL=78.61，ResnetVAE + RNVP p(z) NLL=78.49（接近 BIVA 78.41）；
  - FashionMNIST/Omniglot 趋势类似；
- **消融实验（Table 3）**：
  - 标准 ResnetVAE StaticMNIST NLL=82.95；
  - ResnetVAE + RealNVP q(z|x) NLL=80.97；
  - ResnetVAE + RealNVP p(z) NLL=79.99；
  - 提升最大 ~2 nats；
- **Active Units（Table 5）**：ResnetVAE + RealNVP p(z) StaticMNIST 40、RealNVP q(z|x) 40；标准 ResnetVAE 仅 30；
- **ELBO 拆解（Table 6）**：MNIST 上 ResnetVAE + RNVP p(z) ELBO -80.34、recon -53.64、kl 26.70、klz|x 1.76；标准 ResnetVAE ELBO -84.62、recon -58.70、kl 25.92、klz|x 3.55；
- **率失真曲线（Fig. 4）**：K=20/50 的点更接近"边界"（x & y 轴 + 绿色线）；
- **生成样本（Fig. 1）**：ResnetVAE + RealNVP p(z) 比标准 ResnetVAE 生成更少"难以解释"的数字；最后两列表明模型不是简单记忆训练数据。

## 十、应用场景（Use Cases）

- **二值化图像生成**：MNIST、FashionMNIST、Omniglot 上图像生成与密度估计；
- **浅层 VAE 替代深层次 VAE**：在需要扩展到大型数据集的场景中，浅层 + 可学习先验更可扩展；
- **AIOps 时序重建概率**：可作为 Donut 等时序 VAE 的理论支撑（提供 RealNVP 先验、理论最优 decoder）；
- **聚类 / 表示学习**：β-VAE + RealNVP 先验提供可控的 RD 权衡；
- **生成式建模研究**：为"可学习先验 vs 深层次潜变量"的研究方向提供经验证据。

## 十一、相关论文（Related Papers in this set）

- `zsl期刊`（FUNNEL，使用 SST 异常检测）；
- `peidan`（基于机器学习的智能运维）；
- `TraceSieve_ISSRE23`；
- `刘平issre`（TraceAnomaly）；
- `Donut`（Xu et al., WWW 2018 [8]，单变量 KPI 异常检测 VAE，使用 ELBO 重建概率）。

## 十二、术语表（Glossary）

- **VAE**：Variational Auto-Encoder 变分自编码器；
- **ELBO**：Evidence Lower Bound 证据下界；
- **β-VAE**：通过 β 调节重建-KL 权衡的 VAE；
- **RealNVP**：Real-valued Non-Volume Preserving flow；
- **Standard VAE**：高斯先验 + 高斯后验的普通 VAE；
- **BIVA**：Very Deep Hierarchy of Latent Variables（BIVA）；
- **VampPrior**：Variational Mixture of Posteriors Prior；
- **Lars Prior**：Resampled priors for variational autoencoders [2]；
- **IAF**：Inverse Autoregressive Flow；
- **PixelVAE**：在 ResnetVAE 解码器上叠加 PixelCNN 层；
- **ConvVAE / ResnetVAE / DenseVAE / PixelVAE**：四种 VAE 架构；
- **Rate-Distortion Curve**：率失真曲线；
- **Active Units**：活跃潜变量维度数；
- **Aggregated Posterior**：$q_\phi(z)$ 聚集后验；
- **Bernoulli Decoder**：伯努利解码器；
- **Proposition 1**：Bernoulli p(x|z) 下最优 decoder；
- **Implicit Krylov Approximation (IKA)**：隐式 Krylov 近似；
- **Lanczos Algorithm**：用于 IKA；
- **Joint IS**：Joint Importance Sampling。

## 十三、参考与延伸阅读

- Paper: VAE（Kingma & Welling, ICLR 2014 [12]）；
- Paper: β-VAE（Higgins et al., ICLR 2017 [8]）；
- Paper: Fixing a Broken ELBO（Alemi et al., ICML 2018 [1]）；
- Paper: ELBO surgery（Hoffman & Johnson, NIPS 2016 [9]）；
- Paper: RealNVP（Dinh et al., ICLR 2017 [6]）；
- Paper: Glow（Kingma & Dhariwal, NIPS 2018 [13]）；
- Paper: BIVA（Maaløe et al., 2019 [14]）；
- Paper: VLAE（Chen et al., ICLR 2017 [4]）；
- Paper: PixelVAE（Gulrajani et al., ICLR 2017 [7]）；
- Paper: VampPrior（Tomczak & Welling, AISTATS 2018 [17]）；
- Paper: Lars Prior / Resampled Priors（Bauer & Mnih, AISTATS 2019 [2]）；
- Paper: IAF（Kingma et al., NIPS 2016 [11]）；
- Paper: Importance Weighted Autoencoders（Burda et al., ICLR 2016 [3]）；
- Paper: On the necessity and effectiveness of learning the prior of variational auto-encoder（Xu et al., arXiv 1905.13452 [18]）。
