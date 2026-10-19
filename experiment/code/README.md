# 复现包:病例数瓶颈(case-count-bottleneck)实证与仿真代码

本目录是论文第 4 章(实证)与附录仿真的全部分析代码。所有数字写入 `../analysis/` 下的结果 JSON,
论文中每个数字对应的键见 `../analysis/reproduction_map.md`(机器可读版 `reproduction_map.json`)。

## 1. 环境

| 组件 | 版本 |
|---|---|
| Python | 3.11.2 |
| numpy | 2.4.6 |
| scipy | 1.17.1 |
| pandas | 3.0.6 |
| matplotlib | 3.11.2 |

只用标准库与上述四个包;不调用任何外部 API(独立数据脚本 `r4_i_independent.py` 除外,它从公开接口下载数据,
已下载的文件存在时不再访问网络)。硬件参考:4 核 CPU、8 GiB 内存,无 GPU。

## 2. 数据

| 数据 | 来源 | 本地文件 | sha256 |
|---|---|---|---|
| NHSN 州级每周住院(主数据) | data.cdc.gov“Weekly Hospital Respiratory Data (HRD) Metrics by Jurisdiction” https://data.cdc.gov/Public-Health-Surveillance/Weekly-Hospital-Respiratory-Data-HRD-Metrics-by-Ju/ua7e-t2fy | `Weekly_Hospital_Respiratory_Data_Metrics_by_Jurisdiction.csv`(24,187,778 字节,用户仓库自带的论文快照,本包未重新下载) | `e48c2ea92e0beb552a6510b7b0c2fe7a7c9ea911cd27880169298c34de20c330` |
| ILINet 州级门诊 ILI(方向对照) | https://api.delphi.cmu.edu/epidata/fluview/?regions=<州>&epiweeks=202235-202530 | `../data/external/ilinet_fluview_states_202235_202530.json` | `23af97c412b8a31209ff93d9c7a96fbabd329861f6ddf396569783ff85646ebf` |
| FluSurv-NET 站点住院率 | https://api.delphi.cmu.edu/epidata/flusurv/?locations=<14 站点>&epiweeks=202235-202530 | `../data/external/flusurv_sites_202235_202530.json` | `bf1168d3b2ee6423b070d48f8a4034a03ee9485fa10ce6e0b015decf0888f5cd` |
| HHS Protect 医院日报(一致性核对) | https://healthdata.gov/resource/g62h-syeh.json | `../data/external/hhs_protect_g62h_syeh_flu_2022_2023.json` | `ad56af3f891d6cbbac33183c3e7ef3d648ae435839a7e87371396c6127a2ccaf` |

NHSN 数据集持续回填修订,今天重新下载得到的文件与上表 sha256 不同,数字会有小幅出入;
逐值复现请使用论文快照。数据处理口径与派生文件见 `../analysis/data_contract.md`。

路径通过三个环境变量指定(均有默认值,指向本仓库内的只读用户仓库副本):

| 变量 | 含义 | 默认 |
|---|---|---|
| `REPO_ROOT` | 仓库根目录 | 本文件上溯四级 |
| `USER_REPO` | 用户仓库 `code_and_data/` 目录(提供 CSV 与 `data/empirical_stats.json`) | `$REPO_ROOT/.work/case-count-bottleneck/sources/user-repo/code_and_data` |
| `NHSN_CSV` | NHSN 原始 CSV | `$USER_REPO/data/raw/Weekly_Hospital_Respiratory_Data_Metrics_by_Jurisdiction.csv` |

结果写到代码所在目录的上一级(`../analysis/`、`../data/`、`../logs/`),因此把 `code/` 复制到任意空目录即可独立重跑,
不会覆盖原结果。

## 3. 种子

主种子 `SEED = 20261017`(`common.py`)。各分析的种子偏移:

| 分析 | 种子 |
|---|---|
| 首轮州聚类重抽(`b_bootstrap.py`) | SEED |
| r3 跨病原(`r3_c_pathogens.py`)与其抽样重放(`r4_c_boot.py`) | SEED+5 |
| r4 A 日更新零假设(`r4_a_growth_null.py`) | SEED+41(每格 `SeedSequence([SEED+41, 格号])`) |
| r4 B M-mult 增长期(同一脚本) | SEED+42 |
| r4 J τ 网格(`r4_j_tau_grid.py`) | SEED+43 |
| r4 K 一周两代(`r4_k_two_gen.py`) | SEED+44 |
| r4 I 独立数据(`r4_i_independent.py`) | SEED+45 |

每格的随机数流只由种子与格号决定,与进程数、完成顺序无关。

## 4. 运行顺序与耗时

