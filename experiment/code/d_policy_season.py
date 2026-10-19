"""分析 D:填报制度期 × 流行季,控制季节构成后的离散度比较。

口径:全面板(D_t>=5,N=10303);制度期按 D_t 所在周;流行季 = 10–3 月。
离散度:
- G 的 IQR(正文口径);
- log G 的 IQR,log G 取连续性校正 log((C_{t+1}+0.5)/(D_t+0.5)),消除不同增长水平下 IQR 随均值伸缩的影响;
区间:按州聚类 Bootstrap(51 州有放回,整州全部州周一起抽,6 格及差值在同一次抽样内算),百分位 95%。
季节构成控制:
① 重加权:季内/季外按全面板的季内占比重新加权后计算各期加权 IQR;
② 同月份对照:第二期 5–9 月 vs 其他年份 5–9 月;第二期 10 月 vs 其他年份 10 月(另做只限这 26 个州的版本);
③ 分位数回归:y=|log G − 当月全样本中位数|,τ=0.5,协变量 期别哑变量 + 流行季 + log D(扩展版加 第二期×流行季);
   用 HiGHS 线性规划求解(无 statsmodels),州聚类 Bootstrap 给区间。
敏感性:剔除 t-2..t+1 任一周住院数缺失的州周。
"""
import sys
import time

import numpy as np
import pandas as pd
from scipy.optimize import linprog

from common import SEED, Log, build_panel, iqr, load_raw, update_results

B = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
B_QR = int(sys.argv[2]) if len(sys.argv) > 2 else 500
log = Log("d_policy_season")
rng = np.random.default_rng(SEED + 4)

p = build_panel(load_raw())
p["logg"] = np.log((p.C_next + 0.5) / (p.D_t + 0.5))
p["logD"] = np.log(p.D_t)
p["year"] = p.week_end.dt.year
med_month = p.groupby("month").logg.median()
p["absdev"] = np.abs(p.logg - p.month.map(med_month))
states = np.array(sorted(p.state.unique()))
rows_of = {s: np.flatnonzero(p.state.to_numpy() == s) for s in states}
PI_IN = float(p.in_season.mean())
log(f"全面板 N={len(p)},州 {len(states)},季内占比 {PI_IN:.3f};log G 连续性校正后 G=0 的 {int((p.C_next == 0).sum())} 个州周可用")


def w_quantile(x, w, q):
    o = np.argsort(x)
    x, w = x[o], w[o]
    cw = (np.cumsum(w) - 0.5 * w) / w.sum()
    return np.interp(q, cw, x)


def w_iqr(x, w):
    return float(w_quantile(x, w, 0.75) - w_quantile(x, w, 0.25))


def cell_stats(q):
    """一次(原样本或重抽样本)上的全部统计量,返回扁平字典。"""
    v = {}
    per, ins = q.period.to_numpy(), q.in_season.to_numpy()
    g, lg = q.g.to_numpy(), q.logg.to_numpy()
    for k in (1, 2, 3):
        for s_, lab in ((True, "in"), (False, "out")):
            m = (per == k) & (ins == s_)
            v[f"P{k}_{lab}_iqr"] = iqr(g[m]) if m.sum() >= 4 else np.nan
            v[f"P{k}_{lab}_logiqr"] = iqr(lg[m]) if m.sum() >= 4 else np.nan
        m = per == k
        v[f"P{k}_all_iqr"] = iqr(g[m])
        v[f"P{k}_all_logiqr"] = iqr(lg[m])
        # ① 重加权:季内/季外调成全面板占比
        pin = ins[m].mean()
        if 0 < pin < 1:
            w = np.where(ins[m], PI_IN / pin, (1 - PI_IN) / (1 - pin))
            v[f"P{k}_rw_iqr"] = w_iqr(g[m], w)
            v[f"P{k}_rw_logiqr"] = w_iqr(lg[m], w)
        else:
            v[f"P{k}_rw_iqr"] = v[f"P{k}_rw_logiqr"] = np.nan
    # ② 同月份对照
    mon, yr = q.month.to_numpy(), q.year.to_numpy()
    summer = np.isin(mon, [5, 6, 7, 8, 9])
    for lab, m in (("P2_MaySep", (per == 2) & summer), ("P1_MaySep", (per == 1) & summer), ("P3_MaySep", (per == 3) & summer),
                   ("P2_Oct", (per == 2) & (mon == 10)), ("P1_Oct", (per == 1) & (mon == 10)), ("P3_Oct", (per == 3) & (mon == 10))):
        v[f"{lab}_iqr"] = iqr(g[m]) if m.sum() >= 4 else np.nan
        v[f"{lab}_logiqr"] = iqr(lg[m]) if m.sum() >= 4 else np.nan
    st26 = q.state.isin(OCT_STATES).to_numpy()
    for lab, m in (("P2_Oct26", (per == 2) & (mon == 10) & st26), ("P1_Oct26", (per == 1) & (mon == 10) & st26),
                   ("P3_Oct26", (per == 3) & (mon == 10) & st26)):
        v[f"{lab}_iqr"] = iqr(g[m]) if m.sum() >= 4 else np.nan
        v[f"{lab}_logiqr"] = iqr(lg[m]) if m.sum() >= 4 else np.nan
    for base in ("iqr", "logiqr"):
        for a_, b_ in (("P2_in", "P1_in"), ("P2_in", "P3_in"), ("P2_out", "P1_out"), ("P2_out", "P3_out"),
                       ("P2_all", "P1_all"), ("P2_all", "P3_all"), ("P2_rw", "P1_rw"), ("P2_rw", "P3_rw"),
                       ("P2_MaySep", "P1_MaySep"), ("P2_MaySep", "P3_MaySep"), ("P2_Oct", "P1_Oct"), ("P2_Oct", "P3_Oct"),
                       ("P2_Oct26", "P1_Oct26"), ("P2_Oct26", "P3_Oct26")):
            v[f"diff_{a_}-{b_}_{base}"] = v[f"{a_}_{base}"] - v[f"{b_}_{base}"]
    return v


