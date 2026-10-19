"""r4 A + B:七个病原—窗口组合的增长期零假设范围。

A:φ = 0 环境噪声(R 在日历周内恒定、周间独立),世代间隔取各病原文献值,含入院延迟敏感性。
B:M-mult 增长期(v_R = 0,报告率乘性噪声,对数 AR(1))。
预注册:analysis/r4_preregistration.md 第 1–3 节。用法:python3 r4_a_growth_null.py [每格次数] [进程数]
"""
import json
import sys
import time
from multiprocessing import Pool

import numpy as np

from common import EXP, SEED, Log
from r4_common import r4_update
from r4_sim_core import (R_from_lambda, combo_selectors, disc_gamma, fit_from_counts, lam_from_rbar, segments,
                         simulate_weekly_counts)

REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 300
NPROC = int(sys.argv[2]) if len(sys.argv) > 2 else 4
PILOT = 100
CV2S = [0.0036, 0.0143, 0.0287, 0.0574]
GI = {  # 均值, 标准差(天)
    "flu": {"short": (2.2, 0.98), "mid": (3.6, 1.6), "long": (4.3, 1.91)},
    "covid": {"short": (2.3, 1.5), "mid": (3.2, 2.08), "long": (3.9, 2.54)},
    "rsv": {"short": (6.0, 1.68), "mid": (7.5, 2.1), "long": (9.0, 2.52)},
}
DELAYS = {"none": None, "short": (4.0, 2.0), "long": (7.0, 3.5)}
PSIS, TAUS = [0.0, 0.3, 0.6, 0.9], [0.15, 0.3]

R3 = json.loads((EXP / "analysis/r3_results.json").read_text(encoding="utf-8"))["R5_cross_pathogen"]
SEL = combo_selectors()
COMBOS = list(SEL)
SEGS = {c: segments(*SEL[c]) for c in COMBOS}
DELAY_PMF = {k: (None if v is None else disc_gamma(v[0], v[1], s0=0)) for k, v in DELAYS.items()}
GI_PMF = {pg: {k: disc_gamma(*v) for k, v in d.items()} for pg, d in GI.items()}


def run_reps(combo, rbar_target, gi_key, n, ss, cv2=0.0, delay="none", psi=0.0, tau=0.0):
    pg = SEL[combo][0]
    g = GI_PMF[pg][gi_key]
    lam = lam_from_rbar(rbar_target)
    R0, _ = R_from_lambda(lam, g)
    segs = SEGS[combo]
    lens = [L for _, L, _ in segs]
    rng = np.random.default_rng(ss)
    rows = []
    for _ in range(n):
        C, nw = simulate_weekly_counts(segs, R0, g, rng, lam, cv2=cv2, psi=psi, tau=tau, delay=DELAY_PMF[delay])
        f = fit_from_counts(C, nw, lens)
        o, s1, e3 = f["original"], f["single_1w"], f["equal_3w"]
        rows.append([o["a"], o["b"], o["rbar"], o["N"], o["D_med"], s1["a"], e3["a"]])
    return np.array(rows), lam, R0


def summarize_cell(r):
    a, a1, a3 = r[:, 0], r[:, 5], r[:, 6]
    q1, q2 = a1 / a, a3 / a
    return {"a_mean": float(a.mean()), "a_sd": float(a.std(ddof=1)), "b_mean": float(r[:, 1].mean()),
            "Rbar_mean": float(r[:, 2].mean()), "N_mean": float(r[:, 3].mean()), "D_med_mean": float(r[:, 4].mean()),
            "q1_mean": float(q1.mean()), "q2_mean": float(q2.mean()),
            "q1_median": float(np.median(q1)), "q2_median": float(np.median(q2)),
            "q1_sd": float(q1.std(ddof=1)), "q2_sd": float(q2.std(ddof=1)),
            "q1_ratio_of_means": float(a1.mean() / a.mean()), "q2_ratio_of_means": float(a3.mean() / a.mean()),
            "share_a_nonpos": float(np.mean(a <= 0))}


def task(args):
    part, ci, cell_i, p = args
    t0 = time.time()
    ss = np.random.SeedSequence([SEED + (41 if part == "A" else 42), ci, cell_i])
    r, lam, R0 = run_reps(COMBOS[ci], p["rbar_target"], p["gi"], REPS, ss, cv2=p.get("cv2", 0.0),
                          delay=p["delay"], psi=p.get("psi", 0.0), tau=p.get("tau", 0.0))
    out = {"part": part, "combo": COMBOS[ci], **p, "lambda": lam, "R0": R0, "reps": REPS, **summarize_cell(r),
           "seconds": time.time() - t0}
    return out


def pilot(args):
    ci, gi_i, gi_key, target = args
    ss = np.random.SeedSequence([SEED + 41, ci, 9999, gi_i])
    r, lam, R0 = run_reps(COMBOS[ci], target, gi_key, PILOT, ss, cv2=0.0287)
    return ci, gi_key, float(r[:, 2].mean()), lam, R0


def band(cells, cond):
    sub = [c for c in cells if cond(c)]
    if not sub:
        return None
    return {"q1": [min(c["q1_mean"] for c in sub), max(c["q1_mean"] for c in sub)],
            "q2": [min(c["q2_mean"] for c in sub), max(c["q2_mean"] for c in sub)], "n_cells": len(sub)}


