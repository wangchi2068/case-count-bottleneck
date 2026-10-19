"""r3 分析 0–3:复现门;报告率代理的方差(横截面/州内周间/进入截距的 pi);报告调整估计量与 Delta a;截距比。

预注册:analysis/r3_preregistration.md 第 0–3 节。用法:python3 r3_a_reporting.py [B]
"""
import json
import sys

import numpy as np
import pandas as pd

from common import Log, RESULTS
from r3_common import (EARLY, SEED, SPECS, WEIGHTS, F_factor, build_rows, cluster_bootstrap, cluster_index,
                       early_index, fit, load, series, summarize, update)

B = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
log = Log("r3_a_reporting")
rng = np.random.default_rng(SEED)
prev = json.loads(RESULTS.read_text(encoding="utf-8"))

df = load("flu")
ser = series(df)
in_early = lambda wk: early_index(wk) >= 0

# ---------------------------------------------------------------- 0 复现门
rows = {s: build_rows(ser, WEIGHTS[s], in_early) for s in SPECS}
ref = {it["item"]: it["reference"] for it in prev["A_reproduction"]["items"]}
gate = []


def sig3(x):
    return float(f"{x:.3g}")


fits0 = {}
for s in SPECS:
    r = rows[s]
    rbar, a, b = fit(r.G.to_numpy(), r.D.to_numpy())
    fits0[s] = (rbar, a, b)
    for lab, ours in (("初期 N", len(r)), ("R_bar", rbar), ("a", a), ("b", b), ("b/a", b / a)):
        key = f"[{s}] {lab}"
        rv = ref[key]
        ok = (int(ours) == int(rv)) if lab == "初期 N" else (sig3(ours) == sig3(rv))
        gate.append({"item": key, "ours": ours, "reference": rv, "match_3sf": bool(ok)})
        log(f"[{'一致' if ok else '不一致'}] {key}: {ours:.6g} | 上一轮 {rv:.6g}")
q1 = fits0["single_1w"][1] / fits0["original"][1]
q2 = fits0["equal_3w"][1] / fits0["original"][1]
for lab, ours, rv in (("q1", q1, prev["B_bootstrap"]["stats"]["q1"]["point"]),
                      ("q2", q2, prev["B_bootstrap"]["stats"]["q2"]["point"])):
    ok = sig3(ours) == sig3(rv)
    gate.append({"item": lab, "ours": ours, "reference": rv, "match_3sf": bool(ok)})
    log(f"[{'一致' if ok else '不一致'}] {lab}: {ours:.6g} | 上一轮 {rv:.6g}")
n_ok = sum(g["match_3sf"] for g in gate)
update("R0_reproduction_gate", {"n_match": n_ok, "n_items": len(gate), "items": gate})
if n_ok != len(gate):
    log("复现门未通过,停止"); log.close(); sys.exit(1)
log(f"复现门 {n_ok}/{len(gate)} 通过")

# ---------------------------------------------------------------- 1 报告率代理的方差
w0 = np.asarray(WEIGHTS["original"])


def proxy_variances(sub_df: pd.DataFrame, proxy="h") -> dict:
    """sub_df:州周长表(含 state, week_end, proxy);只用 proxy>0 的州周。"""
    x = sub_df[np.isfinite(sub_df[proxy]) & (sub_df[proxy] > 0)].copy()
    if len(x) < 20:
        return {"n": int(len(x))}
    x["rel_cross"] = x[proxy] / x.groupby("week_end")[proxy].transform("mean")
    tau_cross = float(x.groupby("week_end").rel_cross.var(ddof=0).mean())
    x["rel_within"] = x[proxy] / x.groupby("state")[proxy].transform("mean")
    tau_within = float(x.groupby("state").rel_within.var(ddof=0).mean())
    x["lh"] = np.log(x[proxy]); x["lh"] -= x.groupby("state").lh.transform("mean")
    x = x.sort_values(["state", "week_end"])
    x["lh_lag"] = x.groupby("state").lh.shift(1)
    ok = x.lh_lag.notna()
    num = float((x.lh[ok] * x.lh_lag[ok]).sum()); den = float((x.lh[ok] ** 2).sum())
    psi = num / den if den > 0 else float("nan")
    return {"n_state_weeks": int(len(x)), "n_states": int(x.state.nunique()),
            "h_mean": float(x[proxy].mean()), "h_sd": float(x[proxy].std()),
            "tau2_cross": tau_cross, "tau2_within": tau_within, "psi_hat_lag1": psi,
            "F_main_at_psi_hat": float(F_factor(w0, max(min(psi, 0.999), 0.0))) if np.isfinite(psi) else None,
            "pred_Vpi_from_tau2_within_F": float(tau_within * F_factor(w0, max(min(psi, 0.999), 0.0))) if np.isfinite(psi) else None}


