"""r3 分析 4:v_R(面板中即截距 a = v_R/R_bar^2)的不确定性随规模与期数的变化。

预注册:analysis/r3_preregistration.md 第 4 节。
4a 独立单位结构:三个流行季各自的 a_k(州聚类区间)、留一季、季间异质性;样本外第 4 季(2025–26 增长期)。
4b 聚类口径:按州、州×季、季(3 簇精确枚举 27 种有序重抽)。
4c 规模对期数:二项稀疏 p=0.5/0.25(降 m 不降 T)对照 S/2、S/4 个州的 m-out-of-n 重抽(降 T 不降 m),
   全体/大州/小州三组;加季数:1、2、3 季全部组合与加入第 4 季。
用法:python3 r3_b_scale_periods.py [B]
"""
import sys
import time
from itertools import combinations, product

import numpy as np
import pandas as pd
from scipy import stats as sps

from common import EXP, Log
from r3_common import (SEED, WEIGHTS, build_rows, early_index, fit, growth_weeks, load, season_of, series, summarize,
                       update)

B = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
log = Log("r3_b_scale_periods")
rng = np.random.default_rng(SEED + 4)
w = np.asarray(WEIGHTS["original"])

df = load("flu")
ser = series(df)
gw = growth_weeks(df, "flu")
season4 = lambda wk: (wk in gw) and season_of(wk) == 2025


def sel(wk):
    return early_index(wk) >= 0 or season4(wk)


rows = build_rows(ser, w, sel)
rows["sk"] = [early_index(x) for x in rows.week]
rows.loc[rows.sk < 0, "sk"] = 3                      # 第 4 季(样本外)
log(f"行数:{rows.groupby('sk').size().to_dict()}(0–2 为用户三个窗口,3 为 2025–26 增长期);第 4 季周:"
    f"{sorted(str(pd.Timestamp(x).date()) for x in gw if season_of(x) == 2025)}")

# 每州:完整序列 + 行(按季标记),供稀疏与重抽
per_state = {}
for s, sub in rows.groupby("state"):
    per_state[s] = {"t": sub.t.to_numpy(), "sk": sub.sk.to_numpy(), "G": sub.G.to_numpy(), "D": sub.D.to_numpy(),
                    "c": ser[s]["c"].astype(np.int64)}


def gather(states, seasons, p=None, r=None):
    """拼接所选州(可重复)与季的 (G, D);p 给定时对每个被抽到的州独立做二项稀疏,丢弃 D'=0 的行。"""
    gs, ds, dropped, total = [], [], 0, 0
    for s in states:
        z = per_state[s]
        m = np.isin(z["sk"], seasons)
        if not m.any():
            continue
        if p is None:
            gs.append(z["G"][m]); ds.append(z["D"][m]); total += int(m.sum())
            continue
        c = r.binomial(z["c"], p).astype(float)
        t = z["t"][m]
        d = w[0] * c[t] + w[1] * c[t - 1] + w[2] * c[t - 2]
        ok = d > 0
        dropped += int((~ok).sum()); total += int(m.sum())
        gs.append(c[t + 1][ok] / d[ok]); ds.append(d[ok])
    return np.concatenate(gs), np.concatenate(ds), dropped, total


def a_of(states, seasons, p=None, r=None):
    g, d, dr, tot = gather(states, seasons, p, r)
    rbar, a, b = fit(g, d)
    return a, rbar, b, dr / max(tot, 1)


def boot_a(states, seasons, nb, p=None, n_draw=None, tag=None):
    """州聚类重抽(可选 m-out-of-n、可选稀疏),返回 a 的重抽数组与剔除比例。"""
    st = list(states); nd = n_draw or len(st)
    out = np.empty(nb); drop = np.empty(nb)
    t0 = time.time()
    for i in range(nb):
        draw = [st[j] for j in rng.choice(len(st), size=nd, replace=True)]
        out[i], _, _, drop[i] = a_of(draw, seasons, p, rng)
    if tag:
        log(f"    [{tag}] {nb} 次 {time.time() - t0:.1f} s")
    return out, float(drop.mean())


