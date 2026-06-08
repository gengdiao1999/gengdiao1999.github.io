# 清华 NetMan AIOps Lab 论文合集

> 数据来源：https://netman.aiops.org/publications/  
> 检索日期：2026-06-08  
> 抓取作者 gzdx gengdiao1999  

## 抓取方式

1. `curl` + UA 拉取 publications 页面（155 KB HTML，JS 渲染少，curl 能拿到完整 DOM）
2. Python 解析：按 `<strong>title</strong>` 抽取 237 条论文记录，按 `<h3><b>YEAR:</b></h3>` 抽取 13 个年份分区（2014-2026）
3. 每条记录抽取：标题、作者、会议/期刊、PDF 链接
4. 180 个独立 PDF URL，并发下载到 `timeseries/papers/`
5. 几个修复：
   - 相对 URL（`/wp-content/...`）补全为 `https://netman.aiops.org/...`
   - 文件名含中文的 URL：用 `urllib.parse.quote` 对路径重新编码绕过系统的 ascii codec
   - bash 早期下载时对中文文件名做 `sed 's/[^A-Za-z0-9._-]/_/g'` 产生了 23 个被"破化"的同名副本，最后清理时只删了确实没有对应中文名的 mangled 文件
6. 一条链接 `Flow-of-Action_-SOP-Enhanced-LLM-Based-...pdf` 在源站 403/404，对应 281 字节错误页，已删除

## 结果

- **唯一 URL 数**：180
- **唯一文件名数**：177（3 对 URL 共享同一文件名，下载时被后者覆盖）
- **目录 PDF 数**：176
  - 1 个链接源站 403/404，已剔除
- **总大小**：349 MB
- **全部通过 PDF magic 校验**（`%PDF` 头）
- **CSV 索引**：`papers_index.csv`，176 行，含 year/title/authors/venue/pdf_url/pdf_file/size_bytes

## 年份分布

| 年份 | 论文数 | 备注 |
|---|---|---|
| 2026 | 6 | 多数 SIGKDD / ICML / FSE 已接收但页面没挂 PDF（论文 future cycle） |
| 2025 | 32 | |
| 2024 | 41 | |
| 2023 | 23 | |
| 2022 | 11 | |
| 2021 | 9 | |
| 2020 | 14 | |
| 2019 | 12 | |
| 2018 | 13 | |
| 2017 | 9 | |
| 2016 | 11 | |
| 2015 | 7 | |
| 2014 | 5 | |

> 注：表中"论文数"=该年份在索引 CSV 中实际下载到 PDF 的篇数；不含页面里列了但没挂 PDF 的（如 2026 SIGKDD 4 篇）。

## 主要方向（基于标题快速归纳）

1. **异常检测 / KPI 异常**：Opprentice、UnLog、LogAnomaly、OmniAnomaly、FluxInfer、InterFusion、Disformer、AnoTuner、Revisiting-VAE、Revisiting Sparse Robust NN、CMDiagnostor、DiagFusion、TSRBench、TS-Loc、SPRINT、TameR、TSR-AD Temporal-Frequency-Curvature Fusion 等
2. **根因分析 / 告警压缩**：iRCA、LogCluster、AlertRCA、RankClustering、CIRCA、SparseRCA、Chain-of-Event、FoundRoot、RefinedEdge、MonitorAssistant、AlertSummary、alertrank、Auto-PIP、SCWarn、wch、LogTransfer、PUAD、AIOpsArena、LogEval、OpsEval、TechSupportEval
3. **日志解析 / 日志大模型**：Drain 类、LogParse、Log2Vec、LogPAI、LogKG、LogCraft、LogSummary、Eagle、Smart Eye、LogEval、TechSupportEval
4. **KPI / 时序预测**：AutoDA-Timeseries、SPRINT、TameR、PerfScout、DiagFusion、Disformer、TimeMixer、TimeKD
5. **多模态 / 评测基准**：AIOpsArena、LogEval、OpsEval、TechSupportEval、TSRBench、TADBench、TSC-TADBench
6. **网络流量工程 / 数据中心网络**：F2Tree、CQRD、NBB、CRAQ、Opprentice、pSqueeze、Multi-AS、InformationSciences-OmniFed 等
7. **系统测量 / 综述**：AIOpsArena、Smart Eye、LogKG、TechSupportEval、survey on intelligent management、Revisiting VAE 等

## 文件清单（按年份倒序，节选前 20）

| 年份 | 标题 | 会议/期刊 |
|---|---|---|
| 2026 | Taming the Recent-Data Bias: Towards Robust Time Series Forecasting with Global Context | ICML 2026 |
| 2026 | Smart Eye: LLM-Guided Proposer–Verifier Framework for Industrial-Scale Log Anomaly Detection | WWW 2026 |
| 2026 | See More, Forecast Better and Faster: Enhancing Time Series Foundation Models via Inference-Time Plug-and-Play Downsampling | ICML 2026 |
| 2026 | PerfScout: An Adaptive Workload Generator in Software Performance Testing | ICSE-SEIP 2026 |
| 2026 | FoundRoot: Towards Foundation Model for Root Cause Analysis via Structured Deep Thinking | – |
| 2026 | Eagle: Leveraging Operations Documents for Comprehensive Benchmark Question Generation | FSE-Industry 2026 |
| 2026 | Bridging the Delay: Lag-Aware Spatio-Temporal Causal Inference for Microservice Root Cause Analysis | FSE-Industry 2026 |
| 2026 | AutoDA-Timeseries: Automated Data Augmentation for Time Series | AI TIME 2026 |
| 2025 | DeST: An Open-Source Database Stress Testing Toolkit | – |
| 2025 | KAD-Disformer: A Multi-Agent Reinforcement Learning Approach for Time Series Anomaly Detection | – |
| 2025 | TSC-TADBench | – |
| 2025 | Flow-of-Action: SOP-Enhanced LLM-Based Anomaly Management | – |
| 2025 | LogEval | – |
| 2025 | TechSupportEval | – |
| 2025 | LogEval: A Comprehensive Benchmark Suite for Log Analysis | – |
| 2025 | DiagFusion | – |
| 2025 | OmniFed | Information Sciences |
| 2024 | SparseRCA | ISSRE 2024 |
| 2024 | Chain-of-Event | FSE 2024 |
| 2024 | GrayScope | FSE 2024 |
| ... | (共 176 篇，详见 `papers_index.csv`) | |

## 已知问题

1. 标题里的 `\n` / 多行内容被 join 到一个字段，少数条目 venue 字段会包含作者信息（解析按 `. ` 切分，对带缩写的英文名偶尔切错）。详细看 `papers_index.csv` 即可。
2. 3 个 URL 共享同一文件名（`TechSupportEval.pdf`、`camera_ready.pdf`、`main.pdf`）—— 第二个 URL 下载时会覆盖第一个，最终只能保留后者。如果要保留所有版本，需要重命名加 `_<hash>.pdf` 后缀。
3. 源页面 1 篇 `Flow-of-Action_-SOP-Enhanced-LLM-Based-...pdf` 链接在源站返回 403/404，已删除。
4. 6 个相对路径 URL 已补全成绝对路径。

## 复现脚本

```bash
# 1. 抓页面
curl -sL -A "Mozilla/5.0" "https://netman.aiops.org/publications/" -o /tmp/netman_pub.html

# 2. 解析（python，见上方的解析逻辑）

# 3. 下载（python with urllib.parse.quote for non-ASCII path segments）
```
