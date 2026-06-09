# Accurate and Interpretable Log-Based Fault Diagnosis using Large Language Models（IEEE TSC 2024）

> 作者：Yongqian Sun, Shiyu Ma, Tong Xiao, Yongxin Zhao, Xuhui Cai, Wei Dong, Yue Shen, Yao Zhao, Shenglin Zhang, Jing Han, Dan Pei  
> 机构：南开大学、清华大学、中国移动广东/江苏、中兴通讯  
> 发表年份：2024  
> 会议/期刊：IEEE Transactions on Services Computing（TSC）  
> 关联 PDF：同目录下 `Shiyu__Accurate_and_Interpretable_Log_Fault_Diagnosis_using_Large_Language_Models-2.pdf`

## 一、文档信息速览

| 字段 | 值 |
|---|---|
| 标题 | Accurate and Interpretable Log-Based Fault Diagnosis using Large Language Models（LogInsight） |
| 作者 | Yongqian Sun, Shiyu Ma, Tong Xiao, Yongxin Zhao, Xuhui Cai, Wei Dong, Yue Shen, Yao Zhao, Shenglin Zhang, Jing Han, Dan Pei |
| 机构 | 南开大学软件学院 / Haihe 实验室、清华大学计算机系、中国移动广东/江苏、中兴通讯 |
| 发表年份 | 2024 |
| 会议/期刊 | IEEE Transactions on Services Computing（TSC） |
| 分类 | 日志分析 / 故障诊断 / LLM 微调 / 可解释性 |
| 核心问题 | 在大规模系统故障诊断中，让 LLM 既能准确判定故障类型，又能给出可被运维工程师信任的解释。 |
| 主要贡献 | 1) LogInsight 端到端框架：log preprocessing + FOLS + 知识注入 + 监督微调；2) FOLS（Faut-Oriented Log Summary）模块：DBSCAN 聚类 + TF-IDF 排序压缩日志，绕开 LLM 上下文长度瓶颈；3) LFDInstruction 指令数据集：用 GPT-4 初稿 + 专家复核，赋予 LLM 故障诊断领域知识；4) 在 3 个数据集（2 个公开 + 1 个中国移动生产）上 Weighted F1 提升 7.3%–36.9%。 |

## 二、背景（Background）

现代大规模在线服务系统由成百上千个微服务组成，组件高度耦合。当故障发生时，故障可能沿着调用链迅速扩散，影响数百万终端用户。如果不能在短时间内定位和缓解，损失会非常显著——包括业务停摆、收入下滑和品牌信誉受损。当故障发生时，系统会喷出大量日志，运维工程师的主要任务之一就是**故障分诊（fault triage）**：判断这条故障属于什么类型、应该派给哪个团队处理。

手工分诊耗时且依赖经验，O&M 工程师常常基于经验写"启发式规则"做初筛，但这种规则维护成本高、易失效。于是机器学习/深度学习驱动的自动日志故障诊断成为一个活跃方向。代表性方法包括：
- **LogCluster**：TF-IDF + 层次聚类；
- **Cloud19**：word2vec + 分类器；
- **LogKG**：知识图谱 + OPTICS 聚类；
- **MoniLog / SwissLog**：基于时序/语义嵌入的异常检测。

这些方法的共同短板是：**只给故障分类结果，不给出解释**。而真实工业场景中，运维工程师更需要的是"为什么这么判断"——能否定位到具体日志特征？给出的解释是否合逻辑？这关系到工程师是否敢直接采纳模型结论、能否据此定位根因并采取缓解措施。

LLM 的兴起让"既能分类又能解释"成为可能：它们预训练在海量代码与日志语料上，天然具备语言理解和生成能力。但直接将 GPT-4 等商用 LLM 套到故障诊断上存在两个明显问题：
1. **领域知识不足**：通用 LLM 没有针对"日志 + 故障类型"做过训练，在专业任务上表现有限；
2. **上下文长度限制**：一次故障相关的日志条数动辄成百上千，远超大多数 LLM 的 context window，强行塞入又会因 attention dispersion 引入噪声。

