# 环境方差与报告异质性下再生数估计的不可约误差与监测设计
### Irreducible Error and Surveillance Design for Reproduction Number Estimation under Environmental and Reporting Variance

本仓库包含该研究的全部论文源码、预编译成果、复现代码、数据集及审稿核对材料。

---

## 📌 项目概述

在传染病监测中，扩大病例监测规模通常被认为能单调提升再生数估计精度。本项目研究表明，当环境随机性与报告异质性存在时，这一直觉不再成立：

1. **两个估计目标的区分**：
   - **估计目标 1（条件瞬时再生数 $R_t$）**：真实再生数本身即为目标，误差随规模扩大单调趋近于零，达到 Cramér–Rao 界。
   - **估计目标 2（跨期平均再生数 $\bar{R}$）**：环境方差 $v_R$ 构成不随规模缩减的不可约误差下界，观测方差服从 $V(m) = v_R + A/m$。
2. **监测规模与平衡点**：
   - 定义平衡规模 $m_\times = A/v_R$。当采样规模达到 $m_\times$ 时，可约抽样方差已与不可约方差相当；进一步扩大规模面临强烈的边际收益递减（规模翻倍的方差削减比例由 $1/[2(1+m/m_\times)]$ 决定）。
   - 理论基准参数下 $m_\times \approx 53.1$；引入报告异质性 $\tau=0.15$ 后平衡规模降为 $30.4$。
3. **真实世界实证证据**：
   - 基于美国 CDC NHSN（2020–2026）16,218 州周流感住院数据（有效 10,303 州周，流行初期 1,267 州周），FGLS 估计得到截距 $a = 0.0991$ [0.0837, 0.1165]，斜率 $b = 2.243$ [1.494, 3.007]，比值 $b/a = 22.6$ [13.5, 34.9]。
   - 考虑报告调整后 $\Delta a = -0.0004$（90% BCa [-0.0012, 0.0005]），落在两两等价界 $\pm 0.0050$ 内，可观测报告成分占不可约方差比例不足 1%。
   - 跨病原体与多源监测（FluSight、ILINet、FluSurv-NET）呈现一致的分级特征。

---

## 📂 仓库结构

```text
case-count-bottleneck/
├── paper_zh/                      # 最新版论文（仿照 Eales & Riley 2024 结构重写）
│   ├── build/
│   │   ├── main.pdf               # 正文 PDF（24 页，5 张多面板主图，正文 0 表）
│   │   └── supplement.pdf         # 补充材料 PDF（14 页，表 S1–S8、图 S1–S3 及证明）
│   ├── sections/                  # 各章节 LaTeX 源码（Introduction, Background, Results, etc.）
│   │   ├── introduction.tex
│   │   ├── background.tex
│   │   ├── results.tex
│   │   ├── discussion.tex
│   │   ├── conclusion.tex
│   │   ├── methods.tex
│   │   ├── endmatter.tex
│   │   ├── supp_proofs.tex
│   │   └── supp_robustness_tables.tex
│   ├── figures/                   # 5 张多面板主图与补充图矢量 PDF
│   ├── tables/                    # 补充材料 LaTeX 表格
│   ├── scripts/                   # 图表构建与合成脚本 (build_main_figures.py)
│   ├── main.tex                   # 正文主入口
│   ├── supplement.tex             # 补充材料入口
│   └── bibliography.bib           # 参考文献数据库（采用 author-year 格式）
│
├── paper/                         # 原始版本论文源码及产物存档
│   ├── paper.pdf                  # 原版 PDF
│   ├── main.tex
│   └── ...
│
├── experiment/                    # 实证与仿真复现包
│   ├── code/                      # 数据清洗、模型拟合、Bootstrap 及模拟脚本
│   ├── data/                      # 整理后的研究面板数据及基准参数
│   ├── analysis/                  # 详细分析产物与数字复现映射 (reproduction_map.json)
│   └── logs/                      # 运行日志
│
├── advisor-briefing.pdf           # 汇报简报（含 PDF / DOCX / HTML / MD）
├── derivation-handout.md          # 详细数学推导手册
├── acceptance-r4.md               # 验收标准与关键数据对照清单
└── README.md                      # 本文档
```

---

## 📄 成果文件直接阅读

- **论文正文**：[`paper_zh/build/main.pdf`](paper_zh/build/main.pdf)
- **补充材料**：[`paper_zh/build/supplement.pdf`](paper_zh/build/supplement.pdf)
- **汇报简报**：[`advisor-briefing.pdf`](advisor-briefing.pdf)
- **推导手册**：[`derivation-handout.md`](derivation-handout.md)

---

## 🛠️ 编译指南

本项目使用 `ctexart` 配合 XeLaTeX / Tectonic 进行排版，并支持完整的交叉引用与作者-年份文献索引。

### 推荐方式：使用 Tectonic
```bash
cd paper_zh

# 编译正文
tectonic -X compile main.tex --outdir build --keep-intermediates --keep-logs

# 编译补充材料
tectonic -X compile supplement.tex --outdir build --keep-intermediates --keep-logs
```

### 传统方式：使用 XeLaTeX + BibTeX
```bash
cd paper_zh

xelatex -output-directory=build main.tex
bibtex build/main
xelatex -output-directory=build main.tex
xelatex -output-directory=build main.tex

xelatex -output-directory=build supplement.tex
xelatex -output-directory=build supplement.tex
```

---

## 🔬 复现说明

所有理论推导和实证结果均配有复现映射表：
- 完整数字基准对照：详见 [`acceptance-r4.md`](acceptance-r4.md)
- 实证分析映射与配置：详见 [`experiment/analysis/reproduction_map.json`](experiment/analysis/reproduction_map.json)
- 实证执行脚本：详见 [`experiment/code/`](experiment/code/)

---

## 📑 参考文献

- Eales, O., & Riley, S. (2024). Differences between the true reproduction number and the apparent reproduction number of an epidemic time series. *Epidemics*, 46, 100742. https://doi.org/10.1016/j.epidem.2024.100742
- Cori, A., Ferguson, N. M., Fraser, C., & Cauchemez, S. (2013). A new framework and software to estimate time-varying reproduction numbers during epidemics. *American Journal of Epidemiology*, 178(9), 1505–1512.
- Parag, K. V., & Donnelly, C. A. (2020). Using information theory to optimise epidemic models for real-time prediction and estimation. *PLoS Computational Biology*, 16(7), e1007990.
