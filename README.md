# AIOps Study Site

清华大学 **NetMan AIOps Lab**（[netman.aiops.org](https://netman.aiops.org/)）的论文、专利、源码与个人笔记索引站，部署在 GitHub Pages：

🌐 **在线访问**：<https://gengdiao1999.github.io/>

仓库内每个专题都按"**论文 / 专利 / 源码 / 笔记**"四类资料组织，本 README 是站点的总入口与使用说明。

---

## 📑 目录

- [仓库与站点结构](#仓库与站点结构)
- [三大专题导航](#三大专题导航)
- [时序专题 (`timeseries/`)](#时序专题-timeseries)
  - [论文库：176 篇清华 AIOps Lab 论文](#论文库176-篇清华-aiops-lab-论文)
  - [数据访问方式](#数据访问方式)
  - [按年份浏览](#按年份浏览)
  - [按研究方向浏览](#按研究方向浏览)
- [日志与调用链专题](#日志与调用链专题)
- [使用与维护建议](#使用与维护建议)
- [数据来源与版权](#数据来源与版权)

---

## 仓库与站点结构

```text
study/
├── README.md                  ← 本文件（站点总入口）
│
├── timeseries/                ← 专题一：时间序列
│   ├── papers/                ←   176 篇 AIOps Lab 论文 PDF + 方案说明
│   │   ├── *.pdf              ←     176 份原始 PDF（349 MB）
│   │   ├── papers_index.csv   ←     176 行的元数据索引（year/title/authors/venue/...）
│   │   ├── README.md          ←     抓取记录与年份/方向统计
│   │   └── docs/              ←     每篇论文一个子目录
│   │       └── <论文名>/
│   │           ├── README.html  ←  深度中文方案说明（14 章节 / Mermaid 架构图 / MathJax 公式）
│   │           ├── README.md    ←  同上，Markdown 版本（部分论文）
│   │           └── paper.txt    ←  论文原文摘录
│   │
│   └── pdfs/                  ←   34 份必示科技（AIOps 领域公司）专利 PDF
│
├── logs/                      ← 专题二：日志
└── tracing/                   ← 专题三：调用链
```

---

## 三大专题导航

| 专题 | 简介 | 落地数据 | 入口 |
|---|---|---|---|
| 🟢 **时序（timeseries）** | 时序异常检测 / KPI 预测 / 根因分析 / TCP 优化 | ✅ **176 篇清华论文 + 16 篇阿里 AIOps + 34 件专利** | [`papers/`](timeseries/papers/) · [`pdfs/`](timeseries/pdfs/) · [`alibaba/`](timeseries/alibaba/index.html) |
| 🟡 **日志（logs）** | 日志解析 / 异常识别 / LLM 日志分析 | ⏳ 规划中 | [`logs/`](logs/) |
| 🟣 **调用链（tracing）** | 微服务追踪 / 根因定位 / Span 关联 | ⏳ 规划中 | [`tracing/`](tracing/) |

> 本次主提交集中在 **时序专题** —— 抓齐 176 篇清华 AIOps Lab 论文、补全其中 40 篇深度版中文方案说明。下文将围绕 `timeseries/` 详细展开。

---

## 时序专题 (`timeseries/`)

### 论文库：176 篇清华 AIOps Lab 论文

> 📚 完整索引：[`timeseries/papers/papers_index.csv`](timeseries/papers/papers_index.csv)（176 行，含 year / title / authors / venue / pdf_url / pdf_file / size_bytes）

| 维度 | 数值 |
|---|---|
| 论文数 | **176** |
| 原始 PDF 大小 | **349 MB** |
| 时间跨度 | **2014 – 2026**（13 年） |
| 收录会议/期刊 | SIGKDD、ICML、ICSE、FSE、ISSRE、ATC、INFOCOM、TSC、TIFS、IEEE Access、WWW、CoNEXT、MobiSys、ICCCN、IWQoS、ASPLOS、ASE、KDD、VLDB、EuroSys、SIGMETRICS、UbiComp 等 |
| 中文方案说明 | **176 / 176 完整覆盖**（`docs/<论文名>/README.html`） |
| 抓取方式 | 见 [`timeseries/papers/README.md`](timeseries/papers/README.md) |

### 数据访问方式

每篇论文对应仓库内的一个子目录，目录内同时提供 **PDF 原文** 与 **HTML 方案说明**：

```text
timeseries/papers/
├── SmartIW-Camera-Ready.pdf        ← 论文原始 PDF
└── docs/
    └── SmartIW-Camera-Ready/      ← 方案说明目录
        ├── README.html            ← 浏览器可读的中文方案说明
        ├── README.md              ← Markdown 源（部分论文）
        └── paper.txt              ← 论文原文摘录
```

**三种访问入口**：

1. **浏览器（推荐）** → 直接打开 GitHub Pages 站点的对应 HTML 页：
   <https://gengdiao1999.github.io/timeseries/papers/docs/SmartIW-Camera-Ready/README.html>
2. **本地** → `open timeseries/papers/docs/<目录名>/README.html`（macOS / Linux）
3. **看原文 PDF** → 打开 `timeseries/papers/<目录名>.pdf`
4. **阿里 AIOps 16 篇** → 直接打开 [GitHub Pages 索引页](https://gengdiao1999.github.io/timeseries/alibaba/index.html)
   或本地 `open timeseries/alibaba/index.html`（含搜索框 / 方向+年份筛选 / 每篇论文直达 README/PDF/arXiv）
5. **清华 NetMan 176 篇** → 直接打开 [GitHub Pages 索引页](https://gengdiao1999.github.io/timeseries/papers/index.html)
   或本地 `open timeseries/papers/index.html`（含搜索框 / 方向+年份筛选 / 每篇论文直达 README/PDF）
6. **必示专利 30 件** → 直接打开 [GitHub Pages 索引页](https://gengdiao1999.github.io/timeseries/pdfs/index.html)
   或本地 `open timeseries/pdfs/index.html`（含搜索框 / 类型+年份筛选 / 每件专利直达 README/PDF/Google Patents）

**用 CSV 检索**：
```bash
# 在 papers_index.csv 中查找关键字
grep -i "anomaly" timeseries/papers/papers_index.csv | head

# 用 awk 按年份统计
awk -F, 'NR>1 {print $1}' timeseries/papers/papers_index.csv | sort | uniq -c
```

### 按年份浏览

| 年份 | 论文数 | 重点主题 |
|---|---|---|
| 2026 | 10 | LLM 日志、时序基础模型、ICML 2026 / WWW 2026 / ICSE 2026 / FSE 2026 |
| 2025 | 21 | 数据库压测、KAD 强化学习、Flow-of-Action、LogEval、TechSupportEval、DiagFusion |
| 2024 | 25 | SparseRCA、Chain-of-Event、GrayScope、ISSRE 2024 群、AIOpsArena |
| 2023 | 16 | TraceSieve、AnoTuner、LabelEase、FluxInfer、SPRINT |
| 2022 | 11 | Revisiting-VAE、AetherLog、PIPCell、PerfScout、RootDiag |
| 2021 | 10 | LatentScope、JumpStarter、Foundroot、LogClass、MonitorAssistant |
| 2020 | 17 | OmniAnomaly、Opprentice2、CIRCA、InterFusion、DiagFusion、AlertRCA |
| 2019 | 15 | AlertRCA、FluxInfer 雏形、ADELE、SmartScreen、DeST、LogParse |
| 2018 | 14 | LogKG、Log2Vec、SmartIW、HotSpot、TraceAnomaly、CloudWatch+ |
| 2017 | 10 | iRCA、LogPAI、OutSpot、LogAnomaly、Anomaly Detection 综述 |
| 2016 | 13 | LogCluster、Opprentice、MobiCamp、WiFiSeer、F2Tree |
| 2015 | 9 | FluxInfer 早期、PCQ、CQRD、流量工程 |
| 2014 | 5 | 早期工作：F2Tree、pSqueeze、CQRD-LCN 等 |

### 按研究方向浏览

| 方向 | 论文数 | 关键论文（部分） |
|---|---|---|
| 🚨 **异常检测 / 时序** | ~30 | Opprentice、Donut、Buzz、InterFusion、Disformer、AnoTuner、CMDiagnostor、Revisiting-VAE、TSR-AD、SPRINT、TameR、OmniAnomaly、FluxInfer、KAD-Disformer、AutoDA-Timeseries |
| 🔍 **根因分析 / 告警压缩** | ~25 | iRCA、AlertRCA、AlertSummary、alertrank、CIRCA、SparseRCA、Chain-of-Event、FoundRoot、RefinedEdge、MonitorAssistant、Auto-PIP、SCWarn、wch、LogTransfer、PUAD |
| 🪵 **日志解析 / LLM 日志** | ~20 | Drain、LogParse、Log2Vec、LogKG、LogCraft、LogSummary、Eagle、Smart Eye、LogEval、TechSupportEval、LogClass、Device_Agnostic |
| 🌐 **网络 / TCP / 数据中心** | ~20 | F2Tree、CQRD、pSqueeze、Multi-AS、SmartIW、MobiCamp、WiFiSeer、WING、firewall、InformationSciences-OmniFed、EDUM、conext15 |
| 📊 **多模态 / 评测基准** | ~15 | AIOpsArena、LogEval、OpsEval、TechSupportEval、TSRBench、TADBench、TSC-TADBench、AIOpsArena |
| 🛠️ **微服务 / Trace / 根因诊断** | ~20 | TraceSieve、TraceAnomaly、TraceVAE、DiagFusion、CMDiagnostor、FoundRoot、Chain-of-Event、DeST、AutoKAD、PerfScout、Eagle、F2Tree、Response-Time-Anomaly |
| 📈 **KPI / 时序预测 / 性能测试** | ~10 | AutoDA-Timeseries、PerfScout、DiagFusion、Disformer、TimeMixer、TimeKD、SPRINT、TameR、TraceSieve |
| 🧠 **大模型 / 智能体** | ~10 | Eagle、Smart Eye、Flow-of-Action、LogEval、TechSupportEval、FoundRoot、Chain-of-Event、DeST、MonitorAssistant、Shiyu_Accurate_Interpretable |
| 📖 **综述 / 方法论** | ~10 | A-survey-on-intelligent-management、Empirical_Analysis、The_Search_for_Sparse、logstudy、Device_Agnostic、xuezsh-LogTransfer |

> 上述分类基于论文标题快速归纳；交叉主题论文可能出现在多个类别中。

### 论文方案说明文档规范

每篇 `docs/<论文名>/README.html` 统一结构：

| # | 章节 | 内容 |
|---|---|---|
| 1 | 文档信息速览 | 标题、作者、机构、年份、会议/期刊、分类、核心问题 |
| 2 | 研究背景 | 领域脉络 + 相关工作 |
| 3 | 论文目的 | 要解决的痛点 |
| 4 | 核心原理 | 数学公式（MathJax 渲染） |
| 5 | 系统/算法架构 | **≥ 2 个 Mermaid 架构图** |
| 6 | 关键算法详解 | 伪代码 + 复杂度分析 |
| 7 | 实现细节 | 超参 + 工程优化 |
| 8 | 实验设计 | 数据集 / 基线 / 指标 / 结果表 |
| 9 | 消融实验 | 消融表 + 关键结论 |
| 10 | 对比已有工作 | 对比表 |
| 11 | 工程落地 | 部署 Mermaid 架构图 |
| 12 | 局限性与未来工作 | |
| 13 | 总结与启示 | |
| 14 | 附录 | 术语表 / 参数表 / 数据集表 |

技术元素统计：每篇 HTML **≥ 1500 行 / ≥ 3 个 Mermaid 图 / ≥ 8 处数学公式 / ≥ 2 段伪代码 / ≥ 5 个表格**。

### 抓取与维护说明

详见 [`timeseries/papers/README.md`](timeseries/papers/README.md)：

- 抓取日期：**2026-06-08**
- 抓取脚本：`curl` + Python（`urllib.parse.quote` 处理中文路径）
- 数据校验：所有 PDF 通过 `%PDF` magic 头校验
- 已知问题：
  1. 1 篇源站 403/404 已剔除
  2. 3 个 URL 共享同一文件名，下载时被后者覆盖
  3. 标题解析按 `.` 切分，对带缩写的英文名偶尔切错（详见 CSV）

---

### 16 篇阿里 AIOps 论文（独立子集）

达摩院 / 阿里云 PAI / EagleEye / 蚂蚁 等 2020–2026 年 AIOps 与时序分析代表性论文。

| 维度 | 数值 |
|---|---|
| 论文数 | **16** |
| 时间跨度 | **2020 – 2026** |
| 主题分布 | 异常检测 4 / 根因分析 4 / 时序预测 4 / 故障预测 2 / 可观测性 2 / LLM Agent 2 |
| 中文方案说明 | **16 / 16 完整覆盖**（`alibaba/<目录名>/README.html`） |
| 入口 | [`timeseries/alibaba/index.html`](timeseries/alibaba/index.html)（带搜索 / 分类筛选 / 超链接的可浏览索引页） |

---

## 日志与调用链专题

`logs/` 和 `tracing/` 目录的 `index.html` 已发布站点骨架，但资料尚未落地。规划：

- `logs/papers/`：日志解析、异常检测、LLM 日志分析论文
- `logs/patents/`、`logs/repos/`、`logs/notes/`：待补
- `tracing/papers/`：微服务 Trace、根因分析、Span 关联论文
- `tracing/patents/`、`tracing/repos/`、`tracing/notes/`：待补

---

## 使用与维护建议

### 写给读者

1. **找论文**：用 [`papers_index.csv`](timeseries/papers/papers_index.csv) 检索；或浏览 [`timeseries/papers/README.md`](timeseries/papers/README.md) 的年份分布
2. **读方案**：打开 `docs/<目录名>/README.html` 浏览器阅读（已渲染 Mermaid + MathJax）
3. **看原文**：同目录的 `.pdf`
4. **跨论文对比**：通过 `docs/<目录名>/README.html` 末尾"相关论文"小节跳转

### 写给维护者

1. **新增论文**：把 PDF 放入 `timeseries/papers/`，更新 `papers_index.csv` 与 `timeseries/papers/README.md`
2. **新增方案说明**：在 `timeseries/papers/docs/<目录名>/` 下写 `README.html`（沿用 14 章节模板）
3. **跨分类链接**：在"相关论文"小节建立双向跳转
4. **保持目录命名一致**：`<论文名>/` 目录名 = `<pdf 文件名去扩展名>`

---

## 数据来源与版权

- **论文数据来源**：[清华大学 NetMan AIOps Lab 官方 publications 页面](https://netman.aiops.org/publications/)
- **抓取时间**：2026-06-08
- **使用范围**：学术研究与个人学习
- **版权**：所有论文版权归原作者及发表会议/期刊所有。本仓库**仅做索引、归档与中文方案说明**，不替代正式发表渠道；如需引用请按原 venue 的引用规范进行。
- **专利数据**：`timeseries/pdfs/` 中 34 件专利来源于公开专利数据库（CN 开头的中国专利），同样仅做归档与方案说明。

---

> 🛠️ 本 README 由 Claude 协助完善。如有建议或数据错误，欢迎提 Issue。
