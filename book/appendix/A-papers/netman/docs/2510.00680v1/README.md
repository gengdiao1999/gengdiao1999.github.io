# TShape: Rescuing Machine Learning Models from Complex Shapelet Anomalies（ISSRE 2025）

> 作者：Hang Cui, Jingjing Li, Haotian Si, Quan Zhou, Changhua Pei, Gaogang Xie, Dan Pei
> 机构：中国科学院计算机网络信息中心（CNIC）、中国科学院大学、杭州高等研究院、清华大学
> 发表年份：2025
> 会议/期刊：2025 IEEE 36th International Symposium on Software Reliability Engineering (ISSRE 2025)
> 关联 PDF：同目录下 `2510.00680v1.pdf`

## 一、文档信息速览

| 字段 | 值 |
|---|---|
| 标题 | TShape: Rescuing Machine Learning Models from Complex Shapelet Anomalies |
| 作者 | Hang Cui, Jingjing Li, Haotian Si, Quan Zhou, Changhua Pei, Gaogang Xie, Dan Pei |
| 机构 | CNIC CAS, UCAS, Hangzhou IAS UCAS, Tsinghua University |
| 发表年份 | 2025 |
| 会议/期刊 | ISSRE 2025 |
| 分类 | 异常检测 / 时序分析 / Shapelet |
| 核心问题 | 现有时序异常检测方法在 shapelet（形状）级别建模不足，难以识别复杂形状异常 |
| 主要贡献 | 1) 多尺度卷积提取局部形状特征；2) Patch-wise Dual-Attention 融合局部与全局；3) 五个数据集上平均 F1 提升 10% |

## 二、背景（Background）

时序异常检测（TSAD）是保障现代 IT 基础设施与软件系统可靠性的关键技术。运维工程师需要持续监控关键时序指标（响应时间、成功率等），这些指标由 IT 基础设施每天产生海量数据驱动。一旦系统出现硬件故障、软件 bug、网络攻击等异常，需要及时识别以维持服务质量。

时序异常检测领域经历了从手工监控与基于规则统计到现代深度学习的演进。近期的大规模服务故障（Microsoft、Google、Alibaba Cloud 等）凸显了对更有效 TSAD 方案的迫切需求。然而，现有方法主要关注"点"级别——无论是长期还是短期依赖建模，都未能充分分析 shapelet 之间的相互关系。这与人类专家从"形状"角度识别异常的认知方式不匹配。

所谓 shapelet，指时间序列中具有辨识度的子序列模式。在图 1 给出的样例中，异常片段中的每个周期都包含两个小波峰：第二小的波峰在异常周期呈现出不同的凸起形状（long-term shapelet relationship），两个波峰之间的相对幅度在异常周期变小（short-term shapelet relationship）。人类专家从 shapelet 级别判断异常，而机器学习方法仍在点级别挣扎。

这带来两个核心挑战：（1）如何从多种多样形状中识别异常 shapelet；（2）如何同时考虑短期与长期 shapelet 关系。

## 三、目的（Purpose / Problems Solved）

- **Shapelet 识别难题**：真实世界异常呈现高度多样的形状，需要统一模型学习鲁棒表示以识别广泛形态学模式（特别是复杂形状偏差）。
- **短期与长期 shapelet 关系联合建模**：局部 shapelet 关系代表细节模式，长距离 shapelet 关系用于周期性违规检查（比基于点的周期性检查更鲁棒）。需要有效建模并整合细粒度局部与全局关系。
- **点级别建模的局限**：点级别检测无法捕捉形状异常，特别是在工业时序中常见的多周期、形态学偏差场景。
- **现有 SOTA 在 WSD/AIOps 等数据集上的退化**：SAND 在 WSD vs NAB 上 F1 退化 5.8 倍，凸显跨数据集鲁棒性问题。

## 四、核心原理（Principles）

TShape 是一个用于工业时序异常检测的新颖框架，整体方案由三个主要组件构成：

**1) 多尺度卷积（Multi-scale Convolution）**：在每个 patch 内通过不同尺度的一维卷积核提取丰富的局部特征，捕捉多尺度时序行为。

**2) Patch-wise 位置编码**：通过可学习嵌入注入显式的 patch 顺序信息，使模型感知每个 patch 的时间位置。

**3) Patch-wise Dual-Attention**：在 patch 序列上同时应用局部注意力（intra-patch 依赖）和全局注意力（inter-patch 关系），并通过可学习门控单元自适应融合两者。

**关键概念定义**：
- **Shapelet**：时序中具有辨识度的子序列模式
- **Patch**：将输入窗口分割成的多个子序列段
- **Multi-scale Convolution**：多尺度一维卷积，用于捕捉不同时间分辨率的特征

