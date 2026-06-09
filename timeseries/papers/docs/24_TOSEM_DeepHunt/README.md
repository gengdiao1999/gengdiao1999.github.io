# DeepHunt: Interpretable Failure Localization for Microservice Systems Based on Graph Autoencoder（ACM TOSEM 2024）

> 作者：Yongqian Sun, Zihan Lin, Binpeng Shi, Shenglin Zhang, Shiyu Ma, Pengxiang Jin, Zhenyu Zhong, Lemeng Pan, Yicheng Guo, Dan Pei  
> 机构：南开大学、阿里、华为、清华大学  
> 发表年份：2024  
> 会议/期刊：ACM TOSEM（Transactions on Software Engineering and Methodology）  
> 关联 PDF：同目录下 `24_TOSEM_DeepHunt.pdf`  
> 代码：https://github.com/bbyldebb/DeepHunt；数据集 https://github.com/bbyldebb/Aiops-Dataset

## 一、文档信息速览

| 字段 | 值 |
|---|---|
| 标题 | Interpretable Failure Localization for Microservice Systems Based on Graph Autoencoder（DeepHunt） |
| 作者 | Yongqian Sun, Zihan Lin, Binpeng Shi, Shenglin Zhang, Shiyu Ma, Pengxiang Jin, Zhenyu Zhong, Lemeng Pan, Yicheng Guo, Dan Pei |
| 机构 | 南开大学、阿里、华为、清华大学 |
| 发表年份 | 2024 |
| 会议/期刊 | ACM TOSEM |
| 分类 | 微服务 / 根因定位 / 自监督学习 / 图自编码器 / 可解释性 |
| 核心问题 | 现有根因定位方法要么依赖大量标注（难获取）、要么用深度学习但缺乏可解释性和持续学习能力。 |
| 主要贡献 | 1) 基于 Graph Autoencoder (GAE) 的自监督根因定位框架 DeepHunt，实现 zero-label 冷启动；2) Root Cause Score (RCS) = 重构误差 + 故障传播模式 (upstream-downstream) 提供可解释的根因概率；3) 反馈机制 + 排序损失函数支持持续在线微调；4) 数据增强缓解 GAE 训练数据不足；5) 2 个数据集上 1% 标注即可达 90%+ A@5 准确率。 |

## 二、背景（Background）

云原生时代微服务架构成为主流，但一个实例的故障会通过依赖链迅速传播到整个系统。2021 年 12 月 AWS 微服务故障扩散到全网，定位 root cause 用了 4 小时多，造成重大经济损失。这凸显了**根因实例快速精确定位**的工业刚需。

运维人员持续收集三类可观测数据：traces（服务调用）、logs（运行时消息）、metrics（资源使用和性能指标）。早期根因定位方法多基于单模态，但近期研究证明多模态融合能给出更全面信息。代表工作 DiagFusion、Déjàvu 等需大量标注，而**标注根因实例是极其耗时费力的工作**——RCLIR 论文数据显示 1000 个根因 case 需 4 名资深运维花近 1 个月。微服务系统频繁变更（软硬件更新、部署、运维操作）让数据分布持续漂移，标注数据很快就失效。

自监督学习（SSL）通过 pretext task 从无标注数据提取监督信号，是减少标注依赖的天然方案。其中 **Graph Autoencoder (GAE)** 把图结构 + 节点特征做编解码重构，特别适合微服务系统（有天然的依赖图 + 多模态特征）。但 SSL/GAE 面临三大挑战：

1. **GAE 输出缺乏可解释性**：不能直接给出"为什么这个实例是 root cause"的理由，运维人员难以信任和决策。
2. **缺乏持续学习能力**：模型部署后不能在线更新，新故障出现时无法动态适应。
3. **需要大量历史训练数据**：系统新建或大改时，无标注数据稀缺。

DeepHunt 直击三大挑战：RCS 量化根因概率 → 反馈机制在线微调 → 数据增强解决数据不足。

## 三、目的（Purpose / Problems Solved）