OCT_STATES = set(p[(p.period == 2) & (p.month == 10)].state)


def counts(q):
    out = {}
    for k in (1, 2, 3):
        for s_, lab in ((True, "in"), (False, "out")):
            x = q[(q.period == k) & (q.in_season == s_)]
            out[f"P{k}_{lab}"] = {"N": len(x), "n_states": int(x.state.nunique()), "mean_g": float(x.g.mean()),
                                  "median_D": float(x.D_t.median()), "n_any_missing": int(x.any_missing.sum())}
    for lab, m in (("P2_MaySep", (q.period == 2) & q.month.isin([5, 6, 7, 8, 9])), ("P1_MaySep", (q.period == 1) & q.month.isin([5, 6, 7, 8, 9])),
                   ("P3_MaySep", (q.period == 3) & q.month.isin([5, 6, 7, 8, 9])), ("P2_Oct", (q.period == 2) & (q.month == 10)),
                   ("P1_Oct", (q.period == 1) & (q.month == 10)), ("P3_Oct", (q.period == 3) & (q.month == 10)),
                   ("P2_Oct26", (q.period == 2) & (q.month == 10) & q.state.isin(OCT_STATES)),
                   ("P1_Oct26", (q.period == 1) & (q.month == 10) & q.state.isin(OCT_STATES)),
                   ("P3_Oct26", (q.period == 3) & (q.month == 10) & q.state.isin(OCT_STATES))):
        x = q[m]
        out[lab] = {"N": len(x), "n_states": int(x.state.nunique()), "mean_g": float(x.g.mean()), "median_D": float(x.D_t.median())}
    return out


def boot_cells(q, nb, tag):
    st_ = np.array(sorted(q.state.unique()))
    ro = {s: np.flatnonzero(q.state.to_numpy() == s) for s in st_}
    point = cell_stats(q)
    keys = list(point)
    acc = np.empty((nb, len(keys)))
    t0 = time.time()
    for i in range(nb):
        draw = rng.choice(st_, size=len(st_), replace=True)
        qq = q.iloc[np.concatenate([ro[s] for s in draw])]
        v = cell_stats(qq)
        acc[i] = [v[k] for k in keys]
    res = {}
    for j, k in enumerate(keys):
        x = acc[:, j][np.isfinite(acc[:, j])]
        lo, hi = np.percentile(x, [2.5, 97.5]) if x.size else (np.nan, np.nan)
        res[k] = {"point": float(point[k]), "pct95": [float(lo), float(hi)], "boot_sd": float(x.std(ddof=1)) if x.size > 1 else np.nan,
                  "n_finite": int(x.size)}
        if k.startswith("diff_"):
            res[k]["frac_gt0"] = float(np.mean(x > 0))
    log(f"  [{tag}] Bootstrap B={nb} 用时 {time.time() - t0:.0f} s")
    return res