**数学原理**：
- 多尺度卷积输出：
$$h_i^{(k)} = \text{Conv1D}_k(p_i) \in \mathbb{R}^{C_m \times s}, \quad z_i^{(k)} = \text{GAP}(h_i^{(k)}) \in \mathbb{R}^{C_m}$$
- 局部注意力（intra-patch）：
$$\tilde{L} = \text{MHA}_{local}(V^\top, V^\top, V^\top)^\top + V$$
- 全局注意力（inter-patch）：
$$\tilde{G} = \text{MHA}_{global}(V, V, V) + V$$
- 门控融合：
$$g = \sigma([\tilde{L}; \tilde{G}]W_g + b_g), \quad H = g \odot \tilde{L} + (1 - g) \odot \tilde{G}$$

**与现有技术的差异**：
- 不同于 AnomalyTransformer 基于"点"级别关联差异
- 不同于 FCVAE 频域分解
- 不同于 PatchAD 简单的 patch 距离度量
- TShape 在 patch 级别同时建模局部形状与全局上下文

## 五、算法详解（Algorithm）

### 1. 输入 / 输出
- **输入**：单变量时序 X = {xt}T_t=1，xt ∈ R
- **输出**：每个时间步的异常分数 st ∈ R，st 越大表示越可能异常

### 2. 核心模块
- 多尺度卷积（多核 1D CNN + GAP + BN + GELU）
- Patch-wise 位置编码（可学习 E ∈ R^(P×C)）
- 局部注意力 MHA_local
- 全局注意力 MHA_global
- 门控融合网络

### 3. 伪代码

```python
def TShape(X, patch_size, kernel_sizes, num_patches):
    # 步骤1: 分 patch
    patches = split_into_patches(X, patch_size)  # P 个 patch

    # 步骤2: 多尺度卷积
    multi_scale_feats = []
    for p in patches:
        feats = []
        for k in kernel_sizes:
            h = Conv1D_k(p)
            z = GAP(h)
            feats.append(z)
        multi_scale_feats.append(concat(feats))
    U = BN(GELU(stack(multi_scale_feats)))  # P × C

    # 步骤3: 位置编码
    V = U + E  # E ~ N(0,1), learnable

    # 步骤4: Dual-Attention
    L_tilde = MHA_local(V.T) + V  # 局部（intra-patch）
    G_tilde = MHA_global(V) + V  # 全局（inter-patch）

    # 步骤5: 门控融合
    g = sigmoid(concat([L_tilde, G_tilde]) @ W_g + b_g)
    H = g * L_tilde + (1 - g) * G_tilde

    # 步骤6: 异常评分
    scores = compute_anomaly_score(H, X)
    return scores
```

### 4. 关键数学

门控融合自适应平衡局部与全局注意力：

$$\text{Output} = g \odot \tilde{L} + (1 - g) \odot \tilde{G}$$

### 5. 复杂度分析
- 时间复杂度：多尺度卷积 O(P × M × s × C)，注意力 O(P² × C)
- 空间复杂度：O(P × C) 用于存储注意力权重

### 6. 训练与推理
- 每个时间序列单独训练一个 TShape 实例
- 使用 EASYTSAD 基准的协议
- 推理时输出每个时间步的异常分数

## 六、系统架构图（Architecture）

```mermaid
graph TB
    A[单变量时序 X] --> B[Patch 切分]
    B --> C[多尺度 1D 卷积]
    C --> D[BN + GELU]
    D --> E[多尺度特征 U]
    E --> F[+ 位置编码 E]
    F --> G[V = U + E]
    G --> H1[局部注意力 MHA_local]
    G --> H2[全局注意力 MHA_global]
    H1 --> I1[Add & Norm]
    H2 --> I2[Add & Norm]
    I1 --> J[Concat]
    I2 --> J
    J --> K[门控网络 g = sigmoid]
    K --> L[融合 H = g * L + 1-g) * G]
    L --> M[预测 + 异常分数]
```

## 七、流程图（Process Flow）

```mermaid
flowchart TD
    S1[输入时序 X] --> S2[分 patch P 个]
    S2 --> S3[每个 patch 应用多核 1D 卷积]
    S3 --> S4[GAP 池化 + 拼接]
    S4 --> S5[BN + GELU 激活]
    S5 --> S6[注入可学习位置编码]
    S6 --> S7{计算注意力}
    S7 --> S8[局部: intra-patch MHA]
    S7 --> S9[全局: inter-patch MHA]
    S8 --> S10[残差 + Norm]
    S9 --> S10
    S10 --> S11[门控网络生成权重 g]
    S11 --> S12[加权和 H = g*L + 1-g)*G]
    S12 --> S13[异常分数计算]
    S13 --> S14[与阈值比较]
    S14 --> S15[异常 / 正常]
```

## 八、关键创新点（Key Innovations）

