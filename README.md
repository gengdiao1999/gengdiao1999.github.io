# 时间序列分析：从特征到因果

欢迎来到本仓库。这里正在编写一部面向工程与研究人员的**中文时间序列分析技术书籍**，同时保留并整理了清华 NetMan Lab 论文、阿里 AIOps 论文、时序分类代表论文，以及必示科技专利作为附录。

## 阅读入口

- **📖 书籍正文**：[`book/README.md`](book/README.md)
- **📑 全书目录**：[`book/SUMMARY.md`](book/SUMMARY.md)
- **🧾 编写规范**：[`CLAUDE.md`](CLAUDE.md)
- **📚 附录 A：论文索引**：[`book/appendix/A-papers/index.html`](book/appendix/A-papers/index.html)
- **📜 附录 B：专利索引**：[`book/appendix/B-patents/index.html`](book/appendix/B-patents/index.html)

## 书籍主题

| 篇 | 主题 | 对应目录 |
|---|---|---|
| 基础篇 | 绪论、时序基础 | `book/part-00-fundamentals/` |
| 第一篇 | 特征提取 | `book/part-01-feature-extraction/` |
| 第二篇 | 时域分析 | `book/part-02-time-domain/` |
| 第三篇 | 频域分析 | `book/part-03-frequency-domain/` |
| 第四篇 | 时序分类 | `book/part-04-classification/` |
| 第五篇 | 时序异常检测 | `book/part-05-anomaly-detection/` |
| 第六篇 | 时序预测（单/多指标） | `book/part-06-forecasting/` |
| 第七篇 | 时序因果分析 | `book/part-07-causal-analysis/` |
| 附录 A | 论文 | `book/appendix/A-papers/` |
| 附录 B | 专利 | `book/appendix/B-patents/` |

## 本地构建

```bash
# 生成论文/专利 HTML 索引
python3 tools/build_index.py

# 运行测试
python3 -m pytest tests/test_build_index.py -v
```

## 贡献说明

新增或修改章节前，请先阅读 [`CLAUDE.md`](CLAUDE.md)。每章以独立文件夹组织，预留 `assets/images/`、`assets/code/`、`assets/data/` 目录，便于后续扩展。

---

*本仓库基于 GitHub Pages 部署，原 `timeseries/` 论文与专利资产已迁移到 `book/appendix/`。*
