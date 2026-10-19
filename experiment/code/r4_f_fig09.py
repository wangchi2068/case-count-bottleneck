"""r4 F:图 9 统一为 2,000 次重抽。比较 reanalysis_results.json B_bootstrap(B=2000,州聚类,95% 百分位)
与用户仓库 empirical_stats.json lag_weights_sensitivity(B=1500,原图 9 所用)的 a、b 区间端点。
预注册:analysis/r4_preregistration.md 第 7 节。图由 figures/make_fig_r4.py 09 绘制。
"""
import json

from common import EXP, STATS
from r4_common import r4_update

st = json.loads((EXP / "analysis/reanalysis_results.json").read_text(encoding="utf-8"))["B_bootstrap"]["stats"]
old = json.loads(STATS.read_text(encoding="utf-8"))["lag_weights_sensitivity"]
rows, md = {}, {"a": 0.0, "b": 0.0}
for k in ("single_1w", "original", "equal_3w"):
    for p in ("a", "b"):
        new = st[f"{p}_{k}"]["pct95"]; o = old[k][f"{p}_ci"]
        d = [new[0] - o[0], new[1] - o[1]]
        rows[f"{p}_{k}"] = {"point": st[f"{p}_{k}"]["point"], "pct95_B2000": new, "ci_B1500": o, "diff_endpoints": d}
        md[p] = max(md[p], max(abs(x) for x in d))
r4_update("F_fig09_b2000", {"design": "预注册第 7 节;误差棒改用 B=2000 州聚类 95% 百分位区间", "rows": rows,
                            "max_abs_endpoint_diff": md,
                            "source_B2000": "analysis/reanalysis_results.json#B_bootstrap.stats",
                            "source_B1500": "用户仓库 data/empirical_stats.json#lag_weights_sensitivity(只读)",
                            "figure": "figures/r4_09_denominator_noise.pdf"})
print(json.dumps(md), json.dumps(rows, indent=0)[:1500])
