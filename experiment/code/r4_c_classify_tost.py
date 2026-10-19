"""r4 C + D:按 r4_adoption 第 0 节重新分级七组合;Δa 的 TOST 等价检验。

输入:analysis/r4_boot_draws.npz(r4_c_boot.py,与 r3 逐值一致)、r4_results.json 的 A_growth_null / B_mmult_growth。
预注册:analysis/r4_preregistration.md 第 4–5 节。用法:python3 r4_c_classify_tost.py [tost|classify|all]
"""
import sys

import numpy as np
from scipy import stats

from common import EXP
from r3_common import bca
from r4_common import r4_load, r4_update

Z = np.load(EXP / "analysis/r4_boot_draws.npz", allow_pickle=False)
NAMES = list(Z["names"]); COMBOS = list(Z["combos"])
ix = NAMES.index


def get(i, nm):
    j = ix(nm)
    return Z[f"theta_{i}"][j], Z[f"boot_{i}"][:, j], Z[f"jack_{i}"][:, j]


def ci(i, nm, alpha):
    th, bt, jk = get(i, nm)
    return {"point": float(th), "pct": [float(x) for x in np.percentile(bt, [100 * alpha / 2, 100 * (1 - alpha / 2)])],
            "bca": list(bca(bt, th, jk, alpha=alpha)), "se": float(np.std(bt, ddof=1))}


def tost():
    out = {}
    for i, c in enumerate(COMBOS):
        d90 = ci(i, "dA_original", 0.10)
        a = float(get(i, "a_original")[0]); exc = float(get(i, "excess_scn")[0])
        res = {"dA": d90["point"], "se_boot": d90["se"], "ci90_pct": d90["pct"], "ci90_bca": d90["bca"],
               "ci95_bca": ci(i, "dA_original", 0.05)["bca"], "a_point": a, "excess_point": exc}
        for tag, delta in (("margin_5pct_a", 0.05 * a), ("margin_5pct_excess", 0.05 * exc if exc > 0 else None)):
            if delta is None:
                res[tag] = {"defined": False, "reason": "超出量点估计 ≤ 0,margin 无定义"}
                continue
            p1 = float(1 - stats.norm.cdf((d90["point"] + delta) / d90["se"]))
            p2 = float(stats.norm.cdf((d90["point"] - delta) / d90["se"]))
            res[tag] = {"defined": True, "delta": delta, "p_lower": p1, "p_upper": p2, "p_tost": max(p1, p2),
                        "equivalent_normal": bool(max(p1, p2) < 0.05),
                        "equivalent_ci90_pct": bool(-delta < d90["pct"][0] and d90["pct"][1] < delta),
                        "equivalent_ci90_bca": bool(-delta < d90["bca"][0] and d90["bca"][1] < delta)}
        out[c] = res
        m = res["margin_5pct_a"]
        print(f"{c:18s} Δa={res['dA']:+.5f} 90%BCa [{d90['bca'][0]:+.5f},{d90['bca'][1]:+.5f}] δ=±{m['delta']:.5f} "
              f"p={m['p_tost']:.3g} 等价(正态/百分位/BCa)={m['equivalent_normal']}/{m['equivalent_ci90_pct']}/{m['equivalent_ci90_bca']}")
    r4_update("D_tost_reporting_contribution", {"design": "预注册第 5 节;Δa=a−a*;主 margin 5%×a,次 margin 5%×超出量(仅超出量>0)",
                                                 "B": 2000, "combos": out,
                                                 "n_equivalent_main_bca": sum(v["margin_5pct_a"]["equivalent_ci90_bca"] for v in out.values()),
                                                 "n_equivalent_main_normal": sum(v["margin_5pct_a"]["equivalent_normal"] for v in out.values())})


def disjoint(iv, band):
    return bool(iv[1] < band[0] or iv[0] > band[1])


def hull(*bs):
    bs = [b for b in bs if b]
    return {"q1": [min(b["q1"][0] for b in bs), max(b["q1"][1] for b in bs)],
            "q2": [min(b["q2"][0] for b in bs), max(b["q2"][1] for b in bs)]}


def label(e_ratio, e_excess, direction):
    if e_ratio and e_excess:
        return "复现"
    if e_ratio or e_excess:
        return "部分复现"
    return "方向一致" if direction else "未复现"


def classify():
    R = r4_load()
    A, B = R["A_growth_null"], R["B_mmult_growth"]
    if not (A.get("complete") and B.get("complete")):
        raise SystemExit("A/B 未完成")
    flu_r3 = {"q1": [0.857, 0.937], "q2": [1.226, 1.333]}
    schemes = {}
    for scheme in ("main_all_cells", "no_delay", "r3_flu_growth_band"):
        res = {}
        for i, c in enumerate(COMBOS):
            q1 = ci(i, "q1", 0.05); q2 = ci(i, "q2", 0.05); ex = ci(i, "excess_scn", 0.05)
            if scheme == "main_all_cells":
                band = hull(A["bands"][c]["A_all"], B["bands"][c]["B_all"])
            elif scheme == "no_delay":
                band = hull(A["bands"][c]["A_no_delay"], B["bands"][c]["B_no_delay"])
            else:
                band = flu_r3
            er = disjoint(q1["bca"], band["q1"]) and disjoint(q2["bca"], band["q2"])
            ee = ex["bca"][0] > 0
            dr = q1["bca"][1] < 1 < q2["bca"][0]
            res[c] = {"null_band": band, "q1_bca": q1["bca"], "q2_bca": q2["bca"], "excess_bca": ex["bca"],
                      "q1_disjoint": disjoint(q1["bca"], band["q1"]), "q2_disjoint": disjoint(q2["bca"], band["q2"]),
                      "E_ratio": er, "E_excess": bool(ee), "direction": bool(dr), "label": label(er, ee, dr),
                      "excess_lower_gt0": bool(ee)}
        cnt = {k: sum(v["label"] == k for v in res.values()) for k in ("复现", "部分复现", "方向一致", "未复现")}
        schemes[scheme] = {"combos": res, "counts": cnt}
        print(scheme, cnt, {c: v["label"] for c, v in res.items()})
    r4_update("C_classification", {"design": "预注册第 4 节;主分级 = A 全部格 ∪ B 全部格的凸包;CI 反演",
                                   "combos": schemes["main_all_cells"]["combos"],
                                   "counts": schemes["main_all_cells"]["counts"], "alt_schemes": schemes})


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("tost", "all"):
        tost()
    if what in ("classify", "all"):
        classify()