- **+ 多尺度卷积（Multi-scale Convolution）**：通过并行多尺度 1D 卷积核提取丰富的局部描述符，捕捉复杂时序特征，弥补现有 TSAD 方法对局部形状信息利用不足的缺陷。
- **+ Patch-wise Dual-Attention 机制**：通过局部注意力（intra-patch）与全局注意力（inter-patch）的双重建模，结合可学习门控单元自适应融合，平衡局部复杂形状与全局依赖。
- **+ Patch-wise 位置编码**：在 patch 序列上注入显式的位置信息，保留时序结构，避免模型把每个 patch 当作独立单元。
- **+ 跨数据集鲁棒性**：在 AIOPS、NAB、TODS、UCR、WSD 五个数据集上 F1-E 均排名第一，远超次优 FCVAE（0.7161）。

## 九、实验与结果（Experiments）

### 数据集
- **AIOPS**：来自搜狗、eBay、百度、腾讯、阿里五家互联网企业的多维数据集
- **WSD**：百度、搜狗、eBay 生产 Web 服务的高频采样 KPI
- **UCR**：203 条跨域时序（电网、医疗、IoT）
- **TODS**：合成数据集，可控季节性、趋势、噪声
- **NAB**：AWS 云指标、社交媒体、IoT 传感器的流数据

### Baseline（16 个）
SubLOF、SAND、MatrixProfile、AR、LSTMAD、AE、EncDecAD、SRCNN、AnomalyTransformer、TFAD、TranAD、Donut、FCVAE、TimesNet、OFA、FITS

### 主要指标
- F1（点级）、F1-E（事件级）

### 关键结果数字
- 平均 F1 = 0.9330，**平均 F1-E = 0.8170**
- 比次优 FCVAE（0.7161）**提升 10%** 事件级 F1
- 在 AIOPS 数据集 F1-E = 0.8049（vs LSTMAD 0.7671、FCVAE 0.7364）
- 在 NAB 数据集 F1-E = 0.9186
- 在 TODS 数据集 F1-E = 0.8561
- 在 UCR 数据集 F1-E = 0.5915
- 在 WSD 数据集 F1-E = 0.9137
- **TShape 在所有五个数据集 F1-E 上均排名第 1**

### 消融实验
- 去除多尺度卷积：在 TODS 和 UCR 上性能显著下降
- 滑动窗口替代多尺度卷积：在 TODS 和 UCR 上无法匹配卷积设计
- 去除局部注意力、全局注意力：用 CNN Encoder 替代 dual-attention
- 注意力可视化：异常发生时相邻 patch 注意力得分升高，远处相似模式 patch 也获得高注意力，证明同时利用局部与全局上下文

### 效率分析
- 论文未明确给出时间/空间开销具体数字，侧重于精度提升

## 十、应用场景（Use Cases）

- **云服务监控**：监控响应时间、CPU 利用率、错误率等 KPI 曲线
- **AIOps 平台**：作为时序异常检测引擎集成到运维平台
- **工业 IoT**：检测设备传感器数据的形状异常
- **金融风控**：识别交易量、价格的形态异常
- **电信网络**：监控网络 KPI 的形状异常

## 十一、相关论文（Related Papers in this set）

- **DeST**（ISSRE 2025）：微服务系统的解耦时空异常检测框架，与 TShape 同会议
- **ChronoSage / Integrating GraphSAGE and Mamba**（ISSRE 2025）：微服务系统的时空故障检测
- **CMoS**（ICML 2025）：轻量级时序预测模型，CMoS 的 chunk 思想与 TShape 的 patch 思想互补
- **KAN-AD**（ICML 2025）：基于 KAN 的时序异常检测
- **AIOpsArena**（SANER 2025）：AIOps 算法评测平台，可用于 TShape 部署

## 十二、术语表（Glossary）

- **TSAD（Time Series Anomaly Detection）**：时序异常检测
- **Shapelet**：时序中具有辨识度的子序列模式
- **Patch**：将输入窗口分成的子序列段
- **GAP（Global Average Pooling）**：全局平均池化
- **GELU**：高斯误差线性单元
- **MHA（Multi-Head Attention）**：多头注意力
- **Event-F1**：事件级 F1 分数，将连续异常区间视为单一事件
- **BN（Batch Normalization）**：批归一化

## 十三、参考与延伸阅读

- **AnomalyTransformer**（ICLR 2022）：基于关联差异的 Transformer 异常检测
- **FCVAE**（WWW 2024）：频域分解的 VAE 异常检测
- **TimesNet**（ICLR 2023）：时序 2D 变化建模
- **PatchAD**：基于 patch 的 MLP-Mixer 异常检测
- **TranAD**：基于 Transformer 与对抗训练的多元时序异常检测
- **EASYTSAD 基准**：https://adeval.cstcloud.cn/
- **代码**：https://github.com/CSTCloudOps/TShape
