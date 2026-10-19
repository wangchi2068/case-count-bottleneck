"""分析 E:R_t 服从 AR(1) 时,经验截距 a 相对独立同分布理论值 v_R/R_bar^2 被放大多少。

生成模型(每周一代,与正文情景一致):
- 51 州 × 3 季 = 153 条序列,每条 3 周前置 + 10 周观测 + 1 周前瞻;
- R_t = max(0.05, mu_R + e_t),e_t 平稳 AR(1):方差 v_R,系数 phi(phi=1 表示整季常数偏差,即州-季间异质性);
- 感染 I_{t+1} ~ 负二项(均值 R_t I_t,离散 k I_t),k=0.35;报告 C_t ~ Binomial(I_t, rho),rho=0.021;
- 起始规模:I_0 = D0/rho,D0 从实证流行初期每个州-季第一周的 D_t 中有放回抽取;
- 与实证完全同口径:三种滞后权重构造 D_t,保留 D_t>=5,G_t=C_{t+1}/D_t,R_bar=样本均值,迭代 FGLS 拟合 L=a+b/D。
网格:phi ∈ {0,0.3,0.5,0.7,0.9,1};v_R ∈ {0.04,0.08,0.16};(mu_R, 起始规模倍数) ∈ {(1.67,1)(正文字面), (1.42,1)(使主规格模拟均值 G≈1.67),
(1.42,0.25)(再把模拟 D 中位数压到接近实证的 53)};
每格 R 次重复。比较:a_hat / (v_R/1.67^2)(相对正文 i.i.d. 理论的倍数)、a_hat(phi)/a_hat(0)、截距比 q1、q2。
"""
import json
import sys
import time

import numpy as np
import pandas as pd

from common import EARLY, EXP, SEED, WEIGHTS, Log, fgls_affine, update_results

REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 200
K, RHO, RBAR_TH = 0.35, 0.021, 1.67
PHIS = [0.0, 0.3, 0.5, 0.7, 0.9, 1.0]
VRS = [0.04, 0.08, 0.16]
CONFIGS = [(1.67, 1.0), (1.42, 1.0), (1.42, 0.25)]
PRE, T_OBS = 3, 10
NW = PRE + T_OBS + 1
log = Log("e_ar1_sim")
rng = np.random.default_rng(SEED + 5)

# 实证起始规模
p = pd.read_csv(EXP / "data/panel_original.csv.gz", parse_dates=["week_end"])
d0 = []
for lo, hi in EARLY:
    e = p[(p.week_end >= lo) & (p.week_end <= hi)]
    d0.extend(e.sort_values("week_end").groupby("state").D_t.first().tolist())
D0 = np.array(d0)
emp = p[np.any([(p.week_end >= lo) & (p.week_end <= hi) for lo, hi in EARLY], axis=0)]
log(f"实证起始 D0:{len(D0)} 个州-季,中位数 {np.median(D0):.1f};实证初期样本 D 中位数 {emp.D_t.median():.1f}")
S = len(D0)  # 一次模拟的州-季数与实证一致


def simulate(phi, vR, mu, rng, d0_scale=1.0):
    e = np.zeros((S, NW))
    e[:, 0] = rng.normal(0, np.sqrt(vR), S)
    sd_innov = np.sqrt(vR * (1 - phi ** 2))
    for t in range(1, NW):
        e[:, t] = phi * e[:, t - 1] + sd_innov * rng.normal(size=S)
    R = np.maximum(0.05, mu + e)
    I = np.zeros((S, NW))
    I[:, 0] = np.maximum(1.0, np.round(d0_scale * rng.choice(D0, S) / RHO))
    for t in range(NW - 1):
        m = R[:, t] * I[:, t]
        lam = rng.gamma(shape=np.maximum(K * I[:, t], 1e-9), scale=np.where(I[:, t] > 0, m / np.maximum(K * I[:, t], 1e-9), 0))
        I[:, t + 1] = rng.poisson(lam)
    C = rng.binomial(I.astype(np.int64), RHO).astype(float)
    return C


