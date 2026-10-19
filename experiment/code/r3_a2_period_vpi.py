"""r3 分析 1 补充:三个填报制度期全面板行(D_t>=5)中 V_pi 与州内周间 tau2 的州聚类百分位区间(预注册第 1 节"不确定性")。

用法:python3 r3_a2_period_vpi.py [B]
"""
import sys

import numpy as np

from common import Log
from r3_common import SEED, WEIGHTS, build_rows, cluster_index, load, series, update

B = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
log = Log("r3_a2_period_vpi")
rng = np.random.default_rng(SEED + 1)
ser = series(load("flu"))
rows = build_rows(ser, WEIGHTS["original"], lambda wk: True)
rows = rows[rows.valid_h & np.isfinite(rows.pi)]
out = {}
for k in (1, 2, 3):
    r = rows[rows.period == k]
    p = r.pi.to_numpy() - 1
    st = r.state.to_numpy()
    idx = cluster_index(st)
    cl = sorted(idx)
    v0 = float(np.var(p, ddof=1))
    bs = np.empty(B)
    for i in range(B):
        j = np.concatenate([idx[cl[m]] for m in rng.choice(len(cl), len(cl), replace=True)])
        bs[i] = np.var(p[j], ddof=1)
    lo, hi = np.percentile(bs, [2.5, 97.5])
    out[f"period{k}"] = {"N_rows": int(len(r)), "n_states": len(cl), "V_pi": v0, "pct95": [float(lo), float(hi)],
                         "share_pi_eq_1": float(np.mean(np.abs(p) < 1e-12))}
    log(f"第{k}期:N={len(r)},州 {len(cl)},V_pi={v0:.4g} [{lo:.4g}, {hi:.4g}]")
update("R1b_period_Vpi_ci", out)
log.close()
