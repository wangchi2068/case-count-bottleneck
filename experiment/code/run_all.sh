#!/usr/bin/env bash
# 按依赖顺序重跑全部分析。用法:bash run_all.sh [base|r3|r4|map|all]
# 结果写到本目录上一级的 analysis/、data/、logs/。路径与数据见 README.md 第 2 节(REPO_ROOT / USER_REPO / NHSN_CSV)。
# 全程约 1.5 小时(4 核),其中 r4_a_growth_null.py 约占一小时;建议放到后台:nohup bash run_all.sh > run_all.log 2>&1 &
set -euo pipefail
cd "$(dirname "$0")"
NPROC="${NPROC:-4}"
STAGE="${1:-all}"

run() {
  local t0=$SECONDS
  echo "[$(date -u +%H:%M:%S)] >>> python3 $*"
  python3 "$@"
  echo "[$(date -u +%H:%M:%S)] <<< $1 用时 $((SECONDS - t0)) s"
}

stage_base() {   # 首轮重分析:复现门、州聚类重抽、竞争模型、制度与季节、AR(1) 仿真
  run a_reproduce.py
  run b_bootstrap.py 2000 1000
  run c_competing.py
  run d_policy_season.py 2000 500
  run e_ar1_sim.py 200
}

stage_r3() {     # 第三轮:报告率代理、制度期 V_pi、规模与季节、跨病原
  run r3_a_reporting.py 2000
  run r3_a2_period_vpi.py 2000
  run r3_b_scale_periods.py 2000
  run r3_c_pathogens.py 2000
}

stage_r4() {     # 第四轮:零假设仿真、重新分级、TOST、季随机效应、图 9、表 2、独立数据、τ 网格、一周两代
  run r4_c_boot.py
  run r4_a_growth_null.py 300 "$NPROC"
  run r4_c_classify_tost.py all
  run r4_c_posthoc.py
  run r4_e_seasons.py
  run r4_f_fig09.py
  run r4_g_table2.py
  run r4_i_independent.py 2000
  run r4_j_tau_grid.py 200 200 "$(( NPROC > 2 ? 2 : NPROC ))"
  run r4_k_two_gen.py 300 1
}

stage_map() {    # 数字地图(需要论文 LaTeX 源)与 r4 图
  if [ -d ../../paper/sections ]; then run r4_h_reproduction_map.py; else echo "跳过数字地图:找不到 ../../paper/sections"; fi
  if [ -f ../figures/make_fig_r4.py ]; then run ../figures/make_fig_r4.py 09 12 13; else echo "跳过出图:找不到 ../figures/make_fig_r4.py"; fi
}

case "$STAGE" in
  base) stage_base ;;
  r3) stage_r3 ;;
  r4) stage_r4 ;;
  map) stage_map ;;
  all) stage_base; stage_r3; stage_r4; stage_map ;;
  *) echo "未知阶段 $STAGE(可选 base|r3|r4|map|all)"; exit 2 ;;
esac