LogInsight 正是为解决这两大问题而设计的：先用一个 FOLS 模块把"杂乱长日志"压缩为"短小信息密集的摘要"，再用 GPT-4 + 人工标注的指令数据对开源 LLM 进行 LoRA 微调，把领域知识注入模型。

## 三、目的（Purpose / Problems Solved）

论文明确将两大挑战写进 abstract 与 introduction：

- **挑战 1：LLM 缺乏领域专业能力。** 直接用 GPT-4 / Mistral 等通用模型做故障分诊，缺少专门针对日志与故障模式的训练，分类准确率受限。
- **挑战 2：LLM 上下文长度不足 + 日志噪声大。** 一次故障涉及成百甚至上万条日志，超出大多数 LLM 的 4k–8k token 限制；同时日志中包含大量重复、无关条目（"无信息熵"），直接喂入 LLM 会引入噪声。

解决方案层面：

- 痛点 1 → **Knowledge Injection + Supervised Fine-tuning**：用 GPT-4 生成"故障诊断+解释"伪标签，经 O&M 专家复核后构建 LFDInstruction 数据集，再用 LoRA 对 Mistral-7B 微调，把领域知识注入模型。
- 痛点 2 → **Fault-Oriented Log Summary (FOLS) 模块**：先用 DBSCAN 聚类（Jaccard 距离）把相似日志聚合、再用 TF-IDF 评分排序过滤噪声，把每条故障的日志压缩到 LLM 上下文允许的体量。
- 痛点 3（隐含）→ **可解释性**：LFDInstruction 中每条样本都带"解释"，微调后模型在分类时同步输出自然语言理由，并请 O&M 专家打分验证。

## 四、核心原理（Principles）

LogInsight 整体分为两阶段（offline + online）：

- **Offline（训练）**：
  1. **Log Preprocessing**：用正则从原始日志中抽出 Content 字段，按时间窗 (t-w:t) 聚成 log content sequence；
  2. **FOLS**：先用 DBSCAN 对 N 条日志做 N×N Jaccard 距离聚类，类内选 centroid；再对每个候选日志用 TF-IDF 打分排序；
  3. **Knowledge Injection**：用 GPT-4 对每条 FOLS 摘要生成"故障类型 + 解释"草稿，专家复核，构建 LFDInstruction；
  4. **Supervised Fine-tuning**：用 LoRA 在 Mistral-7B 上做监督微调，目标函数是最小化模型输出与真实 (fault type + explanation) 之间的损失。
- **Online（推理）**：
  1. 故障发生后取 t 前 w 时段的原始日志 → preprocess → FOLS 摘要；
  2. 构造 prompt：`<instruction> + <log summary>`；
  3. 微调后的 LLM 输出 (fault type, explanation)。

关键概念定义：

- **Log Content Sequence**：去除 timestamp / level 等冗余字段后按时间排列的纯文本日志序列。
- **Jaccard 距离**：对两条日志内容 X、Y 的 token 集合，$d(x,y)=1-|X\cap Y|/|X\cup Y|$，度量二者重合度。
- **Centroid**：聚类内与所有其他点平均 Jaccard 距离最小的代表日志。
- **FOLS 评分**：$\mathrm{score}(x)=\sum_{t\in T_x}\mathrm{TF}(t)\cdot\mathrm{IDF}(t)$，对每个 token 用 TF 局部权重和 IDF 全局权重相乘累加。
- **LFDInstruction**：形如 `(I_i, x_i, y_i)` 的三元组，I 是 instruction 模板，x 是 FOLS 摘要，y 是 (故障类型 + 解释)。

**与现有方法的差异**：

- vs **LogKG / LogCluster / Cloud19**：本方法利用 LLM 的语义理解与生成能力，能同时给出分类与解释，传统方法只能给分类。
- vs **直接用 GPT-4（zero/few-shot）**：本方法通过微调把领域知识固化进 LLM，在 3 个数据集上的 Weighted F1 远超 GPT-4。
- vs **LogPrompt / LogGPT（仅异常检测）**：本方法聚焦"故障诊断（fault triage）"，输出"故障类型"而非仅"是否异常"。
- vs **传统 LLM 故障分类的"截断输入"做法**：本方法用 FOLS 进行"信息密度更高的截断"，避免关键信息因硬截断丢失。

