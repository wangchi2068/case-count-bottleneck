# 论文结构化精读

本文档精读两篇论文。第一部分是用户的小论文《病例规模与再生数估计精度:环境波动下的收益边界及美国流感住院数据检验》,第二部分是参照文献 Parag、Donnelly 与 Zarebski 2022 年发表在 Nature Computational Science 上的 Quantifying the information in noisy epidemic curves [1],第三部分对照两文,汇总对另一份 AI 分析的核实结论,并给出范本裁决。第四部分按用户补充的要求,以同行审稿人身份给出意见和分项评分。

几点说明:

- 用户论文的数字都标注了出处。正文出处写作 sections/文件名:行号;仓库结果文件写作 JSON 路径,例如 empirical_stats.json 中的 early.affine.b。
- Parag 2022 的内容以上传 PDF 为准,页码用期刊页码 584–594。
- 文中凡标注"评注"的段落,是精读者的判断,不是原文内容。

---

## 第一部分 用户论文精读

### (1) 一句话总结

论文以负二项传播和二项报告构成单代模型,区分两个估计目标:当期再生数 $R_t$ 与跨期平均水平 $\bar R$。对前者,估计量 $C_t/(\rho n)$ 在任意有限规模上达到 Cramér–Rao 下界;对后者,方差为 $v_R+A/m$,其中环境方差 $v_R$ 构成一个扩大规模也无法消除的下限。论文用交叉点 $m_\times=A/v_R$ 刻画规模收益开始递减的位置,并用美国 NHSN 流感住院数据检验误差是否呈"常数加规模反比"的形状。

### (2) 核心贡献

论文自述有三项贡献(introduction.tex:10–15)。

1. 区分两个估计目标。目标Ⅰ的方差随规模趋于零。目标Ⅱ的方差有环境底板,二者的过渡由 $m_\times$ 刻画:规模达到 $m_\times$ 后再翻一倍,方差只降 25%。
2. 从方差结构推出三条监测设计结论:
   - 扩大覆盖面比提高报告率更有效(命题3);
   - 多期预算下的最优单期规模为 $m^*=\sqrt{(c_0/c_1)m_\times}$(推论1),这个问题与 Cochran 两阶段抽样的费用分配同构 [6];
   - 小规模下应使用精确增长检验(命题5)。
3. 用 16,218 个州周的住院数据检验误差形状,得到经验交叉点 22.6 例/周,与情景区间 21.3–49.2 处在同一量级。论文同时说明,截距与斜率都被放大。

评注:

- 命题1 是单参数指数族的标准结论。命题2 是全方差公式的直接应用。数学上的新意有限,论文的价值在于把环境方差单列为一个成分,并由此导出监测设计的结论。
- Parag 等 [1] 的 Fisher 信息框架只处理当期 $R_t$。用户论文在讨论部分(discussion.tex:15)把自己的目标Ⅰ结论与之对齐,目标Ⅱ才是增量所在。
- 写作上,引言应把这一定位说清楚:已有工作量化的是给定数据所含的关于 $R_t$ 的信息,本文增加的是"信息无法降低的那部分误差"。

### (3) 方法

**模型**(model.tex:4–29)。给定 $R_t$,$n$ 名上一代感染者各自产生 $X_i\sim\mathrm{NB}(k,\,k/(k+R_t))$ 个继发感染,均值为 $R_t$,离散参数为 $k$(负二项是刻画超传播的常用分布 [5])。每例感染以概率 $\rho$ 被报告。由负二项分布的可加性和二项稀疏后的封闭性(附录 A.1 用概率母函数证明),报告数满足

$$C_t\mid n,R_t\sim \mathrm{NB}\!\left(nk,\ \frac{k}{k+\rho R_t}\right),\qquad \mathrm{E}(C_t\mid n,R_t)=\rho nR_t,\qquad \mathrm{Var}(C_t\mid n,R_t)=\rho nR_t+\frac{\rho^2nR_t^2}{k}.$$

记 $m=\rho n$。各期 $R_t$ 围绕均值波动,$\mathrm{E}(R_t)=\bar R$,$\mathrm{Var}(R_t)=v_R$。

**假设 H1–H4**(model.tex:44–54):

- H1:给定 $R_t$ 时条件独立;
- H2:同期感染者共享同一个 $R_t$;
- H3:$k$ 与 $\rho$ 已知;
- H4:规模 $n$ 与当期环境无关。

作者在 model.tex:54 自己指出,真实监测序列不满足 H4。

**理论推导**:

- 命题1 用得分函数的形式 $\mathcal I(R_t)(\hat R_t-R_t)$ 证明有限样本下达到 CRLB,用完备充分统计量证明 UMVUE。
- 命题2 用全方差公式。
- 命题4 用 AR(1) 部分和的方差。
- 推论1 对 $f(m)=(c_0+c_1m)(v_R+A/m)/\mathcal B$ 求极小。
- 命题5 用单调似然比与 Karlin–Rubin 定理。
- 第5节的注1 两次使用全方差公式,把感染压力 $\Lambda_{t+1}$ 的不确定性加进分解:

$$\frac{\mathrm{Var}(C_{t+1}\mid\mathcal F_t)}{[\rho\,\mathrm{E}(\Lambda_{t+1}\mid\mathcal F_t)]^2}=v_R+\frac{A}{m}+\mathrm{CV}^2(\Lambda_{t+1}\mid\mathcal F_t)\,(\bar R^2+v_R).$$

