"""r4 G:新版表 2 数据。在 r3 表 2 的基础上,把 M-env“增长期”一列拆成每周一代(r3,φ=0,9 格)与日分辨率更新过程
(r4 A,φ=0,各病原世代间隔与入院延迟,全部格与无延迟格),并新增 M-mult 增长期列(r4 B)。

输入:analysis/reanalysis_results.json(B_bootstrap 实证区间)、r4_results.json(A_growth_null、B_mmult_growth)。
输出:r4_results.json 键 G_table2;LaTeX 草稿 tables/tab_02_lag_ratios_r4.tex(只供修订步参考,不进 output)。
"""
import json

from common import EXP
from r4_common import r4_load, r4_update

C = "flu|W-cal"
RE = json.loads((EXP / "analysis/reanalysis_results.json").read_text(encoding="utf-8"))["B_bootstrap"]["stats"]
R4 = r4_load()
A, B = R4["A_growth_null"], R4["B_mmult_growth"]
emp = {k: {"point": RE[k]["point"], "pct95": RE[k]["pct95"]} for k in ("r1", "r2", "q1", "q2", "a_original")}
# r3 表 2 已有列(数值来自 tab_02_lag_ratios.tex,出处见 reproduction_map)
OLD = {"M-env 平稳": {"r1": [1.419, 1.463], "r2": [0.852, 0.866], "q1": [1, 1], "q2": [1, 1]},
       "M-env 增长期(每周一代,r3)": {"r1": [1.450, 1.630], "r2": [0.693, 0.763], "q1": [0.857, 0.937], "q2": [1.226, 1.333]},
       "M-mult 平稳": {"r1": [1.462, 1.462], "r2": [0.852, 0.852], "q1": [0.883, 1.338], "q2": [0.892, 1.374]}}
bA = A["bands"][C]; bB = B["bands"][C]
NEW = {"M-env 增长期(日更新,无延迟)": {"q1": bA["A_no_delay"]["q1"], "q2": bA["A_no_delay"]["q2"], "n_cells": bA["A_no_delay"]["n_cells"]},
       "M-env 增长期(日更新,全部格)": {"q1": bA["A_all"]["q1"], "q2": bA["A_all"]["q2"], "n_cells": bA["A_all"]["n_cells"]},
       "M-mult 增长期": {"q1": bB["B_all"]["q1"], "q2": bB["B_all"]["q2"], "n_cells": bB["B_all"]["n_cells"]}}


def disjoint(band, iv):
    return band[1] < iv[0] or band[0] > iv[1]


cols = {**OLD, **NEW}
flags = {c: {q: disjoint(v[q], emp[q]["pct95"]) for q in ("r1", "r2", "q1", "q2") if q in v} for c, v in cols.items()}
out = {"combo": C, "empirical": emp, "columns": cols, "disjoint_from_empirical_pct95": flags,
       "complete": bool(A.get("complete") and B.get("complete")),
       "note": "日更新列只算截距比(仿真只存 a 的三权重值);斜率比沿用 r3 列。范围 = 格点均值的 [最小, 最大]。"}
r4_update("G_table2", out)


def f(v):
    return f"{v[0]:.3f}" if abs(v[1] - v[0]) < 1e-9 else f"{v[0]:.3f}--{v[1]:.3f}"


def cell(c, q):
    v = cols[c].get(q)
    if v is None:
        return "--"
    s = "1" if v == [1, 1] else f(v)
    return f"\\textbf{{{s}}}" if flags[c].get(q) else s


order = ["M-env 平稳", "M-env 增长期(每周一代,r3)", "M-env 增长期(日更新,无延迟)", "M-env 增长期(日更新,全部格)",
         "M-mult 平稳", "M-mult 增长期"]
lab = {"r1": "$r_1$", "r2": "$r_2$", "q1": "$q_1$", "q2": "$q_2$"}
rows = []
for q in ("r1", "r2", "q1", "q2"):
    e = emp[q]
    rows.append(f"    {lab[q]} & {e['point']:.3f}（{e['pct95'][0]:.3f}--{e['pct95'][1]:.3f}） & " + " & ".join(cell(c, q) for c in order) + r" \\")
ea = emp["a_original"]
rows.append(f"    $a$ & {ea['point']:.4f}（{ea['pct95'][0]:.4f}--{ea['pct95'][1]:.4f}） & " + " & ".join(["$>0$"] * len(order)) + r" \\")
tex = r"""% r4 草稿:表 2 新版(M-bin0、M-meas、M-nodn 三列不变,修订时并入;此处只列变化的列)
\begin{tabular}{@{}lccccccc@{}}
  \toprule
  & & \multicolumn{4}{c}{M-env} & \multicolumn{2}{c}{M-mult} \\
  \cmidrule(lr){3-6}\cmidrule(lr){7-8}
  量 & 实证（95\% 区间） & 平稳 & 增长期 每周一代 & 增长期 日更新 无延迟 & 增长期 日更新 全部 & 平稳 & 增长期 \\
  \midrule
""" + "\n".join(rows) + "\n  \\bottomrule\n\\end{tabular}\n"
(EXP / "tables").mkdir(exist_ok=True)
(EXP / "tables/tab_02_lag_ratios_r4.tex").write_text(tex, encoding="utf-8")
print(tex)
print(json.dumps(flags, ensure_ascii=False))