数学上，FOLS 的 TF-IDF 评分定义为：

$$\mathrm{score}(x) = \sum_{t\in T_x} \mathrm{TF}(t)\cdot \mathrm{IDF}(t) = \sum_{t\in T_x}\frac{n_t}{n}\cdot \log\frac{N}{n_t+1}$$

其中 $n_t$ 是 token $t$ 在该条日志中的频次，$n$ 是该条日志总 token 数，$N$ 是总故障数，$n_t$ 在公式 4 中代表"包含 token t 的故障数"。把 $\mathrm{TF}\cdot\mathrm{IDF}$ 加和的目的是：罕见但出现频次不低的 token（往往是故障关键词，如 "Error"、"CRC"、"OSPF"）会获得更高分数。

微调目标：

$$\theta^* = \arg\min_\theta \frac{1}{N}\sum_{i=1}^{N}\mathcal{L}\big(M_\theta(x_i, I_i), y_i\big)$$

$M_\theta$ 是带 LoRA 的 LLM，$\mathcal{L}$ 是标准的自回归 token 损失。

## 五、算法详解（Algorithm）

### 1. 输入 / 输出

- **输入**：原始日志流；故障时间 t；时间窗 w；可选的故障类型集合。
- **输出**：故障类型 $y$（多分类标签）+ 自然语言解释 $e$。

### 2. 核心模块

- **Log Preprocessing**：正则抽取 Content 字段，组成时间序列。
- **FOLS**：
  - (i) **Distance Measurement**：计算 N×N Jaccard 距离矩阵。
  - (ii) **Clustering**：DBSCAN（$\epsilon$ 和 $MinPts$ 来自经验默认值）。
  - (iii) **Representative Selection**：选 centroid 作为类代表。
  - **TF-IDF Ranking**：计算每条日志的 TF-IDF 总分，排序后过滤低分，最后按原时间顺序重排。
- **Knowledge Injection**：GPT-4 草稿 + 专家复核，构建 LFDInstruction。
- **Supervised Fine-tuning**：LoRA（rank=8, alpha=32, dropout=0.05）微调 Mistral-7B。
- **Online Inference**：构造 prompt，微调后 LLM 输出 (fault type, explanation)。

### 3. 伪代码

```python
# === Offline 训练阶段 ===
def build_lfdinstruction(raw_logs_by_fault, fault_types):
    dataset = []
    for fault_id, raw_logs in raw_logs_by_fault.items():
        # 1) 日志预处理
        content_seq = [regex_extract_content(line) for line in raw_logs]

        # 2) FOLS 摘要
        # (i) Jaccard 距离矩阵
        N = len(content_seq)
        D = jaccard_distance_matrix(content_seq)
        # (ii) DBSCAN 聚类
        clusters = DBSCAN(eps=eps, min_pts=min_pts).fit(D)
        # (iii) 取每个簇的 centroid
        representatives = [centroid(c) for c in clusters]
        # TF-IDF 排序 + 时间重排
        fols_summary = tfidf_rank_and_rereorder(representatives)

        # 3) GPT-4 生成解释草稿
        draft = gpt4_generate(fols_summary, fault_types)

        # 4) 专家复核 & 修正
        final_label, final_explanation = expert_review(draft, fols_summary)

        # 5) 构造指令三元组
        instruction = build_instruction(fault_types)
        dataset.append((instruction, fols_summary, (final_label, final_explanation)))
    return dataset


def supervised_finetune(lfdinstruction, base_model='Mistral-7B'):
    model = load(base_model)
    lora = LoRA(rank=8, alpha=32, dropout=0.05)
    model.add_lora(lora)
    optimizer = Adam(lora.params(), lr=1e-4, weight_decay=0.1)
    for (I, x, y) in lfdinstruction:
        input_text = I + x
        target = y
        loss = autoregressive_loss(model, input_text, target)
        optimizer.step(loss)
    return model

# === Online 推理阶段 ===
def online_diagnose(model, raw_logs, fault_time, w, fault_types):
    window_logs = raw_logs_in_window(raw_logs, fault_time, w)
    content_seq = [regex_extract_content(l) for l in window_logs]
    fols = run_fols(content_seq)
    prompt = build_instruction(fault_types) + fols
    return model.generate(prompt)  # -> (fault_type, explanation)
```