**数值核对**:

- 命题1 用蒙特卡洛核对:10 个规模,每个规模 20,000 次。
- 第5节用更新过程仿真(每个初始规模 400 条轨迹,种子 20261014)考察单代公式在时间序列中的表现。

**实证**(empirical.tex):

- 数据为 NHSN 州级流感住院周报。
- 规模代理取 $D_t=0.65C_t+0.25C_{t-1}+0.10C_{t-2}$,增长统计量取 $G_t=C_{t+1}/D_t$,损失为 $L_t=[(G_t-\bar R)/\bar R]^2$。
- 用加权最小二乘拟合 $\mathrm{E}(L_t\mid D_t)\approx a+b/D_t$。理论上 $a=v_R/\bar R^2$,$b=A/\bar R^2$,$b/a=m_\times$。
- 置信区间来自聚类 bootstrap(1,500 次)。
- 稳健性检验包括:替换滞后权重、剔除极值、工具变量(滞后 3–5 周的规模)、Cori 滑动窗口基准、全国汇总序列、FluSight 集成预测、欧洲 COVID-19 数据。

### (4) 主要结果

下表的数字均可追溯。JSON 路径都相对于用户仓库的 code_and_data/ 目录。

| 结果 | 数值 | 正文位置 | 可追溯来源 |
|---|---|---|---|
| 蒙特卡洛方差与 CRLB 之比 | 0.98–1.02($m$=1–1000) | variance.tex:24 | results/sim_theory.json → variance_mc.rows[].ratio_I |
| 示例参数下的 $A$ 与 $m_\times$($\bar R=1.15$, $v_R=0.04$, $k=0.35$, $\rho=0.25$) | $A=2.1232$,$m_\times=53.1$ | 第3.2节 | results/checks/c03_prop2_mx_prop3.json 记录 3.3;本次独立 sympy 复算一致 |
| 规模翻倍时的方差降幅 | 42.1% / 25.0% / 10.5%($m$=10 / 53.1 / 200) | 第3.2节 | c03 记录 3.6.*;复算一致 |
| 住院情景下 $A/\bar R$ | 1.02–1.18(覆盖面与报告率几乎等效) | 第3.3节 | c03 记录 3.12 |
| 最优单期规模 $m^*$ | 14.6–22.2($c_0/c_1=10$);46.1–70.1($c_0/c_1=100$) | design.tex:45 | results/checks/c05_cor1.json |
| Wald 检验实际水平 | 7.81%($k=0.1$,$m=5$,名义 5%) | 第4.2节 | sim_theory.json → growth_test |
| 更新过程:模拟误差与单代参照之比 | 按初始规模 0.75–0.98;按实际规模 $D_t<400$ 为 1.04–1.23,$D_t\ge400$ 为 0.98–1.03 | 第5.2节 | sim_theory.json → renewal.groups |
| 样本 | 16,218 州周,有效观测 10,303,流行初期 1,267 | empirical.tex:6–16、第6.2节 | data/empirical_stats.json → n_state_weeks, n_valid, early.N |
| 流行初期拟合 | $\bar R=1.6706$;$a=0.0991$(0.0841–0.1173);$b=2.2434$(1.5019–3.0161);$b/a=22.6$(13.7–33.7) | 第6.2节 | early.R_bar;early.affine.{a,b,m_x};区间见正文 |
| 剔除 1% 极值后的交叉点 | 10.6 | 第6.2节 | early.affine_trim1pct.m_x |
| 误差份额(环境 / 规模 / 模型外) | 54.6% / 45.1% / 0.2% | 第6.2节 | early.error_budget.* |
| 截距与斜率对情景值的倍数 | $a$ 为 3.5–6.9 倍,$b$ 为 3.2–3.7 倍 | 第6.2–6.3节 | results/checks/c09_empirical.json 记录 9.31、9.32 |
| 滞后权重敏感性(原始 / 单周 / 等权) | 斜率 2.243 / 3.134 / 1.926;截距 0.0991 / 0.0682 / 0.1524 | 第6.3节 | lag_weights_sensitivity.{original, single_1w, equal_3w} |
| 达峰期 | 损失的 88.9% 来自基准偏移;换用峰期基准后 $a=0.0665$,$b=7.927$,交叉点 119.2 | 第6.4节 | peak.bias_share;peak.affine_cond.* |
| 报告制度切换前后 $G_t$ 的标准差 | 0.624 → 1.823 → 0.649(四分位距几乎不变) | 第6.4节 | policy.period{1,2,3}.g_std |
| 工具变量 | $b=2.53$,一阶段 $F=1147.1$ | 第6.5节 | seasonal_subsample_iv.pooled_within_phase |
| Cori 窗口基准的平均损失 | 2 周窗 0.288,3 周窗 0.249(阶段均值基准 0.181) | empirical.tex:138 | competing_baselines.overall.* |
| 全国汇总序列的平均损失 | 0.0348,约为单州截距的三分之一 | 第6.5节 | national.relmse_mean |
| 外部对照 | FluSight 交叉点 60.3,峰期偏差占比 15.5%;欧洲 COVID-19 交叉点 124.7 | 第6.5节 | extended_validation_flusight.*;extended_validation_covid19.sensitivity_table[0] |
| 各规格经验交叉点的范围 | 10.6–124.7,规模项在所有规格下为正 | empirical.tex:119 | 汇总自上列各项 |