def pi_summary(r: pd.DataFrame) -> dict:
    p = r.pi[np.isfinite(r.pi)].to_numpy()
    return {"N_rows": int(len(r)), "N_finite_pi": int(p.size), "V_pi": float(np.var(p - 1, ddof=1)),
            "E_pi": float(p.mean()), "q01_q50_q99": [float(v) for v in np.percentile(p, [1, 50, 99])],
            "share_abs_gt_0.05": float(np.mean(np.abs(p - 1) > 0.05)),
            "share_pi_eq_1": float(np.mean(np.abs(p - 1) < 1e-12))}


per_res = {}
full_rows = build_rows(ser, w0, lambda wk: True)
log(f"全面板(D>=5)行数 {len(full_rows)}(上一轮 10303)")
df["period"] = np.where(df.week_end <= pd.Timestamp("2024-04-30"), 1,
                        np.where(df.week_end < pd.Timestamp("2024-11-01"), 2, 3))
for k in (1, 2, 3):
    sub = df[df.period == k]
    rr = full_rows[full_rows.period == k]
    per_res[f"period{k}"] = {"weeks": [str(sub.week_end.min().date()), str(sub.week_end.max().date())],
                             "share_h_zero_or_missing": float(np.mean(~(sub.h > 0))),
                             "proxy_all_state_weeks": proxy_variances(sub),
                             "pi_in_panel_rows": pi_summary(rr),
                             "pi_in_panel_rows_numberproxy": pi_summary(build_rows(
                                 {s: z for s, z in ser.items()}, w0,
                                 lambda wk, k=k: (pd.Timestamp(wk) <= pd.Timestamp("2024-04-30")) if k == 1 else
                                 ((pd.Timestamp("2024-04-30") < pd.Timestamp(wk) < pd.Timestamp("2024-11-01")) if k == 2
                                  else pd.Timestamp(wk) >= pd.Timestamp("2024-11-01")), proxy="hn"))}
    pr = per_res[f"period{k}"]
    log(f"第{k}期:h 均值 {pr['proxy_all_state_weeks'].get('h_mean', float('nan')):.3f};τ²横截面 "
        f"{pr['proxy_all_state_weeks'].get('tau2_cross', float('nan')):.4g};τ²州内 {pr['proxy_all_state_weeks'].get('tau2_within', float('nan')):.4g};"
        f"ψ̂ {pr['proxy_all_state_weeks'].get('psi_hat_lag1', float('nan')):.3f};面板行 V_pi {pr['pi_in_panel_rows']['V_pi']:.4g}"
        f"(N={pr['pi_in_panel_rows']['N_finite_pi']});h=0/缺失占比 {pr['share_h_zero_or_missing']:.3f}")
early_df = df[[early_index(x) >= 0 for x in df.week_end]]
per_res["early_sample"] = {"proxy_all_state_weeks": proxy_variances(early_df),
                           "pi_in_rows": pi_summary(rows["original"]),
                           "pi_in_rows_numberproxy": pi_summary(build_rows(ser, w0, in_early, proxy="hn"))}