### 4. 关键数学

Jaccard 距离：

$$d(x,y)=1-\frac{|X\cap Y|}{|X\cup Y|}$$

TF：

$$\mathrm{TF}(t)=\frac{n_t}{n}$$

IDF：

$$\mathrm{IDF}(t)=\log\frac{N}{n_t+1}$$

每条日志得分：

$$\mathrm{score}(x)=\sum_{t\in T_x}\mathrm{TF}(t)\cdot\mathrm{IDF}(t)$$

Centroid 选择（类内平均距离最小）：

$$\mathrm{centroid}=\arg\min_{x_i\in\mathrm{cluster}}\frac{1}{n}\sum_{j=1}^{n}d(x_i,x_j)$$

F1 度量（Macro / Micro / Weighted）：

$$\mathrm{Macro\ F1}=\frac{1}{N}\sum_i \mathrm{F1}_i$$

$$\mathrm{Precision}_\mathrm{micro}=\frac{\sum TP}{\sum TP+\sum FP},\ \ \mathrm{Recall}_\mathrm{micro}=\frac{\sum TP}{\sum TP+\sum FN}$$

$$\mathrm{Weighted\ F1}=\sum_i w_i\cdot \mathrm{F1}_i,\ w_i=\frac{\text{samples in class }i}{\text{total}}$$

### 5. 复杂度分析

论文未给出严格复杂度公式，但 Table IV 给出实测：在线诊断单条故障 2.7s – 8.5s，离线训练 1800s – 4000s 量级（取决于数据集）。DBSCAN 距离矩阵 $O(N^2)$，但每个故障的 N 通常仅几百到几千，可接受。

### 6. 训练与推理

- **训练目标**：标准自回归损失，LoRA 微调 7B 模型。
- **超参**：lr=1e-4，weight_decay=0.1，batch=16，max_token=4096，LoRA rank=8, alpha=32, dropout=0.05。
- **推理流程**：故障事件 → 时间窗取日志 → preprocess → FOLS → prompt → LLM generate → 解析 (fault_type, explanation)。

### 7. 示例

论文 Fig.8 给出两个真实案例：
- **Case 1（Port Flapping Fault）**：10 分钟窗口内 796 条日志，FOLS 提取出关键端口震荡信息；模型诊断为"Port Flapping Fault"，解释定位到端口状态反复 Up/Down。
- **Case 2（Power Supply Fault）**：从供电电压异常日志出发，模型给出"Power Supply Fault"判定 + 解释，包含具体模块和阈值。

## 六、系统架构图（Architecture）

```mermaid
graph TB
    subgraph Offline["Offline 训练"]
        A1[原始日志库]
        A2[Log Preprocessing<br>正则提取 Content]
        A3[FOLS: Jaccard 距离 + DBSCAN 聚类]
        A4[FOLS: TF-IDF 排序 + 时间重排]
        A5[FOLS 摘要]
        A6[GPT-4 生成 (label, explanation) 草稿]
        A7[O&M 专家复核]
        A8[LFDInstruction 数据集]
        A9[LoRA 监督微调 Mistral-7B]
        A10[微调后 LLM]
    end
    subgraph Online["Online 推理"]
        B1[新故障事件]
        B2[取 t-w:t 窗口原始日志]
        B3[Log Preprocessing]
        B4[FOLS 摘要]
        B5[构造 Prompt: Instruction + 摘要]
        B6[微调 LLM 生成]
        B7[(故障类型, 解释)]
    end
    A1 --> A2 --> A3 --> A4 --> A5
    A5 --> A6 --> A7 --> A8
    A8 --> A9 --> A10
    B1 --> B2 --> B3 --> B4 --> B5
    A10 --> B6
    B5 --> B6 --> B7
```

## 七、流程图（Process Flow）

