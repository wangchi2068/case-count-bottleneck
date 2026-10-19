"""r4 H:干净重跑核对。把 r4_repro_check/(只复制 code/、按 README 命令重跑)产出的表 2 与图 12 数据,与原结果逐值比较。

比较范围:reanalysis_results.json#B_bootstrap(表 2 实证列)、r3_results.json#R5_cross_pathogen(图 12 点与区间)、
r4_results.json 的 C0_r3c_rerun_check、A_calibration、A_growth_null、B_mmult_growth、C_classification、
D_tost_reporting_contribution、G_table2,以及表 2 LaTeX 草稿全文。计时类字段(秒数、更新时间)不比。
输出:r4_results.json 键 H_repro_check。用法:python3 r4_h_repro_compare.py
"""
import json
import math

from common import EXP
from r4_common import r4_update

RC = EXP / "r4_repro_check"
SKIP = ("seconds", "elapsed_s", "updated", "seconds_per_draw", "timing_50_draws_s", "draws_file")
TOL = 1e-9


def walk(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in SKIP:
                continue
            yield from walk(v, f"{p}.{k}" if p else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f"{p}[{i}]")
    else:
        yield p, o


def compare(a, b):
    fa, fb = dict(walk(a)), dict(walk(b))
    keys = sorted(set(fa) | set(fb))
    n_num, n_other, bad, maxd = 0, 0, [], 0.0
    for k in keys:
        x, y = fa.get(k, "<缺>"), fb.get(k, "<缺>")
        if isinstance(x, (int, float)) and isinstance(y, (int, float)) and not isinstance(x, bool):
            n_num += 1
            if math.isnan(x) and math.isnan(y):
                continue
            d = abs(x - y)
            maxd = max(maxd, d)
            if d > TOL * max(1.0, abs(x)):
                bad.append({"path": k, "original": x, "rerun": y})
        else:
            n_other += 1
            if x != y:
                bad.append({"path": k, "original": x, "rerun": y})
    return {"n_numeric": n_num, "n_other": n_other, "max_abs_diff": maxd, "n_mismatch": len(bad), "mismatches": bad[:20]}


CELL_ID = ("part", "combo", "growth", "gi", "cv2", "psi", "tau", "delay")


def load(rel, base):
    return json.loads((base / rel).read_text(encoding="utf-8"))


def sort_cells(v):
    """格点按完成顺序写入,顺序随进程调度变化;比较前按格标识排序。"""
    if isinstance(v, dict) and isinstance(v.get("cells"), list):
        v = dict(v, cells=sorted(v["cells"], key=lambda c: tuple(str(c.get(k)) for k in CELL_ID)))
    return v


def main():
    items = [("analysis/reanalysis_results.json", "B_bootstrap"), ("analysis/r3_results.json", "R5_cross_pathogen")]
    items += [("analysis/r4_results.json", k) for k in ("C0_r3c_rerun_check", "A_calibration", "A_growth_null",
                                                        "B_mmult_growth", "C_classification",
                                                        "D_tost_reporting_contribution", "G_table2")]
    res = {}
    for rel, key in items:
        r = compare(sort_cells(load(rel, EXP)[key]), sort_cells(load(rel, RC)[key]))
        res[f"{rel.split('/')[-1]}#{key}"] = r
        print(f"{key}: 数值 {r['n_numeric']},其他 {r['n_other']},不一致 {r['n_mismatch']},最大绝对差 {r['max_abs_diff']:.3g}")
    t0 = (EXP / "tables/tab_02_lag_ratios_r4.tex").read_text(encoding="utf-8")
    t1 = (RC / "tables/tab_02_lag_ratios_r4.tex").read_text(encoding="utf-8")
    res["tables/tab_02_lag_ratios_r4.tex"] = {"identical_text": t0 == t1}
    print("表 2 草稿全文一致:", t0 == t1)
    total_num = sum(v.get("n_numeric", 0) for v in res.values())
    total_bad = sum(v.get("n_mismatch", 0) for v in res.values())
    r4_update("H_repro_check", {
        "design": "干净目录 r4_repro_check/ 只复制 code/,按 code/README.md 第 4 节命令依次运行步骤 1、2、9、10、11、12、15"
                  "(a_reproduce → b_bootstrap → r3_c_pathogens → r4_c_boot → r4_a_growth_null → r4_c_classify_tost → r4_g_table2),"
                  "再与原结果逐值比较;容差 1e-9(相对,|x|<1 时为绝对);格点列表按格标识排序后比较(写入顺序随进程调度变化)",
        "script": "r4_repro_check/run_check.sh", "tolerance": TOL, "items": res,
        "total_numeric_compared": total_num, "total_mismatch": total_bad,
        "all_identical": total_bad == 0 and t0 == t1})
    print(f"合计数值 {total_num},不一致 {total_bad}")


if __name__ == "__main__":
    main()
