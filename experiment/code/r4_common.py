"""r4 公共:结果文件 analysis/r4_results.json 的增量写入(加文件锁,允许多个 r4 脚本并行写不同键)。"""
import fcntl
import json
import time

from common import EXP, SEED

R4 = EXP / "analysis/r4_results.json"
LOCK = EXP / "analysis/.r4_results.lock"


def r4_update(key: str, value) -> None:
    with open(LOCK, "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        d = json.loads(R4.read_text(encoding="utf-8")) if R4.exists() else {}
        d.setdefault("provenance", {
            "mode": "measured",
            "source": "自写脚本 .work/case-count-bottleneck/experiment/code/r4_*.py(未执行用户仓库代码)",
            "preregistration": "analysis/r4_preregistration.md",
            "seed_base": SEED,
        })
        d[key] = value
        d["provenance"]["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        tmp = R4.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
        tmp.replace(R4)
        fcntl.flock(lk, fcntl.LOCK_UN)


def r4_load() -> dict:
    return json.loads(R4.read_text(encoding="utf-8")) if R4.exists() else {}
