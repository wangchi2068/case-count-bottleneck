"""r4 J:报告离散度 τ 网格上 Δa 判据的水平与功效。

报告率 = ρ · h_w^κ · u_w;h_w 为段对应州周的实证填报医院比例(缺失或 0 取 1),u_w 为不可观测乘性噪声(对数正态,CV = τ,周间独立)。
每次模拟算未调整 a 与按 h 调整的 a*,Δa = a − a*;州聚类 B 次重抽 + jackknife 得 BCa 95%;
D1 = BCa 下端 > 0 且点估计 ≥ 0.02;D2 上界 = max(BCa 上端, 0)。
预注册:analysis/r4_preregistration.md 第 9 节。种子 SEED+43。用法:python3 r4_j_tau_grid.py [每格次数] [B] [进程数]
"""
import sys
import time
from multiprocessing import Pool

import numpy as np

from common import EXP, SEED, Log
from r3_common import bca, load, series
from r4_a_growth_null import GI_PMF, SEL
from r4_common import r4_load, r4_update
from r4_sim_core import PRE_W, R_from_lambda, lam_from_rbar, simulate_weekly_counts

REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 200
BOOT = int(sys.argv[2]) if len(sys.argv) > 2 else 200
NPROC = int(sys.argv[3]) if len(sys.argv) > 3 else 4
COMBO = "flu|W-cal"
TAUS = [0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5]
KAPPAS = [0, 1, 3, 5, 8]
CV2 = 0.0287
W = np.array([0.65, 0.25, 0.10])


def segments_h(pathogen, select):
    """同 r4_sim_core.segments,另返回每段 PRE_W + 段长 + 1 周的实证 h(对应实证 t0−3 … t0+段长)。"""
    ser = series(load(pathogen))
    segs, hs = [], []
    for s, z in ser.items():
        c, wk, h = z["c"], z["week"], z["h"]
        n = len(c)
        t = np.arange(2, n - 1)
        tt = t[np.array([select(x) for x in wk[t]], bool)]
        if len(tt) == 0:
            continue
        brk = np.where(np.diff(tt) != 1)[0]
        for a, b in zip(np.r_[0, brk + 1], np.r_[brk, len(tt) - 1]):
            t0, L = tt[a], int(b - a + 1)
            d0 = W[0] * c[t0] + W[1] * c[t0 - 1] + W[2] * c[t0 - 2]
            segs.append((s, L, float(max(d0, 1.0))))
            idx = np.arange(t0 - PRE_W, t0 + L + 1)
            hv = np.array([h[i] if 0 <= i < n else np.nan for i in idx])
            hs.append(np.where(np.isfinite(hv) & (hv > 0), hv, 1.0))
    return segs, hs


SEGS, HS = segments_h(*SEL[COMBO])
LENS = np.array([L for _, L, _ in SEGS])
WMAX = int((PRE_W + LENS + 1).max())
H = np.ones((len(SEGS), WMAX))
for i, hv in enumerate(HS):
    H[i, :len(hv)] = np.minimum(hv, 1.0)
STATE = np.array([s for s, _, _ in SEGS])


def fgls(L, D, maxit=200, tol=1e-10):
    """与 common.fgls_affine 相同的迭代 FGLS(权 1/μ̂²),用 2×2 正规方程实现以提速。"""
    x = 1.0 / D
    def wls(w):
        s0, s1, s2 = w.sum(), (w * x).sum(), (w * x * x).sum()
        t0, t1 = (w * L).sum(), (w * x * L).sum()
        det = s0 * s2 - s1 * s1
        return np.array([(s2 * t0 - s1 * t1) / det, (s0 * t1 - s1 * t0) / det])
    beta = wls(np.ones_like(L))
    for _ in range(maxit):
        mu = np.clip(beta[0] + beta[1] * x, 1e-6, None)
        new = wls(1.0 / mu ** 2)
        done = np.max(np.abs(new - beta) / (np.abs(beta) + 1e-12)) < tol
        beta = new
        if done:
            break
    return beta[0]


def rows_from(C):
    """返回 (D, G, G*, 州) 的观测行(原权重,D ≥ 5)。"""
    S, Wd = C.shape
    t = np.arange(2, Wd - 1)
    in_seg = (t[None, :] >= PRE_W) & (t[None, :] < PRE_W + LENS[:, None])
    D = W[0] * C[:, t] + W[1] * C[:, t - 1] + W[2] * C[:, t - 2]
    Hh = H[:, :Wd]
    Ds = W[0] * C[:, t] / Hh[:, t] + W[1] * C[:, t - 1] / Hh[:, t - 1] + W[2] * C[:, t - 2] / Hh[:, t - 2]
    keep = in_seg & (D >= 5) & (Ds > 0)
    st = np.broadcast_to(STATE[:, None], D.shape)
    G = C[:, t + 1] / np.where(D > 0, D, 1)
    Gs = (C[:, t + 1] / Hh[:, t + 1]) / np.where(Ds > 0, Ds, 1)
    return D[keep], G[keep], Gs[keep], st[keep]


