"""第三轮公用:按病原读 NHSN 原始 CSV(含填报医院比例/数),保留州周序列,构造未调整与报告调整的增长统计量,
州聚类 Bootstrap + BCa,结果增量写入 analysis/r3_results.json。

口径与上一轮 common.py 相同(51 个辖区、缺失按 0、D_t>=5、迭代 FGLS、流行初期窗口、制度期),新增:
- 报告率代理 h = Percent Hospitals Reporting <病原> Admissions / 100(主)或 Number Hospitals Reporting(敏感性);
- 报告调整:C* = C/h,D* = sum_j w_j C*_{t-j},G* = C*_{t+1}/D*_t = G/pi,pi = h_{t+1}/sum_j w_j h_{t-j};
  行集合按原始 D_t>=5 选定,窗口内任一周 h 缺失或为 0 的行记 valid_h=False;
- 增长期窗口 W-growth:全国合计 G_nat = C_nat(t+1)/D_nat(t) >= 1.05 的周,2022-08-01 起,剔除第二填报期;
  RSV 自 2024-11-01 起。
预注册见 analysis/r3_preregistration.md。只读用户仓库数据,不执行用户仓库代码。
"""
from __future__ import annotations

import json
import time
from itertools import product

import numpy as np
import pandas as pd
from scipy import stats as sps

from common import CSV, EARLY, EXCLUDE, EXP, LOGS, P1_END, P3_START, SEED, WEIGHTS, fgls_affine

R3 = EXP / "analysis/r3_results.json"
PATHOGENS = {
    "flu": ("Total Influenza Admissions", "Influenza Admissions"),
    "covid": ("Total COVID-19 Admissions", "COVID-19 Admissions"),
    "rsv": ("Total RSV Admissions", "RSV Admissions"),
}
GROWTH_START = pd.Timestamp("2022-08-01")
RSV_START = pd.Timestamp("2024-11-01")
G_NAT_MIN = 1.05
SPECS = list(WEIGHTS)                      # original, single_1w, equal_3w


def load(pathogen: str) -> pd.DataFrame:
    tot, tail = PATHOGENS[pathogen]
    cols = ["Week Ending Date", "Geographic aggregation", tot,
            f"Percent Hospitals Reporting {tail}", f"Number Hospitals Reporting {tail}"]
    df = pd.read_csv(CSV, usecols=cols)
    g = df["Geographic aggregation"].astype(str)
    df = df[(g.str.len() == 2) & ~g.isin(EXCLUDE)].copy()
    out = pd.DataFrame({
        "state": df["Geographic aggregation"].to_numpy(),
        "week_end": pd.to_datetime(df["Week Ending Date"]).to_numpy(),
        "missing": df[tot].isna().to_numpy(),
        "C": df[tot].fillna(0).astype(float).to_numpy(),
        "h": (df[f"Percent Hospitals Reporting {tail}"] / 100.0).to_numpy(float),
        "hn": df[f"Number Hospitals Reporting {tail}"].to_numpy(float),
    })
    return out.sort_values(["state", "week_end"]).reset_index(drop=True)


def series(df: pd.DataFrame) -> dict:
    """州 -> 完整周序列(计数、两种代理、日期)。"""
    out = {}
    for s, sub in df.groupby("state", sort=True):
        if len(sub) < 10:
            continue
        out[s] = {"c": sub.C.to_numpy(), "h": sub.h.to_numpy(), "hn": sub.hn.to_numpy(),
                  "week": sub.week_end.to_numpy(), "miss": sub.missing.to_numpy()}
    return out


def growth_weeks(df: pd.DataFrame, pathogen: str, w=WEIGHTS["original"]) -> set:
    """全国增长期周(按 D_t 所在周)。"""
    nat = df.groupby("week_end").C.sum().sort_index()
    c = nat.to_numpy(); wk = nat.index.to_numpy()
    t = np.arange(2, len(c) - 1)
    d = w[0] * c[t] + w[1] * c[t - 1] + w[2] * c[t - 2]
    with np.errstate(divide="ignore", invalid="ignore"):
        gn = np.where(d > 0, c[t + 1] / d, np.nan)
    wt = pd.to_datetime(wk[t])
    ok = (gn >= G_NAT_MIN) & (wt >= GROWTH_START) & ~((wt > P1_END) & (wt < P3_START))
    if pathogen == "rsv":
        ok &= wt >= RSV_START
    return set(wk[t][ok])


def season_of(week) -> int:
    """流行季编号:8 月 1 日至次年 7 月 31 日,记为起始年。"""
    ts = pd.Timestamp(week)
    return ts.year if ts.month >= 8 else ts.year - 1


def early_index(week) -> int:
    for i, (lo, hi) in enumerate(EARLY):
        if pd.Timestamp(lo) <= pd.Timestamp(week) <= pd.Timestamp(hi):
            return i
    return -1


