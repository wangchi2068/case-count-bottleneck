"""分析 A(复现门)与 F(顺手核对):自写管线复现正文与 empirical_stats.json 的点估计。

容差:三位有效数字(相对差 < 0.5e-2 记"一致",整数样本量要求完全相等)。
同时把后续分析要用的小型派生表写到 data/(州周面板,只含需要的列)。
"""
import json

import numpy as np
import pandas as pd

from common import (EXP, STATS, USER, WEIGHTS, Log, build_panel, early_mask, fgls_affine, iqr,
                    load_raw, update_results)

log = Log("a_reproduce")
st = json.loads(STATS.read_text(encoding="utf-8"))
rows = []


def sig3(x):
    return float(f"{x:.3g}")


def check(item, ours, ref, kind="float"):
    if kind == "int":
        ok = int(ours) == int(ref)
    else:
        ok = sig3(ours) == sig3(ref) or abs(ours - ref) <= 0.005 * abs(ref)
    rows.append({"item": item, "ours": ours, "reference": ref, "match_3sf": bool(ok)})
    log(f"[{'一致' if ok else '不一致'}] {item}: 自写 {ours:.6g} | 参照 {ref:.6g}")
    return ok


df = load_raw()
check("州周总数 n_state_weeks", len(df), st["n_state_weeks"], "int")
check("缺失住院州周", int(df.missing.sum()), 504, "int")

panels = {}
for name, w in WEIGHTS.items():
    p = build_panel(df, w)
    panels[name] = p
p = panels["original"]
check("有效面板 n_valid(D>=5)", len(p), st["n_valid"], "int")

# ---- 流行初期主拟合 ----
fits = {}
for name, pw in panels.items():
    e = pw[early_mask(pw)].copy()
    rbar = e.g.mean()
    L = ((e.g - rbar) / rbar) ** 2
    a, b = fgls_affine(L.to_numpy(), e.D_t.to_numpy())
    a1, b1 = fgls_affine(L.to_numpy(), e.D_t.to_numpy(), iterate=False)
    fits[name] = {"N": len(e), "R_bar": rbar, "a": a, "b": b, "b_over_a": b / a,
                  "one_step_a": a1, "one_step_b": b1}
    log(f"  [{name}] 一步 FGLS(论文文字口径)a={a1:.6f}, b={b1:.5f};迭代 FGLS a={a:.6f}, b={b:.5f}")
    ref = st["lag_weights_sensitivity"][name]
    check(f"[{name}] 初期 N", len(e), ref["N"], "int")
    check(f"[{name}] R_bar", rbar, ref["R_bar"])
    check(f"[{name}] a", a, ref["a"])
    check(f"[{name}] b", b, ref["b"])
    check(f"[{name}] b/a", b / a, ref["m_x"])
r1 = fits["single_1w"]["b"] / fits["original"]["b"]
r2 = fits["equal_3w"]["b"] / fits["original"]["b"]
check("斜率比 单周/主规格(正文 1.40)", r1, 1.40)
check("斜率比 等权/主规格(正文 0.86)", r2, 0.86)
r1_one = fits["single_1w"]["one_step_b"] / fits["original"]["one_step_b"]
r2_one = fits["equal_3w"]["one_step_b"] / fits["original"]["one_step_b"]
log(f"  一步 FGLS 下斜率比 {r1_one:.4f}/{r2_one:.4f}(迭代 {r1:.4f}/{r2:.4f})")

e = p[early_mask(p)].copy()
rbar = fits["original"]["R_bar"]
e["L"] = ((e.g - rbar) / rbar) ** 2
check("初期 sd(G)", e.g.std(ddof=1), st["early"]["sd"])
check("初期平均损失 0.181", e.L.mean(), st["early"]["error_budget"]["total_mean_relmse"])

# ---- 制度期与流行季 ----
pol = st["policy"]
keys = {1: "period1_mandatory", 2: "period2_voluntary", 3: "period3_remandated"}
period_tab = {}
for k, key in keys.items():
    x = p[p.period == k]
    s = x[x.in_season]
    period_tab[k] = {"N": len(x), "iqr": iqr(x.g), "sd": float(x.g.std(ddof=1)), "mad": float(np.median(np.abs(x.g - x.g.median()))),
                     "coverage_mean": float(x.coverage.mean()),
                     "season_N": len(s), "season_iqr": iqr(s.g), "season_sd": float(s.g.std(ddof=1)),
                     "season_mean": float(s.g.mean()), "season_states": int(s.state.nunique())}
    check(f"第{k}期 N", len(x), pol[key]["N"], "int")
    check(f"第{k}期 IQR", iqr(x.g), pol[key]["g_iqr"])
    check(f"第{k}期 SD", x.g.std(ddof=1), pol[key]["g_std"])
    check(f"第{k}期 MAD", period_tab[k]["mad"], pol[key]["g_mad"])
    check(f"第{k}期 平均填报率", period_tab[k]["coverage_mean"], pol[key]["coverage_mean"])
    ref = pol["flu_season_only"][key]
    check(f"第{k}期 流行季 N", len(s), ref["N"], "int")
    check(f"第{k}期 流行季 IQR", iqr(s.g), ref["iqr"])
    check(f"第{k}期 流行季 SD", s.g.std(ddof=1), ref["std"])
    check(f"第{k}期 流行季 均值", s.g.mean(), ref["mean"])
log(f"第二期季内 55 个州周来自 {period_tab[2]['season_states']} 个州,周末日期:"
    f"{sorted(p[(p.period == 2) & p.in_season].week_end.dt.date.astype(str).unique())}")

