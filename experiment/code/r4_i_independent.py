"""r4 I:独立数据。非 NHSN 方向对照(ILINet 州级 num_ili)按同一截距比管线重跑;
FluSurv-NET(Delphi flusurv,只有率)只报 q1/q2;HHS Protect(healthdata.gov g62h-syeh)只做一致性核对。

每个 URL 最多尝试 2 次,失败记「源不可达」及状态码。数据落 data/external/,sha256 记入结果与数据契约。
预注册:analysis/r4_preregistration.md 第 9 节。种子 SEED+45,B=2000。用法:python3 r4_i_independent.py [B]
"""
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request

import numpy as np
import pandas as pd

from common import EXP, SEED, WEIGHTS
from r3_common import bca, build_rows, cluster_bootstrap, cluster_index, early_index, fit, load
from r4_common import r4_update

B = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
EXT = EXP / "data/external"
EXT.mkdir(parents=True, exist_ok=True)
SPECS = ("original", "single_1w", "equal_3w")
fetch_log = []


def fetch(url, dest, tries=2, timeout=90):
    """最多 tries 次;返回 bytes 或 None,状态写入 fetch_log。dest 已存在时直接读本地文件(复现用,不访问网络)。"""
    if dest.exists():
        body = dest.read_bytes()
        fetch_log.append({"url": url, "attempt": 0, "status": "local", "bytes": len(body),
                          "file": str(dest.relative_to(EXP)), "sha256": hashlib.sha256(body).hexdigest()})
        return body
    last = None
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "apevon-research/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read()
                last = r.status
            dest.write_bytes(body)
            fetch_log.append({"url": url, "attempt": k + 1, "status": last, "bytes": len(body),
                              "file": str(dest.relative_to(EXP)), "sha256": hashlib.sha256(body).hexdigest()})
            return body
        except urllib.error.HTTPError as e:
            last = e.code
        except Exception as e:  # noqa: BLE001 —— 记录任何网络错误
            last = f"{type(e).__name__}: {e}"[:200]
        fetch_log.append({"url": url, "attempt": k + 1, "status": last})
        time.sleep(3)
    return None


def epiweek_end(ew):
    """MMWR 周号 → 周六(与 NHSN Week Ending Date 同口径)。"""
    y, w = divmod(int(ew), 100)
    jan4 = pd.Timestamp(y, 1, 4)
    # MMWR 第 1 周 = 含 1 月 4 日的那一周(周日起),周末为周六
    wk1_sun = jan4 - pd.Timedelta(days=(jan4.dayofweek + 1) % 7)
    return wk1_sun + pd.Timedelta(days=7 * (w - 1) + 6)


def series_from(df, col, unit):
    """df: unit, week_end, col → 与 r3_common.series 同结构;报告代理 h 置 1(无代理,Δa 不报)。"""
    out = {}
    for s, sub in df.sort_values([unit, "week_end"]).groupby(unit):
        sub = sub.drop_duplicates("week_end")
        full = pd.date_range(sub.week_end.min(), sub.week_end.max(), freq="7D")
        sub = sub.set_index("week_end").reindex(full)
        if len(sub) < 10:
            continue
        c = sub[col].to_numpy(float)
        miss = ~np.isfinite(c)
        out[s] = {"c": np.where(miss, 0, c), "h": np.ones(len(c)), "hn": np.ones(len(c)), "week": full.to_numpy(),
                  "miss": miss}
    return out


