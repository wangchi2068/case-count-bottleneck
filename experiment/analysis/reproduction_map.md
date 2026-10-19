# 数字地图(reproduction map)

本表把论文 LaTeX 源(r3 定稿,r4 修订前)中的数字、表、图映射到结果 JSON 的键。机器可读全集见同目录
`reproduction_map.json`(每个数含文件、行号、上下文、命中键与命中数)。生成命令:
`python3 code/r4_h_reproduction_map.py`(在 `.work/case-count-bottleneck/experiment/` 下运行)。

## 1. 来源

| 代号 | 文件 | 说明 |
|---|---|---|
| T | `experiment/analysis/r3_results.json` | r3 实证 |
| V | `derivation/r3/verify_r3.json` | r3 推导核验 |
| R | `experiment/analysis/reanalysis_results.json` | 首轮重分析 |
| V4 | `derivation/r4/verify_r4_claims.json` | r4 推导核验 |
| D0 | `derivation/verify_results.json` | 首轮推导核验 |
| U | `sources/user-repo/code_and_data/results/sim_theory.json` | 用户仓库理论仿真(只读) |
| UE | `sources/user-repo/code_and_data/data/empirical_stats.json` | 用户仓库实证统计(只读) |
| F | `experiment/analysis/r4_results.json` | r4 新算 |

## 2. 覆盖情况

共抽取 1638 个数字。已映射 1550 个,年份 35 个,未匹配 36 个,参数设定 17 个。
已映射数字按来源:R 104 个,T 1246 个,D0 45 个,V 63 个,U 15 个,UE 68 个,F 1 个,V4 8 个。
“中”置信度表示同一显示值在 JSON 中出现多处,地图取优先来源的第一个命中,人工核对时以上下文为准。

## 3. 图表

| 图表 | 文件标识 | 生成脚本 | 数据键 | r4 状态 |
|---|---|---|---|---|
| 表 1 | `tab:shape` | paper/tables/make_tables.py | `R:C_competing_fits.original` | 沿用 |
| 表 2 | `tab:ratios` | paper/tables/make_tables.py(r4 改版草稿见 experiment/tables/tab_02_lag_ratios_r4.tex) | `R:B_bootstrap`; `R:E_ar1_simulation`; `V:A_ratio_signature`; `F:G_table2`; `F:A_growth_null.bands.flu|W-cal`; `F:B_mmult_growth.bands.flu|W-cal` | r4 改版:增长期列换成三种零假设带 |
| 图 1 | `fig_01_model_schematic` | image-2 示意图(无数据) |  | 沿用 |
| 图 2 | `fig_02_variance_theory` | paper/figures/make_fig_02_variance_theory.py | `U:variance_mc` | 沿用 |
| 图 3 | `fig_03_growth_test` | paper/figures/make_fig_03_growth_test.py | `U:growth_test` | 沿用 |
| 图 4 | `fig_04_vR_precision` | paper/figures/make_figs_theory_design.py | `V:(闭式曲线)` | 沿用 |
| 图 5 | `fig_05_levers_budget` | paper/figures/make_figs_theory_design.py | `V:(闭式曲线)` | 沿用 |
| 图 6 | `fig_06_renewal_scale` | paper/figures/make_fig_06_renewal_scale.py | `U:renewal` | 沿用 |
| 图 7 | `fig_07_nhsn_series` | 用户仓库 code/make_figures.py(只读,未执行) | `UE:(序列)` | 沿用 |
| 图 8 | `fig_08_early_scale` | 用户仓库 code/make_figures.py(只读,未执行) | `UE:(分箱)`; `R:A_reproduce` | 沿用 |
| 图 9 | `fig_09_denominator_noise` | experiment/figures/make_fig_r4.py 09 | `R:B_bootstrap.stats.b_*.pct95`; `R:B_bootstrap.stats.a_*.pct95`; `F:F_fig09_b2000` | r4 重画:2,000 次重抽 |
| 图 10 | `fig_10_bootstrap_ratios` | paper/figures/make_fig_10_bootstrap_ratios.py | `R:B_bootstrap` | 沿用 |
| 图 11 | `fig_11_reporting_adjustment` | paper/figures/make_figs_empirical_design.py | `T:R1_reporting_proxy_variance`; `T:R2_adjusted_estimator` | 沿用 |
| 图 12 | `fig_12_cross_pathogen` | experiment/figures/make_fig_r4.py 12 | `T:R5_cross_pathogen`; `F:A_growth_null.bands`; `F:B_mmult_growth.bands`; `F:C_classification` | r4 重画:三种零假设带 + 新分级 |
| 图 13 | `fig_13_scale_vs_seasons` | experiment/figures/make_fig_r4.py 13 | `T:R4_vR_scale_periods.4c_scale_vs_periods`; `F:E_season_random_effects` | r4 重画:加第 4 季与 S=3/4 下界 |
| 图 14 | `fig_14_peak_decomp` | 用户仓库 code/make_figures.py(只读,未执行) | `UE:(达峰期)` | 沿用 |
| 图 15 | `fig_15_period_season_iqr` | paper/figures/make_fig_15_period_season_iqr.py | `R:D_policy_season` | 沿用 |
| 图 16 | `fig_16_mx_forest` | 用户仓库 code/make_figures.py(只读,未执行) | `UE:(各规格 b/a)`; `R:C_competing_fits` | 沿用 |