def fit_specs(C):
    out = {}
    t = np.arange(2, NW - 1)
    for name, w in WEIGHTS.items():
        D = w[0] * C[:, t] + w[1] * C[:, t - 1] + w[2] * C[:, t - 2]
        G = C[:, t + 1] / np.where(D > 0, D, np.nan)
        keep = (D >= 5) & (t >= PRE - 1)[None, :]
        Dk, Gk = D[keep], G[keep]
        rbar = Gk.mean()
        L = ((Gk - rbar) / rbar) ** 2
        a, b = fgls_affine(L, Dk)
        out[name] = (a, b, rbar, len(Dk), float(np.median(Dk)))
    return out


t_start = time.time()
cells = []
prog = open(EXP / "logs/e_ar1_sim_cells.jsonl", "w", encoding="utf-8")
for mu, d0s in CONFIGS:
    for vR in VRS:
        for phi in PHIS:
            rows = []
            for _ in range(REPS):
                f = fit_specs(simulate(phi, vR, mu, rng, d0s))
                rows.append([f["original"][0], f["original"][1], f["original"][2], f["original"][3], f["original"][4],
                             f["single_1w"][0], f["equal_3w"][0], f["single_1w"][1], f["equal_3w"][1]])
            r = np.array(rows)
            a = r[:, 0]
            cell = {"mu_R": mu, "d0_scale": d0s, "v_R": vR, "phi": phi, "reps": REPS,
                    "a_mean": float(a.mean()), "a_sd": float(a.std(ddof=1)), "a_q025": float(np.percentile(a, 2.5)), "a_q975": float(np.percentile(a, 97.5)),
                    "a_iid_theory": vR / RBAR_TH ** 2, "inflation_vs_theory": float(a.mean() / (vR / RBAR_TH ** 2)),
                    "b_mean": float(r[:, 1].mean()), "Rbar_mean": float(r[:, 2].mean()), "N_mean": float(r[:, 3].mean()),
                    "median_D_mean": float(r[:, 4].mean()),
                    "q1_mean": float(np.mean(r[:, 5] / a)), "q2_mean": float(np.mean(r[:, 6] / a)),
                    "r1_mean": float(np.mean(r[:, 7] / r[:, 1])), "r2_mean": float(np.mean(r[:, 8] / r[:, 1])),
                    "P_a_in_emp_CI": float(np.mean((a >= 0.0837) & (a <= 0.1165)))}
            cells.append(cell)
            prog.write(json.dumps(cell, ensure_ascii=False) + "\n"); prog.flush()
            log(f"mu={mu} d0×{d0s} vR={vR} phi={phi}: a={cell['a_mean']:.4f}±{cell['a_sd']:.4f}(理论 {cell['a_iid_theory']:.4f},×{cell['inflation_vs_theory']:.2f}),"
                f"q1={cell['q1_mean']:.2f}, q2={cell['q2_mean']:.2f}, r1={cell['r1_mean']:.2f}, r2={cell['r2_mean']:.2f}, "
                f"R_bar={cell['Rbar_mean']:.3f}, N={cell['N_mean']:.0f}, D中位={cell['median_D_mean']:.0f},落入实证 a 区间比例 {cell['P_a_in_emp_CI']:.2f}"
                f" [{time.time() - t_start:.0f}s]")
            # 相对 phi=0 的放大倍数
            base = [c for c in cells if c["mu_R"] == mu and c["d0_scale"] == d0s and c["v_R"] == vR and c["phi"] == 0.0]
            if base:
                cell["inflation_vs_phi0"] = cell["a_mean"] / base[0]["a_mean"]
            update_results("E_ar1_simulation", {"design": __doc__, "reps_per_cell": REPS, "seed": SEED + 5,
                                                "empirical_targets": {"a": 0.09906, "a_pct95": [0.0837, 0.1165], "q1": 0.688, "q2": 1.539,
                                                                      "inflation_range_text": "3.5–6.9"},
                                                "cells": cells, "elapsed_s": time.time() - t_start})
prog.close()
log.close()
