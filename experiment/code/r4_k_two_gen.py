"""r4 K:一周跨两代。环境噪声块 = 日历周(7 天)vs 每代独立(4 天块);给定周尺度相关 φ_week,块系数 φ_week^(块天数/7)。

结构:流感 W-cal 段,世代间隔中档,R̄ 点估计(用 A 的试点修正因子),报告率无额外噪声。
预注册:analysis/r4_preregistration.md 第 10 节。种子 SEED+44。用法:python3 r4_k_two_gen.py [每格次数] [进程数]
"""
import json
import sys
import time
from multiprocessing import Pool

import numpy as np

from common import EXP, SEED, Log
from r4_a_growth_null import DELAY_PMF, GI_PMF, SEGS, SEL, summarize_cell
from r4_common import r4_load, r4_update
from r4_sim_core import R_from_lambda, fit_from_counts, lam_from_rbar, simulate_weekly_counts

REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 300
NPROC = int(sys.argv[2]) if len(sys.argv) > 2 else 1
COMBO = "flu|W-cal"
PHIS = [0.0, 0.3, 0.5, 0.7, 0.9]
CV2S = [0.0143, 0.0287, 0.0574]
BLOCKS = [7, 4]
EMP = {"a": 0.0991, "a_pct95": [0.0835, 0.1163], "q1": 0.688, "q2": 1.539, "ba": 22.6}
R3 = json.loads((EXP / "analysis/r3_results.json").read_text(encoding="utf-8"))["R5_cross_pathogen"][COMBO]["stats"]
Q1_BCA, Q2_BCA = R3["q1"]["bca95"], R3["q2"]["bca95"]


def task(args):
    cell_i, p, rbar_target = args
    t0 = time.time()
    g = GI_PMF["flu"]["mid"]
    lam = lam_from_rbar(rbar_target)
    R0, _ = R_from_lambda(lam, g)
    segs = SEGS[COMBO]
    lens = [L for _, L, _ in segs]
    rng = np.random.default_rng(np.random.SeedSequence([SEED + 44, cell_i]))
    phib = p["phi_week"] ** (p["block_days"] / 7)
    rows = []
    for _ in range(REPS):
        C, nw = simulate_weekly_counts(segs, R0, g, rng, lam, cv2=p["cv2"], phi=phib, block_days=p["block_days"],
                                       delay=DELAY_PMF[p["delay"]])
        f = fit_from_counts(C, nw, lens)
        o, s1, e3 = f["original"], f["single_1w"], f["equal_3w"]
        rows.append([o["a"], o["b"], o["rbar"], o["N"], o["D_med"], s1["a"], e3["a"]])
    r = np.array(rows)
    q1, q2 = r[:, 5] / r[:, 0], r[:, 6] / r[:, 0]
    out = {**p, "phi_block": phib, **summarize_cell(r), "ba_mean": float(np.mean(r[:, 1] / r[:, 0])),
           "share_q1_in_emp_bca": float(np.mean((q1 >= Q1_BCA[0]) & (q1 <= Q1_BCA[1]))),
           "share_q2_in_emp_bca": float(np.mean((q2 >= Q2_BCA[0]) & (q2 <= Q2_BCA[1]))),
           "share_a_in_emp_pct95": float(np.mean((r[:, 0] >= EMP["a_pct95"][0]) & (r[:, 0] <= EMP["a_pct95"][1]))),
           "reps": REPS, "seconds": time.time() - t0}
    m = out
    out["reproduces_a_q1_q2"] = bool(EMP["a_pct95"][0] <= m["a_mean"] <= EMP["a_pct95"][1]
                                     and Q1_BCA[0] <= m["q1_mean"] <= Q1_BCA[1] and Q2_BCA[0] <= m["q2_mean"] <= Q2_BCA[1])
    return out


def main():
    log = Log("r4_k_two_gen")
    fac = r4_load()["A_calibration"]["calib"][COMBO]["mid"]["factor"]
    rbar_t = R3["rbar_original"]["point"] * fac
    tasks, k = [], 0
    for bd in BLOCKS:
        for phi in PHIS:
            for cv2 in CV2S:
                for dk in ("none", "long"):
                    tasks.append((k, {"block_days": bd, "phi_week": phi, "cv2": cv2, "delay": dk}, rbar_t)); k += 1
    cells = []
    t0 = time.time()
    with Pool(NPROC) as pool:
        for out in pool.imap_unordered(task, tasks):
            cells.append(out)
            if len(cells) % 10 == 0 or len(cells) == len(tasks):
                log(f"{len(cells)}/{len(tasks)} [{time.time() - t0:.0f}s]")
                write(cells, len(cells) == len(tasks), rbar_t, fac)
    for c in sorted(cells, key=lambda c: (c["delay"], c["cv2"], c["phi_week"], c["block_days"])):
        log(f"块{c['block_days']} φw={c['phi_week']} CV²={c['cv2']} 延迟={c['delay']}: a={c['a_mean']:.4f} "
            f"q1={c['q1_mean']:.3f} q2={c['q2_mean']:.3f} b/a={c['ba_mean']:.1f} 复现={c['reproduces_a_q1_q2']}")
    log.close()


def write(cells, final, rbar_t, fac):
    pairs = []
    for c7 in [c for c in cells if c["block_days"] == 7]:
        c4 = next((c for c in cells if c["block_days"] == 4 and all(c[x] == c7[x] for x in ("phi_week", "cv2", "delay"))),
                  None)
        if c4:
            pairs.append({k: c7[k] for k in ("phi_week", "cv2", "delay")} |
                         {"d_a": c4["a_mean"] - c7["a_mean"], "d_q1": c4["q1_mean"] - c7["q1_mean"],
                          "d_q2": c4["q2_mean"] - c7["q2_mean"]})
    r4_update("K_two_generations_per_week", {
        "design": "预注册第 10 节;流感 W-cal 段,世代间隔中档,块 7 天 vs 4 天,φ_block = φ_week^(块天数/7)",
        "reps_per_cell": REPS, "seed": SEED + 44, "rbar_target_after_pilot": rbar_t, "pilot_factor": fac,
        "empirical": EMP | {"q1_bca95": Q1_BCA, "q2_bca95": Q2_BCA}, "complete": final, "cells": cells,
        "block4_minus_block7": pairs,
        "max_abs_diff_block4_vs_7": {k: max((abs(p[k]) for p in pairs), default=None) for k in ("d_a", "d_q1", "d_q2")},
        "cells_reproducing_a_q1_q2": [{k: c[k] for k in ("block_days", "phi_week", "cv2", "delay")}
                                      for c in cells if c["reproduces_a_q1_q2"]]})


if __name__ == "__main__":
    main()