```mermaid
flowchart TD
    S1[故障发生: 时间 t] --> S2[取 t-w:t 时段原始日志]
    S2 --> S3[正则抽取 Content 字段]
    S3 --> S4[构造 Log Content Sequence]
    S4 --> S5[计算 N×N Jaccard 距离矩阵]
    S5 --> S6[DBSCAN 聚类]
    S6 --> S7[每簇选 Centroid]
    S7 --> S8[TF-IDF 打分排序]
    S8 --> S9[过滤低分 + 时间重排]
    S9 --> S10[FOLS 摘要]
    S10 --> S11{是否训练阶段?}
    S11 -- 是 --> S12[GPT-4 生成诊断草稿]
    S12 --> S13[专家复核]
    S13 --> S14[构造 LFDInstruction 三元组]
    S14 --> S15[LoRA 微调 Mistral-7B]
    S11 -- 否 --> S16[构造 Prompt]
    S16 --> S17[微调 LLM 推理]
    S17 --> S18[输出 (故障类型, 解释)]
```

## 八、关键创新点（Key Innovations）

- **+ Fault-Oriented Log Summary (FOLS) 模块**：在 LLM 上下文受限的前提下，用 DBSCAN 聚类 + TF-IDF 评分两步压缩日志，既能消除重复条目、又能保留对故障诊断关键的"低频高信息量" token（如 "OSPF"、"CRC"）。Table V 消融显示，去掉 FOLS 后 Micro F1 最多跌 0.5，验证模块关键。
- **+ LFDInstruction 知识注入流程**：GPT-4 草稿 + O&M 专家复核 + LoRA 微调，把领域知识从"零散的经验"转化为"LLM 的稳定参数"。Table III 显示，LogInsight 在所有数据集上击败 GPT-4 zero-shot，证明微调带来的是"领域化而非零样本对齐"增益。
- **+ 同时输出"故障类型 + 自然语言解释"**：区别于传统 LogCluster/LogKG 只给分类，LogInsight 在 instruction 中显式要求"provide your explanation"，使 O&M 工程师能直接定位证据。
- **+ 与多种 7B LLM 兼容**：Fig.7 显示在 Mistral-7B、Qwen1.5-7B-Chat、LLaMA2-7B、Gemma-7B 上都能跑通，证明框架不锁定特定基座。
- **+ 工业级部署证据**：Dataset 3 来自中国移动 CMCC 真实生产环境（4G/5G 核心网 322 台交换机一年告警日志），并请 CMCC 的 O&M 专家给解释打 1–5 分，R1/R2/R3 平均 Usefulness 3.80、Readability 4.04，证明落地可信。

## 九、实验与结果（Experiments）

- **数据集**：
  - Dataset 1：服务器日志（公开），2,671 个故障 case，3 种类型（CPU Caterr / Memory Constraint Error / Hardware Error）。
  - Dataset 2：OpenStack 日志（公开），1,461,006 条日志，93 个 case，6 种类型（AMQP Server Unreachable 等）。
  - Dataset 3：中国移动 CMCC 4G/5G 核心网生产日志，178,773 条日志，322 台交换机一年数据，9 种类型（Power Supply / Fan / Optics Module / Port Flapping / CRC / STP / BFD Down / LACP / OSPF Neighbor Flapping）。
  - 每个数据集随机选 50 个 case 构造 LFDInstruction 用于微调，其余用于测试。
- **Baseline**：LogCluster（无监督）、Cloud19、LogKG，外加 GPT-4（同一 prompt）。
- **基座模型**：Mistral-7B、Qwen1.5-7B-Chat、LLaMA2-7B、Gemma-7B 四个 7B 开源 LLM。
- **主要指标**：Micro F1、Macro F1、Weighted F1。
- **关键结果数字**（Table III）：
  - LogInsight 在 3 个数据集上 Weighted F1 = **0.883 / 0.997 / 0.997**，分别比最佳 baseline 高 36.9% / 12.8% / 7.3%。
  - 在 Dataset 1 上 GPT-4（0.490）→ LogInsight（0.883）大幅领先。
  - 4 个基座 LLM 中 Mistral-7B 最强（Table II），后续实验都基于它。
  - FOLS 消融（Table V）：去 FOLS 后 Dataset 2 跌到 Micro F1=0.470（最严重），证明 FOLS 在长日志场景最关键。
  - 聚类 vs 解析（Drain/DivLog/LILAC）：DBSCAN 全维度优于解析类（解析会引入占位符 " * " 误导 LLM）。
  - 效率（Table IV）：在线 2.7s / 8.5s / 2.8s，远低于 1 分钟/case 的工业阈值。
  - 可解释性（Table VII）：3 位 O&M 专家对 200 个 case 打分，Usefulness 均值 3.80，Readability 均值 4.04。
