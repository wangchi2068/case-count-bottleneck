# Scaling Limits and Surveillance Design for Epidemic Reproduction Numbers Under Environmental and Reporting Stochasticity
### 环境随机性与报告异质性下疫情再生数监测的尺度极限与资源配置设计

本仓库包含该研究的最终中英文论文排版成稿、全套 LaTeX 源码工程、插图附表及完全可复现的代码与实证数据。

---

## 📌 研究概述

在疫情监测中，通常假设报告病例越多，再生数估计精度越高。然而，真实传播伴随着气候、行为与节假日等跨期环境随机性以及非完全报告异质性。本项目系统研究了环境与报告随机性下再生数监测的尺度极限与资源优化配置：

1. **统一方差结构模型**：
   - 在带二项报告的负二项分支过程下，证明单期平均再生数的误差方差服从 $V(m) = v_R + A/m$，其中 $v_R$ 为跨期环境方差，$m$ 为报告病例规模。
   - 定义微观抽样向宏观环境变异过渡的**方差平衡规模** $m_\times = A/v_R$。当监测规模达到 $m_\times$ 时，规模每翻倍一次仅能消除最多 25% 的剩余方差，面临显著的边际收益递减。
   - 预算最优分配律满足 $m^* = \sqrt{(c_0/c_1)m_\times}$（$c_0/c_1$ 为观测期数与单期个案的成本比）。
2. **两步动力学仿真反演**：
   - 针对表观指标时间平滑对真实方差的放缩变形，建立了数据匹配的动力学仿真校准反演框架。
   - 实证分析全美 2020–2026 年四个流感季（10,506 州周数据），更新型比值 $R_A$ 反演的潜伏环境方差为 **$0.040$ [0.026, 0.056]**，加权增长比 $G$ 反演的潜伏环境方差为 **$0.043$ [0.025, 0.064]**。
   - 两者之比为 **$0.93$（90% CI: [0.81, 1.13]）**，显著落在 $[0.80, 1.25]$ 国际通用等效检验判定带内。
3. **多尺度方差解耦与监测设计**：
   - 误差截距中 41%~51% 为全国同一日历周内共享的宏观同步冲击，无法通过单州扩样消除，为跨辖区协同监测（Spatial Pooling）提供了定量依据。
   - 确立了表观尺度周住院平衡点 $37.4$ 例/周（潜伏尺度约为 $30.3$ 例/代，约每周 59 例）。当周报告量超过该平衡规模后，增加观测期数与跨区协同的精度增益显著高于单期盲目扩样。

---

## 📂 仓库结构

```text
├── paper_en/                     # 英文论文工程（目标期刊：Epidemics）
│   ├── paper.pdf                 # 24 页英文排版定稿 PDF
│   ├── paper.html                # 英文定稿自包含 HTML（免阅读器双击即看）
│   ├── main.tex, compile.sh      # LaTeX 编译入口与自动化脚本
│   ├── bibliography.bib, *.bst   # 44 条全引用参考文献库与定制样式表
│   ├── sections/                 # 9 个正文章节 LaTeX 源码（含附录全套定理证明）
│   ├── tables/                   # 附表 S1–S10 源码 (tab_s1 ~ tab_s10) 与指纹清单
│   └── figures/                  # 8 张论文专用插图（6 张矢量 PDF + 2 张位图）
│
├── paper_zh/                     # 中文论文工程（内容与数字同英文定稿 100% 对齐）
│   ├── paper.pdf                 # 24 页中文排版定稿 PDF
│   ├── paper.html                # 中文自包含 HTML
│   ├── main.tex, compile.sh      # 中文 LaTeX 编译入口与脚本
│   ├── bibliography.bib, *.bst   # 中文参考文献库
│   ├── sections/                 # 9 个中文章节源码
│   ├── tables/                   # 中文附表 S1–S10 源码
│   └── figures/                  # 8 张中文排版矢量图与位图
│
└── experiment/                   # 实验与数据复现工程（开箱即用，已剔除运行日志）
    ├── code/                     # 全套核心清洗、分析、反演与制图脚本
    │   ├── run_all.sh            # 一键重跑全流程脚本
    │   ├── cc_common.py          # 公共基础类与数据接口
    │   ├── fig_style.py          # Dark2 调色与绘图门禁规范
    │   ├── s01_data_panel.py ~ s10_polish.py # s01–s10 阶段分析脚本
    │   ├── make_fig*.py          # 图表生成脚本
    │   └── make_tables*.py       # 附表自动化提取脚本
    ├── data/                     # 数据资产
    │   ├── DATA_MANIFEST.md      # 数据来源与哈希指纹清册
    │   ├── national_flu.csv      # 全美流感参考序列
    │   ├── panel_nhsn_vintage_2026-10-20.csv.gz # 清洗后 10,506 州周分析面板
    │   └── external/             # CDC NHSN 原始数据快照与 Delphi 实验室数据
    └── analysis/                 # 核心计算与两步反演结果库
        ├── results.json          # 权威单一数据源（包含 549 项经核查的计算结果）
        ├── results_summary.md    # 结果摘要
        ├── data_decision.md      # 分析窗口规则及决策记录
        └── parts/                # 14 个模块局部分析输出与反演抽样分布文件
```

---

## 🛠️ 编译与复现指南

### 1. 论文编译 (LaTeX)

论文采用标准 `pdflatex` / `xelatex` 编译环境，支持作者-年份文献索引与跨章节交叉引用。

```bash
# 编译英文版
cd paper_en
bash compile.sh
# 或直接调用: pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex

# 编译中文版
cd paper_zh
bash compile.sh
```

### 2. 实验与图表一键复现 (Python)

环境要求：`Python >= 3.10`, 安装依赖 `pip install numpy scipy pandas matplotlib statsmodels`。

```bash
cd experiment/code
bash run_all.sh
```

该脚本将依次执行：
- 数据面板提取与质量审计 (`s01_data_panel.py`)
- 双向聚类推断与模型拟合 (`s02_inference.py`)
- 时空多尺度方差解耦 (`s03_decomposition.py`)
- 法定与自愿填报制度分析 (`s04_reporting.py`)
- 两步动力学仿真反演与校准 (`s08` ~ `s10`)
- 自动重绘正文全部 6 张高清图表及提取附表 S1–S10