论文显式给出三大挑战对应方案：

- **挑战 1：GAE 缺乏可解释性。** 解决方案：**RCS（Root Cause Score）**——结合 GAE 重构误差（"这个实例的特征是否偏离"）和故障传播模式（upstream-downstream 依赖关系），给出每个实例的根因概率。
- **挑战 2：缺乏持续学习能力。** 解决方案：**反馈机制**——运维人员对诊断结果给出反馈标签，DeepHunt 用这些反馈在线微调参数；同时设计**排序损失函数**应对 root cause vs 非 root cause 类别不平衡。
- **挑战 3：GAE 需要大量历史训练数据。** 解决方案：**数据增强**模块，在 GAE 训练过程中扩充训练样本。

## 四、核心原理（Principles）

DeepHunt 框架包含四大模块：

### 1) System Behavior Graph（SBG，系统行为图，2.1）
- 把微服务系统抽象为有向图 $G = (V, E, F)$。
- $V$：所有候选实例集合（微服务实例 + host 实例）。
- $E$：依赖关系（调用/部署），$v_j \to v_i$ 表示 $v_j$ 依赖 $v_i$。
- $F$：每个实例的多模态特征向量（traces + logs + metrics 融合）。
- 每分钟构建一个 SBG，捕捉时序动态。

### 2) 多模态特征融合（4.2）
- 从三模态（traces / logs / metrics）提取特征 → 拼接为统一向量表示 $F$。

### 3) Graph Autoencoder (GAE, 3.1)
- 经典 GAE：编码器把 SBG 的节点 + 边映射到潜在空间，解码器重构。
- 自监督：无需根因标签。
- DeepHunt 在标准 GAE 基础上加数据增强和排序损失。

### 4) Root Cause Score (RCS) = 重构误差 + 故障传播模式
- **重构误差 $r_i$**：GAE 对实例 $v_i$ 的特征重构误差，误差越大越可能是异常。
- **故障传播 $p_i$**：结合 upstream-downstream 关系，root cause 通常在依赖链上游，重构误差会向下游"传递"。
- **RCS 综合公式**：
  $$\mathrm{RCS}(v_i) = \alpha \cdot r_i + (1-\alpha) \cdot p_i$$
  其中 $\alpha$ 是平衡超参。
- RCS 给出可解释的根因概率（"高重构误差 + 在 upstream + 触发下游异常"）。

### 5) 数据增强（针对 GAE 训练）
- 论文给出多种增强策略（如节点特征扰动、边扰动、子图采样等）扩充训练样本。

### 6) 反馈机制（5.x）
- 运维人员在线给出 root cause 标签（少量增量反馈）；
- DeepHunt 用这些反馈持续微调参数。

### 7) 排序损失函数
- 类别不平衡（root cause 少、非 root cause 多）时，标准分类损失容易偏向多数类；
- 改用 **Ranking Loss**（如 margin ranking loss）：让 root cause 的 RCS 高于非 root cause 的 RCS 一个 margin。

**与现有方法差异**：
- vs **监督方法（DiagFusion、Déjàvu）**：本方法 GAE 自监督，零标注冷启动。
- vs **RCLIR 等需要 1000 标注的方法**：本方法只需 1% 标注即可达 90%+ A@5。
- vs **普通 GAE 异常检测**：本方法加 RCS 量化可解释性 + 反馈机制持续学习 + 排序损失应对不平衡。
- vs **单模态方法**：本方法融合 traces + logs + metrics 多模态。

数学核心：

RCS：

$$\mathrm{RCS}(v_i) = \alpha \cdot r_i + (1-\alpha) \cdot p_i$$

GAE 重构误差：

$$r_i = \|F_i - \hat{F}_i\|^2$$

其中 $\hat{F}_i$ 是 GAE 重构的特征。

Ranking Loss（简化）：

$$L = \sum_{(i,j)\in \mathcal{P}}\max(0, \mathrm{margin} - (\mathrm{RCS}(v_i) - \mathrm{RCS}(v_j)))$$

