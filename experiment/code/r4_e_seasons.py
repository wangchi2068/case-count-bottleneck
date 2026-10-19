"""r4 E:第 4 季(2025–26)纳入季节随机效应;按推论 2 报 S=3 与 S=4 的相对标准误下界。

输入:r3_results.json 的 R4_vR_scale_periods(各季拟合 4a_structure.season_fits 与 DL 随机效应 4d_post_hoc)。
新增:τ² 的 Q-profile 95% 区间(Viechtbauer 2007)与 t_{S-1} 区间复算。预注册:analysis/r4_preregistration.md 第 6 节。
"""
import json

import numpy as np
from scipy import optimize, stats

from common import EXP
from r4_common import r4_update

R4S = json.loads((EXP / "analysis/r3_results.json").read_text(encoding="utf-8"))["R4_vR_scale_periods"]
sf = R4S["4a_structure"]["season_fits"]
ph = R4S["4d_post_hoc"]
LAB = {0: "2022–23(日历窗口)", 1: "2023–24(日历窗口)", 2: "2024–25(日历窗口)", 3: "2025–26(增长期规则,样本外)"}


def dl(a, se):
    w = 1 / se ** 2
    mu_f = np.sum(w * a) / w.sum()
    Q = float(np.sum(w * (a - mu_f) ** 2))
    S = len(a)
    tau2 = max(0.0, (Q - (S - 1)) / (w.sum() - np.sum(w ** 2) / w.sum()))
    ws = 1 / (se ** 2 + tau2)
    mu = float(np.sum(ws * a) / ws.sum())
    se_mu = float(np.sqrt(1 / ws.sum()))
    tq = stats.t.ppf(0.975, S - 1)
    return {"S": S, "Q": Q, "p_Q": float(stats.chi2.sf(Q, S - 1)), "tau2": tau2, "a_RE": mu, "se_RE": se_mu,
            "ci95_t": [mu - tq * se_mu, mu + tq * se_mu], "I2": max(0.0, (Q - (S - 1)) / Q)}


def q_profile(a, se, alpha=0.05):
    """Q_gen(τ²) = Σ w_i(τ²)(a_i − μ̂(τ²))² ~ χ²_{S−1};反解得 τ² 区间。"""
    S = len(a)

    def Qgen(t2):
        w = 1 / (se ** 2 + t2)
        mu = np.sum(w * a) / w.sum()
        return np.sum(w * (a - mu) ** 2)

    lo_c, hi_c = stats.chi2.ppf([1 - alpha / 2, alpha / 2], S - 1)
    f_lo = lambda t2: Qgen(t2) - lo_c
    f_hi = lambda t2: Qgen(t2) - hi_c
    big = 10.0
    lo = 0.0 if f_lo(0) < 0 else optimize.brentq(f_lo, 0, big)
    hi = 0.0 if f_hi(0) < 0 else optimize.brentq(f_hi, 0, big)
    return [float(lo), float(hi)]


out = {"seasons": [], "notes": "第 4 季用增长期规则窗口(全国 G≥1.05 的周),前三季为用户日历窗口;合并时窗口规则不同,作敏感性。"}
for k in range(4):
    s = sf[str(k)]
    out["seasons"].append({"season": LAB[k], "N": s["N"], "n_states": s["n_states"], "a": s["a"], "R_bar": s["R_bar"],
                           "pct95": s["pct95"], "se_state_cluster": s["sd"]})
for S, key in ((3, "season_random_effects_S3"), (4, "season_random_effects_S4_incl_out_of_sample")):
    a = np.array([sf[str(k)]["a"] for k in range(S)])
    se = np.array([sf[str(k)]["sd"] for k in range(S)])
    r = dl(a, se)
    r["tau2_qprofile95"] = q_profile(a, se)
    r["r3_check_abs_diff"] = {"a_RE": abs(r["a_RE"] - ph[key]["a_RE"]), "tau2": abs(r["tau2"] - ph[key]["tau2_between"]),
                              "Q": abs(r["Q"] - ph[key]["Q"])}
    r["relSE_lower_bound_known_means_sqrt_2_over_S"] = float(np.sqrt(2 / S))
    r["relSE_lower_bound_sample_mean_sqrt_2_over_S_minus_1"] = float(np.sqrt(2 / (S - 1)))
    r["ci95_width_t"] = r["ci95_t"][1] - r["ci95_t"][0]
    out[f"S{S}"] = r
    print(S, json.dumps({k: v for k, v in r.items()}, ensure_ascii=False, default=float))
r4_update("E_season_random_effects", out)