def build_rows(ser: dict, w, select, dmin: float = 5.0, proxy: str = "h") -> dict:
    """按 select(week)->bool 选行;返回扁平数组(state、t、week、D、Cn、G、pi、Dstar、Gstar、valid_h)。"""
    w = np.asarray(w, float)
    recs = []
    for s, z in ser.items():
        c, hh, wk = z["c"], z[proxy], z["week"]
        n = len(c)
        t = np.arange(2, n - 1)
        d = w[0] * c[t] + w[1] * c[t - 1] + w[2] * c[t - 2]
        keep = (d >= dmin) & np.array([select(x) for x in wk[t]], bool)
        t = t[keep]
        if len(t) == 0:
            continue
        d = d[keep]
        hw = np.column_stack([hh[t - 2], hh[t - 1], hh[t], hh[t + 1]])
        valid = np.all(np.isfinite(hw) & (hw > 0), axis=1)
        with np.errstate(divide="ignore", invalid="ignore"):
            pi = hh[t + 1] / (w[0] * hh[t] + w[1] * hh[t - 1] + w[2] * hh[t - 2])
            ds = w[0] * c[t] / hh[t] + w[1] * c[t - 1] / hh[t - 1] + w[2] * c[t - 2] / hh[t - 2]
            gs = (c[t + 1] / hh[t + 1]) / ds
        recs.append(pd.DataFrame({"state": s, "t": t, "week": wk[t], "D": d, "Cn": c[t + 1], "G": c[t + 1] / d,
                                  "pi": pi, "Dstar": ds, "Gstar": gs, "valid_h": valid,
                                  "any_missing": z["miss"][t - 2] | z["miss"][t - 1] | z["miss"][t] | z["miss"][t + 1]}))
    r = pd.concat(recs, ignore_index=True)
    r["week"] = pd.to_datetime(r["week"])
    r["season"] = [season_of(x) for x in r.week]
    r["period"] = np.where(r.week <= P1_END, 1, np.where(r.week < P3_START, 2, 3))
    return r


def fit(g, D):
    """返回 (R_bar, a, b)。"""
    rbar = float(np.mean(g))
    L = ((g - rbar) / rbar) ** 2
    a, b = fgls_affine(L, D)
    return rbar, a, b


def cluster_index(keys: np.ndarray) -> dict:
    order = np.argsort(keys, kind="stable")
    uk, start = np.unique(keys[order], return_index=True)
    bounds = np.append(start, len(order))
    return {k: order[bounds[i]:bounds[i + 1]] for i, k in enumerate(uk)}


def bca(boot, th, jack, alpha=0.05):
    boot = boot[np.isfinite(boot)]
    z0 = sps.norm.ppf(np.clip(np.mean(boot < th), 1e-6, 1 - 1e-6))
    jack = jack[np.isfinite(jack)]
    jm = jack.mean()
    den = 6 * (np.sum((jm - jack) ** 2) ** 1.5)
    acc = np.sum((jm - jack) ** 3) / den if den > 0 else 0.0
    zs = sps.norm.ppf([alpha / 2, 1 - alpha / 2])
    adj = sps.norm.cdf(z0 + (z0 + zs) / (1 - acc * (z0 + zs)))
    lo, hi = np.percentile(boot, 100 * adj)
    return float(lo), float(hi)


def summarize(names, theta, boot, jack) -> dict:
    out = {}
    for j, k in enumerate(names):
        x = boot[:, j]
        xf = x[np.isfinite(x)]
        if xf.size < 10:
            out[k] = {"point": float(theta[j]), "n_finite": int(xf.size)}
            continue
        lo, hi = np.percentile(xf, [2.5, 97.5])
        blo, bhi = bca(x, theta[j], jack[:, j]) if jack is not None else (float("nan"), float("nan"))
        out[k] = {"point": float(theta[j]), "boot_sd": float(xf.std(ddof=1)), "pct95": [float(lo), float(hi)],
                  "bca95": [blo, bhi], "pct_width": float(hi - lo), "n_finite": int(xf.size)}
    return out


def cluster_bootstrap(stat_fn, clusters, idx_maps, B, rng, progress=None, n_draw=None, jackknife=True):
    """stat_fn(rows_by_key) -> 向量;idx_maps: {key: {cluster: rows}}。返回 (theta, boot, jack)。"""
    def rows_for(cl):
        return {k: np.concatenate([m.get(c, np.empty(0, int)) for c in cl]) for k, m in idx_maps.items()}
    theta = stat_fn(rows_for(clusters))
    nd = n_draw or len(clusters)
    boot = np.empty((B, len(theta)))
    t0 = time.time()
    fh = open(LOGS / f"{progress}.log", "w", encoding="utf-8") if progress else None
    for i in range(B):
        draw = rng.choice(len(clusters), size=nd, replace=True)
        boot[i] = stat_fn(rows_for([clusters[j] for j in draw]))
        if fh and ((i + 1) % 200 == 0 or i + 1 == B):
            fh.write(f"{i + 1}/{B} {time.time() - t0:.1f} s\n"); fh.flush()
    if fh:
        fh.close()
    jack = None
    if jackknife:
        jack = np.array([stat_fn(rows_for([c for c in clusters if c != drop])) for drop in clusters])
    return theta, boot, jack


def update(key: str, value) -> None:
    d = json.loads(R3.read_text(encoding="utf-8")) if R3.exists() else {}
    d.setdefault("provenance", {
        "mode": "measured",
        "source": "自写脚本 .work/case-count-bottleneck/experiment/code/r3_*.py 读取用户仓库 NHSN 原始 CSV(未执行用户仓库代码)",
        "preregistration": "analysis/r3_preregistration.md",
        "dataset_contract": "analysis/data_contract.md",
        "seed": SEED,
    })
    d[key] = value
    d["provenance"]["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    R3.write_text(json.dumps(d, ensure_ascii=False, indent=1, default=float), encoding="utf-8")


def F_factor(w, psi):
    """命题 A(vii) 的 F(w, psi)。"""
    w = np.asarray(w, float); s = np.arange(1, len(w) + 1)
    return 1 - 2 * np.sum(w * psi ** s) + sum(w[i] * w[j] * psi ** abs(i - j) for i in range(len(w)) for j in range(len(w)))


__all__ = ["R3", "PATHOGENS", "SPECS", "WEIGHTS", "EARLY", "SEED", "LOGS", "EXP", "load", "series", "growth_weeks",
           "season_of", "early_index", "build_rows", "fit", "cluster_index", "bca", "summarize", "cluster_bootstrap",
           "update", "F_factor", "product"]