pe = per_res["early_sample"]
log(f"流行初期:V_pi={pe['pi_in_rows']['V_pi']:.5g},E pi={pe['pi_in_rows']['E_pi']:.4f};医院数代理 V_pi={pe['pi_in_rows_numberproxy']['V_pi']:.5g};"
    f"τ²横截面 {pe['proxy_all_state_weeks']['tau2_cross']:.4g},τ²州内 {pe['proxy_all_state_weeks']['tau2_within']:.4g},ψ̂ {pe['proxy_all_state_weeks']['psi_hat_lag1']:.3f}")
update("R1_reporting_proxy_variance", per_res)

# ---------------------------------------------------------------- 2–3 报告调整估计量 + 截距比(Bootstrap)
rows_hn = build_rows(ser, w0, in_early, proxy="hn")
data = {}
for s in SPECS:
    r = rows[s]
    data[s] = {"G": r.G.to_numpy(), "Gs": r.Gstar.to_numpy(), "D": r.D.to_numpy(), "Ds": r.Dstar.to_numpy(),
               "pi": r.pi.to_numpy(), "valid": r.valid_h.to_numpy(), "state": r.state.to_numpy()}
data["hn"] = {"G": rows_hn.G.to_numpy(), "Gs": rows_hn.Gstar.to_numpy(), "D": rows_hn.D.to_numpy(),
              "valid": rows_hn.valid_h.to_numpy(), "state": rows_hn.state.to_numpy(), "pi": rows_hn.pi.to_numpy()}
invalid = {k: int((~v["valid"]).sum()) for k, v in data.items()}
log(f"代理缺失/为 0 的行数:{invalid}")
for k in data:
    keep = data[k]["valid"]
    for f in list(data[k]):
        data[k][f] = data[k][f][keep]

NAMES = []
for s in SPECS:
    NAMES += [f"rbar_{s}", f"a_{s}", f"b_{s}", f"rbarS_{s}", f"aS_{s}", f"bS_{s}", f"dA_{s}", f"aSDs_{s}"]
NAMES += ["q1", "q2", "q1S", "q2S", "V_pi", "E_pi", "beta_logG_logpi", "aS_hn", "dA_hn", "dA_pred",
          "dA_minus_pred"]


def stat_fn(rb):
    v = {}
    for s in SPECS:
        d = data[s]; i = rb[s]
        g, gs, D, Ds = d["G"][i], d["Gs"][i], d["D"][i], d["Ds"][i]
        v[f"rbar_{s}"], v[f"a_{s}"], v[f"b_{s}"] = fit(g, D)
        v[f"rbarS_{s}"], v[f"aS_{s}"], v[f"bS_{s}"] = fit(gs, D)
        v[f"dA_{s}"] = v[f"a_{s}"] - v[f"aS_{s}"]
        v[f"aSDs_{s}"] = fit(gs, Ds)[1]
    v["q1"] = v["a_single_1w"] / v["a_original"]; v["q2"] = v["a_equal_3w"] / v["a_original"]
    v["q1S"] = v["aS_single_1w"] / v["aS_original"]; v["q2S"] = v["aS_equal_3w"] / v["aS_original"]
    i = rb["original"]; p = data["original"]["pi"][i]; g = data["original"]["G"][i]
    v["V_pi"] = float(np.var(p - 1, ddof=1)); v["E_pi"] = float(p.mean())
    pos = g > 0
    x = np.log(p[pos]); y = np.log(g[pos])
    v["beta_logG_logpi"] = float(np.cov(x, y, ddof=1)[0, 1] / np.var(x, ddof=1))
    j = rb["hn"]; dh = data["hn"]
    v["aS_hn"] = fit(dh["Gs"][j], dh["D"][j])[1]
    v["dA_hn"] = fit(dh["G"][j], dh["D"][j])[1] - v["aS_hn"]
    v["dA_pred"] = v["V_pi"] * (1 + v["a_original"]) / v["E_pi"] ** 2
    v["dA_minus_pred"] = v["dA_original"] - v["dA_pred"]
    return np.array([v[k] for k in NAMES])


