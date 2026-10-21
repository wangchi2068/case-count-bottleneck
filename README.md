# 最终交付成果物归档（Final Deliverables）

本项目包含流行病学再生数估计误差下限与监测设计论文的三轮同行评审、理论反演、补充实证及最终中英文成稿全套工程资产。

已彻底过滤中间冗余日志与模拟临时断点文件（体积从原始 48MB 精炼压缩至 26MB，文件由 507 个净化为 131 个），所有文件均为干净、有效、开箱即用的交付资产。

---

## 📂 目录架构与资产索引

```text
final/
├── 01_Final_Reports/             # 最终结项总结报告（含多格式与对应图件）
│   ├── final-report.pdf          # 结项总结报告 PDF
│   ├── final-report.html         # 结项总结报告自包含 HTML
│   ├── final-report.docx         # 结项总结报告 Word 文档
│   ├── final-report.md           # 结项总结报告 Markdown 原文
│   └── figures/                  # 结项报告引用的 3 张高清图表
│
├── 02_Manuscripts/               # 中英文论文成稿与完整编译工程
│   ├── en/                       # 英文定稿（目标期刊：Epidemics）
│   │   ├── paper.pdf             # 24 页英文排版定稿 PDF（8.5分小修通过）
│   │   ├── paper.html            # 自包含 HTML 版本（免阅读器即开即览）
│   │   ├── main.tex, compile.sh  # LaTeX 编译入口与一键编译脚本
│   │   ├── bibliography.bib      # 44 条全引用参考文献库
│   │   ├── plainnat-nodoi.bst    # 期刊定制样式表
│   │   ├── sections/             # 9 个正文章节 LaTeX 源码（含附录全套定理证明）
│   │   ├── tables/               # 附表 S1–S10 源码 (tab_s1 ~ tab_s10) 与指纹清单
│   │   └── figures/              # 8 张论文插图（6 张矢量图 + 2 张位图）
│   └── zh/                       # 中文定稿（与英文版内容及数字 100% 对齐）
│       ├── paper.pdf             # 24 页中文排版定稿 PDF
│       ├── paper.html            # 中文自包含 HTML
│       ├── main.tex, compile.sh  # 中文编译入口与脚本
│       ├── bibliography.bib      # 中文参考文献库
│       ├── sections/             # 9 个中文章节源码
│       ├── tables/               # 中文附表 S1–S10 源码
│       └── figures/              # 8 张全中文标注排版图件
│
├── 03_Peer_Reviews/              # 三轮独立同行评审双语报告
│   ├── review_original.md        # 第一轮评审：用户 GitHub 现稿（大修，4/10分）
│   ├── review_revised.md         # 第二轮评审：重构新稿（大修，6/10分）
│   └── review_round3.md          # 第三轮评审与终修核查：终修定稿（小修，8.5/10分）
│
└── 04_Reproduction_Package/      # 实验与数据复现包（已净化）
    ├── code/                     # 全套核心清洗、分析、两步反演与出图脚本
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
    └── analysis/                 # 核心计算与反演结果库
        ├── results.json          # 权威单一数据源（包含 549 项经核查的计算结果）
        ├── results_summary.md    # 结果摘要
        ├── data_decision.md      # 分析窗口规则及决策记录
        ├── vintage_r4_results.json # 零模型基准结果
        └── parts/                # 14 个模块局部分析输出与反演抽样分布文件
```

---

## 🔍 核心成果速览

1. **论文题眼更新**：
   - 英文标题：*Scaling limits and surveillance design for epidemic reproduction numbers under environmental and reporting stochasticity*
   - 中文标题：《环境随机性与报告异质性下疫情再生数监测的尺度极限与资源配置设计》
2. **两步仿真反演核心发现**：
   - 更新型比值 $R_A$ 反演潜伏环境方差 $v_R = 0.040$ [0.026, 0.056]；
   - 加权增长比 $G$ 反演潜伏环境方差 $v_R = 0.043$ [0.025, 0.064]；
   - 两者比值 0.93，90% 置信区间 [0.81, 1.13] 落在 [0.80, 1.25] 国际通用等效区间内。
3. **尺度清晰解耦**：
   - 明确表观统计量尺度平衡点 $37.4$（约 55% 早期增长州周已达到此规模）；
   - 潜伏尺度平衡规模 $m_\times \approx 30.3$ 例/代（折合每周约 59 例住院）。
4. **评审最终成绩**：
   - 由最初的 4 分（大修）历经 6 分、7.5 分，最终达到 **8.5/10 分（小修，仅余编辑性细节）**。