def ci(x):
    x = x[np.isfinite(x)]
    lo, hi = np.percentile(x, [2.5, 97.5])
    q25, q75 = np.percentile(x, [25, 75])
    return {"pct95": [float(lo), float(hi)], "width": float(hi - lo), "sd": float(x.std(ddof=1)), "mean": float(x.mean()),
            "sd_robust_iqr": float((q75 - q25) / 1.349)}


S3 = [0, 1, 2]
all_states = sorted(s for s in per_state if np.isin(per_state[s]["sk"], S3).any())
res = {}

# ---------------------------------------------------------------- 4a 结构与季别 a_k
units = {"n_seasons": 3, "n_states": len(all_states),
         "n_state_seasons": int(rows[rows.sk.isin(S3)].groupby(["state", "sk"]).ngroups),
         "n_state_weeks": int(rows.sk.isin(S3).sum()),
         "season4_state_weeks": int((rows.sk == 3).sum()), "season4_states": int(rows[rows.sk == 3].state.nunique())}
log("独立单位:", units)
season_fits = {}
for k in [0, 1, 2, 3]:
    stk = sorted(s for s in per_state if (per_state[s]["sk"] == k).any())
    a, rbar, b, _ = a_of(stk, [k])
    bt, _ = boot_a(stk, [k], B, tag=f"季 {k}")
    season_fits[k] = {"N": int((rows.sk == k).sum()), "n_states": len(stk), "a": a, "R_bar": rbar, "b": b,
                      "vR_implied": a * rbar ** 2, **ci(bt)}
    log(f"  季 {k}:N={season_fits[k]['N']},a={a:.4f} [{season_fits[k]['pct95'][0]:.4f},{season_fits[k]['pct95'][1]:.4f}],"
        f"R̄={rbar:.3f},a·R̄²={a * rbar ** 2:.4f}")
ak = np.array([season_fits[k]["a"] for k in S3]); sek = np.array([season_fits[k]["sd"] for k in S3])
wts = 1 / sek ** 2; abar = float(np.sum(wts * ak) / wts.sum())
Q = float(np.sum(wts * (ak - abar) ** 2))
tau2_season = max(0.0, (Q - 2) / (wts.sum() - (wts ** 2).sum() / wts.sum()))
loso = {k: a_of(all_states, [j for j in S3 if j != k])[0] for k in S3}
res["4a_structure"] = {"units": units, "season_fits": season_fits, "leave_one_season_out_a": loso,
                       "heterogeneity": {"Q": Q, "df": 2, "p": float(sps.chi2.sf(Q, 2)), "a_fixed_effect": abar,
                                         "tau2_between_season_DL": tau2_season,
                                         "sd_between_season_a": float(np.std(ak, ddof=1)),
                                         "mean_within_season_sd": float(sek.mean()),
                                         "relSE_floor_sqrt_2_over_S_minus_1": float(np.sqrt(2 / 2)),
                                         "relSE_floor_sqrt_2_over_S": float(np.sqrt(2 / 3))}}
log(f"  季间异质性 Q={Q:.2f}(df=2,p={sps.chi2.sf(Q, 2):.3g});留一季 a={loso}")
update("R4_vR_scale_periods", res)

# ---------------------------------------------------------------- 4b 聚类口径
a_full, rbar_full, _, _ = a_of(all_states, S3)
bt_state, _ = boot_a(all_states, S3, B, tag="州聚类")
# 州×季
ss_keys = sorted({(s, k) for s in all_states for k in S3 if (per_state[s]["sk"] == k).any()})
bt_ss = np.empty(B)
for i in range(B):
    draw = [ss_keys[j] for j in rng.choice(len(ss_keys), size=len(ss_keys), replace=True)]
    gs = [per_state[s]["G"][per_state[s]["sk"] == k] for s, k in draw]
    ds = [per_state[s]["D"][per_state[s]["sk"] == k] for s, k in draw]
    bt_ss[i] = fit(np.concatenate(gs), np.concatenate(ds))[1]
# 季:3 簇精确枚举
enum = []
for combo in product(S3, repeat=3):
    gs = []; ds = []
    for k in combo:
        for s in all_states:
            m = per_state[s]["sk"] == k
            if m.any():
                gs.append(per_state[s]["G"][m]); ds.append(per_state[s]["D"][m])
    enum.append(fit(np.concatenate(gs), np.concatenate(ds))[1])