# ---- 主表 ----
cnt = counts(p)
for k, v in cnt.items():
    log(f"  {k}: N={v['N']}, 州数={v['n_states']}, 均值 G={v['mean_g']:.3f}, D 中位数={v['median_D']:.1f}")
cells = boot_cells(p, B, "主样本")
for k, v in cells.items():
    if k.endswith("_iqr") or k.endswith("_logiqr"):
        extra = f",P(差>0)={v['frac_gt0']:.3f}" if "frac_gt0" in v else ""
        log(f"  {k:36s} {v['point']:.3f} [{v['pct95'][0]:.3f}, {v['pct95'][1]:.3f}]{extra}")
update_results("D_policy_season", {"design": __doc__, "B": B, "pi_in_season_pooled": PI_IN, "counts": cnt, "cells": cells,
                                   "oct_p2_states": sorted(OCT_STATES)})

# ---- 敏感性:剔除含缺失周的州周 ----
q = p[~p.any_missing].reset_index(drop=True)
cells_nm = boot_cells(q, 1000, "剔除缺失")
log(f"  剔除含缺失周后 N={len(q)}(剔除 {int(p.any_missing.sum())})")
for k in ("P1_in_iqr", "P2_in_iqr", "P3_in_iqr", "P1_all_iqr", "P2_all_iqr", "P3_all_iqr", "diff_P2_in-P1_in_iqr", "diff_P2_in-P3_in_iqr"):
    v = cells_nm[k]
    log(f"  {k:28s} {v['point']:.3f} [{v['pct95'][0]:.3f}, {v['pct95'][1]:.3f}]")
update_results("D_policy_season_sens_no_missing", {"N": len(q), "n_dropped": int(p.any_missing.sum()), "counts": counts(q), "cells": cells_nm})


# ---- ③ 分位数回归 ----
def qreg(y, X, tau=0.5):
    """对偶形式:max y'd,s.t. X'd=(1-τ)X'1,0<=d<=1;系数 = −等式约束的对偶乘子(与原问题解已核对一致,快约 5 倍)。"""
    r = linprog(-y, A_eq=X.T, b_eq=(1 - tau) * X.sum(0), bounds=(0, 1), method="highs")
    if r.status != 0:
        raise RuntimeError(r.message)
    return -r.eqlin.marginals


def design(q, inter):
    cols = {"const": np.ones(len(q)), "P2": (q.period == 2).astype(float).to_numpy(), "P3": (q.period == 3).astype(float).to_numpy(),
            "season": q.in_season.astype(float).to_numpy(), "logD": (q.logD - np.log(50)).to_numpy()}
    if inter:
        cols["P2xseason"] = cols["P2"] * cols["season"]
        cols["P3xseason"] = cols["P3"] * cols["season"]
    return np.column_stack(list(cols.values())), list(cols)


qr_res = {}
for inter in (False, True):
    for tau in (0.5, 0.75):
        tag = f"tau{tau}_{'inter' if inter else 'main'}"
        X, names = design(p, inter)
        y = p.absdev.to_numpy()
        t0 = time.time()
        beta = qreg(y, X, tau)
        t1 = time.time() - t0
        nb = B_QR if (tau == 0.5) else max(200, B_QR // 2)
        bb = np.empty((nb, len(names)))
        for i in range(nb):
            draw = rng.choice(states, size=len(states), replace=True)
            idx = np.concatenate([rows_of[s] for s in draw])
            bb[i] = qreg(y[idx], X[idx], tau)
        ci = np.percentile(bb, [2.5, 97.5], axis=0)
        qr_res[tag] = {"tau": tau, "interaction": inter, "B": nb, "seconds_per_fit": t1,
                       "coef": {n: {"est": float(b), "pct95": [float(ci[0, j]), float(ci[1, j])], "frac_gt0": float(np.mean(bb[:, j] > 0))}
                                for j, (n, b) in enumerate(zip(names, beta))}}
        log(f"  分位数回归 {tag}(B={nb},单次 {t1:.2f} s):" + "; ".join(
            f"{n}={b:.4f} [{ci[0, j]:.4f}, {ci[1, j]:.4f}]" for j, (n, b) in enumerate(zip(names, beta))))
        update_results("D_quantile_regression", {"y": "|log((C_{t+1}+0.5)/(D_t+0.5)) − 当月全样本中位数|", "logD_centered_at": "log 50",
                                                 "fits": qr_res})
log.close()