**理论核心公式**(命题2):

$$V(m)=\mathrm{Var}(\hat R_t\mid n)=v_R+\frac{\bar R}{\rho n}+\frac{\bar R^2+v_R}{kn}=v_R+\frac{A}{m},\qquad A=\bar R+\frac{\rho(\bar R^2+v_R)}{k},\qquad m_\times=\frac{A}{v_R}.$$

### (5) 局限与未解问题

**作者在第7.2节自列七条局限**(discussion.tex:17–40):

1. 周增长比 $G_t$ 跨约两代,与单代 $R_t$ 的口径不同,因此实证只检验了误差形状。
2. 分母 $D_t$ 含报告噪声,会抬高斜率,使 $b/a$ 高估 $m_\times$。
3. 单代公式在时间序列中不构成下界。
4. 环境存在时间相关,而理论部分没有对这种相关建模。
5. 聚类重抽只做了单向,工具变量也有弱点。
6. $k$ 与 $\rho$ 依赖外部取值。
7. 样本窗口是事后划定的,第二期缺失的 36 个州周按 0 处理。

**精读者补充的问题**:

- **目标Ⅱ的估计设定不自然。** 用单期估计量 $\hat R_t$ 去估计 $\bar R$,方差底板 $v_R$ 是这一设定的直接结果。实际估计 $\bar R$ 时会使用多期数据,底板随之变为 $v_R/T$ 或 AR(1) 下的对应式,命题4 已经给出。在讲义和重构稿中,应把"单期估计跨期均值"作为一个刻意的分析设定写明,否则审稿人会质疑底板是人为构造出来的。
- **理论与实证之间有断层。** 理论参数是单代的 $k$、$\rho$、$v_R$,实证拟合的是两代合成的 $G_t$ 的损失。拟合出的 $a$、$b$ 都是理论值的三倍以上,所以实证只支持"常数加反比"这一函数形状,支持不了 $m_\times$ 的数值。论文已经承认这一点,但摘要和引言仍把 22.6 与情景区间并列,容易让读者误读为数值吻合。
- **自查记录里还有两处未在正文交代。**
  - c12 记录 12.3/12.4:保留二阶项后,斜率多出 $2(v_R/\bar R^2)c$,占比约 1.8%。附录 A.8 只给出一阶结果,没有注明略去了这一项。
  - c06 有一条蒙特卡洛核对未通过($z=-4.45$),记录本身要求用多种子复核。它不在主结论链上,但复现说明里应交代复核结果。
- **H3 在实践中只是近似。** 精确检验与 CRLB 都要求 $k$ 已知。$k$ 由数据估计时,两者都只是近似成立。
- **题目与英文摘要。** 导师已指出题目需要改。论文只有中文摘要;按领域惯例,中文期刊通常也要求英文摘要。

### (6) 摘要的忠实中文翻译

原摘要本身就是中文,没有英文版本,因此照录原文(abstract.tex:2;只把 LaTeX 宏改写为通用记号)。

> 多收集病例能让再生数估计精确多少,取决于要估计什么。本文在负二项传播与二项报告的框架下区分两个估计目标。估计当期再生数时,报告数除以预计报告规模得到的估计量在每个有限规模上都达到 Cramér–Rao 下界,方差随规模趋于零。估计跨期平均传播水平时,方差为 $v_R+A/m$,其中 $v_R$ 是环境波动造成的方差,$m$ 是预计报告病例数;环境项构成规模无法突破的底板。两项相等处的交叉点 $m_\times=A/v_R$ 为规模提供了一把尺子。规模达到 $m_\times$ 后,再翻一倍只能把方差降低 25%。这一结构有三点设计含义。扩大覆盖面比提高报告率更能压低方差。多期预算下,最优单期规模取成本比与交叉点的几何平均。小规模时应使用精确增长检验,常用的正态近似检验会超过名义水平。更新过程仿真表明,在时间序列中单代公式只能作参照曲线,不构成误差下界。本文用美国国家医疗安全网络 16,218 个州周的流感住院数据做检验。流行初期的预测误差呈"常数加规模反比"的形状,经验交叉点为 22.6 例/周,与理论情景区间 21.3–49.2 同一量级。规模项在多种替代规格和两组外部数据中都为正。拟合的截距与斜率则都在情景隐含值的三倍以上。滞后权重的比较表明,报告噪声使分母随机,抬高了斜率;截距随分母的回溯滞后上升,与环境的时间相关一致。因此经验交叉点只能作量级参考。达峰期 88.9% 的误差来自基准偏移,换用阶段自身基准后规模效应依然存在。结果提示,预警和趋势估计宜分开设计。
>
> 关键词:再生数;环境随机性;超传播;监测规模;方差分解;流感住院

---

## 第二部分 参照文献 Parag (2022) 精读

书目:Kris V. Parag, Christl A. Donnelly, Alexander E. Zarebski. Quantifying the information in noisy epidemic curves. Nature Computational Science, 2022, 2: 584–594. DOI 10.1038/s43588-022-00313-1 [1]。2022 年 3 月 1 日收稿,8 月 8 日接收,9 月 26 日在线发表。代码与数据见 https://github.com/kpzoo/information-in-epidemic-curves 。

