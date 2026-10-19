"""r4 C/D 前置:以 r3_c 原代码、原种子(SEED+5)、B=2000 重跑七组合州聚类重抽,保存全部抽样,并逐值核对 r3 结果。

做法:运行 r3_c_pathogens.py 源码本身,只替换三处副作用——结果不写回 r3_results.json、日志改名、
cluster_bootstrap 的返回值另存;随机数消耗顺序不变,因此抽样与 r3 逐次相同。
输出:analysis/r4_boot_draws.npz;r4_results.json 键 C0_r3c_rerun_check。
"""
import json
import runpy
import time

import numpy as np

import common
import r3_common
from common import EXP
from r4_common import r4_update

captured = []
_orig_cb = r3_common.cluster_bootstrap


def cb(stat_fn, clusters, idx_maps, B, rng, progress=None, **kw):
    theta, boot, jack = _orig_cb(stat_fn, clusters, idx_maps, B, rng, progress=None, **kw)
    captured.append((theta, boot, jack))
    return theta, boot, jack


rerun = {}
r3_common.cluster_bootstrap = cb
r3_common.update = lambda key, value: rerun.__setitem__(key, value)
_Log = common.Log
common.Log = lambda name: _Log("r4_c_boot_" + name)

t0 = time.time()
g = runpy.run_path(str(EXP / "code/r3_c_pathogens.py"), run_name="__r4__")
names = g["NAMES"]
keys = list(rerun["R5_cross_pathogen"])
assert len(keys) == len(captured)

r3 = json.loads((EXP / "analysis/r3_results.json").read_text(encoding="utf-8"))["R5_cross_pathogen"]
maxdiff = 0.0
for k in keys:
    for nm in names:
        a, b = r3[k]["stats"][nm], rerun["R5_cross_pathogen"][k]["stats"][nm]
        for fld in ("point", "pct95", "bca95"):
            if fld in a:
                maxdiff = max(maxdiff, float(np.max(np.abs(np.atleast_1d(a[fld]) - np.atleast_1d(b[fld])))))
np.savez_compressed(EXP / "analysis/r4_boot_draws.npz", names=np.array(names), combos=np.array(keys),
                    **{f"theta_{i}": c[0] for i, c in enumerate(captured)},
                    **{f"boot_{i}": c[1] for i, c in enumerate(captured)},
                    **{f"jack_{i}": c[2] for i, c in enumerate(captured)})
r4_update("C0_r3c_rerun_check", {"combos": keys, "B": int(captured[0][1].shape[0]), "seed": common.SEED + 5,
                                 "max_abs_diff_vs_r3": maxdiff, "identical": bool(maxdiff < 1e-9),
                                 "draws_file": "analysis/r4_boot_draws.npz", "seconds": time.time() - t0})
print("max abs diff vs r3:", maxdiff, "seconds", time.time() - t0)