def main():
    log = Log("r4_a_growth_null")
    t_start = time.time()
    targets = {}
    for c in COMBOS:
        s = R3[c]["stats"]["rbar_original"]
        pt, (lo, hi) = s["point"], s["bca95"]
        targets[c] = {"lo": min(lo, 0.97 * pt), "point": pt, "hi": max(hi, 1.03 * pt)}
        log(f"{c}: 段 {len(SEGS[c])} 个,段长合计 {sum(L for _, L, _ in SEGS[c])},R̄ 目标 {targets[c]}")
    # 试点校准
    jobs = [(ci, gi_i, gk, targets[c]["point"]) for ci, c in enumerate(COMBOS) for gi_i, gk in enumerate(GI["flu"])]
    calib = {}
    with Pool(NPROC) as pool:
        for ci, gk, sim, lam, R0 in pool.imap_unordered(pilot, jobs):
            c = COMBOS[ci]
            tgt = targets[c]["point"]
            calib.setdefault(c, {})[gk] = {"target": tgt, "pilot_Rbar": sim, "factor": tgt / sim, "lambda": lam, "R0": R0}
            log(f"  试点 {c} GI={gk}: 目标 {tgt:.4f},模拟 {sim:.4f},修正因子 {tgt / sim:.4f}")
    r4_update("A_calibration", {"pilot_reps": PILOT, "cv2": 0.0287, "calib": calib})
    # 任务表
    tasks = []
    for ci, c in enumerate(COMBOS):
        pg = SEL[c][0]
        k = 0
        for gname in ("lo", "point", "hi"):
            for gk in GI[pg]:
                tgt = targets[c][gname] * calib[c][gk]["factor"]
                for cv2 in CV2S:
                    for dk in DELAYS:
                        tasks.append(("A", ci, k, {"growth": gname, "rbar_target": tgt, "gi": gk, "cv2": cv2, "delay": dk}))
                        k += 1
        k = 0
        for gname in ("lo", "point", "hi"):
            tgt = targets[c][gname] * calib[c]["mid"]["factor"]
            for psi in PSIS:
                for tau in TAUS:
                    for dk in ("none", "long"):
                        tasks.append(("B", ci, k, {"growth": gname, "rbar_target": tgt, "gi": "mid", "psi": psi, "tau": tau,
                                                   "delay": dk}))
                        k += 1
    log(f"共 {len(tasks)} 格,每格 {REPS} 次,{NPROC} 进程")
    # 先跑 A 再跑 B;组内按耗时大的组合先跑
    cells = {"A": [], "B": []}
    prog = open(EXP / "logs/r4_a_growth_null_cells.jsonl", "w", encoding="utf-8")
    done = 0
    with Pool(NPROC) as pool:
        for out in pool.imap_unordered(task, tasks, chunksize=1):
            cells[out["part"]].append(out)
            prog.write(json.dumps(out, ensure_ascii=False) + "\n"); prog.flush()
            done += 1
            if done % 20 == 0 or done == len(tasks):
                log(f"  {done}/{len(tasks)} 格 [{time.time() - t_start:.0f}s]")
                write(cells, targets, t_start)
    prog.close()
    write(cells, targets, t_start, final=True, log=log)
    log.close()


def write(cells, targets, t_start, final=False, log=None):
    bands = {}
    for c in COMBOS:
        A = [x for x in cells["A"] if x["combo"] == c]
        B = [x for x in cells["B"] if x["combo"] == c]
        bands[c] = {
            "A_no_delay": band(A, lambda x: x["delay"] == "none"),
            "A_with_delay": band(A, lambda x: x["delay"] != "none"),
            "A_all": band(A, lambda x: True),
            "A_mid_gi_no_delay": band(A, lambda x: x["delay"] == "none" and x["gi"] == "mid"),
            "B_no_delay": band(B, lambda x: x["delay"] == "none"),
            "B_all": band(B, lambda x: True),
        }
        if final and log:
            for k, v in bands[c].items():
                if v:
                    log(f"{c} {k}: q1 [{v['q1'][0]:.3f}, {v['q1'][1]:.3f}]  q2 [{v['q2'][0]:.3f}, {v['q2'][1]:.3f}]  ({v['n_cells']} 格)")
    r4_update("A_growth_null", {"design": "预注册第 2 节;日分辨率更新过程,φ=0,各病原文献世代间隔,入院延迟敏感性",
                                "reps_per_cell": REPS, "seed": SEED + 41, "cv2_grid": CV2S, "gi_days": GI,
                                "delays_days": DELAYS, "rbar_targets": targets, "complete": final,
                                "bands": {c: {k: v for k, v in b.items() if k.startswith("A")} for c, b in bands.items()},
                                "cells": cells["A"], "elapsed_s": time.time() - t_start})
    r4_update("B_mmult_growth", {"design": "预注册第 3 节;v_R=0,报告率对数 AR(1) 乘性噪声",
                                 "reps_per_cell": REPS, "seed": SEED + 42, "psi_grid": PSIS, "tau_grid": TAUS,
                                 "complete": final,
                                 "bands": {c: {k: v for k, v in b.items() if k.startswith("B")} for c, b in bands.items()},
                                 "cells": cells["B"]})


if __name__ == "__main__":
    main()
