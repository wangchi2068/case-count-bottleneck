"""r4 仿真核心:日分辨率更新过程(离散化 gamma 世代间隔)+ 周汇总报告 + 与实证同口径的拟合。

供 r4_a_growth_null.py(A/B)、r4_k_two_gen.py(K)调用。设计见 analysis/r4_preregistration.md 第 2–3、10 节。

- 段结构:按组合的选窗规则(未加 D 过滤)在各州连续入选周上切段,段长 = 连续入选周数,
  起始规模 = 段首周实证 D_t(<1 取 1);每段前置 3 周预热 + 1 周前瞻。
- 感染:I_d ~ Poisson(Gamma(shape = k·Λ̃_d, scale = R_d/k)),Λ̃_d = Σ_s g_s I_{d-s},即均值 R_d Λ̃_d、离散 kΛ̃_d。
- 环境噪声块:R 在一个块内恒定;块 = 日历周(主)或 block_days 天(K 用);块间 AR(1) 系数 phi(A/B 为 0)。
  R_块 = max(0.05, R0·(1 + ε)),ε 方差 cv2(相对方差)。
- 报告:每日 Bin(I_d, ρ·p_周),p_周 为乘性报告噪声(B 用;对数 AR(1),系数 psi,CV tau);
  可选入院延迟(离散 gamma,多项分配到之后各日);按周汇总得 C_w。
- 拟合:三种滞后权重 D_t,D_t ≥ 5,G_t = C_{t+1}/D_t,R̄ = 样本均值,迭代 FGLS 拟合 L = a + b/D。
"""
import numpy as np
import pandas as pd
from scipy import stats as sps
from scipy.optimize import brentq

from common import fgls_affine
from r3_common import EARLY, SPECS, WEIGHTS, early_index, growth_weeks, load, season_of, series

K_DISP, RHO = 0.35, 0.021
PRE_W = 3
R_FLOOR = 0.05


def disc_gamma(mean, sd, s0=1, q=0.999):
    """离散化 gamma:g_s = F(s+0.5) − F(s−0.5),s ≥ s0;s0 以下的质量并入 s0;截到 q 分位并归一。"""
    shape = (mean / sd) ** 2
    scale = sd ** 2 / mean
    smax = int(np.ceil(sps.gamma.ppf(q, shape, scale=scale))) + 1
    s = np.arange(s0, smax + 1)
    F = sps.gamma.cdf(s + 0.5, shape, scale=scale) - sps.gamma.cdf(s - 0.5, shape, scale=scale)
    F[0] += sps.gamma.cdf(s0 - 0.5, shape, scale=scale)
    return F / F.sum()


def lam_from_rbar(rbar, w=WEIGHTS["original"]):
    """常增长下 G = λ / (w0 + w1/λ + w2/λ²);由目标 R̄ 反解周增长因子 λ。"""
    f = lambda lam: lam / (w[0] + w[1] / lam + w[2] / lam ** 2) - rbar
    return brentq(f, 0.2, 10.0)


def R_from_lambda(lam, g):
    """Euler–Lotka:日增长率 r = ln λ / 7,R = 1 / Σ g_s e^{-r s}。"""
    r = np.log(lam) / 7.0
    s = np.arange(1, len(g) + 1)
    return 1.0 / np.sum(g * np.exp(-r * s)), r


def combo_selectors():
    """r3_c 的 7 个病原—窗口组合:{name: (pathogen, select_fn)}。"""
    out = {}
    for pg in ("flu", "covid", "rsv"):
        df = load(pg)
        gw = growth_weeks(df, pg)
        wcal = (lambda wk: early_index(wk) == 2) if pg == "rsv" else (lambda wk: early_index(wk) >= 0)
        out[f"{pg}|W-cal"] = (pg, wcal)
        out[f"{pg}|W-growth"] = (pg, lambda wk, gw=gw: wk in gw)
        if pg == "flu":
            out["flu|W-growth-2025"] = (pg, lambda wk, gw=gw: (wk in gw) and season_of(wk) == 2025)
    return out


def segments(pathogen, select, w=WEIGHTS["original"]):
    """各州连续入选周段:返回 [(state, 段长, 段首 D)]。"""
    ser = series(load(pathogen))
    w = np.asarray(w, float)
    segs = []
    for s, z in ser.items():
        c, wk = z["c"], z["week"]
        n = len(c)
        t = np.arange(2, n - 1)
        sel = np.array([select(x) for x in wk[t]], bool)
        tt = t[sel]
        if len(tt) == 0:
            continue
        brk = np.where(np.diff(tt) != 1)[0]
        starts = np.r_[0, brk + 1]
        ends = np.r_[brk, len(tt) - 1]
        for a, b in zip(starts, ends):
            t0 = tt[a]
            d0 = w[0] * c[t0] + w[1] * c[t0 - 1] + w[2] * c[t0 - 2]
            segs.append((s, int(b - a + 1), float(max(d0, 1.0))))
    return segs