### (1) 一句话总结

作者用 Fisher 信息量化漏报和报告延迟使发病曲线损失多少关于瞬时再生数 $R_t$ 的信息,得到一个只依赖监测特征的无量纲指标 $\theta=G(\rho_t)\,G(F_{\tau-t})$,并用它说明"死亡曲线比病例曲线更可靠"这一常见看法在许多情形下并不成立。

### (2) 核心贡献

1. **解析框架。** 在更新模型下推导出带噪观测序列关于 $R_1,\dots,R_\tau$ 的总信息,不依赖仿真,作者称之为 simulation-agnostic(p585)。
2. **核心结果(p587,式 5)。** 信息损失只取决于报告比例的几何均值与累积延迟概率的几何均值之积。由试验设计理论可以证明:
   - 均值固定时,恒定报告(CONR)信息最多;
   - 延迟分布越分散越好,固定延迟反而损失最大,因为它在序列末端造成信息瓶颈(p587–588)。
3. **数据流排序(式 7–8,p589)。** 给出病例与死亡数据的比较准则,充分条件为 $G(\rho_t)\ge \mathrm{ifr}\approx0.01$。按 COVID-19 的报告率估计,45%–90% 的 Beta 报告分布满足这一条件,病例数据信息更多。
4. **实际应用(Fig. 5,p590–591)。** 对 COVID-19,病例数据信息更多。对 EVD,由于感染致死率高,死亡数据可能更可靠,但若死亡确诊率 $\sigma_t\ll1$,结论就可能反转。

### (3) 方法

更新模型(Methods,式 9–10,p591)为

$$I_t\sim\mathrm{Pois}(\Lambda_tR_t),\qquad \Lambda_t=\sum_{s=1}^{t-1}w_sI_{t-s},\qquad \ell(R_{1:\tau})=\sum_t\left(I_t\log R_t-\Lambda_tR_t\right)+\text{const}.$$

由此得到 $\mathrm{FI}(R_t)=\Lambda_t/R_t$。作者做变换 $2\sqrt{R_t}$ 使信息与参数无关,即 $\mathrm{FI}(2\sqrt{R_t})=\Lambda_t$(式 11,p592)。总信息 $T(I)=\prod_t\sqrt{\Lambda_t}$ 定义为 Fisher 信息矩阵行列式的平方根,对应 D-optimal 设计准则(式 12–13)。

引入报告比例 $\rho_t$ 与延迟分布 $\delta_x$ 后,病例满足 $C_t\sim\mathrm{Pois}\big(\sum_x\delta_{t-x}\rho_x\Lambda_xR_x\big)$(式 1,p586)。

- 在 OBNR 延迟下,$\mathcal F_C(R_t)=\rho_tF_{\tau-t}\Lambda_t/R_t$(式 15),$T(C)=\prod_t\sqrt{\rho_tF_{\tau-t}\Lambda_t}$(式 3)。
- 与理想数据相比,$\eta(C)=T(C)/T(I)=\prod_t\sqrt{\rho_tF_{\tau-t}}\le1$(式 4)。$\Lambda_t$ 在比值中消去,所以结论对世代间隔设定不敏感。
- 对长度取几何平均,得到 $\theta(C)=G(\rho_t)\,G(F_{\tau-t})$(式 5)。
- NEVR 延迟下,式 16–18 给出信息上界。
- 推导中用到 Cramér–Rao 界(p591)和数据处理不等式(p592)。

案例分析部分:

- 用 Beta 分布产生报告比例,用负二项分布产生延迟,每组各取 $10^4$ 个样本,覆盖 2,000 种分布形状(Fig. 2–4)。
- 对 COVID-19 与 EVD 的噪声参数,按最大熵原则设均匀分布,再用蒙特卡洛传播不确定性(p590)。

### (4) 主要结果

| 结果 | 内容 | 页 |
|---|---|---|
| 报告比例 | 均值 $\bar\rho$ 固定时,$\bar\rho=\arg\max G(\rho_t)$,恒定报告信息最多;报告比例在 0 与 1 之间极端切换时最差 | 587–588,Fig. 2 |
| 报告延迟 | 平均延迟固定时,分散的延迟分布(少数病例延迟很长、多数很短)信息最多;固定延迟最差,因为截去末端造成瓶颈 | 588,Fig. 3 |
| 病例与死亡 | 当 $\theta(C)\ge\mathrm{ifr}$ 时病例更可靠;$\bar\rho=0.07$ 时约 45% 的报告分布满足,$\bar\rho=0.38$ 时约 90% 满足;即使死亡确诊完全,1% 的 ifr 也意味着丢失 99% 的发病信息 | 589,Fig. 4 |
| 实际应用 | COVID-19 死亡数据的信息少于病例;EVD 死亡数据可能信息更多,但对确诊率敏感 | 590–591,Fig. 5 |
| 局限(作者自述) | 依赖更新模型(均匀混合、已知世代间隔);需要噪声参数的估计;假设各 $R_t$ 独立;采用 D-optimal 而非 E-optimal 准则 | 591 |

### (5) 局限与未解问题

**作者自述**(Discussion,p591):

- 框架依赖更新模型,假设均匀混合、世代间隔已知。不过,相对指标中的 $\Lambda_t$ 相互抵消,因此对世代间隔的误设比较稳健。
- 需要延迟和漏报的估计;完全没有估计时,$R_t$ 不可识别。
- 假设各期 $R_t$ 独立;相关时需要加入非对角项,或把指标当作上界使用。
- 信息准则选用 D-optimal,若关心最差情形则应使用 E-optimal。

