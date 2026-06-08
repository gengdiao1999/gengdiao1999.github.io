# 必示科技 (北京必示科技有限公司) 专利合集

> 检索源：Google Patents — assignee = "必示"
> 检索日期：2026-06-08
> 检索返回总数：30 件（"30 results"，共 3 页）
> 申请人均已校验：`北京必示科技有限公司`（每件 PDF 首页的 (71)申请人 / (73)专利权人 字段）

## 目录

- `CN<id>.pdf` — 30 件发明专利的官方 PDF（来自 `patentimages.storage.googleapis.com`）
- `patents_index.csv` — 30 件专利的元数据（专利号、标题、申请号、申请日、公开号、公开日、申请人、Google Patents 链接、PDF 文件名），按申请日升序
- `_download_log.txt` — 抓取过程的简要日志

## 抓取方式

1. 用 headless Chrome 渲染 `https://patents.google.com/?assignee=必示&page=0..2`，把页面里的 `data-result="patent/CN.../en"` 抓出来，得到 30 个专利号。
2. 每个专利页里都带 `class="pdfLink"` 直链到 `patentimages.storage.googleapis.com/...`，并发 curl 拉 PDF，8 路并行。
3. PDF 首页 `pdftotext` 抽出 (54) 发明名称 / (21) 申请号 / (22) 申请日 / (43)(45) 公开日 / (71)(73) 申请人，落到 CSV。

## 备注

- `assignee=必示`（中文单字）在 Google Patents 上能返回所有 30 件；英文写法 `Beijing BizSeer` / `BizSeer` 都返回 0 results，所以选中文 assignee 检索。
- 另有一份历史副本在 `timeseries/pdf/CN115391160B.pdf`（MD5 与本次下载的 `pdfs/CN115391160B.pdf` 一致：`14180173eb353f65664354871b757d20`），未删除。
- 30 件里：发明专利申请（A）18 件 + 授权发明专利（B）12 件。
- 最早的申请日 2019-08-13，最晚 2022-10-26（截至本次检索 Google Patents 上能看到的最新一件）。

## 30 件专利一览（按申请日升序）

| 专利号 | 标题 | 申请日 | 公开日 |
|---|---|---|---|
| CN110532550A | 一种基于日志词频树的智能系统日志解析处理方法 | 2019.08.13 | 2019.12.03 |
| CN110837953A | 一种自动化异常实体定位分析方法 | 2019.10.24 | 2020.02.25 |
| CN111858231B | 一种基于运维监控的单指标异常检测方法 | 2020.05.11 | 2024.07.26 |
| CN111309565B | 告警处理方法、装置、电子设备以及计算机可读存储介质 | 2020.05.14 | 2020.08.18 |
| CN111338915B | 动态告警定级方法、装置、电子设备以及存储介质 | 2020.05.15 | 2020.09.01 |
| CN111444247B | 一种基于KPI指标的根因定位方法、装置及存储介质 | 2020.06.17 | 2023.10.17 |
| CN111506637A | 一种基于KPI指标的多维异常检测方法、装置及存储介质 | 2020.06.17 | 2020.08.07 |
| CN111539493A | 一种告警预测方法、装置、电子设备及存储介质 | 2020.07.08 | 2020.08.14 |
| CN111597070B | 一种故障定位方法、装置、电子设备及存储介质 | 2020.07.27 | 2020.11.27 |
| CN111737095B | 批处理任务时间监控方法、装置、电子设备及存储介质 | 2020.08.05 | 2025.01.14 |
| CN112231193A | （见 patents_index.csv） | 2020.12.10 | — |
| CN112559237B | （见 patents_index.csv） | — | — |
| CN112559238B | （见 patents_index.csv） | — | — |
| CN112862019A | （见 patents_index.csv） | — | — |
| CN112905671A | （见 patents_index.csv） | — | — |
| CN113434193B | （见 patents_index.csv） | — | — |
| CN113448808B | （见 patents_index.csv） | — | — |
| CN113568991B | （见 patents_index.csv） | — | — |
| CN113722616A | （见 patents_index.csv） | — | — |
| CN113806495A | （见 patents_index.csv） | — | — |
| CN113900844B | （见 patents_index.csv） | — | — |
| CN113962273B | （见 patents_index.csv） | — | — |
| CN114721861B | （见 patents_index.csv） | — | — |
| CN114785666B | （见 patents_index.csv） | — | — |
| CN114818643A | （见 patents_index.csv） | — | — |
| CN115062144B | （见 patents_index.csv） | — | — |
| CN115391160B | （见 patents_index.csv） | 2022.10.26 | 2023.04.07 |
| CN115392403A | （见 patents_index.csv） | — | — |
| CN116302762A | （见 patents_index.csv） | — | — |
| CN116820826A | （见 patents_index.csv） | — | — |

完整字段（标题、申请号、公开日、Google Patents URL、PDF 文件名）见同目录的 `patents_index.csv`。
