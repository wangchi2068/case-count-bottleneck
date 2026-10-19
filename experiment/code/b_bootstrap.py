"""分析 B:按州聚类 Bootstrap,给三种滞后权重下 a、b、b/a 与斜率比、截距比的区间。

做法:
- 以州为单位有放回抽 S 个州(S=流行初期样本中出现的州数),三种权重规格共用同一组抽样;
- 每次重估各规格的基准 R_bar 与迭代 FGLS(与 empirical_stats.json 同口径);
- 另记一个"R_bar 固定为全样本值"的主规格 b,用来对照用户仓库已有的 b 区间 [1.5019, 3.0161];
- 只保存每次重抽的统计量(B×K 的小矩阵),不保存重抽样本;
- 区间:95% 百分位 + BCa(加速度由留一州刀切估计);偏态:Bootstrap 分布的样本偏度与区间两侧长度比。
- 敏感性:以"州×流行季"为聚类单位(153 个簇)再抽 B_sens 次。

用法:python3 b_bootstrap.py [B] [B_sens]
"""
import sys
import time

import numpy as np
from scipy import stats as sps

from common import EXP, SEED, WEIGHTS, EARLY, Log, build_panel, early_mask, fgls_affine, load_raw, update_results

B = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
B_SENS = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
log = Log(f"b_bootstrap_B{B}")
rng = np.random.default_rng(SEED)

df = load_raw()
specs = list(WEIGHTS)
data = {}
for name in specs:
    p = build_panel(df, WEIGHTS[name])
    e = p[early_mask(p)].reset_index(drop=True)
    season = np.zeros(len(e), int)
    for i, (lo, hi) in enumerate(EARLY):
        season[((e.week_end >= lo) & (e.week_end <= hi)).to_numpy()] = i
    data[name] = {"g": e.g.to_numpy(), "D": e.D_t.to_numpy(), "state": e.state.to_numpy(), "season": season}
states = sorted(set().union(*[set(d["state"]) for d in data.values()]))
S = len(states)
log(f"B={B};流行初期样本覆盖 {S} 个州;各规格 N = " + ", ".join(f"{k}:{len(v['g'])}" for k, v in data.items()))

RBAR_FULL = float(data["original"]["g"].mean())
NAMES = ["a_original", "b_original", "ba_original", "a_single_1w", "b_single_1w", "ba_single_1w",
         "a_equal_3w", "b_equal_3w", "ba_equal_3w", "r1", "r2", "q1", "q2", "b_original_fixedRbar", "a_original_fixedRbar"]


def index_by(cluster_key):
    """每个规格:簇 -> 行号数组。"""
    out = {}
    for name, d in data.items():
        keys = cluster_key(d)
        order = np.argsort(keys, kind="stable")
        uk, start = np.unique(keys[order], return_index=True)
        bounds = np.append(start, len(order))
        out[name] = {k: order[bounds[i]:bounds[i + 1]] for i, k in enumerate(uk)}
    return out


def stats_for(rows_by_spec):
    v = {}
    for name in specs:
        idx = rows_by_spec[name]
        g, D = data[name]["g"][idx], data[name]["D"][idx]
        rbar = g.mean()
        L = ((g - rbar) / rbar) ** 2
        a, b = fgls_affine(L, D)
        v[f"a_{name}"], v[f"b_{name}"], v[f"ba_{name}"] = a, b, b / a
        if name == "original":
            Lf = ((g - RBAR_FULL) / RBAR_FULL) ** 2
            af, bf = fgls_affine(Lf, D)
            v["a_original_fixedRbar"], v["b_original_fixedRbar"] = af, bf
    v["r1"] = v["b_single_1w"] / v["b_original"]
    v["r2"] = v["b_equal_3w"] / v["b_original"]
    v["q1"] = v["a_single_1w"] / v["a_original"]
    v["q2"] = v["a_equal_3w"] / v["a_original"]
    return np.array([v[k] for k in NAMES])


