"""r4 C 事后敏感性(非预注册,只作说明):零假设带的格点统计量改用中位数或均值之比时分级是否变化;
以及 A(φ=0)哪些格能同时落入实证 a(BCa 95%)、q1、q2(BCa 95%)。

预注册第 2 节规定带取格点均值;截距很小的格里 q 的均值重尾(rsv W-cal 有格的 q1 均值达 3.7),故补此敏感性。
输入:r3_results.json 的 R5_cross_pathogen、r4_results.json 的 A_growth_null / B_mmult_growth 格点。输出键 C_posthoc。
"""
import json

from common import EXP
from r4_common import r4_load, r4_update

R5 = json.loads((EXP / "analysis/r3_results.json").read_text(encoding="utf-8"))["R5_cross_pathogen"]
R4 = r4_load()
CELLS = R4["A_growth_null"]["cells"] + R4["B_mmult_growth"]["cells"]
STATS = {"mean": ("q1_mean", "q2_mean"), "median": ("q1_median", "q2_median"),
         "ratio_of_means": ("q1_ratio_of_means", "q2_ratio_of_means")}


def disjoint(band, iv):
    return band[1] < iv[0] or band[0] > iv[1]


out = {"note": "事后敏感性,不改变预注册主分级;带 = A 全部格 ∪ B 全部格的 [最小, 最大]", "by_statistic": {}, "joint_A_cells": {}}
for name, (k1, k2) in STATS.items():
    labels, bands = {}, {}
    for combo, v in R5.items():
        cs = [c for c in CELLS if c["combo"] == combo]
        if not cs:
            continue
        st = v["stats"]
        band = {"q1": [min(c[k1] for c in cs), max(c[k1] for c in cs)], "q2": [min(c[k2] for c in cs), max(c[k2] for c in cs)]}
        q1b, q2b = st["q1"]["bca95"], st["q2"]["bca95"]
        exc = R4["C_classification"]["alt_schemes"]["main_all_cells"]["combos"][combo]["excess_bca"]
        e_ratio = disjoint(band["q1"], q1b) and disjoint(band["q2"], q2b)
        e_exc = exc[0] > 0
        lab = "复现" if e_ratio and e_exc else "部分复现" if e_ratio or e_exc else \
            "方向一致" if q1b[1] < 1 < q2b[0] else "未复现"
        labels[combo], bands[combo] = lab, band
    cnt = {k: sum(1 for x in labels.values() if x == k) for k in ("复现", "部分复现", "方向一致", "未复现")}
    out["by_statistic"][name] = {"labels": labels, "counts": cnt, "bands": bands}
    print(name, cnt)

for combo, v in R5.items():
    st = v["stats"]
    a_iv, q1b, q2b = st["a_original"]["bca95"], st["q1"]["bca95"], st["q2"]["bca95"]
    A = [c for c in R4["A_growth_null"]["cells"] if c["combo"] == combo]
    hit = [{k: c[k] for k in ("growth", "gi", "cv2", "delay") if k in c} |
           {"a_mean": c["a_mean"], "q1_mean": c["q1_mean"], "q2_mean": c["q2_mean"]}
           for c in A if a_iv[0] <= c["a_mean"] <= a_iv[1] and q1b[0] <= c["q1_mean"] <= q1b[1] and q2b[0] <= c["q2_mean"] <= q2b[1]]
    out["joint_A_cells"][combo] = {"n_cells": len(A), "n_joint": len(hit), "a_bca95": a_iv, "cells": hit}
    print(combo, f"A 格同时复现 a、q1、q2:{len(hit)}/{len(A)}")
r4_update("C_posthoc", out)