def intercept_pipeline(ser, select, dmin, seed, B):
    rows = {s: build_rows(ser, WEIGHTS[s], select, dmin=dmin) for s in SPECS}
    rows = {s: r[~r.any_missing].reset_index(drop=True) for s, r in rows.items()}
    data = {s: {"G": r.G.to_numpy(), "D": r.D.to_numpy(), "state": r.state.to_numpy()} for s, r in rows.items()}
    names = [f"{k}_{s}" for s in SPECS for k in ("rbar", "a", "b")] + ["q1", "q2", "vR_implied"]

    def stat_fn(rb):
        v = {}
        for s in SPECS:
            d = data[s]; i = rb[s]
            v[f"rbar_{s}"], v[f"a_{s}"], v[f"b_{s}"] = fit(d["G"][i], d["D"][i])
        v["q1"] = v["a_single_1w"] / v["a_original"]; v["q2"] = v["a_equal_3w"] / v["a_original"]
        v["vR_implied"] = v["a_original"] * v["rbar_original"] ** 2
        return np.array([v[k] for k in names])

    units = sorted(set(data["original"]["state"]))
    idx = {s: cluster_index(data[s]["state"]) for s in SPECS}
    rng = np.random.default_rng(seed)
    theta, boot, jack = cluster_bootstrap(stat_fn, units, idx, B, rng)
    st = {}
    for j, k in enumerate(names):
        x = boot[:, j]
        st[k] = {"point": float(theta[j]), "pct95": [float(v) for v in np.percentile(x[np.isfinite(x)], [2.5, 97.5])],
                 "bca95": list(bca(x, theta[j], jack[:, j]))}
    q1b, q2b = st["q1"]["bca95"], st["q2"]["bca95"]
    jq1, jq2 = names.index("q1"), names.index("q2")
    return {"N": int(len(rows["original"])), "n_units": len(units), "D_median": float(np.median(data["original"]["D"])),
            "stats": st, "direction_q1_lt1_lt_q2_bca": bool(q1b[1] < 1 < q2b[0]),
            "boot_share_q1_lt1_and_q2_gt1": float(np.mean((boot[:, jq1] < 1) & (boot[:, jq2] > 1)))}


wcal = lambda wk: early_index(wk) >= 0
res = {"design": "预注册第 9 节;同一截距比管线(D≥5、FGLS、州聚类重抽 BCa),窗口 = 用户日历窗口 W-cal;只看方向",
       "B": B, "seed": SEED + 45}

# 1) ILINet(非 NHSN,门诊 ILI 就诊数;已在本步先行下载,文件存在则不重抓)
ili_f = EXT / "ilinet_fluview_states_202235_202530.json"
if not ili_f.exists():
    st_list = sorted(set(load("flu").state))
    recs = []
    for i in range(0, len(st_list), 10):
        regs = ",".join(s.lower() for s in st_list[i:i + 10])
        body = fetch(f"https://api.delphi.cmu.edu/epidata/fluview/?regions={regs}&epiweeks=202235-202530",
                     EXT / f"ilinet_chunk{i // 10}.json")
        if body:
            recs += json.loads(body).get("epidata") or []
    ili_f.write_text(json.dumps(recs), encoding="utf-8")
else:
    fetch_log.append({"url": "https://api.delphi.cmu.edu/epidata/fluview/?regions=<51 州分 6 批>&epiweeks=202235-202530",
                      "attempt": 1, "status": 200, "file": str(ili_f.relative_to(EXP)), "note": "本步先行下载,6 批均 200"})
ili_raw = ili_f.read_bytes()
ili = pd.DataFrame(json.loads(ili_raw))
ili["week_end"] = [epiweek_end(e) for e in ili.epiweek]
ili["state"] = ili.region.str.upper()
ili_ser = series_from(ili, "num_ili", "state")
res["ILINet"] = {"source": "Delphi Epidata fluview(CDC ILINet 州级),字段 num_ili",
                 "url": "https://api.delphi.cmu.edu/epidata/fluview/?regions=<state>&epiweeks=202235-202530",
                 "file": str(ili_f.relative_to(EXP)), "sha256": hashlib.sha256(ili_raw).hexdigest(),
                 "n_records": int(len(ili)), "n_states": int(ili.state.nunique()),
                 "caveat": "门诊 ILI 就诊数受报告点数与就诊总数变化影响,非入院计数;只作方向对照,不并入主估计",
                 "W-cal": intercept_pipeline(ili_ser, wcal, 5.0, SEED + 45, B)}
print("ILINet", {k: res["ILINet"]["W-cal"]["stats"][k]["bca95"] for k in ("q1", "q2", "a_original")},
      res["ILINet"]["W-cal"]["N"])
r4_update("I_independent_data", {**res, "fetch_log": fetch_log})