**精读者补充**:

- 观测模型是泊松分布。文中说负二项传播在解析上不易处理,并称补充材料中的结果不受影响(p586)。上传的 PDF 不含补充材料,这一点无法核对。
- 框架只量化关于当期 $R_t$ 的信息。环境波动造成的"信息无法降低的误差"不在其范围内,用户论文的目标Ⅱ正好补在这里。
- 案例分析中的噪声参数来自均匀分布假设,结论是"可能不成立",不是"不成立"。作者的措辞(possibly untrue in many settings)与证据强度相称。这正是用户论文可以学的地方。

### (6) 英文摘要逐句忠实翻译

1. Reliably estimating the dynamics of transmissible diseases from noisy surveillance data is an enduring problem in modern epidemiology.
   从带噪的监测数据中可靠地估计传染病的传播动态,是现代流行病学中一个长期存在的问题。
2. Key parameters are often inferred from incident time series, with the aim of informing policy-makers on the growth rate of outbreaks or testing hypotheses about the effectiveness of public health interventions.
   关键参数通常由发病时间序列推断,目的是向决策者提供疫情增长速度的信息,或检验关于公共卫生干预效果的假设。
3. However, the reliability of these inferences depends critically on reporting errors and latencies innate to the time series.
   然而,这些推断的可靠性在很大程度上取决于时间序列固有的报告误差与报告延迟。
4. Here, we develop an analytical framework to quantify the uncertainty induced by under-reporting and delays in reporting infections, as well as a metric for ranking surveillance data informativeness.
   本文建立了一个解析框架,用以量化感染漏报和报告延迟所引起的不确定性,并提出一个按信息量对监测数据排序的指标。
5. We apply this metric to two primary data sources for inferring the instantaneous reproduction number: epidemic case and death curves.
   我们将该指标应用于推断瞬时再生数的两类主要数据来源:病例曲线和死亡曲线。
6. We find that the assumption of death curves as more reliable, commonly made for acute infectious diseases such as COVID-19 and influenza, is not obvious and possibly untrue in many settings.
   我们发现,在 COVID-19 和流感等急性传染病中常见的"死亡曲线更可靠"这一假定并不显然,在许多情形下可能并不成立。
7. Our framework clarifies and quantifies how actionable information about pathogen transmissibility is lost due to surveillance limitations.
   该框架阐明并量化了监测条件的局限如何使关于病原体传播力的、可据以行动的信息丢失。

---

## 第三部分 两文对照

### 3.1 结构与行文差异

| 维度 | Parag 2022 [1] | 用户论文 | 重构时的建议 |
|---|---|---|---|
| 总体骨架 | 无标题引言 → Results(7 个粗体段首小标题)→ Discussion(无小节)→ Methods(3 个小标题)→ 数据与代码可得性 | 引言 → 模型 → 方差结构 → 监测设计 → 时间序列 → 实证 → 讨论 → 结论 → 附录证明 | 中文期刊通常保留编号章节,不必照搬 Nature 的 Methods 后置;但可借鉴其"正文给结论式,推导进附录"的做法,把第3–4节的证明性文字压缩 |
| 引言 | 约 11 段:定义 $R_t$ 及其用途 → 监测质量决定可靠性 → 各类代理数据 → 两种噪声 → 缺口段 → Here we develop → We prove → We find → 意义 | 5 段:直觉 → "两处不成立" → 一段文献 → "三项结果"编号列表 → 结构段 | 缺口单独成段,并点名已有工作做到哪一步;贡献改为两三段连贯叙述,去掉编号列表 |
| 缺口句 | there exists no formal framework for assessing and exposing how they inherently limit information(p585) | "它们很少把环境波动单列为一个方差成分"(introduction.tex:8),夹在文献段末 | 写成独立的缺口段,先肯定已有框架(Fisher 信息、更新模型),再说明它们没有处理信息无法消除的误差 |
| 结论的语气 | We find… possibly untrue in many settings;限定语与证据相称 | "只能作量级参考"等保留语在多处重复;另有"一把尺子""无济于事"等口语 | 每个结论只说一次,限定语跟在具体数字后面,删去比喻 |
| 段落 | 主题句加 2–4 句展开,用 However、In contrast、Importantly 衔接,句长自然变化 | 大量单分句短句连排,一句一事,读起来碎 | 把相关短句合并成复句,用因果、转折连接,避免"第一处……第二处……"式框架 |
| 图 | 5 张图,每张对应 Results 的一个小节;图注先用一句粗体概括结论,再逐个说明面板 | 图较多,框架图放在引言 | 图注采用"一句话结论加面板说明"的格式 |
| 局限 | Discussion 中一段完成,用 First / Further / We also assume / Finally 串联 | 单独小节,七条,每条一段 | 可保留七条内容,但合并为两三段,按"模型假设、数据口径、推断方法"归类 |
| 数据与代码 | 正文末尾单列 Data availability 与 Code availability | 附录 B 复现说明 | 保留附录,另加一段数据与代码可得性声明 |

