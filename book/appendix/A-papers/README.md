# 附录 A：论文

本附录收录与时间序列分析、AIOps、系统可靠性相关的代表性论文，作为正文各章节的延伸阅读与文献索引。

## 结构说明

| 子目录 | 内容 | 数量 |
|---|---|---|
| `netman/` | 清华大学 NetMan AIOps Lab 论文 | 176 篇 |
| `alibaba/` | 阿里 / 达摩院 / 蚂蚁 AIOps 论文 | 16 篇 |
| `classification/` | 时序分类（TSC）代表论文 | 22 篇 |

## 浏览索引

- [A 论文总索引](./index.html)
- [清华 NetMan Lab 论文索引](./netman/index.html)
- [阿里 AIOps 论文索引](./alibaba/index.html)
- [时序分类代表论文索引](./classification/index.html)

## 维护方式

索引页由 `tools/build_index.py` 根据各子目录下的 CSV 文件自动生成。新增论文时，请按对应子目录的约定放置 PDF 与 README，然后运行：

```bash
python3 tools/build_index.py papers
```

## 版权说明

所有论文 PDF 与方案说明仅用于学习研究目的，版权归原作者及发表会议/期刊所有。