$\mathcal{P}$ 是 (root cause, non-root cause) 对的集合。

## 五、算法详解（Algorithm）

### 1. 输入 / 输出

- **输入**：微服务系统的 traces + logs + metrics + 少量 root cause 标签（可选）。
- **输出**：每个实例的 RCS 排名 → top-K 为疑似 root cause。

### 2. 核心模块

- **SBG Construction**：每分钟构造一个有向图，节点是实例、边是依赖关系、节点特征是多模态融合向量。
- **Multimodal Feature Extraction**：从 traces（响应时间、调用关系）、logs（错误日志、模板频次）、metrics（资源使用、QoS）提取特征。
- **Graph Autoencoder**：编码器（GCN/GAT）+ 解码器（重构邻接矩阵 + 节点特征）。
- **Data Augmentation**：节点/边/子图扰动。
- **RCS Computation**：重构误差 + 故障传播。
- **Feedback Loop**：运维反馈在线微调。
- **Ranking Loss**：margin ranking loss。

### 3. 伪代码

```python
# === 1) SBG Construction ===
def build_sbg(instances, dependencies, multi_modal_data):
    V = instances
    E = dependencies  # (v_j, v_i): v_j 依赖 v_i
    F = extract_features(multi_modal_data)  # 多模态融合
    return SBG(V, E, F)

# === 2) GAE 训练 ===
def train_gae(sbg_dataset, augmentation_fn):
    encoder = GCN(input_dim, hidden_dim, latent_dim)
    decoder = InnerProductDecoder()
    for epoch in range(epochs):
        for sbg in sbg_dataset:
            sbg_aug = augmentation_fn(sbg)  # 数据增强
            Z = encoder(sbg_aug)
            A_hat = decoder(Z)
            loss = recon_loss(A_hat, sbg.adj) + ranking_loss(RCS(Z, sbg))
            loss.backward(); optimizer.step()
    return encoder, decoder

# === 3) RCS 计算 ===
def compute_rcs(sbg, encoder, decoder, alpha=0.5):
    Z = encoder(sbg)
    A_hat = decoder(Z)
    recon_error = ||A_hat - sbg.adj||^2  # 重构误差
    # 故障传播：考虑 upstream-downstream
    prop_score = propagation_score(sbg, recon_error)
    rcs = alpha * recon_error + (1 - alpha) * prop_score
    return rcs

# === 4) 反馈机制 ===
def feedback_loop(encoder, decoder, sbg, operator_label):
    rcs = compute_rcs(sbg, encoder, decoder)
    # 用 operator_label 微调
    loss = ranking_loss_with_feedback(rcs, operator_label)
    loss.backward(); optimizer.step()
```

### 4. 关键数学

GAE 重构误差：

$$r_i = \|F_i - \hat{F}_i\|^2$$

RCS：

$$\mathrm{RCS}(v_i) = \alpha \cdot r_i + (1-\alpha) \cdot p_i$$

Ranking Loss：

$$L = \sum_{(i,j)\in \mathcal{P}}\max(0, \mathrm{margin} - (\mathrm{RCS}(v_i) - \mathrm{RCS}(v_j)))$$

A@K 准确率（top-K 内 root cause 命中率）：