**诊断**:修改说明 docs/小论文_修改说明.md 第四节记录,上一轮按"主语在前、一句只讲一件事"做了改写。空话和欧化句式删掉了,但又走到另一个极端。现在全文都是短句,每段都有"三项""两处"这类预告数字,还加了"要说清楚""一把尺子"这样对读者讲话的口语。导师说"AI 味太大",主要指的就是这些。相关样例与行号已整理在精读笔记中,下游重构稿会逐条处理。

### 3.2 对另一份 AI 分析的核实结论

| 条目 | 结论 | 说明 |
|---|---|---|
| Parag 2022 的书目信息 | 正确(以 PDF 为准) | 首页与页脚为 Nature Computational Science, VOL 2, September 2022, 584–594,DOI 10.1038/s43588-022-00313-1。PDF 未印期号,9 月号对应第 9 期,属于推断 |
| 该文是"封面文章" | 需修正(说法不成立) | PDF 全文没有封面字样。期刊该期(第 2 卷第 9 期)目录页显示,封面主题是诺贝尔奖与计算科学专题(A computational account of Nobel Prize history),与本文无关。本文确实收录在该期,并配有一篇同期 News & Views 评述:McGough, Getting the most out of noisy surveillance data [9]。因此可以写"获同期 News & Views 评述",不能写"封面文章" |
| 粘贴给出的 Parag 结构骨架 | 未核实,以真实结构为准 | 粘贴内容没有附具体骨架文本可供逐项比对。真实结构是:无标题引言、Results 七个段首小标题、无小节的 Discussion、放在最后的 Methods。任何按"引言—方法—结果—讨论"顺序写的骨架都与原文不符 |
| 个体负二项后代 + 二项报告稀疏 | 正确 | 与用户论文 model.tex 一致。自写 sympy 脚本用概率母函数验证了稀疏后仍为负二项 $\mathrm{NB}(nk,\cdot)$,均值 $\rho nR_t$,方差 $\rho nR_t+\rho^2nR_t^2/k$ |
| $\mathrm{Var}(\hat R_t-\bar R)=v_R+A/m$,$A=\bar R+\rho(\bar R^2+v_R)/k$ | 正确(在 H1–H4 下) | 由全方差公式逐项复算一致;因为 $\hat R_t$ 对 $\bar R$ 无偏,这就是均方误差 |
| $m_\times=A/v_R$ 及示例数值 | 正确 | 复算得 $A=2.1232$,$m_\times=53.08$,翻倍降幅 42.1% / 25.0% / 10.5%,规模项份额与弹性公式成立 |
| $m\equiv\rho n$ 的含义 | 需修正措辞 | $m$ 是上一代 $n$ 名感染者中预计被报告的人数。实际预计报告病例数是 $\rho n\bar R$。论文引言称 $m$ 为"预计报告的病例数",口径需要统一 |
| 目标1 = 时点/条件有效再生数 | 需修正 | 领域通用术语是瞬时再生数(instantaneous reproduction number)或时变再生数 [2][3];Wallinga 与 Teunis 的病例再生数是另一个量 [4]。"条件再生数"不是通用说法 |
| 目标2 = 潜在基线传播水平 | 需修正 | "潜在基线"没有出处;用户论文原话是"平均水平 $\bar R$"。建议写作跨期平均再生数,并在定义句中说明它是环境波动下 $R_t$ 的期望 |
| 建议题目《环境随机性下有效再生数估计的方差界与最优监测规模》 | 需修正 | 第一,"方差界"只适用于目标1 的 CRLB,目标2 是精确方差,不是界。第二,"最优监测规模"仅在推论1 的成本模型下成立,而 $m_\times$ 本身不是最优点,论文明确说它不是收益消失的位置(variance.tex:50)。第三,题目没有反映实证部分。题目由下游重构稿给出候选 |

### 3.3 后续交付预告

- **推导讲义**(下一步 derivation-handout):从个体负二项后代出发,依次推出:
  1. 稀疏封闭性;
  2. 条件矩;
  3. 全方差分解 $v_R+A/m$;
  4. 交叉点及其三个推论(份额、翻倍降幅、弹性);
  5. 命题1 的 CRLB 达到性。

  每一步都标明用到的假设(H1–H4),方便在黑板上一步一步推。讲义会统一使用目标1 / 目标2 的称呼。
- **重构稿**(之后的 paper-restructure):
  - 按 3.1 节的建议重写引言、缺口段与贡献段;
  - 合并碎句,删去比喻与重复的保留语;
  - 统一术语(瞬时再生数、跨期平均再生数、目标1 / 目标2);
  - 给出题目候选;
  - 图注改为"一句话结论加面板说明";
  - 局限部分合并成段。

### 3.4 候选范本与裁决

用户在便签中提出,也可以另找一篇文献照着学。为此,在 Parag 2022 之外另读了三篇同行评议论文。