## 4. 未在结果 JSON 中找到的数字

下列数字在八个来源中都没有按显示精度命中。多数来自理论部分的闭式计算(由推导脚本当场算出、未落盘)
或首轮重分析中只写进报告的派生量,修订步若保留这些数字,应在对应脚本中补写 JSON 键。

| 文件 | 行 | 数 | 上下文 |
|---|---|---|---|
| methods.tex | 165 | 468 | 个州周，其中 504 个州周的住院数缺失并按 0 处理，【468】 个在第一期，36 个在第二期。规模用此 |
| results.tex | 58 | 0.313 | 0.038 倍，phi=0.5 时为 0.516、【0.313】、0.109 倍，phi=0.8 |
| results.tex | 58 | 0.605 | 0.109 倍，phi=0.8 时为 0.774、【0.605】、0.287 倍。这些结果把 v_R |
| results.tex | 142 | 699 | delta=0.3 为例，n 从 400 增加到 【699】 的过程中功效下降了 82 次。规模要求 |
| results.tex | 213 | 178.6 | >17.9 处反转，nu=1000 时在 m>【178.6】 处反转。制度型波动下，图示参数与  |
| results.tex | 261 | 0.505 | .8，随规模单调上升并趋近上界。相对标准误的下界为 (【0.505】T)^{-1/2}，T=3、10、 |
| results.tex | 261 | 144 | }、phiin{0,0.5,0.8} 共 【144】 个格点（图~ ）。m=10^4 时 |
| results.tex | 293 | 22.5 | 、phi=psi=0.5 为基线，均方误差为 【22.5】 ^{-3}，其中环境项 10.40、 |
| results.tex | 293 | 10.40 | 基线，均方误差为 22.5 ^{-3}，其中环境项 【10.40】、报告项 7.85、抽样项 4.29（单 |
| results.tex | 293 | 7.85 | 22.5 ^{-3}，其中环境项 10.40、报告项 【7.85】、抽样项 4.29（单位 10^{-3 |
| results.tex | 338 | 60,000 | T=40。堆叠柱为式~  的三类项，空心点为每种设置 【60,000】 次模拟及其   倍标准误。(b) |
| results.tex | 371 | 0.161 | 0.244--0.415），[20,50) 箱降到 【0.161】，[100,250) 箱为 0.11 |
| results.tex | 371 | 100,250 | .415），[20,50) 箱降到 0.161，[【100,250】) 箱为 0.112，此后两箱为 0. |
| results.tex | 390 | 0.0056 | ，kin[0.2,0.5] ，rhoin[【0.0056】,0.021] ，v_Rin[0. |
| results.tex | 395 | 1.566 | 55、1.660、0.993，情景模拟值为 1.195、【1.566】、0.999。 |
| results.tex | 399 | 2.019 | 一个可能来源，情景模拟中加入这类离散后，模拟斜率可升到 【2.019】；现有数据无法区分这一来源与其他解释，斜 |
| results.tex | 403 | 59.2 | 0214，几乎不变，分母噪声因而把 b/a 推高到 【59.2】，而真实的 A/v_R 只有 30. |
| results.tex | 403 | 30.7 | a 推高到 59.2，而真实的 A/v_R 只有 【30.7】，用 b/a 估计 mx 会系 |
| results.tex | 472 | 59.5 | 波动两部分。偏差项占总损失的 88.9%，从最小箱的 【59.5】% 升到最大箱的 94.8%。除最小 |
| results.tex | 488 | 0.529 | a）。按流行季分层后，季外三期的四分位距为 0.524、【0.529】（0.438--0.611）和 0.44 |
| results.tex | 488 | 0.438 | 季分层后，季外三期的四分位距为 0.524、0.529（【0.438】--0.611）和 0.448，第二期减 |
| results.tex | 488 | 0.611 | 三期的四分位距为 0.524、0.529（0.438--【0.611】）和 0.448，第二期减第一期为 0. |
| results.tex | 488 | 0.821 | 10（0.667--0.749），第三期为 0.864（【0.821】--0.906），第二期为 1.818（ |
| results.tex | 488 | 0.906 | 7--0.749），第三期为 0.864（0.821--【0.906】），第二期为 1.818（1.004-- |
| results.tex | 488 | 2.144 | 1--0.906），第二期为 1.818（1.004--【2.144】），第二期减第一期为 1.107（0.2 |
| results.tex | 488 | 1.446 | 的季内占比重新加权，第二期为 1.013（0.716--【1.446】），比第一期的 0.630 高 0.38 |
| results.tex | 488 | 0.788 | 长率的四分位距给出同样的格局，季内第二期为 1.688（【0.788】--2.455）。 |
| results.tex | 488 | 2.455 | 给出同样的格局，季内第二期为 1.688（0.788--【2.455】）。 |
| results.tex | 497 | -0.106 | ~ b）。5--9 月第二期减第一期为 0.004（-【-0.106】--0.093）；10 月为 0.98 |
| results.tex | 497 | 0.432 | 一期与第三期 10 月的四分位距分别为 0.829 与 【0.432】。以对数增长率偏离当月中位数的绝对值为因 |
| results.tex | 497 | 0.924 | 后，第二期季内剩 54 个州周，四分位距为 1.729（【0.924】--2.141），与第一期之差为 1.0 |
| results.tex | 497 | 1.434 | 2.141），与第一期之差为 1.022（0.229--【1.434】）。 |
| results.tex | 515 | 22.5 | 7。三种口径下所有重抽的 b 都为正，经验比值在 【22.5】--42.7 之间，截距在总损失中的份额 |
| results.tex | 515 | 42.7 | 径下所有重抽的 b 都为正，经验比值在 22.5--【42.7】 之间，截距在总损失中的份额为 39% |
| discussion.tex | 6 | 0.279 | =0.0825；先验中心偏离 Rbar 不超过 【0.279】 时，最优收缩的均方误差就低于 v_R |
| appendix.tex | 189 | -6 | 令 z(x)=(6+4x+x^2)e^{-x}-【-6】+2x，z(0)=0，z'(x) |

## 5. r4 新增数字的键

r4 新算的数字(零假设带、重新分级、TOST、季随机效应、独立数据、τ 网格、一周两代)全部在
`experiment/analysis/r4_results.json`,键名与 r4-report.md 各节一一对应:
`A_growth_null`、`B_mmult_growth`、`C_classification`、`D_tost_reporting_contribution`、
`E_season_random_effects`、`F_fig09_b2000`、`G_table2`、`I_independent_data`、`J_tau_grid_dA_criterion`、
`K_two_generations_per_week`;复现核对见 `H_repro_check`。