def rows_for(clusters, idx_map):
    return {name: np.concatenate([idx_map[name].get(c, np.empty(0, int)) for c in clusters]) for name in specs}


state_idx = index_by(lambda d: d["state"])
theta = stats_for({name: np.arange(len(data[name]["g"])) for name in specs})
log("点估计:" + ", ".join(f"{k}={x:.5g}" for k, x in zip(NAMES, theta)))


def run_boot(clusters, idx_map, nb, tag):
    out = np.empty((nb, len(NAMES)))
    t0 = time.time()
    with open(EXP / f"logs/b_bootstrap_{tag}_progress.log", "w", encoding="utf-8") as f:
        for i in range(nb):
            draw = rng.choice(len(clusters), size=len(clusters), replace=True)
            out[i] = stats_for(rows_for([clusters[j] for j in draw], idx_map))
            if (i + 1) % 100 == 0 or i + 1 == nb:
                f.write(f"{i + 1}/{nb} 已完成,{time.time() - t0:.1f} s\n"); f.flush()
    return out, time.time() - t0


def bca(boot, th, jack, alpha=0.05):
    z0 = sps.norm.ppf(np.clip(np.mean(boot < th), 1e-6, 1 - 1e-6))
    jm = jack.mean()
    den = 6 * (np.sum((jm - jack) ** 2) ** 1.5)
    acc = np.sum((jm - jack) ** 3) / den if den > 0 else 0.0
    zs = sps.norm.ppf([alpha / 2, 1 - alpha / 2])
    adj = sps.norm.cdf(z0 + (z0 + zs) / (1 - acc * (z0 + zs)))
    lo, hi = np.percentile(boot, 100 * adj)
    return float(lo), float(hi), float(z0), float(acc)


def summarize(boot, jack):
    res = {}
    for j, k in enumerate(NAMES):
        x = boot[:, j]
        x = x[np.isfinite(x)]
        lo, hi = np.percentile(x, [2.5, 97.5])
        blo, bhi, z0, acc = bca(x, theta[j], jack[:, j])
        res[k] = {
            "point": float(theta[j]), "boot_mean": float(x.mean()), "boot_median": float(np.median(x)),
            "boot_sd": float(x.std(ddof=1)), "pct95": [float(lo), float(hi)], "bca95": [blo, bhi],
            "bca_z0": z0, "bca_accel": acc, "skewness": float(sps.skew(x)),
            "upper_over_lower_arm": float((hi - theta[j]) / (theta[j] - lo)) if theta[j] > lo else float("nan"),
            "n_finite": int(x.size),
        }
    return res


# ---- 计时 ----
_, t50 = run_boot(states, state_idx, 50, "timing")
log(f"50 次计时:{t50:.1f} s,每次 {t50 / 50 * 1000:.0f} ms;预计 B={B} 需 {t50 / 50 * B:.0f} s")

# ---- 刀切(留一州) ----
jack = np.array([stats_for(rows_for([s for s in states if s != drop], state_idx)) for drop in states])

# ---- 主 Bootstrap ----
boot, tb = run_boot(states, state_idx, B, f"state_B{B}")
np.savez_compressed(EXP / "data/bootstrap_state_stats.npz", names=np.array(NAMES), theta=theta, boot=boot, jack=jack)
res = summarize(boot, jack)
log(f"州聚类 Bootstrap B={B} 完成,{tb:.0f} s")
for k in NAMES:
    r = res[k]
    log(f"  {k:22s} 点 {r['point']:.4f} | 百分位 [{r['pct95'][0]:.4f}, {r['pct95'][1]:.4f}] | BCa [{r['bca95'][0]:.4f}, {r['bca95'][1]:.4f}]"
        f" | 偏度 {r['skewness']:.2f} | 上/下臂 {r['upper_over_lower_arm']:.2f}")