| 候选 | 出处 | 结构特点 | 与用户论文的贴合度 |
|---|---|---|---|
| Parag & Donnelly 2022 [7] | PLoS Computational Biology 18(4): e1010004,15 页 | 引言 4 段;Results 只有 3 个小节,标题都是完整的结论句(如 Epidemic resurgence is statistically more difficult to infer than control);Methods 放在最后,开头一句 We derive some of the mathematical formulae central to the main text | 高。论证路线与用户论文相同:先给解析的精度极限(Fisher 信息 $\lambda/R$),再用模拟验证,最后落到"改进监测数据比改进模型更重要"。英文比 Parag 2022 直白,句式更容易模仿。不足是没有漏报项、环境方差和真实数据部分 |
| Cori 等 2013 [2] | American Journal of Epidemiology 178(9): 1505–1512 | 经典的短方法论文。引言按"背景、现有方法、逐条缺点(First…)、本文目的"四步展开;局限段用 First / Second / Finally | 中。定义段与局限段可以直接借鉴,也是目标1 术语(瞬时再生数)的标准出处;Results 按数据集组织,不适合照搬 |
| Gostic 等 2020 [8] | PLoS Computational Biology 16(12): e1008409 | Perspective 类文章,不是研究论文 | 低到中。只用于术语对照和监测含义(漏报、虚假精度);其图 1 图注与正文对 Cori 方法所估计量的说法不一致,不宜引用该图注 |

**裁决**:

- 整体结构仍以 Parag 2022 为准。
- 论证路线与行文的首要模仿对象定为 Parag & Donnelly 2022。
- 定义段、局限段的写法及目标1 的术语出处取自 Cori 2013。
- Gostic 2020 只作术语参考。

理由有三点:

1. Parag & Donnelly 2022 与用户论文的论证骨架几乎同构,篇幅和句子密度也更接近一篇小论文。
2. Parag 2022 覆盖了漏报与延迟的信息量框架,结构规范,适合作整体模板。但它的句子较密,研究生直接模仿有难度。
3. 用户论文是中文稿,三篇范本都只借鉴段落组织、论证顺序和限定语的用法,不逐句翻译英文句式。

具体做法将在重构稿中落实:

- 第3–5节合并为两三个用结论句命名的小节,推导移入附录;
- 引言按"背景、已有方法、缺口、本文做法"四步重写;
- 局限合并成段,用"第一……其次……最后……"串联。

---

## 第四部分 同行审阅与评分

本部分回应用户后来补充的要求("顺便同行审阅一下打个分")。下面按期刊审稿意见的通常格式撰写,审稿人设定为熟悉再生数估计与抽样设计的统计学同行。评分只代表一位审稿人的判断,用来帮助作者排定修改的先后,不能预测某一期刊的录用结果。

### 4.1 审稿意见摘要

稿件在负二项传播与二项报告的单代模型下,把再生数估计误差分解为环境方差 $v_R$ 与规模项 $A/m$,由此定义交叉点 $m_\times=A/v_R$,并推出三条结论:覆盖面与报告率的取舍、多期预算分配、小样本精确检验。作者用 NHSN 流感住院数据检验误差的 $a+b/D$ 形状。

稿件的优点有四个方面:

- 推导完整,命题的条件写得清楚;
- 作者对自己的结论设了较多限定,主动报告了截距与斜率被放大三倍以上这一不利结果;
- 稳健性检验覆盖面广;
- 代码、数据与自查记录齐全。

主要问题集中在三处:理论贡献的定位、目标2 的估计设定、实证检验的鉴别力。写作也需要较大幅度的修改。

### 4.2 主要意见

1. **理论新意需要重新定位。** 命题1 是单参数指数族中充分统计量达到 Cramér–Rao 下界的标准结论;命题2 是全方差公式的直接应用;推论1 与 Cochran 两阶段抽样的最优分配同构 [6],作者自己也指出了这一点。稿件的实际贡献在于把环境方差单列为一个方差成分,并把它翻译成监测设计的语言。建议:
   - 在引言中如实写明这一定位,不要把命题1–2 写成新定理;
   - 补充与环境随机性和过离散分层模型相关的文献对照。
2. **目标2 的估计设定需要论证。** 用单期估计量 $\hat R_t$ 去估计跨期均值 $\bar R$,方差底板 $v_R$ 几乎是这一设定的直接结果。实际估计 $\bar R$ 会使用多期数据,底板随之变为 $v_R/T$(命题4)。作者应说明:在什么监测场景下,决策者只能依据单期数据估计 $\bar R$?或者,应把交叉点重新表述为"单期规模与期数之间的权衡点",让命题4 与推论1 成为主线,而不是附带结论。
3. **实证检验的鉴别力有限。**
   - "常数加规模反比"的误差形状并非本模型独有:任何均值—方差成比例、再叠加乘性异质性的计数模型都会给出这一形状。规模项为正,因此不能区分本模型与竞争模型。
   - 拟合出的 $a$、$b$ 都是理论情景值的三倍以上,$b/a$ 落在情景区间内,是分子分母同向放大的结果,作者在第6.3节也承认了这一点。
   - 相比之下,第6.3节用滞后权重的平方和预测斜率之比(预测 1.44 / 0.86,观测 1.40 / 0.86),是一项更有鉴别力的检验。建议把它提升为主要证据,并说明哪些竞争模型给不出这一预测。
4. **H4 与时间相关。**
   - 真实序列中,规模 $n_t$ 由此前的传播决定,与 $R_t$ 相关,这一点作者在 model.tex:54 已经指出。但更新过程仿真仍假设各周 $R_t$ 独立,而实证截距随回溯滞后上升,又被解释为时间相关的证据。
   - 理论部分应至少给出 AR(1) 环境下交叉点的修正式,仿真部分应加入相关环境的情形,否则第5节与第6.3节之间的解释链是断开的。