# 2) FluSurv-NET(Delphi flusurv;只有每 10 万人率 → 不用 D≥5 过滤,规模项无计数含义,只报 q1/q2)
locs = "CA,CO,CT,GA,MD,MI,MN,NM,NY_albany,NY_rochester,OH,OR,TN,UT"
fs_f = EXT / "flusurv_sites_202235_202530.json"
body = fetch(f"https://api.delphi.cmu.edu/epidata/flusurv/?locations={locs}&epiweeks=202235-202530", fs_f)
fs_recs = (json.loads(body).get("epidata") or []) if body else []
if fs_recs:
    fs = pd.DataFrame(fs_recs)
    fs["week_end"] = [epiweek_end(e) for e in fs.epiweek]
    fs_ser = series_from(fs, "rate_overall", "location")
    try:
        r = intercept_pipeline(fs_ser, wcal, 1e-9, SEED + 45, B)
        r = {"N": r["N"], "n_units": r["n_units"], "q1": r["stats"]["q1"], "q2": r["stats"]["q2"],
             "direction_q1_lt1_lt_q2_bca": r["direction_q1_lt1_lt_q2_bca"],
             "boot_share_q1_lt1_and_q2_gt1": r["boot_share_q1_lt1_and_q2_gt1"]}
    except Exception as e:  # noqa: BLE001
        r = {"error": f"{type(e).__name__}: {e}"}
    res["FluSurv-NET"] = {"status": "ok", "file": str(fs_f.relative_to(EXP)), "sha256": hashlib.sha256(body).hexdigest(),
                          "n_records": len(fs_recs), "caveat": "率数据,a 的绝对值无计数含义;站点仅 14 个,聚类重抽单元少",
                          "W-cal": r}
    print("FluSurv", r)
else:
    res["FluSurv-NET"] = {"status": "源不可达", "detail": [x for x in fetch_log if "flusurv" in x["url"]]}
r4_update("I_independent_data", {**res, "fetch_log": fetch_log})

# 3) HHS Protect(healthdata.gov g62h-syeh;日度,2024-04 后停更)→ 周汇总后与 NHSN 流感入院做一致性核对
q = ("https://healthdata.gov/resource/g62h-syeh.json?$select=state,date,previous_day_admission_influenza_confirmed"
     "&$where=date%3E='2022-09-25'%20AND%20date%3C'2023-12-31'&$limit=60000")
hp_f = EXT / "hhs_protect_g62h_syeh_flu_2022_2023.json"
body = fetch(q, hp_f, timeout=120)
if body:
    try:
        hp = pd.DataFrame(json.loads(body))
        hp["date"] = pd.to_datetime(hp.date)
        hp["v"] = pd.to_numeric(hp.previous_day_admission_influenza_confirmed, errors="coerce")
        # previous_day_* 记的是前一日入院;前移一天后按周六结束的周汇总
        hp["adm_day"] = hp.date - pd.Timedelta(days=1)
        hp["week_end"] = hp.adm_day + pd.to_timedelta((5 - hp.adm_day.dt.dayofweek) % 7, unit="D")
        wk = hp.groupby(["state", "week_end"]).v.sum(min_count=1).reset_index()
        nh = load("flu")
        m = wk.merge(nh[["state", "week_end", "C"]], on=["state", "week_end"])
        m = m[np.isfinite(m.v)]
        rel = (m.v - m.C) / m.C.where(m.C > 0)
        res["HHS_Protect"] = {"status": "ok", "file": str(hp_f.relative_to(EXP)), "sha256": hashlib.sha256(body).hexdigest(),
                              "n_state_weeks_matched": int(len(m)), "pearson_r": float(np.corrcoef(m.v, m.C)[0, 1]),
                              "median_abs_rel_diff": float(np.nanmedian(np.abs(rel))),
                              "share_identical": float(np.mean(m.v == m.C)),
                              "note": "一致性核对,不另作估计"}
    except Exception as e:  # noqa: BLE001
        res["HHS_Protect"] = {"status": "解析失败", "error": f"{type(e).__name__}: {e}"[:300]}
else:
    res["HHS_Protect"] = {"status": "源不可达", "detail": [x for x in fetch_log if "healthdata" in x["url"]]}
print("HHS", {k: v for k, v in res["HHS_Protect"].items() if k != "detail"})
r4_update("I_independent_data", {**res, "fetch_log": fetch_log})
