"""r4 H:数字地图。把论文(当前 r3 版 LaTeX 源)里的每个数、每张表、每张图映射到结果 JSON 的键。

做法:逐节抽取正文数字(去掉 label/ref/cite/文件名),按显示位数的半个末位作容差,在结果 JSON 中查找;
来源优先级 T > V > R > V4 > D0 > U > UE > F(F 为 r4 新算,只在前述来源都查不到时使用,U 为用户仓库自带结果,只读、本仓未重跑)。
图表的生成脚本与数据键为人工登记(FIGTAB)。输出 analysis/reproduction_map.json 与 reproduction_map.md。
用法:python3 r4_h_reproduction_map.py
"""
import json
import math
import re
from pathlib import Path

from common import EXP

W = EXP.parent
SECTIONS = ["abstract", "highlights", "introduction", "methods", "results", "discussion", "appendix"]
SRC = {
    "T": ("experiment/analysis/r3_results.json", "r3 实证"),
    "V": ("derivation/r3/verify_r3.json", "r3 推导核验"),
    "R": ("experiment/analysis/reanalysis_results.json", "首轮重分析"),
    "V4": ("derivation/r4/verify_r4_claims.json", "r4 推导核验"),
    "D0": ("derivation/verify_results.json", "首轮推导核验"),
    "U": ("sources/user-repo/code_and_data/results/sim_theory.json", "用户仓库理论仿真(只读)"),
    "UE": ("sources/user-repo/code_and_data/data/empirical_stats.json", "用户仓库实证统计(只读)"),
    "F": ("experiment/analysis/r4_results.json", "r4 新算"),
}
SKIP_KEYS = ("cells", "fetch_log", "provenance", "seasons_draws")