def stat(D, G, Gs):
    rb = G.mean(); a = fgls(((G - rb) / rb) ** 2, D)
    rbs = Gs.mean(); a_s = fgls(((Gs - rbs) / rbs) ** 2, D)
    return np.array([a - a_s, a, rb])


def one_rep(C, rng):
    D, G, Gs, st = rows_from(C)
    units = np.unique(st)
    idx = {u: np.where(st == u)[0] for u in units}
    th = stat(D, G, Gs)
    boot = np.empty(BOOT)
    for b in range(BOOT):
        ii = np.concatenate([idx[u] for u in rng.choice(units, len(units), replace=True)])
        boot[b] = stat(D[ii], G[ii], Gs[ii])[0]
    jack = np.array([stat(D[st != u], G[st != u], Gs[st != u])[0] for u in units])
    lo, hi = bca(boot, th[0], jack)
    return th, lo, hi


def task(args):
    cell_i, tau, kappa, rbar_target = args
    t0 = time.time()
    g = GI_PMF["flu"]["mid"]
    lam = lam_from_rbar(rbar_target)
    R0, _ = R_from_lambda(lam, g)
    rng = np.random.default_rng(np.random.SeedSequence([SEED + 43, cell_i]))
    pm = None if kappa == 0 else H ** kappa
    rec = []
    for _ in range(REPS):
        C, _ = simulate_weekly_counts(SEGS, R0, g, rng, lam, cv2=CV2, tau=tau, psi=0.0, pmult=pm)
        th, lo, hi = one_rep(C, rng)
        rec.append([th[0], lo, hi, th[1], th[2]])
    r = np.array(rec)
    dA, lo, hi, a, rb = r.T
    d1 = (lo > 0) & (dA >= 0.02)
    up = np.maximum(hi, 0)
    exc = a - 0.08 / rb ** 2
    with np.errstate(divide="ignore", invalid="ignore"):
        up_exc = np.where(exc > 0, up / exc, np.inf)
    return {"tau": tau, "kappa": kappa, "reps": REPS, "B": BOOT, "dA_mean": float(dA.mean()), "dA_sd": float(dA.std(ddof=1)),
            "a_mean": float(a.mean()), "Rbar_mean": float(rb.mean()), "D1_rate": float(d1.mean()),
            "share_lower_gt0": float(np.mean(lo > 0)), "D2_upper_median": float(np.median(up)),
            "share_upper_over_excess_lt_1pct": float(np.mean(up_exc < 0.01)),
            "median_upper_over_excess": float(np.median(up_exc)), "share_excess_pos": float(np.mean(exc > 0)),
            "median_upper_over_a": float(np.median(up / a)), "seconds": time.time() - t0}


def main():
    log = Log("r4_j_tau_grid")
    fac = r4_load()["A_calibration"]["calib"][COMBO]["mid"]["factor"]
    import json
    R3 = json.loads((EXP / "analysis/r3_results.json").read_text(encoding="utf-8"))["R5_cross_pathogen"][COMBO]["stats"]
    rbar_t = R3["rbar_original"]["point"] * fac
    hk = H[H < 1]
    log(f"段 {len(SEGS)},h<1 的周占比 {np.mean(H < 1):.3f},h 中位数 {np.median(H):.3f},每格 {REPS} 次 × B={BOOT}")
    tasks = [(i, tau, kap, rbar_t) for i, (kap, tau) in enumerate((k, t) for k in KAPPAS for t in TAUS)]
    cells, t0 = [], time.time()
    with Pool(NPROC) as pool:
        for out in pool.imap_unordered(task, tasks):
            cells.append(out)
            log(f"{len(cells)}/{len(tasks)} κ={out['kappa']} τ={out['tau']}: D1={out['D1_rate']:.3f} Δa={out['dA_mean']:.5f} "
                f"上界/超出量<1% 占比 {out['share_upper_over_excess_lt_1pct']:.3f} 中位 {out['median_upper_over_excess']:.4f} "
                f"[{time.time() - t0:.0f}s]")
            lvl = [c for c in cells if c["kappa"] == 0]
            r4_update("J_tau_grid_dA_criterion", {
                "design": "预注册第 9 节;流感 W-cal 段,世代间隔中档,无延迟,φ=0,CV²=0.0287;报告率 ρ·h^κ·u",
                "reps_per_cell": REPS, "B": BOOT, "seed": SEED + 43, "rbar_target_after_pilot": rbar_t,
                "h_summary": {"share_lt1": float(np.mean(H < 1)), "median": float(np.median(H)),
                              "p10_of_h_lt1": float(np.percentile(hk, 10)) if hk.size else None},
                "complete": len(cells) == len(tasks), "cells": cells,
                "level_max_D1_rate_kappa0": max((c["D1_rate"] for c in lvl), default=None),
                "lt1pct_holds_all_cells_median": all(c["median_upper_over_excess"] < 0.01 for c in cells)})
    log.close()


if __name__ == "__main__":
    main()
