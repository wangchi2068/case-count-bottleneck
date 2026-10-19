"""r3 分析 5:跨病原复制。同一 NHSN 文件的 COVID-19 与 RSV 入院数按流感主回归同口径重跑 a、b、b/a、q1、q2,
以及报告调整估计量与 Delta a;流感并列(W-cal 即主分析,W-growth 为病原自适应窗口,另列样本外 2025–26 季)。

预注册:analysis/r3_preregistration.md 第 5 节。用法:python3 r3_c_pathogens.py [B]
"""
import sys
import time

import numpy as np
import pandas as pd

from common import EXP, Log
from r3_common import (EARLY, SEED, SPECS, WEIGHTS, build_rows, cluster_bootstrap, cluster_index, early_index, fit,
                       growth_weeks, load, season_of, series, summarize, update)

B = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
log = Log("r3_c_pathogens")
rng = np.random.default_rng(SEED + 5)
VR_SCN = 0.08
RNG_Q1, RNG_Q2 = (0.883, 1.338), (0.892, 1.373)

configs = []
for pg in ("flu", "covid", "rsv"):
    df = load(pg)
    ser = series(df)
    gw = growth_weeks(df, pg)
    if pg == "rsv":
        wcal = lambda wk: early_index(wk) == 2
    else:
        wcal = lambda wk: early_index(wk) >= 0
    wins = {"W-cal": wcal, "W-growth": (lambda wk, gw=gw: wk in gw)}
    if pg == "flu":
        wins["W-growth-2025"] = lambda wk, gw=gw: (wk in gw) and season_of(wk) == 2025
    gwk = sorted(pd.Timestamp(x) for x in gw)
    log(f"[{pg}] 增长期周 {len(gwk)} 个:" + ", ".join(f"{season_of(x)}季 {sum(season_of(y) == season_of(x) for y in gwk)}"
                                                for x in sorted({pd.Timestamp(f'{season_of(z)}-09-01') for z in gwk})))
    for wname, selfn in wins.items():
        rows = {s: build_rows(ser, WEIGHTS[s], selfn) for s in SPECS}
        configs.append((pg, wname, rows, gwk))

# 流感 W-growth 与用户日历窗口的重合度
fl_cal = next(c for c in configs if c[0] == "flu" and c[1] == "W-cal")[2]["original"]
fl_gro = next(c for c in configs if c[0] == "flu" and c[1] == "W-growth")[2]["original"]
key = lambda r: set(zip(r.state, r.week))
kc, kg = key(fl_cal), key(fl_gro)
overlap = {"cal_rows": len(kc), "growth_rows": len(kg), "intersection": len(kc & kg),
           "share_cal_in_growth": len(kc & kg) / len(kc), "share_growth_in_cal": len(kc & kg) / len(kg),
           "growth_rows_by_season": fl_gro.groupby("season").size().to_dict()}
log("流感增长期窗口与用户窗口重合:", overlap)
update("R5_flu_growth_window_overlap", overlap)

NAMES = []
for s in SPECS:
    NAMES += [f"rbar_{s}", f"a_{s}", f"b_{s}", f"ba_{s}", f"aS_{s}", f"dA_{s}"]
NAMES += ["q1", "q2", "q1S", "q2S", "V_pi", "excess_scn", "vR_implied"]

