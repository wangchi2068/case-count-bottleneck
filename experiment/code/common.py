"""公用:读 NHSN 原始 CSV、按论文口径构造州周面板、迭代 FGLS、结果增量落盘。

口径(只读阅读用户仓库 code/prep_nhsn.py 与论文 empirical.tex 后重写,未执行用户代码):
- 51 个辖区:两字母代码,去掉 PR/VI/GU/MP/AS/US;缺失住院数按 0;
- D_t = sum_s w_s C_{t+1-s}(主规格 w=(0.65,0.25,0.10)),只保留 D_t >= 5;G_t = C_{t+1}/D_t;
- FGLS:先 OLS 拟合 L = a + b/D,再以 1/mu_hat^2 加权重拟合,**迭代至收敛**。分析 A 发现只有迭代版
  能把三种滞后权重的 a、b 复现到 6 位有效数字(一步版单周规格 b=3.102,与 empirical_stats.json 的 3.134 不符);
  论文"一步拟合值"的表述与生成 JSON 的实际做法不一致;
- Cori 滑动窗:R_hat(k) = sum_{j<k} C_{t-j} / sum_{j<k} D_{t-1-j},分母(感染压力之和) < 5 的点剔除
  (该判据把 N 复现为 1197/1244/1251);
- 流行初期窗:2022-10-08–11-26、2023-10-14–12-16、2024-11-09–2025-01-18(按 D_t 所在周的周末日期);
- 填报制度期:第一期 ≤2024-04-30,第二期 2024-05-01–10-31,第三期 ≥2024-11-01(按 D_t 所在周);
- 流行季:10 月至次年 3 月(用户仓库 thesis/chapters/ch5_empirical.tex:283 的口径)。
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(os.environ.get("REPO_ROOT", Path(__file__).resolve().parents[4]))   # 仓库根(复现时可用环境变量覆盖)
EXP = Path(__file__).resolve().parents[1]           # .work/case-count-bottleneck/experiment
USER = Path(os.environ.get("USER_REPO", ROOT / ".work/case-count-bottleneck/sources/user-repo/code_and_data"))
CSV = Path(os.environ.get("NHSN_CSV", USER / "data/raw/Weekly_Hospital_Respiratory_Data_Metrics_by_Jurisdiction.csv"))
STATS = USER / "data/empirical_stats.json"
RESULTS = EXP / "analysis/reanalysis_results.json"
LOGS = EXP / "logs"
(EXP / "data").mkdir(parents=True, exist_ok=True)     # 只复制 code/ 到空目录重跑时,派生面板写入 ../data/

COLS = ["Week Ending Date", "Geographic aggregation", "Total Influenza Admissions",
        "Percent Hospitals Reporting Influenza Admissions"]
EXCLUDE = {"PR", "VI", "GU", "MP", "AS", "US"}
WEIGHTS = {"original": (0.65, 0.25, 0.10), "single_1w": (1.0, 0.0, 0.0), "equal_3w": (1 / 3, 1 / 3, 1 / 3)}
EARLY = [("2022-10-08", "2022-11-26"), ("2023-10-14", "2023-12-16"), ("2024-11-09", "2025-01-18")]
P1_END, P3_START = pd.Timestamp("2024-04-30"), pd.Timestamp("2024-11-01")
SEASON_MONTHS = {10, 11, 12, 1, 2, 3}
SEED = 20261017


def load_raw() -> pd.DataFrame:
    df = pd.read_csv(CSV, usecols=COLS)
    g = df["Geographic aggregation"].astype(str)
    df = df[(g.str.len() == 2) & ~g.isin(EXCLUDE)].copy()
    df["week_end"] = pd.to_datetime(df["Week Ending Date"])
    df["missing"] = df["Total Influenza Admissions"].isna()
    df["C"] = df["Total Influenza Admissions"].fillna(0).astype(float)
    df["coverage"] = df["Percent Hospitals Reporting Influenza Admissions"]
    return df.sort_values(["Geographic aggregation", "week_end"]).reset_index(drop=True)


def build_panel(df: pd.DataFrame, w=WEIGHTS["original"], dmin: float = 5.0) -> pd.DataFrame:
    """与 prep_nhsn.build_panel 同口径;另带出缺失标记、制度期、流行季与 Cori 所需的滞后量。"""
    w = np.asarray(w, float)
    out = []
    for state, sub in df.groupby("Geographic aggregation", sort=True):
        c = sub["C"].to_numpy()
        miss = sub["missing"].to_numpy()
        d = sub["week_end"].to_numpy()
        cov = sub["coverage"].to_numpy()
        n = len(c)
        if n < 10:
            continue
        t = np.arange(2, n - 1)
        dt = w[0] * c[t] + w[1] * c[t - 1] + w[2] * c[t - 2]
        keep = dt >= dmin
        t = t[keep]
        D_all = np.full(n, np.nan)             # 每一周的 D(用于 Cori 窗口的分母)
        tt = np.arange(2, n)
        D_all[tt] = w[0] * c[tt] + w[1] * c[tt - 1] + w[2] * c[tt - 2]
        rec = pd.DataFrame({
            "state": state, "week_end": d[t], "D_t": dt[keep], "C_t": c[t], "C_next": c[t + 1],
            "coverage": cov[t],
            "any_missing": miss[t - 2] | miss[t - 1] | miss[t] | miss[t + 1],
        })
        # Cori 滑动窗:R_hat(k) = sum_{j<k} C_{t-j} / sum_{j<k} D_{t-1-j}
        for k in (1, 2, 3):
            num = np.zeros(len(t)); den = np.zeros(len(t)); ok = np.ones(len(t), bool)
            for j in range(k):
                ii = t - j
                ok &= (ii - 1) >= 2
                num += c[np.clip(ii, 0, n - 1)]
                den += np.nan_to_num(D_all[np.clip(ii - 1, 0, n - 1)])
            with np.errstate(divide="ignore", invalid="ignore"):
                r = np.where(ok & (den >= 5), num / den, np.nan)
            rec[f"cori_{k}w"] = r
        out.append(rec)
    p = pd.concat(out, ignore_index=True)
    p["week_end"] = pd.to_datetime(p["week_end"])
    p["g"] = p["C_next"] / p["D_t"]
    p["period"] = np.where(p.week_end <= P1_END, 1, np.where(p.week_end < P3_START, 2, 3))
    p["month"] = p.week_end.dt.month
    p["in_season"] = p.month.isin(SEASON_MONTHS)
    return p


def early_mask(p: pd.DataFrame) -> np.ndarray:
    m = np.zeros(len(p), bool)
    for a, b in EARLY:
        m |= ((p.week_end >= a) & (p.week_end <= b)).to_numpy()
    return m


def fgls_affine(L, D, iterate: bool = True, tol: float = 1e-10, maxit: int = 200):
    """FGLS:OLS → 以 1/mu_hat^2 加权(行乘 1/mu_hat)。iterate=True 时迭代到系数收敛(复现 JSON 的口径);
    iterate=False 为用户仓库 checks/_common.fgls_affine 的一步版。"""
    L = np.asarray(L, float); D = np.asarray(D, float)
    X = np.column_stack([np.ones_like(D), 1.0 / D])
    beta = np.linalg.lstsq(X, L, rcond=None)[0]
    for _ in range(maxit if iterate else 1):
        mu = np.clip(X @ beta, 1e-6, None)
        wt = 1.0 / mu
        new = np.linalg.lstsq(X * wt[:, None], L * wt, rcond=None)[0]
        done = np.max(np.abs(new - beta) / (np.abs(beta) + 1e-12)) < tol
        beta = new
        if done:
            break
    return float(beta[0]), float(beta[1])


def iqr(x) -> float:
    q75, q25 = np.percentile(np.asarray(x, float), [75, 25])
    return float(q75 - q25)


def update_results(key: str, value) -> None:
    """读-改-写 reanalysis_results.json,每完成一项立即落盘。"""
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    d = json.loads(RESULTS.read_text(encoding="utf-8")) if RESULTS.exists() else {}
    d.setdefault("provenance", {
        "mode": "measured",
        "source": "自写脚本 .work/case-count-bottleneck/experiment/code/*.py 读取用户仓库 NHSN 原始 CSV(未执行用户仓库代码)",
        "dataset_contract": "analysis/data_contract.md",
        "seed": SEED,
    })
    d[key] = value
    d["provenance"]["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    RESULTS.write_text(json.dumps(d, ensure_ascii=False, indent=1, default=float), encoding="utf-8")


class Log:
    def __init__(self, name: str):
        LOGS.mkdir(parents=True, exist_ok=True)
        self.f = open(LOGS / f"{name}.log", "w", encoding="utf-8")
        self.t0 = time.time()

    def __call__(self, *a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        self.f.write(s + "\n"); self.f.flush()

    def close(self):
        self(f"耗时 {time.time() - self.t0:.1f} s")
        self.f.close()