def walk(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in SKIP_KEYS:
                continue
            yield from walk(v, f"{p}.{k}" if p else str(k))
    elif isinstance(o, list):
        if len(o) > 400:
            return
        for i, v in enumerate(o):
            yield from walk(v, f"{p}[{i}]")
    elif isinstance(o, (int, float)) and not isinstance(o, bool):
        if math.isfinite(float(o)):
            yield p, float(o)


FLAT = {}
for s, (rel, _) in SRC.items():
    f = W / rel
    FLAT[s] = list(walk(json.loads(f.read_text(encoding="utf-8")))) if f.exists() else []

STRIP = re.compile(r"\\(label|ref|eqref|cite|citep|citet|includegraphics|input|url|href)(\[[^\]]*\])?\{[^}]*\}")
NUM = re.compile(r"(?<![A-Za-z_\\.\d])\d+(?:,\d\d\d(?!\d))*(?:\.\d+)?")
SEC = re.compile(r"\\(section|subsection|subsubsection)\*?\{([^}]*)\}")
CAP = re.compile(r"\\caption\{")


def find(val, dec, pct):
    tol = 0.5 * 10 ** (-dec) + 1e-12
    cands = [val] + ([val / 100] if pct else []) + ([-val] if val > 0 else [])
    for s in SRC:
        hits = [(p, x) for p, x in FLAT[s] for c in cands if abs(x - c) <= tol * (0.01 if c != val else 1)
                or abs(x - c) <= tol and c == val]
        if not hits and pct:
            t2 = 0.5 * 10 ** (-(dec + 2)) + 1e-12
            hits = [(p, x) for p, x in FLAT[s] if abs(x - val / 100) <= t2]
        if hits:
            return s, hits
    return None, []


def classify_unmatched(val, dec, ctx):
    if dec == 0 and val in (51, 25, 26, 2000, 1500, 400, 20000, 300, 100, 10, 50, 7, 14, 3, 4, 5, 6, 8, 9, 12, 13, 2):
        return "设计常数/计数"
    if dec == 0 and 1990 <= val <= 2030:
        return "年份"
    if re.search(r"(=|取|为|设)\s*$", ctx[0][-6:]):
        return "参数设定"
    return "未匹配"


def numbers_in(sec):
    p = W / f"paper/sections/{sec}.tex"
    out = []
    cur = sec
    for ln, raw in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("%")[0] if not raw.lstrip().startswith("\\%") else raw
        line = re.sub(r"(?<!\\)%.*", "", raw)
        m = SEC.search(line)
        if m:
            cur = m.group(2)
        txt = STRIP.sub(" ", line)
        txt = re.sub(r"\\[a-zA-Z]+\d+", " ", txt)
        for m in NUM.finditer(txt):
            s = m.group(0)
            v = float(s.replace(",", ""))
            pre = txt[max(0, m.start() - 2):m.start()]
            if pre.endswith(("-", "−")) and not re.search(r"[-\dA-Za-z{]", pre[:-1] or " "):
                v, s = -v, "-" + s
            dec = len(s.split(".")[1]) if "." in s else 0
            if dec == 0 and abs(v) < 2:
                continue
            after = txt[m.end():m.end() + 3]
            pct = after.startswith("\\%") or after.startswith("%")
            before = txt[max(0, m.start() - 28):m.start()]
            out.append({"file": f"paper/sections/{sec}.tex", "line": ln, "section": cur, "text": s, "value": v,
                        "decimals": dec, "percent": pct, "context": (before + "【" + s + "】" + txt[m.end():m.end() + 20]).strip()})
    return out


FIGTAB = [
    ("表 1", "tab:shape", "paper/tables/make_tables.py", ["R:C_competing_fits.original"], "沿用"),
    ("表 2", "tab:ratios", "paper/tables/make_tables.py(r4 改版草稿见 experiment/tables/tab_02_lag_ratios_r4.tex)",
     ["R:B_bootstrap", "R:E_ar1_simulation", "V:A_ratio_signature", "F:G_table2", "F:A_growth_null.bands.flu|W-cal",
      "F:B_mmult_growth.bands.flu|W-cal"], "r4 改版:增长期列换成三种零假设带"),
    ("图 1", "fig_01_model_schematic", "image-2 示意图(无数据)", [], "沿用"),
    ("图 2", "fig_02_variance_theory", "paper/figures/make_fig_02_variance_theory.py", ["U:variance_mc"], "沿用"),
    ("图 3", "fig_03_growth_test", "paper/figures/make_fig_03_growth_test.py", ["U:growth_test"], "沿用"),
    ("图 4", "fig_04_vR_precision", "paper/figures/make_figs_theory_design.py", ["V:(闭式曲线)"], "沿用"),
    ("图 5", "fig_05_levers_budget", "paper/figures/make_figs_theory_design.py", ["V:(闭式曲线)"], "沿用"),
    ("图 6", "fig_06_renewal_scale", "paper/figures/make_fig_06_renewal_scale.py", ["U:renewal"], "沿用"),
    ("图 7", "fig_07_nhsn_series", "用户仓库 code/make_figures.py(只读,未执行)", ["UE:(序列)"], "沿用"),
    ("图 8", "fig_08_early_scale", "用户仓库 code/make_figures.py(只读,未执行)", ["UE:(分箱)", "R:A_reproduce"], "沿用"),
    ("图 9", "fig_09_denominator_noise", "experiment/figures/make_fig_r4.py 09",
     ["R:B_bootstrap.stats.b_*.pct95", "R:B_bootstrap.stats.a_*.pct95", "F:F_fig09_b2000"], "r4 重画:2,000 次重抽"),
    ("图 10", "fig_10_bootstrap_ratios", "paper/figures/make_fig_10_bootstrap_ratios.py", ["R:B_bootstrap"], "沿用"),
    ("图 11", "fig_11_reporting_adjustment", "paper/figures/make_figs_empirical_design.py",
     ["T:R1_reporting_proxy_variance", "T:R2_adjusted_estimator"], "沿用"),
    ("图 12", "fig_12_cross_pathogen", "experiment/figures/make_fig_r4.py 12",
     ["T:R5_cross_pathogen", "F:A_growth_null.bands", "F:B_mmult_growth.bands", "F:C_classification"],
     "r4 重画:三种零假设带 + 新分级"),
    ("图 13", "fig_13_scale_vs_seasons", "experiment/figures/make_fig_r4.py 13",
     ["T:R4_vR_scale_periods.4c_scale_vs_periods", "F:E_season_random_effects"], "r4 重画:加第 4 季与 S=3/4 下界"),
    ("图 14", "fig_14_peak_decomp", "用户仓库 code/make_figures.py(只读,未执行)", ["UE:(达峰期)"], "沿用"),
    ("图 15", "fig_15_period_season_iqr", "paper/figures/make_fig_15_period_season_iqr.py", ["R:D_policy_season"], "沿用"),
    ("图 16", "fig_16_mx_forest", "用户仓库 code/make_figures.py(只读,未执行)", ["UE:(各规格 b/a)", "R:C_competing_fits"], "沿用"),
]


def main():
    nums = [n for s in SECTIONS for n in numbers_in(s)]
    for n in nums:
        s, hits = find(n["value"], n["decimals"], n["percent"])
        if s:
            n["source"] = s
            n["key"] = f"{SRC[s][0]}#{hits[0][0]}"
            n["json_value"] = hits[0][1]
            n["n_hits"] = len(hits)
            n["status"] = "已映射"
            n["confidence"] = "高" if (n["decimals"] >= 3 or n["n_hits"] <= 2) else "中(多处同值,取优先来源)"
        else:
            n["status"] = classify_unmatched(n["value"], n["decimals"], (n["context"].split("【")[0], ""))
    stat = {}
    for n in nums:
        stat[n["status"]] = stat.get(n["status"], 0) + 1
    by_src = {}
    for n in nums:
        if n.get("source"):
            by_src[n["source"]] = by_src.get(n["source"], 0) + 1
    out = {"sources": {k: {"path": v[0], "desc": v[1]} for k, v in SRC.items()},
           "paper_version": "paper/sections/*.tex(r3 定稿,r4 修订前)",
           "method": "逐节抽数;容差 = 显示末位的一半;百分数同时按 /100 查;来源按优先级取第一个命中",
           "summary": {"n_numbers": len(nums), "by_status": stat, "mapped_by_source": by_src},
           "figures_tables": [{"label": a, "id": b, "generator": c, "data_keys": d, "r4_status": e} for a, b, c, d, e in FIGTAB],
           "numbers": nums}
    (EXP / "analysis/reproduction_map.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    write_md(out)
    print(json.dumps(out["summary"], ensure_ascii=False))
    return out


def write_md(out):
    L = ["# 数字地图(reproduction map)", "",
         "本表把论文 LaTeX 源(r3 定稿,r4 修订前)中的数字、表、图映射到结果 JSON 的键。机器可读全集见同目录",
         "`reproduction_map.json`(每个数含文件、行号、上下文、命中键与命中数)。生成命令:",
         "`python3 code/r4_h_reproduction_map.py`(在 `.work/case-count-bottleneck/experiment/` 下运行)。", "",
         "## 1. 来源", "", "| 代号 | 文件 | 说明 |", "|---|---|---|"]
    for k, v in out["sources"].items():
        L.append(f"| {k} | `{v['path']}` | {v['desc']} |")
    sm = out["summary"]
    L += ["", "## 2. 覆盖情况", "",
          f"共抽取 {sm['n_numbers']} 个数字。" + ",".join(f"{k} {v} 个" for k, v in sm["by_status"].items()) + "。",
          "已映射数字按来源:" + ",".join(f"{k} {v} 个" for k, v in sm["mapped_by_source"].items()) + "。",
          "“中”置信度表示同一显示值在 JSON 中出现多处,地图取优先来源的第一个命中,人工核对时以上下文为准。", "",
          "## 3. 图表", "", "| 图表 | 文件标识 | 生成脚本 | 数据键 | r4 状态 |", "|---|---|---|---|---|"]
    for f in out["figures_tables"]:
        L.append(f"| {f['label']} | `{f['id']}` | {f['generator']} | " + "; ".join(f"`{k}`" for k in f["data_keys"])
                 + f" | {f['r4_status']} |")
    L += ["", "## 4. 未在结果 JSON 中找到的数字", "",
          "下列数字在八个来源中都没有按显示精度命中。多数来自理论部分的闭式计算(由推导脚本当场算出、未落盘)",
          "或首轮重分析中只写进报告的派生量,修订步若保留这些数字,应在对应脚本中补写 JSON 键。", "",
          "| 文件 | 行 | 数 | 上下文 |", "|---|---|---|---|"]
    for n in out["numbers"]:
        if n["status"] == "未匹配":
            ctx = n["context"].replace("|", "/").replace("$", "").replace("\\", "")[:60]
            L.append(f"| {n['file'].split('/')[-1]} | {n['line']} | {n['text']} | {ctx} |")
    L += ["", "## 5. r4 新增数字的键", "",
          "r4 新算的数字(零假设带、重新分级、TOST、季随机效应、独立数据、τ 网格、一周两代)全部在",
          "`experiment/analysis/r4_results.json`,键名与 r4-report.md 各节一一对应:",
          "`A_growth_null`、`B_mmult_growth`、`C_classification`、`D_tost_reporting_contribution`、",
          "`E_season_random_effects`、`F_fig09_b2000`、`G_table2`、`I_independent_data`、`J_tau_grid_dA_criterion`、",
          "`K_two_generations_per_week`;复现核对见 `H_repro_check`。", ""]
    (EXP / "analysis/reproduction_map.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()