states = sorted(set(data["original"]["state"]))
idx = {k: cluster_index(data[k]["state"]) for k in data}
theta, boot, jack = cluster_bootstrap(stat_fn, states, idx, B, rng, progress=f"r3_a_boot_B{B}_progress")
np.savez_compressed(f"{__import__('common').EXP}/data/r3_a_boot.npz", names=np.array(NAMES), theta=theta, boot=boot, jack=jack)
res = summarize(NAMES, theta, boot, jack)
for k in NAMES:
    r = res[k]
    log(f"  {k:18s} 点 {r['point']:.5g} | 百分位 [{r['pct95'][0]:.5g}, {r['pct95'][1]:.5g}] | BCa [{r['bca95'][0]:.5g}, {r['bca95'][1]:.5g}]")

# ---- 判据 ----
dA = res["dA_original"]; rbar = res["rbar_original"]["point"]; a0 = res["a_original"]["point"]
excess_scn = a0 - 0.08 / rbar ** 2
excess_ar1 = a0 - 0.058
d1 = dA["bca95"][0] > 0 and dA["point"] >= 0.02
upper = max(dA["bca95"][1], 0.0)
psi_e = per_res["early_sample"]["proxy_all_state_weeks"]["psi_hat_lag1"]
F_e = float(F_factor(w0, max(min(psi_e, 0.999), 0.0)))
tau2w_upper = upper / F_e
verdict = {
    "criterion_D1_detectable": bool(d1),
    "verdict": "D1:报告成分有可检出贡献" if d1 else "D2:可观测报告成分不解释截距超出",
    "dA_point": dA["point"], "dA_bca95": dA["bca95"], "dA_pct95": dA["pct95"],
    "dA_pred_point": res["dA_pred"]["point"], "dA_pred_range_pre_registered": [-res["dA_pred"]["point"], res["dA_pred"]["point"]],
    "pred_in_dA_bca95": bool(dA["bca95"][0] <= res["dA_pred"]["point"] <= dA["bca95"][1]),
    "neg_pred_in_dA_bca95": bool(dA["bca95"][0] <= -res["dA_pred"]["point"] <= dA["bca95"][1]),
    "upper_bound_obs_reporting_contribution_to_a": upper,
    "excess_vs_scenario_vR0.08": excess_scn, "excess_after_ar1_0.058": excess_ar1,
    "max_share_of_excess_scn": upper / excess_scn, "max_share_of_excess_ar1": upper / excess_ar1,
    "psi_hat_early": psi_e, "F_main_at_psi_hat": F_e,
    "tau2_w_obs_upper": tau2w_upper, "tau_w_obs_upper_cv": float(np.sqrt(tau2w_upper)),
    "vH_obs_over_Rbar2_upper": tau2w_upper * (1 + 0.08 / rbar ** 2),
    "needed_cv_if_all_excess_iid": float(np.sqrt(excess_scn / F_factor(w0, 0.0))),
}
sig = {"q1_range_pure_report": [0.883, 1.338], "q2_range_pure_report": [0.892, 1.373]}
for k, rng_ in (("q1", sig["q1_range_pure_report"]), ("q2", sig["q2_range_pure_report"]),
                ("q1S", sig["q1_range_pure_report"]), ("q2S", sig["q2_range_pure_report"])):
    lo, hi = res[k]["bca95"]
    sig[f"{k}_disjoint_from_pure_report_range"] = bool(hi < rng_[0] or lo > rng_[1])
log("判据:", json.dumps(verdict, ensure_ascii=False))
log("截距比:", json.dumps(sig, ensure_ascii=False))
update("R2_adjusted_estimator", {
    "design": f"州聚类 B={B}(种子 {SEED}),未调整与调整共用同一组重抽;BCa 加速度用留一州刀切;主代理 Percent Hospitals Reporting Influenza Admissions",
    "n_rows": {k: int(len(v["G"])) for k, v in data.items()}, "rows_dropped_invalid_proxy": invalid,
    "n_states": len(states), "stats": res, "verdict": verdict,
})
update("R3_intercept_ratio_signature", {k: (res[k] if k in res else v) for k, v in
                                        {"q1": None, "q2": None, "q1S": None, "q2S": None}.items()} | sig)
log.close()