out = {}
for pg, wname, rows, gwk in configs:
    data = {}
    for s in SPECS:
        r = rows[s][rows[s].valid_h].reset_index(drop=True)
        data[s] = {"G": r.G.to_numpy(), "Gs": r.Gstar.to_numpy(), "D": r.D.to_numpy(), "pi": r.pi.to_numpy(),
                   "state": r.state.to_numpy()}
    n_info = {s: {"N": int(len(rows[s])), "N_valid_proxy": int(rows[s].valid_h.sum()),
                  "n_states": int(rows[s].state.nunique()),
                  "seasons": rows[s].season.value_counts().sort_index().to_dict(),
                  "D_median": float(rows[s].D.median())} for s in SPECS}

    def stat_fn(rb):
        v = {}
        for s in SPECS:
            d = data[s]; i = rb[s]
            v[f"rbar_{s}"], v[f"a_{s}"], v[f"b_{s}"] = fit(d["G"][i], d["D"][i])
            v[f"ba_{s}"] = v[f"b_{s}"] / v[f"a_{s}"]
            v[f"aS_{s}"] = fit(d["Gs"][i], d["D"][i])[1]
            v[f"dA_{s}"] = v[f"a_{s}"] - v[f"aS_{s}"]
        v["q1"] = v["a_single_1w"] / v["a_original"]; v["q2"] = v["a_equal_3w"] / v["a_original"]
        v["q1S"] = v["aS_single_1w"] / v["aS_original"]; v["q2S"] = v["aS_equal_3w"] / v["aS_original"]
        p = data["original"]["pi"][rb["original"]]
        v["V_pi"] = float(np.var(p - 1, ddof=1))
        v["excess_scn"] = v["a_original"] - VR_SCN / v["rbar_original"] ** 2
        v["vR_implied"] = v["a_original"] * v["rbar_original"] ** 2
        return np.array([v[k] for k in NAMES])

    states = sorted(set(data["original"]["state"]))
    idx = {s: cluster_index(data[s]["state"]) for s in SPECS}
    t0 = time.time()
    theta, boot, jack = cluster_bootstrap(stat_fn, states, idx, B, rng, progress=f"r3_c_{pg}_{wname}_progress")
    res = summarize(NAMES, theta, boot, jack)
    q1b, q2b, exb, dAb = res["q1"]["bca95"], res["q2"]["bca95"], res["excess_scn"]["bca95"], res["dA_original"]["bca95"]
    excess_pos = exb[0] > 0
    q_pattern = q1b[1] < 1 < q2b[0]
    verdict = ("截距异常跨病原复现" if excess_pos and q_pattern else
               ("部分复现" if (excess_pos or q_pattern) else "未复现"))
    dA = res["dA_original"]
    crit = {"excess_bca_lower_gt0": bool(excess_pos), "q1_lt1_lt_q2_bca": bool(q_pattern), "verdict": verdict,
            "dA_D1_detectable": bool(dA["bca95"][0] > 0 and dA["point"] >= 0.02),
            "dA_upper_bound": max(dA["bca95"][1], 0.0),
            "q1_disjoint_pure_report": bool(q1b[1] < RNG_Q1[0] or q1b[0] > RNG_Q1[1]),
            "q2_disjoint_pure_report": bool(q2b[1] < RNG_Q2[0] or q2b[0] > RNG_Q2[1]),
            "boot_share_q1_lt1_and_q2_gt1": float(np.mean((boot[:, NAMES.index("q1")] < 1) & (boot[:, NAMES.index("q2")] > 1)))}
    out[f"{pg}|{wname}"] = {"pathogen": pg, "window": wname, "n_info": n_info, "n_states_boot": len(states),
                            "seconds": time.time() - t0, "stats": res, "criteria": crit}
    log(f"[{pg} {wname}] N={n_info['original']['N']}(有效代理 {n_info['original']['N_valid_proxy']}),州 {len(states)},"
        f"季 {n_info['original']['seasons']},D 中位数 {n_info['original']['D_median']:.0f}")
    for k in ("rbar_original", "a_original", "b_original", "ba_original", "q1", "q2", "excess_scn", "vR_implied",
              "dA_original", "V_pi", "q1S", "q2S"):
        r = res[k]
        log(f"    {k:14s} {r['point']:.4g}  BCa [{r['bca95'][0]:.4g}, {r['bca95'][1]:.4g}]")
    log(f"    判据:{crit}")
    update("R5_cross_pathogen", out)
log.close()
