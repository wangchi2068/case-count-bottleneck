# 数据契约(empirical-rerun,2026-10-17)

## 来源

- 原始数据:用户论文源仓库自带的 NHSN 周报文件 `code_and_data/data/raw/Weekly_Hospital_Respiratory_Data_Metrics_by_Jurisdiction.csv`。该文件位于本任务的只读浅克隆中,由用户提供,本步没有重新下载。
  - 大小 24,187,778 字节;SHA-256 `e48c2ea92e0beb552a6510b7b0c2fe7a7c9ea911cd27880169298c34de20c330`。
  - 读入列:`Week Ending Date`、`Geographic aggregation`、`Total Influenza Admissions`、`Percent Hospitals Reporting Influenza Admissions`。
  - 保留 50 州与哥伦比亚特区,共 51 个辖区。周末日期为 2020-08-08 至 2026-09-05,共 16,218 个州周,其中 504 个住院数缺失。
- 对照文件(只读,只用来比对数字,不作为输入):`data/derived/national_weekly.csv`、`nhsn_bins.json`、`data/empirical_stats.json`、`results/sim_theory.json`。
- 用户仓库里的任何脚本都没有执行。所有计算由本目录 `code/` 下的自写脚本完成。

## 处理口径

- 缺失的住院数按 0 计入,与 empirical_stats.json 一致。分析 D 另做了剔除缺失行的敏感性分析。
- 规模 $D_t=0.65C_t+0.25C_{t-1}+0.10C_{t-2}$,只保留 $D_t\ge5$。增长统计量 $G_t=C_{t+1}/D_t$。
- 流行初期窗口、制度分期(第一期至 2024-04-30,第二期 2024-05-01 至 10-31,第三期自 2024-11-01 起)与流行季(10–3 月)都照抄 empirical_stats.json 的定义,详见 `code/common.py`。

## 派生文件(`data/`,合计约 0.5 MB)

| 文件 | 内容 | 生成脚本 |
|---|---|---|
| `panel_original.csv.gz` | 主规格州周面板,含州、周、$C_t$、$D_t$、$G_t$、分期、季节、缺失标记、Cori 分母 | `a_reproduce.py` |
| `early_single_1w.csv.gz`、`early_equal_3w.csv.gz` | 单周权重和三周等权两种规格的流行初期样本 | `a_reproduce.py` |
| `bootstrap_state_stats.npz` | 州聚类 Bootstrap 的统计量矩阵($B=2000$)、点估计与留一州刀切值 | `b_bootstrap.py` |

不发布原始 CSV 的副本。重跑时从用户仓库的原路径读取。

## 复用边界

- NHSN 数据是美国疾控中心发布的公开数据,本步只把它用于本论文的再分析。
- 派生面板只覆盖本文用到的 4 列,不能替代原始数据集。
- 结果文件 `reanalysis_results.json` 的 `provenance.mode` 为 `measured`。所有数字都来自真实数据或明确标注的蒙特卡洛仿真(分析 E),没有任何人工设定的数值。

## 外部独立数据(empirical-r4,2026-10-18)

下列文件由 `code/r4_i_independent.py` 从公开接口下载,放在 `data/external/`。每个 URL 最多请求 2 次,本步全部一次成功(HTTP 200),请求记录见 `r4_results.json` 键 `I_independent_data.fetch_log` 与 `data/external/ilinet_fetch_log.json`。

| 文件 | 来源 | 内容与用途 | SHA-256 |
|---|---|---|---|
| `ilinet_fluview_states_202235_202530.json` | Delphi Epidata `fluview`(CDC ILINet 州级),2022 年第 35 周至 2025 年第 30 周 | 7,752 条州周记录、51 个辖区;字段 `num_ili`(门诊流感样病例数)。按主分析同一截距比管线重跑,只看 $q_1<1<q_2$ 的方向 | `23af97c412b8a31209ff93d9c7a96fbabd329861f6ddf396569783ff85646ebf` |
| `flusurv_sites_202235_202530.json` | Delphi Epidata `flusurv`(FluSurv-NET 14 个站点) | 1,568 条记录;只有每 10 万人住院率,不是计数,只报 $q_1$、$q_2$ | `bf1168d3b2ee6423b070d48f8a4034a03ee9485fa10ce6e0b015decf0888f5cd` |
| `hhs_protect_g62h_syeh_flu_2022_2023.json` | healthdata.gov 数据集 `g62h-syeh`(HHS Protect 医院日报),2022-09-25 至 2023-12-30 | 字段 `previous_day_admission_influenza_confirmed`,前移一天后按周六结束的周汇总,与 NHSN 流感入院做一致性核对,不另作估计 | `ad56af3f891d6cbbac33183c3e7ef3d648ae435839a7e87371396c6127a2ccaf` |

- 三个来源都是美国政府或学术机构公开发布的数据,只用于本论文的方向对照与一致性核对,不并入主估计。
- ILINet 的就诊数受哨点数量与就诊总量变化影响;FluSurv-NET 的率已四舍五入,站点只有 14 个,聚类重抽单元少。两者的限制写在结果键的 `caveat` 字段。
- 上游接口会回填修订,重新下载的文件与上表 SHA-256 可能不同。复现时文件存在则脚本不再访问网络。