def simulate_weekly_counts(segs, R0, g, rng, lam, cv2=0.0, phi=0.0, block_days=7,
                           psi=0.0, tau=0.0, delay=None, rho=RHO, k=K_DISP, pmult=None):
    """pmult:可选 (段数, 最大周数) 的报告率乘子(J 用 h^κ)。返回 C:(段数, 最大周数) 的周报告数矩阵与每段有效周数 nweeks(= PRE_W + 段长 + 1)。"""
    S = len(segs)
    lens = np.array([L for _, L, _ in segs])
    d0 = np.array([d for _, _, d in segs])
    nweeks = PRE_W + lens + 1
    W = int(nweeks.max())
    ndays = 7 * W
    smax = len(g)
    r = np.log(lam) / 7.0
    # 历史:前 smax 天按 e^{r d} 的指数增长,使预热第 1 周报告约为 d0 / λ^PRE_W
    i_start = d0 / lam ** PRE_W / (7 * rho)
    hist_days = np.arange(-smax, 0)
    I = np.zeros((S, smax + ndays))
    I[:, :smax] = np.maximum(0, np.round(i_start[:, None] * np.exp(r * hist_days)[None, :]))
    # 环境噪声:块级 R
    nblk = int(np.ceil(ndays / block_days))
    eps = np.zeros((S, nblk))
    if cv2 > 0:
        sd = np.sqrt(cv2)
        eps[:, 0] = rng.normal(0, sd, S)
        si = sd * np.sqrt(1 - phi ** 2)
        for j in range(1, nblk):
            eps[:, j] = phi * eps[:, j - 1] + si * rng.normal(size=S)
    Rb = np.maximum(R_FLOOR, R0 * (1 + eps))
    blk_of_day = np.arange(ndays) // block_days
    grev = g[::-1]
    for d in range(ndays):
        lamt = I[:, d:d + smax] @ grev           # Σ_s g_s I_{d-s}
        Rd = Rb[:, blk_of_day[d]]
        shape = k * lamt
        pos = lamt > 0
        x = np.zeros(S)
        if pos.any():
            x[pos] = rng.gamma(shape[pos], Rd[pos] / k)  # 均值 R·Λ̃,方差 R²Λ̃/k
        I[:, smax + d] = rng.poisson(x)
    Id = I[:, smax:]
    # 报告率乘性噪声(按日历周)
    p = np.ones((S, W))
    if tau > 0:
        sig = np.sqrt(np.log(1 + tau ** 2))
        x = np.zeros((S, W))
        x[:, 0] = rng.normal(0, sig, S)
        si = sig * np.sqrt(1 - psi ** 2)
        for j in range(1, W):
            x[:, j] = psi * x[:, j - 1] + si * rng.normal(size=S)
        p = np.exp(x - sig ** 2 / 2)
    if pmult is not None:
        p = p * pmult
    rep_p = np.clip(rho * np.repeat(p, 7, axis=1), 0, 1)
    Cd = rng.binomial(Id.astype(np.int64), rep_p).astype(float)
    if delay is not None:
        M = rng.multinomial(Cd.astype(np.int64), delay)   # (S, ndays, 延迟天数)
        out = np.zeros((S, ndays + len(delay)))
        for j in range(len(delay)):
            out[:, j:j + ndays] += M[:, :, j]
        Cd = out[:, :ndays]
    C = Cd.reshape(S, W, 7).sum(axis=2)
    return C, nweeks


def fit_from_counts(C, nweeks, segs_len, need=("original", "single_1w", "equal_3w")):
    """同实证口径拟合。段内观测周为 PRE_W .. PRE_W+段长-1(对应 D_t 所在周),G 用下一周。"""
    out = {}
    S, W = C.shape
    t = np.arange(2, W - 1)
    lens = np.asarray(segs_len)
    in_seg = (t[None, :] >= PRE_W) & (t[None, :] < PRE_W + lens[:, None])
    for name in need:
        w = WEIGHTS[name]
        D = w[0] * C[:, t] + w[1] * C[:, t - 1] + w[2] * C[:, t - 2]
        keep = in_seg & (D >= 5)
        Dk = D[keep]
        Gk = C[:, t + 1][keep] / Dk
        rbar = float(Gk.mean())
        L = ((Gk - rbar) / rbar) ** 2
        a, b = fgls_affine(L, Dk)
        out[name] = {"a": a, "b": b, "rbar": rbar, "N": int(keep.sum()), "D_med": float(np.median(Dk))}
    return out


__all__ = ["disc_gamma", "lam_from_rbar", "R_from_lambda", "combo_selectors", "segments",
           "simulate_weekly_counts", "fit_from_counts", "K_DISP", "RHO", "SPECS", "EARLY"]