enum = np.array(enum)
res["4b_cluster_units"] = {
    "a_point": a_full, "state_51": ci(bt_state), "state_season": {"n_clusters": len(ss_keys), **ci(bt_ss)},
    "season_3_exact_enumeration": {"n_ordered_draws": 27, "n_distinct_multisets": 10,
                                   "values_min_max": [float(enum.min()), float(enum.max())],
                                   "pct95_of_27": [float(np.percentile(enum, 2.5)), float(np.percentile(enum, 97.5))],
                                   "sd": float(enum.std(ddof=0))}}
log(f"  聚类口径 a 宽度:州 {res['4b_cluster_units']['state_51']['width']:.4f},州×季 {res['4b_cluster_units']['state_season']['width']:.4f},"
    f"季(27 枚举)范围 {enum.min():.4f}–{enum.max():.4f}")
update("R4_vR_scale_periods", res)

# ---------------------------------------------------------------- 4c 规模对期数
mean_D = {s: float(per_state[s]["D"][np.isin(per_state[s]["sk"], S3)].mean()) for s in all_states}
med = float(np.median(list(mean_D.values())))
groups = {"all": all_states, "large": [s for s in all_states if mean_D[s] > med],
          "small": [s for s in all_states if mean_D[s] <= med]}
scale = {"median_state_mean_D": med}
for gname, gst in groups.items():
    Ng = int(sum(np.isin(per_state[s]["sk"], S3).sum() for s in gst))
    Dg = np.concatenate([per_state[s]["D"][np.isin(per_state[s]["sk"], S3)] for s in gst])
    a0 = a_of(gst, S3)[0]
    base, _ = boot_a(gst, S3, B, tag=f"{gname} 基线")
    out = {"n_states": len(gst), "N": Ng, "D_median": float(np.median(Dg)), "D_harmonic_mean": float(1 / np.mean(1 / Dg)),
           "a_point": a0, "baseline": ci(base)}
    for p in (0.5, 0.25):
        bt, dr = boot_a(gst, S3, B, p=p, tag=f"{gname} 稀疏 p={p}")
        out[f"thin_p{p}"] = {**ci(bt), "mean_rows_dropped_share": dr,
                             "width_ratio_vs_baseline": ci(bt)["width"] / out["baseline"]["width"]}
    for frac in (2, 4):
        nd = max(2, len(gst) // frac)
        bt, _ = boot_a(gst, S3, B, n_draw=nd, tag=f"{gname} S/{frac}")
        out[f"states_div{frac}"] = {**ci(bt), "n_draw": nd,
                                    "width_ratio_vs_baseline": ci(bt)["width"] / out["baseline"]["width"],
                                    "sqrt_rule": float(np.sqrt(len(gst) / nd))}
    scale[gname] = out
    log(f"  [{gname}] 州 {len(gst)},N={Ng},D 中位数 {np.median(Dg):.1f};宽度 基线 {out['baseline']['width']:.4f};"
        f"稀疏0.5 ×{out['thin_p0.5']['width_ratio_vs_baseline']:.3f};稀疏0.25 ×{out['thin_p0.25']['width_ratio_vs_baseline']:.3f};"
        f"S/2 ×{out['states_div2']['width_ratio_vs_baseline']:.3f};S/4 ×{out['states_div4']['width_ratio_vs_baseline']:.3f}")
    res["4c_scale_vs_periods"] = scale
    update("R4_vR_scale_periods", res)
L = scale["large"]
crit = {"large_thin0.5_width_increase_le_15pct": bool(L["thin_p0.5"]["width_ratio_vs_baseline"] <= 1.15),
        "large_halfT_width_increase_ge_30pct": bool(L["states_div2"]["width_ratio_vs_baseline"] >= 1.30)}
crit["supports_prop_B"] = crit["large_thin0.5_width_increase_le_15pct"] and crit["large_halfT_width_increase_ge_30pct"]
crit["large_over_small_baseline_width"] = L["baseline"]["width"] / scale["small"]["baseline"]["width"]
scale["criteria"] = crit
log("  判据:", crit)

# ---- 加季数 ----
by_nseason = {}
for nsz in (1, 2, 3):
    ws = []
    for combo in combinations(S3, nsz):
        stc = sorted(s for s in per_state if np.isin(per_state[s]["sk"], combo).any())
        bt, _ = boot_a(stc, list(combo), B // 2)
        ws.append({"seasons": list(combo), "a": a_of(stc, list(combo))[0], **ci(bt)})
    by_nseason[str(nsz)] = {"combos": ws, "mean_width": float(np.mean([x["width"] for x in ws]))}
st4 = sorted(s for s in per_state if np.isin(per_state[s]["sk"], [0, 1, 2, 3]).any())
bt4, _ = boot_a(st4, [0, 1, 2, 3], B // 2)
by_nseason["4_incl_out_of_sample"] = {"a": a_of(st4, [0, 1, 2, 3])[0], **ci(bt4)}
res["4c_scale_vs_periods"] = scale
res["4c_number_of_seasons"] = by_nseason

# ---- 事后分析(未预注册,报告中标明):①稀疏方差外推 Var(a)=alpha+beta/p,p→∞ 为无限规模;②季层面随机效应 ----
post = {}
for gname in ("all", "large"):
    o = scale[gname]
    ps = np.array([1.0, 0.5, 0.25])
    v = np.array([o["baseline"]["sd_robust_iqr"], o["thin_p0.5"]["sd_robust_iqr"], o["thin_p0.25"]["sd_robust_iqr"]]) ** 2
    X = np.column_stack([np.ones(3), 1 / ps])
    alpha, beta = np.linalg.lstsq(X, v, rcond=None)[0]
    post[f"thinning_extrapolation_{gname}"] = {
        "var_robust": v.tolist(), "alpha_infinite_scale": float(alpha), "beta": float(beta),
        "sd_ratio_infinite_scale_vs_current": float(np.sqrt(max(alpha, 0) / (alpha + beta))),
        "sd_ratio_double_scale_vs_current": float(np.sqrt((alpha + beta / 2) / (alpha + beta))),
        "sd_ratio_double_states_vs_current_sqrt_rule": float(np.sqrt(0.5))}
for lab, ks in (("S3", [0, 1, 2]), ("S4_incl_out_of_sample", [0, 1, 2, 3])):
    ak = np.array([season_fits[k]["a"] for k in ks]); se = np.array([season_fits[k]["sd"] for k in ks])
    wt = 1 / se ** 2; fe = np.sum(wt * ak) / wt.sum(); Qk = np.sum(wt * (ak - fe) ** 2); S_ = len(ks)
    t2 = max(0.0, (Qk - (S_ - 1)) / (wt.sum() - (wt ** 2).sum() / wt.sum()))
    wr = 1 / (se ** 2 + t2); re = np.sum(wr * ak) / wr.sum(); se_re = np.sqrt(1 / wr.sum())
    tq = sps.t.ppf(0.975, S_ - 1)
    se_inf = np.sqrt(t2 / S_)                       # 季内抽样误差为 0(无限规模)时
    post[f"season_random_effects_{lab}"] = {
        "S": S_, "a_k": ak.tolist(), "within_se_k": se.tolist(), "Q": float(Qk), "p": float(sps.chi2.sf(Qk, S_ - 1)),
        "tau2_between": float(t2), "sd_between": float(np.sqrt(t2)), "a_RE": float(re), "se_RE": float(se_re),
        "ci95_t_df": [float(re - tq * se_re), float(re + tq * se_re)], "width_t": float(2 * tq * se_re),
        "width_t_infinite_scale": float(2 * tq * se_inf),
        "width_state_cluster_conditional_on_seasons": res["4b_cluster_units"]["state_51"]["width"],
        "relSE_between_variance_floor_sqrt_2_over_S_minus_1": float(np.sqrt(2 / (S_ - 1)))}
res["4d_post_hoc"] = post
log("  事后分析:", post)
log("  季数 → 平均宽度:", {k: (v["mean_width"] if "mean_width" in v else v["width"]) for k, v in by_nseason.items()})
update("R4_vR_scale_periods", res)
log.close()
