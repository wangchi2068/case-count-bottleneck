"""分析 C:竞争模型的拟合比较(预注册见 analysis/competing_models.md 第 4 节规则 5)。

均值形状:M0 L=b/D;M1 L=a+b/D(论文);M2 L=c·D^{-p}。
工作族:Gamma(方差 ∝ mu^2),形状参数 nu 与均值参数联合极大似然;M1 的均值参数在 Gamma 族下的
估计方程与迭代 FGLS 相同(作为一致性检查)。
准则:AIC(参数数 = 均值参数 + nu);留一州交叉验证(51 折)的 Gamma 偏差与相对平方误差,
用州间配对差给标准误。三种滞后权重各跑一遍,主结论看主规格。
"""
import numpy as np
from scipy import optimize, special

from common import WEIGHTS, Log, build_panel, early_mask, fgls_affine, load_raw, update_results

log = Log("c_competing")
df = load_raw()


def mean_fn(model, th, D):
    if model == "M0":
        return np.exp(th[0]) / D
    if model == "M1":
        return th[0] + th[1] / D
    return np.exp(th[0]) * D ** (-th[1])


def nll(params, model, L, D):
    k = {"M0": 1, "M1": 2, "M2": 2}[model]
    th, lognu = params[:k], params[k]
    mu = mean_fn(model, th, D)
    if np.any(mu <= 0):
        return 1e12
    nu = np.exp(lognu)
    # Gamma(shape=nu, scale=mu/nu) 的对数密度
    ll = nu * np.log(nu / mu) + (nu - 1) * np.log(L) - nu * L / mu - special.gammaln(nu)
    return -ll.sum()


def fit(model, L, D):
    a, b = fgls_affine(L, D)
    start = {"M0": [np.log(max(b, 0.1))], "M1": [a, b], "M2": [np.log(max(L.mean(), 1e-3)), 0.3]}[model] + [np.log(0.5)]
    best = None
    for meth in ("Nelder-Mead", "Powell"):
        r = optimize.minimize(nll, start, args=(model, L, D), method=meth,
                              options={"maxiter": 20000, "xatol": 1e-9, "fatol": 1e-9} if meth == "Nelder-Mead" else {"maxiter": 20000})
        if best is None or r.fun < best.fun:
            best = r
        start = list(best.x)
    return best


def gamma_dev(L, mu):
    return 2 * np.sum(-np.log(L / mu) + (L - mu) / mu)


out = {}
for name, w in WEIGHTS.items():
    p = build_panel(df, w)
    e = p[early_mask(p)].reset_index(drop=True)
    rbar = e.g.mean()
    L = (((e.g - rbar) / rbar) ** 2).to_numpy()
    D = e.D_t.to_numpy()
    st = e.state.to_numpy()
    n_zero = int(np.sum(L <= 0))
    L = np.clip(L, 1e-12, None)
    res = {}
    for m in ("M0", "M1", "M2"):
        r = fit(m, L, D)
        k = len(r.x)
        th = r.x[:-1]
        res[m] = {"nll": float(r.fun), "k": k, "AIC": float(2 * r.fun + 2 * k), "nu": float(np.exp(r.x[-1])),
                  "theta": [float(x) for x in (np.exp(th) if m == "M0" else th)]}
        if m == "M2":
            res[m]["theta"] = [float(np.exp(th[0])), float(th[1])]
    a_f, b_f = fgls_affine(L, D)
    res["M1"]["fgls_check"] = [a_f, b_f]
    # 留一州交叉验证
    states = np.unique(st)
    cv = {m: {"dev": [], "relsq": [], "sq": []} for m in ("M0", "M1", "M2")}
    for s in states:
        tr, te = st != s, st == s
        rb = e.g[tr].mean()          # 基准 R_bar 也只用训练州估计
        Ltr = np.clip((((e.g[tr] - rb) / rb) ** 2).to_numpy(), 1e-12, None)
        Lte = np.clip((((e.g[te] - rb) / rb) ** 2).to_numpy(), 1e-12, None)
        for m in ("M0", "M1", "M2"):
            r = fit(m, Ltr, D[tr])
            mu = mean_fn(m, r.x[:-1], D[te])
            cv[m]["dev"].append(gamma_dev(Lte, mu))
            cv[m]["relsq"].append(np.sum(((Lte - mu) / mu) ** 2))
            cv[m]["sq"].append(np.sum((Lte - mu) ** 2))
    cvsum = {}
    for m in cv:
        cvsum[m] = {k: float(np.sum(v)) for k, v in cv[m].items()}
    pair = {}
    for a_, b_ in (("M0", "M1"), ("M2", "M1")):
        for crit in ("dev", "relsq", "sq"):
            d = np.array(cv[a_][crit]) - np.array(cv[b_][crit])
            pair[f"{a_}-{b_}_{crit}"] = {"diff_total": float(d.sum()), "se_total": float(np.sqrt(len(d)) * d.std(ddof=1)),
                                        "n_states_favoring_M1": int(np.sum(d > 0))}
    out[name] = {"N": len(e), "n_L_zero_clipped": n_zero, "fits": res, "loso_cv_totals": cvsum, "loso_paired": pair}
    log(f"[{name}] N={len(e)}")
    for m in ("M0", "M1", "M2"):
        log(f"  {m}: θ={['%.5g' % x for x in res[m]['theta']]}, ν={res[m]['nu']:.3f}, AIC={res[m]['AIC']:.2f}, "
            f"LOSO 偏差={cvsum[m]['dev']:.2f}, 相对平方误差={cvsum[m]['relsq']:.1f}, 平方误差={cvsum[m]['sq']:.3f}")
    log(f"  M1 Gamma MLE 均值参数 vs 迭代 FGLS: {res['M1']['theta']} vs {[a_f, b_f]}")
    for k_, v in pair.items():
        log(f"  {k_}: 差 {v['diff_total']:.3f} ± {v['se_total']:.3f}(州间标准误),偏向 M1 的州 {v['n_states_favoring_M1']}/{len(states)}")
    update_results("C_competing_fits", out)
log.close()