- **消融实验**：FOLS（Table V）、不同聚类/解析方法、不同基座 LLM（Fig.7）。
- **效率分析**：LoRA 7B + 4096 token，单 case 推理 2.7–8.5s；训练 1800–4000s（Table IV）。
- **超参分析**：未做系统超参扫描，但 Table II 显示基座模型对结果影响巨大（Mistral-7B 远胜 LLaMA2-7B、Gemma-7B）。

## 十、应用场景（Use Cases）

- **运营商核心网告警诊断**：中国移动 4G/5G 核心网 9 类故障（电源、风扇、光模块、端口震荡、CRC、STP、BFD、LACP、OSPF）自动分类与解释。
- **云平台故障分诊**：OpenStack 6 类故障（AMQP、MySQL、Computing Node、Disk、Linuxbridge、Nova-conductor）自动分诊，缩短 MTTR。
- **企业服务器硬件故障告警**：CPU、内存、硬件类故障自动归类，定位到具体模块。
- **AIOps 平台集成**：把 LogInsight 作为"故障分诊"插件嵌入告警平台，让告警带可读理由。
- **运维知识库构建**：将 LogInsight 输出的 (label, explanation) 自动沉淀到内部知识图谱或 FAQ。

## 十一、相关论文（Related Papers in this set）

- `LabelEase_ISSRE24_CameraReady`：自动打标/主动学习，与本工作"LFDInstruction 专家标注"形成对照。
- `Shiyu__Accurate_and_Interpretable_Log_Fault_Diagnosis_using_Large_Language_Models-2`（本篇）：LLM 微调 + 可解释故障诊断。
- `Mengyao__SiameseLSTM`：KPI 时序维度异常检测，与本篇日志维度互补。
- `InformationSciences-OmniFed`：联邦场景，与本篇中心化 LLM 微调对照。
- `24_TOSEM_DeepHunt`：深度异常检测（同样是 DeepHunt 模式但不同模态）。

## 十二、术语表（Glossary）

- **LogInsight**：论文提出的端到端日志故障诊断框架名。
- **FOLS（Fault-Oriented Log Summary）**：面向故障的日志摘要模块。
- **LFDInstruction**：作者为 LogInsight 构建的指令微调数据集。
- **Jaccard 距离**：基于 token 集合交并比的两条文本距离度量。
- **DBSCAN**：基于密度的聚类算法，无需指定簇数。
- **TF-IDF**：词频-逆文档频率，常用于信息检索与文本打分。
- **LoRA（Low-Rank Adaptation）**：参数高效微调方法，仅训练低秩矩阵。
- **Mistral-7B**：7B 参数量开源 LLM，论文选定的基座。
- **GPT-4**：OpenAI 闭源大模型，论文中作为知识注入阶段的"草稿生成器"和 zero-shot 对照。
- **Fault Triage（故障分诊）**：将故障归类并派给对应处理团队的过程。
- **Interpretability（可解释性）**：模型输出可被人类理解、信任并据此行动的程度。

## 十三、参考与延伸阅读

- **LogCluster**（论文 [7]）：TF-IDF + 层次聚类的早期日志聚类工作。
- **Cloud19**（论文 [3]）：基于 word2vec 的日志语义分类。
- **LogKG**（论文 [8]）：故障导向日志表示 + OPTICS 聚类 + 知识图谱，GitHub 公开。
- **LoRA**（论文 [36]/[37]）：参数高效微调代表工作，是 LogInsight 微调策略基础。
- **Drain**（论文 [52]）：日志模板解析领域的代表方法，论文 FOLS 消融中作为对照。
- **DivLog**（论文 [42]）与 **LILAC**（论文 [43]）：LLM 驱动的日志解析方法，论文同样作为消融对照。
- **LogPrompt**（论文 [11]）：用 prompt 而非微调做日志异常检测，是 LogInsight 的"非微调"对照。