# ---- F:顺手核对 ----
a, b = fits["original"]["a"], fits["original"]["b"]
cf = float(np.mean(a + b / np.maximum(e.D_t.to_numpy(), 250)))
check("F1 counterfactual_D250(把 D<250 提到 250 后的模型平均损失)", cf, st["early"]["error_budget"]["counterfactual_D250"])
model250 = a + b / 250
log(f"F1 模型值 a+b/250 = {model250:.5f};counterfactual 口径 = mean(a+b/max(D,250)) = {cf:.5f};"
    f"两者差 {model250 - cf:.5f}(D>=250 的州周规模项小于 b/250)")
big = e[e.D_t >= 250]
check("F1 D>=250 实际平均损失 0.104", big.L.mean(), st["realized_large_scale"]["mean_loss"])
check("F1 D>=250 N", len(big), st["realized_large_scale"]["N"], "int")

cori = {}
for k in (1, 2, 3):
    r = e[f"cori_{k}w"]
    ok = r > 0
    loss = (e.g[ok] / r[ok] - 1) ** 2
    cori[k] = {"N": int(ok.sum()), "mean": float(loss.mean()), "median": float(loss.median())}
    ref = st["competing_baselines"]["overall"][f"cori_{k}w"]
    check(f"F2 Cori {k} 周窗 N", int(ok.sum()), ref["N"], "int")
    check(f"F2 Cori {k} 周窗平均损失", loss.mean(), ref["mean"])
    if k in (2, 3):
        aa, bb = fgls_affine(loss.to_numpy(), e.D_t[ok].to_numpy())
        cori[k].update({"a": aa, "b": bb, "b_over_a": bb / aa})
        check(f"F2 Cori {k} 周窗 a", aa, st["competing_baselines"][f"affine_cori_{k}w"]["a"])
        check(f"F2 Cori {k} 周窗 b", bb, st["competing_baselines"][f"affine_cori_{k}w"]["b"])
naive = ((e.C_next - e.C_t) / e.C_t) ** 2
okn = e.C_t > 0
check("F2 朴素预测平均损失", naive[okn].mean(), st["competing_baselines"]["overall"]["naive"]["mean"])

sim = json.loads((USER / "results/sim_theory.json").read_text(encoding="utf-8"))


def walk(o, path=""):
    if isinstance(o, dict):
        for kk, vv in o.items():
            yield from walk(vv, f"{path}.{kk}")
    elif isinstance(o, list):
        yield path, o


exact_max = []
for path, lst in walk(sim):
    if path.split(".")[-1] == "exact":
        arr = np.array([v for v in np.ravel(np.array(lst, dtype=object)) if isinstance(v, (int, float))], float)
        if arr.size:
            exact_max.append((path, float(arr.max()), arr.size))
for path, mx, n in exact_max:
    log(f"F3 sim_theory{path}: n={n}, max={mx:.7f}")
emax = max(m for _, m, _ in exact_max) if exact_max else float("nan")
log(f"F3 精确检验最大实际水平 = {emax:.7f};正文写 0.05000(四舍五入到 5 位小数为 {emax:.5f})")

# ---- 落盘 ----
small = p[["state", "week_end", "D_t", "C_t", "C_next", "g", "coverage", "any_missing", "period", "month",
           "in_season", "cori_1w", "cori_2w", "cori_3w"]].copy()
small["D_t"] = small.D_t.round(4); small["g"] = small.g.round(6); small["coverage"] = small.coverage.round(2)
for c in ("cori_1w", "cori_2w", "cori_3w"):
    small[c] = small[c].round(6)
small.to_csv(EXP / "data/panel_original.csv.gz", index=False, compression="gzip")
for name in ("single_1w", "equal_3w"):
    q = panels[name]
    q = q[early_mask(q)][["state", "week_end", "D_t", "g"]].copy()
    q["D_t"] = q.D_t.round(4); q["g"] = q.g.round(6)
    q.to_csv(EXP / f"data/early_{name}.csv.gz", index=False, compression="gzip")

n_ok = sum(r["match_3sf"] for r in rows)
log(f"复现门:{n_ok}/{len(rows)} 项三位有效数字一致")
update_results("A_reproduction", {
    "tolerance": "三位有效数字或相对差 ≤0.5%;样本量要求完全相等",
    "n_match": n_ok, "n_items": len(rows), "items": rows,
    "fits_by_weight": fits, "slope_ratio_point": [r1, r2], "slope_ratio_one_step": [r1_one, r2_one],
    "fgls_note": "empirical_stats.json 的 a、b 由迭代至收敛的 FGLS 得到;论文与用户仓库 checks/_common.py 写的是一步 FGLS。一步版单周规格 b=3.102(JSON 3.134),斜率比 1.384。本轮全部分析用迭代版。",
    "cori_note": "Cori 窗口内感染压力之和 <5 的点剔除,复现 N=1197/1244/1251;用户仓库 theory/sections/empirical.tex:309 的表注写「局部比值非正剔除」,与能复现 N 的判据不同。",
    "period_table": period_tab,
})
update_results("F_spot_checks", {
    "counterfactual_D250": cf, "model_value_a_plus_b_over_250": model250,
    "note_D250": "0.107 = mean(a + b/max(D_t,250)),只把不足 250 的州周提到 250;0.108 = a+b/250,是 D 恰为 250 时的模型值。两者口径不同。",
    "realized_D_ge_250": {"N": len(big), "mean_loss": float(big.L.mean())},
    "cori": cori, "naive_mean": float(naive[okn].mean()),
    "exact_test_max_level": emax, "exact_test_arrays": [{"path": a_, "max": m_, "n": n_} for a_, m_, n_ in exact_max],
})
log.close()