$$A@K = \frac{\#\{\text{真实 root cause} \in \text{top-K 预测}\}}{\#\{\text{所有 case}\}}$$

### 5. 复杂度分析

论文未给严格复杂度公式，强调：
- **GAE 训练**：$O(|V| \cdot d^2 \cdot L)$，$d$ 嵌入维度、$L$ 层数。
- **数据增强**：$O(|E| \cdot r)$，$r$ 增强比例。
- **反馈微调**：$O(|\text{feedback}| \cdot d^2)$，远小于全量训练。
- **在线推理**：每分钟一个 SBG，RCS 计算可并行。

### 6. 训练与推理

- **训练**：自监督 GAE + 数据增强 + 排序损失；无需 root cause 标签。
- **微调**：用 operator 反馈（少量）持续学习。
- **推理**：SBG 构造 → GAE 编码 → RCS 计算 → top-K 实例。
- **冷启动**：零标注即可训练。

### 7. 示例

论文 Fig.1 展示一个故障在 trace（latency 异常）、log（"request error"）、metric（响应时间飙升）三模态的表现。S1-S7 是不同微服务实例，根因可能在某一上游实例。SBG 捕捉这些实例的依赖关系 + 特征，GAE 重建后通过 RCS 排序输出 top-K 候选。

Fig.2 给出从微服务系统构建 SBG 的示意：节点 S1-S7，边表示调用/部署，节点特征 F 从多模态数据提取。

## 六、系统架构图（Architecture）

```mermaid
graph TB
    subgraph Inputs["多模态输入"]
        A1[Trace 追踪]
        A2[Log 日志]
        A3[Metric 指标]
    end
    subgraph SBG["SBG 构造"]
        B1[提取多模态特征 F]
        B2[每分钟构造有向图: 节点=实例, 边=依赖, F=特征]
    end
    subgraph GAE["Graph Autoencoder"]
        C1[Data Augmentation: 节点/边/子图扰动]
        C2[GCN/GAT 编码器]
        C3[InnerProduct 解码器]
        C4[重构损失 + Ranking Loss]
    end
    subgraph RCS["Root Cause Score"]
        D1[重构误差 r_i]
        D2[故障传播 p_i (upstream-downstream)]
        D3[RCS = α·r_i + (1-α)·p_i]
    end
    subgraph Feedback["反馈机制"]
        E1[运维人员在线反馈 root cause 标签]
        E2[在线微调 GAE 参数]
    end
    subgraph Output["输出"]
        F1[Top-K 候选 root cause 列表]
    end
    A1 & A2 & A3 --> B1 --> B2
    B2 --> C1 --> C2 --> C3 --> C4
    C3 --> D1 --> D3
    B2 --> D2 --> D3
    D3 --> F1
    E1 --> E2 -.微调.-> C2
    C4 -.回传.-> E2
```

## 七、流程图（Process Flow）

```mermaid
flowchart TD
    S1[采集多模态数据: trace+log+metric] --> S2[提取多模态特征 F]
    S2 --> S3[每分钟构造 SBG: 节点=实例, 边=依赖]
    S3 --> S4[数据增强: 节点/边扰动]
    S4 --> S5[GAE 编码: GCN 编码器]
    S5 --> S6[GAE 解码: 重构邻接矩阵 + 节点特征]
    S6 --> S7[计算 RCS: α·重构误差 + (1-α)·传播模式]
    S7 --> S8[Top-K 候选 root cause]
    S8 --> S9[运维人员给出反馈标签]
    S9 --> S10[反馈微调: 排序损失更新 GAE 参数]
    S10 -.持续学习.-> S5
```

## 八、关键创新点（Key Innovations）

- **+ RCS = 重构误差 + 故障传播**：把 GAE 的"黑盒"输出转为"重构误差（这个实例多异常）+ 故障传播（它在依赖链哪个位置）"的组合，给出可解释的根因概率。
- **+ GAE 自监督 zero-label 冷启动**：无需 root cause 标注即可训练，破解"标注数据难获取"难题。
- **+ 数据增强解决训练数据不足**：节点/边/子图扰动让 GAE 在少量历史数据下也能学得稳定。
- **+ 反馈机制持续学习**：运维人员的在线反馈（少量增量标注）可在线微调 GAE 参数，避免"模型部署后性能漂移"。
- **+ 排序损失应对类别不平衡**：root cause 远少于非 root cause，用 margin ranking loss 让 RCS 排序正确而非严格分类。
- **+ 1% 标注即可达 90%+ A@5**：相比 RCLIR 需要 1000 标注，本方法在极少量标注下即可达高准确率，工程价值极高。

## 九、实验与结果（Experiments）

- **数据集**：2 个公开微服务 benchmark（具体见 §5.x）。
- **Baseline**：DiagFusion、Déjàvu、RCLIR 等。
- **评估指标**：A@K（top-K 内 root cause 命中率）、Precision@K、Recall@K。
- **关键结果数字**：
  - **A@5 准确率 90%+** on 2 个数据集。
  - 只需 **1% 标注样本** 即可达此效果。
  - 比 RCLIR 等需要 1000 标注的方法节省 99% 标注成本。
- **消融实验**：RCS 各组件（重构误差、故障传播）、数据增强、反馈机制、排序损失 vs 分类损失。
- **效率分析**：训练时间、推理时间、反馈微调成本。
- **超参分析**：$\alpha$（重构 vs 传播）、margin（ranking loss）、GAE 嵌入维度等。

## 十、应用场景（Use Cases）

- **微服务根因自动定位**：A@5 90%+ 意味着 top-5 候选几乎覆盖真实 root cause。
- **冷启动新系统**：zero-label 自监督，无需等待足够标注。
- **AIOps 平台集成**：作为"故障根因定位"核心模块。
- **运维培训**：RCS 提供"为什么这是 root cause"的可解释理由。
- **在线持续学习**：每次故障后用反馈微调，系统越用越准。
- **CI/CD 门禁**：根因分析嵌入发布流程，自动识别新版本引入的故障源。

## 十一、相关论文（Related Papers in this set）

- `Mengyao__SiameseLSTM`：KPI 时序异常检测（单设备），与本篇多模态根因定位对照。
- `TSC-TADBench`：trace 异常检测评测，与本篇 trace 维度互补。
- `Shiyu__Accurate_and_Interpretable_Log_Fault_Diagnosis_using_Large_Language_Models-2`：日志故障诊断（仅 log），与本篇多模态对照。
- `InformationSciences-OmniFed`：联邦 MTS 异常检测，与本篇都是"自监督/无监督"思路但视角不同。
- `3691620.3695489`（Medicine）：多模态微服务故障诊断（侧重故障分类），与本篇多模态根因定位对照。
- `24_TOSEM_DeepHunt`（本篇，DeepHunt）：GAE 自监督 + 可解释 + 持续学习的多模态根因定位。

## 十二、术语表（Glossary）

- **RCA（Root Cause Analysis）**：根因分析。
- **SBG（System Behavior Graph）**：系统行为图，DeepHunt 提出的微服务系统有向图表示。
- **RCS（Root Cause Score）**：根因分数，DeepHunt 提出的可解释根因概率。
- **GAE（Graph Autoencoder）**：图自编码器。
- **SSL（Self-Supervised Learning）**：自监督学习。
- **A@K Accuracy**：top-K 命中率。
- **RCLIR**：RCA 论文作为对照的方法。
- **DiagFusion / Déjàvu**：根因定位 baseline。
- **RCLIR (Root Cause Localization via Information Retrieval)**：信息检索式 RCA 方法。
- **Graph Augmentation**：图数据增强。
- **Ranking Loss / Margin Ranking Loss**：排序损失。
- **Cold Start**：冷启动，零标注训练。
- **Feedback Loop**：反馈机制。
- **Upstream / Downstream**：依赖链上下游。
- **Feature Fusion**：多模态特征融合。

## 十三、参考与延伸阅读

- **DiagFusion**（论文 [56]）：多模态事件表示 + GNN 根因定位，DeepHunt 的 baseline。
- **Déjàvu**（论文 [26]）：GNN-based 故障诊断，DeepHunt 的 baseline。
- **RCLIR**（论文 [6]）：信息检索式 RCA，对照 DeepHunt 节省 99% 标注。
- **Graph Autoencoder**（论文 [17-19]）：GAE 基础。
- **GCN / GAT**：图卷积/图注意力网络，DeepHunt 编码器选择。
- **Margin Ranking Loss**：DeepHunt 排序损失基础。
- **AWS 2021 故障案例**：论文引用的真实案例。
- **DeepHunt 代码**：https://github.com/bbyldebb/DeepHunt
- **D1 数据集**：https://github.com/bbyldebb/Aiops-Dataset