5. **口径与术语。**
   - 周增长比 $G_t$ 跨约两代,与单代 $R_t$ 的口径不同。
   - $m=\rho n$ 被称为"预计报告病例数",实际预计报告病例数为 $\rho n\bar R$。
   - "当期再生数"应与领域通用的瞬时再生数 [2][3] 建立对应关系。

   建议在模型一节集中交代这三点。

### 4.3 次要意见

1. 摘要约 700 字,包含十余个数字,远超中文期刊通常 200–300 字的篇幅。同时缺少英文摘要。
2. 题目需要修改,导师已提出这一意见。现题较长,且"收益边界"不是领域通用说法。
3. 写作方面:
   - 引言的贡献写成编号列表;
   - 全文多处使用"三项""两处"这类预告数字和单分句短句;
   - 用了"一把尺子""无济于事"等比喻和口语;
   - "只能作量级参考"在摘要、正文、结论中重复出现;
   - 结论几乎逐句复述摘要。

   建议参照领域文献的段落组织重写。
4. 附录 A.8 的一阶推导略去了一个二阶项,该项使斜率多出 $2(v_R/\bar R^2)c$,在情景参数下约占 1.8%。应注明略去这一项及其量级。复现材料中有一条蒙特卡洛核对未通过(单种子 $z=-4.45$),应报告多种子复核的结果。
5. 第二期缺失的 36 个州周按 0 处理。建议补充按缺失处理的敏感性结果。
6. 聚类 bootstrap 只做了单向聚类。在第7.2节说明的基础上,可补充 wild cluster bootstrap 等适合少聚类情形的方法作为对照。

### 4.4 分项评分

评分标准:每项满 10 分,6 分为"可接受但需修改",8 分及以上为"达到发表水准"。总分按括号中的权重加权,换算为百分制。

| 维度(权重) | 得分 | 理由 |
|---|---|---|
| 选题与意义(15%) | 7 | 监测规模与估计目标的关系有实际价值,但目标2 的场景还需论证 |
| 理论创新(20%) | 5.5 | 方差分解与最优分配都属已知工具;新意在于问题的提法,而不在定理本身 |
| 理论严谨性(15%) | 8 | 命题条件清楚,证明完整,数值核对充分;唯一缺口是附录中一处二阶项未注明 |
| 实证设计与证据强度(20%) | 6 | 稳健性检验很多,但核心检验对竞争模型的鉴别力弱,参数数值与理论不符 |
| 写作与规范(20%) | 5 | 结构完整,但摘要过长、缺少英文摘要、题目不佳,AI 写作痕迹明显 |
| 可复现性(10%) | 9 | 代码、数据、种子与自查记录齐全 |
| **加权总分** | **64 / 100** | — |

**审稿建议:大修(major revision)。**

- 主要意见 1–3 是能否录用的关键。若重新定位贡献、论证目标2 的设定、把滞后权重检验提升为主证据,并完成写作上的修改,估计总分可提高到 75 分左右,达到国内统计类核心期刊的常见录用水平。
- 若投向国际期刊(如 Statistics in Medicine、Journal of the Royal Society Interface),理论新意会受到更严格的审视,建议同时补充与环境随机性文献的系统比较。

后续的重构稿将优先处理写作类意见(次要意见 1–3 与主要意见 5)。主要意见 1–2 的定位修改也会体现在新引言中。主要意见 3–4 涉及新的分析,需要作者本人决定是否补做,重构稿会在修改说明中逐条列出。

---

## 参考文献

[1] Parag K V, Donnelly C A, Zarebski A E. Quantifying the information in noisy epidemic curves. Nature Computational Science, 2022, 2: 584–594. https://doi.org/10.1038/s43588-022-00313-1

[2] Cori A, Ferguson N M, Fraser C, Cauchemez S. A new framework and software to estimate time-varying reproduction numbers during epidemics. American Journal of Epidemiology, 2013, 178(9): 1505–1512. https://doi.org/10.1093/aje/kwt133

[3] Fraser C. Estimating individual and household reproduction numbers in an emerging epidemic. PLoS ONE, 2007, 2(8): e758. https://doi.org/10.1371/journal.pone.0000758

[4] Wallinga J, Teunis P. Different epidemic curves for severe acute respiratory syndrome reveal similar impacts of control measures. American Journal of Epidemiology, 2004, 160(6): 509–516. https://doi.org/10.1093/aje/kwh255

[5] Lloyd-Smith J O, Schreiber S J, Kopp P E, Getz W M. Superspreading and the effect of individual variation on disease emergence. Nature, 2005, 438: 355–359. https://doi.org/10.1038/nature04153

[6] Cochran W G. Sampling Techniques. 3rd ed. New York: Wiley, 1977.

[7] Parag K V, Donnelly C A. Fundamental limits on inferring epidemic resurgence in real time using effective reproduction numbers. PLoS Computational Biology, 2022, 18(4): e1010004. https://doi.org/10.1371/journal.pcbi.1010004

[8] Gostic K M, McGough L, Baskerville E B, et al. Practical considerations for measuring the effective reproductive number, Rt. PLoS Computational Biology, 2020, 16(12): e1008409. https://doi.org/10.1371/journal.pcbi.1008409

[9] McGough L. Getting the most out of noisy surveillance data. Nature Computational Science, 2022, 2(9)(News & Views,2022-09-26 在线). https://doi.org/10.1038/s43588-022-00319-9