# ---- 预测是否落在区间内 ----
PRED = {
    "r1": {"M-env 中点": 1.437, "M-env 下端": 1.419, "M-env 上端": 1.463, "正文 1.44": 1.44, "M-bin0": 1.432, "M-meas/M-mult": 1.462, "M-nodn": 1.0},
    "r2": {"M-env 中点": 0.860, "M-env 下端": 0.852, "M-env 上端": 0.866, "正文 0.86": 0.86, "M-bin0": 0.862, "M-meas/M-mult": 0.852, "M-nodn": 1.0},
    "q1": {"M-env/M-nodn": 1.0, "M-mult": 1.338},
    "q2": {"M-env/M-nodn": 1.0, "M-mult": 0.892},
    "a_original": {"M-bin0/M-meas": 0.0},
}
checks = {}
for k, preds in PRED.items():
    lo, hi = res[k]["pct95"]; blo, bhi = res[k]["bca95"]
    checks[k] = {m: {"value": v, "in_pct95": bool(lo <= v <= hi), "in_bca95": bool(blo <= v <= bhi)} for m, v in preds.items()}
    log(f"  {k}: " + "; ".join(f"{m}={v} {'在' if c['in_pct95'] else '不在'}百分位区间/{'在' if c['in_bca95'] else '不在'}BCa" for m, (v, c) in
                                 zip(preds, [(preds[m], checks[k][m]) for m in preds])))
frac = {"a_original<=0": float(np.mean(boot[:, NAMES.index("a_original")] <= 0)),
        "a_single_1w<=0": float(np.mean(boot[:, NAMES.index("a_single_1w")] <= 0)),
        "q1<1": float(np.mean(boot[:, NAMES.index("q1")] < 1)), "q2>1": float(np.mean(boot[:, NAMES.index("q2")] > 1)),
        "q1<1_and_q2>1": float(np.mean((boot[:, NAMES.index("q1")] < 1) & (boot[:, NAMES.index("q2")] > 1)))}
log("  Bootstrap 比例:" + ", ".join(f"{k}={v:.4f}" for k, v in frac.items()))
update_results("B_bootstrap", {
    "design": f"按州聚类有放回重抽 {S} 个州,三种权重共用同一组抽样,每次重估 R_bar 与迭代 FGLS;B={B};种子 {SEED};BCa 加速度用留一州刀切",
    "B": B, "n_clusters": S, "seconds": tb, "seconds_per_draw": tb / B, "timing_50_draws_s": t50,
    "stats": res, "prediction_checks": checks, "boot_fractions": frac,
    "comparison_existing_b_ci": {"user_repo_b_ci_fixed_Rbar_B1500": [1.5019, 3.0161],
                                 "ours_fixed_Rbar_pct95": res["b_original_fixedRbar"]["pct95"],
                                 "ours_reestimated_Rbar_pct95": res["b_original"]["pct95"]},
})

# ---- 敏感性:州×流行季 聚类 ----
ss_idx = index_by(lambda d: np.array([f"{s}|{q}" for s, q in zip(d["state"], d["season"])]))
ss_clusters = sorted(set().union(*[set(v) for v in ss_idx.values()]))
boot_ss, tss = run_boot(ss_clusters, ss_idx, B_SENS, f"stateseason_B{B_SENS}")
sens = {k: [float(x) for x in np.percentile(boot_ss[:, j], [2.5, 97.5])] for j, k in enumerate(NAMES)}
log(f"敏感性:州×流行季聚类({len(ss_clusters)} 簇)B={B_SENS},{tss:.0f} s")
for k in ("b_original", "a_original", "r1", "r2", "q1", "q2"):
    log(f"  {k:12s} 百分位 [{sens[k][0]:.4f}, {sens[k][1]:.4f}]")
update_results("B_bootstrap_sensitivity_state_season", {
    "design": f"以州×流行季为簇({len(ss_clusters)} 簇)有放回重抽,B={B_SENS},其余同主 Bootstrap", "pct95": sens, "seconds": tss,
})
log.close()