一键运行:`bash run_all.sh [阶段]`(阶段 `base`、`r3`、`r4`、`map`、`all`,默认 `all`)。按依赖顺序逐条列出:

| 序 | 命令(在 `code/` 下) | 产出键 | 依赖 | 参考耗时 |
|---|---|---|---|---|
| 1 | `python3 a_reproduce.py` | `reanalysis_results.json` 的 `A_reproduction`、`F_spot_checks`;`../data/panel_*.csv.gz` | NHSN CSV | 1 s |
| 2 | `python3 b_bootstrap.py 2000 1000` | `B_bootstrap`、`B_bootstrap_sensitivity_state_season` | 1 | 12 s |
| 3 | `python3 c_competing.py` | `C_competing_fits` | 1 | 17 s |
| 4 | `python3 d_policy_season.py 2000 500` | `D_policy_season`、`D_quantile_regression` | 1 | 323 s |
| 5 | `python3 e_ar1_sim.py 200` | `E_ar1_simulation` | 1 | 159 s |
| 6 | `python3 r3_a_reporting.py 2000` | `r3_results.json` 的 `R0_reproduction_gate`、`R1_reporting_proxy_variance`、`R2_adjusted_estimator`、`R3_intercept_ratio_signature` | CSV | 20 s |
| 7 | `python3 r3_a2_period_vpi.py 2000` | `R1b_period_Vpi_ci` | 6 | 1 s |
| 8 | `python3 r3_b_scale_periods.py 2000` | `R4_vR_scale_periods` | CSV | 138 s |
| 9 | `python3 r3_c_pathogens.py 2000` | `R5_cross_pathogen` | CSV | 125 s |
| 10 | `python3 r4_c_boot.py` | `r4_results.json` 的 `C0_r3c_rerun_check`;`../analysis/r4_boot_draws.npz` | 9 | 129 s |
| 11 | `python3 r4_a_growth_null.py 300 4` | `A_calibration`、`A_growth_null`、`B_mmult_growth` | 9 | 约 45–60 min(4 进程) |
| 12 | `python3 r4_c_classify_tost.py all` | `D_tost_reporting_contribution`、`C_classification` | 10、11 | 1 min |
| 12b | `python3 r4_c_posthoc.py` | `C_posthoc`(事后敏感性,非预注册) | 11、12 | 1 s |
| 13 | `python3 r4_e_seasons.py` | `E_season_random_effects` | 8 | 1 s |
| 14 | `python3 r4_f_fig09.py` | `F_fig09_b2000` | 2 | 1 s |
| 15 | `python3 r4_g_table2.py` | `G_table2`;`../tables/tab_02_lag_ratios_r4.tex` | 2、11 | 1 s |
| 16 | `python3 r4_i_independent.py 2000` | `I_independent_data` | 网络或 `../data/external/` | 约 2 min |
| 17 | `python3 r4_j_tau_grid.py 200 200 2` | `J_tau_grid_dA_criterion` | 9、11 | 约 15 min(2 进程) |
| 18 | `python3 r4_k_two_gen.py 300 1` | `K_two_generations_per_week` | 9、11 | 319 s |
| 19 | `python3 r4_h_reproduction_map.py` | `../analysis/reproduction_map.{json,md}` | 全部 + 论文源 | 5 s |
| 20 | `python3 ../figures/make_fig_r4.py 09 12 13` | `../figures/r4_*.{pdf,png}` | 2、9、11、12、13 | 10 s |

耗时取自 `../logs/` 中本次运行的日志。步骤 19 需要论文 LaTeX 源(`../../paper/sections/`),独立重跑时可跳过。

## 5. 复现核对

`../r4_repro_check/` 是一次干净重跑:只复制本目录,按本 README 第 4 节命令重跑步骤 1、2、9–12、15,
重新生成表 2 与图 12 的全部数据(重跑脚本 `../r4_repro_check/run_check.sh`),再用 `python3 r4_h_repro_compare.py`
与原结果逐值比较(容差 1e-9,计时字段不比)。比较结果在 `r4_results.json` 的 `H_repro_check` 键。

## 6. 文件说明

- `common.py`、`r3_common.py`、`r4_common.py`:读数、面板构造、迭代 FGLS、州聚类重抽 + BCa、结果增量写入。
- `r4_sim_core.py`:日分辨率更新过程仿真(Poisson-Gamma 传播、二项报告、入院延迟、周汇总)。
- `a_*`–`e_*`:首轮重分析;`r3_*`:第三轮;`r4_*`:第四轮(零假设仿真与复现包)。
- 预注册:`../analysis/r3_preregistration.md`、`../analysis/r4_preregistration.md`。
- 用户仓库(`sources/user-repo/`)只读,本包不执行其中任何代码;图 7、8、14、16 由用户仓库脚本生成,未在此重跑。
