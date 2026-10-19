# 理论推导讲义:病例规模、环境波动与再生数估计的方差

本讲义对应你的论文仓库 commit 8ff67a9 的文本(`paper/sections/model.tex`、`variance.tex`、`design.tex`、`renewal.tex`、`empirical.tex`、`appendix.tex`)。目的只有一个:让你能在导师面前,不看稿子,从模型假设一路推到 $v_R+A/m$ 和 $m_\times=A/v_R$,并且回答得了追问。

全文分八部分。第 1 部分是主线,15 分钟能在白板上推完;第 2 部分是论文其余命题的推导要点,每条标注"现场必推 / 被问再推 / 只需陈述";第 3 部分说明你的结果与 Parag 等 (2022) [2] 的 Fisher 信息结果之间能推出什么关系;第 4 部分是导师追问预案;第 5、6 部分是板书顺序和速记卡;第 7 部分是勘误;第 8 部分是验证记录。

关于验证标注。每个关键式子后面的括号注明它是怎么核对的:"符号验证 S5"表示脚本中编号 S5 的 sympy 检查通过;"模拟验证 MC3"表示编号 MC3 的蒙特卡洛场景通过,并给出模拟值与理论值之比或相对误差;"精确计算 N8"表示用负二项分布函数直接算出、没有模拟误差。脚本为 `.work/case-count-bottleneck/derivation/verify_derivation.py`,结果为同目录 `verify_results.json`,42 项检查全部通过。所有蒙特卡洛场景使用固定种子(20261017–20261024),每个场景 2×10⁵ 到 10⁶ 次重复,峰值内存约 260 MiB。用户仓库里的脚本一个都没有运行。

---

## 0 记号、假设与命名

### 0.1 记号(沿用论文原记号)

| 记号 | 含义 | 出处 |
|---|---|---|
| $n$ | 上一代感染者人数(第 $t$ 期的"父代"规模) | model.tex 2.1 节 |
| $X_{i,t}$ | 第 $i$ 名感染者产生的继发感染数 | 式 (offspring) |
| $R_t$ | 第 $t$ 期的再生数,即给定当期环境时 $X_{i,t}$ 的均值 | 式 (offspring) |
| $k$ | 负二项离散参数,越小超传播越强 | 式 (offspring) |
| $I_t=\sum_{i=1}^n X_{i,t}$ | 当期新感染总数 | 2.1 节 |
| $\rho$ | 报告率,每名新感染者独立被报告的概率 | 2.1 节 |
| $C_t$ | 报告数,$C_t\mid I_t\sim\mathrm{Bin}(I_t,\rho)$ | 2.1 节 |
| $m=\rho n$ | 监测规模:上一代 $n$ 人中预计被报告的人数 | model.tex:22 |
| $\widehat R_t=C_t/m$ | 自然估计量 | 2.2 节 |
| $\overline R=\mathrm E(R_t)$,$v_R=\mathrm{Var}(R_t)$ | 环境均值与环境方差 | 2.2 节 |
| $A=\overline R+\rho(\overline R^2+v_R)/k$ | 规模项系数 | 式 (var-average) |
| $m_\times=A/v_R$ | 交叉点 | 命题 2 |
| $\mathcal I(R_t)$ | $C_t$ 关于 $R_t$ 的 Fisher 信息 | 命题 1 |

负二项分布一律用论文附录的"失败次数"参数化:$\mathrm{NB}(r,p)$ 的概率母函数(PGF)为 $G(s)=p^r/[1-(1-p)s]^r$,均值 $r(1-p)/p$,方差 $r(1-p)/p^2$。

### 0.2 四条假设(论文原文 H1–H4)

- H1:给定 $R_t$,各感染者的继发感染数相互独立且服从 $\mathrm{NB}(k,\,k/(k+R_t))$;报告为独立二项抽样。
- H2:同一期的感染者共享同一个 $R_t$,环境扰动作用在"期"这一层。
- H3:$k$ 与 $\rho$ 已知。
- H4:$n$ 与当期环境无关,$\mathrm E(R_t\mid n)=\overline R$,$\mathrm{Var}(R_t\mid n)=v_R$。

主线推导用到全部四条。H4 最容易被问,它在固定样本设计下自然成立,在时间序列中不成立,论文第 5 节(renewal.tex)单独处理。

### 0.3 两个估计目标的命名

导师要求把"目标A/目标B"改成"目标1/目标2"。现稿已改为"目标Ⅰ/Ⅱ"(改名原因是字母 A 与系数 $A$ 撞名)。改成数字后会和"命题1、命题2"撞号,讲义统一写作"估计目标1""估计目标2",并给出领域内通用的名称:

- 估计目标1:瞬时再生数 $R_t$(instantaneous reproduction number)。这是 Fraser [5] 提出、Cori 等 [4] 和 Parag 等 [2] 沿用的术语。你的单代模型里 $n$ 扮演 Cori 定义中"总感染力"$\Lambda_t$ 的角色,$\widehat R_t=C_t/(\rho n)$ 对应 Cori 的比值 $I_t/\Lambda_t$。
- 估计目标2:跨期平均再生数 $\overline R=\mathrm E(R_t)$,即一段时期内各期再生数的均值。

### 0.4 与粘贴分析的记号差异(以论文为准)

| 项目 | 粘贴分析 | 论文与本讲义 | 说明 |
|---|---|---|---|
| 估计目标1 名称 | "时点/条件有效再生数" | 瞬时再生数 $R_t$ | "条件有效再生数"不是领域通用术语 |
| 估计目标2 名称 | "潜在基线传播水平" | 跨期平均再生数 $\overline R$ | "潜在基线"无出处 |
| 误差写法 | $\mathrm{Var}(\widehat R_t-\overline R)$ | $\mathrm{Var}(\widehat R_t\mid n)$ | 因 $\overline R$ 是常数,二者相等;但成立需要 H4 |
| $m_\times$ 的名称 | 特征尺度 | 交叉点 | 讲义沿用"交叉点" |
| 负二项写法 | 均值 $R_t$、离散 $k$ | $\mathrm{NB}(k,\,k/(k+R_t))$ | 同一分布,两种参数化 |
| "方差界" | 题目中称"方差界" | 目标2 是精确方差 | 只有加上"条件无偏估计类"限定,它才是下界(见 1.8 节) |

---

## 1 主线推导(白板 15 分钟)

### 1.0 一览

| 步 | 板书写什么 | 口头怎么讲 | 为什么成立 |
|---|---|---|---|
| 1 | $X_{i,t}\mid R_t\sim\mathrm{NB}$,$I_t=\sum X_{i,t}$,$C_t\mid I_t\sim\mathrm{Bin}(I_t,\rho)$ | 个体传播有超传播,报告是逐人抛硬币 | H1、H2;Gamma–泊松混合 |
| 2 | $G_C(s)=G_I(1-\rho+\rho s)$ ⇒ $C_t\sim\mathrm{NB}(nk,\,k/(k+\rho R_t))$ | 负二项求和、稀疏后仍是负二项 | PGF 乘法与复合 |
| 3 | $\widehat R_t=C_t/m$,条件均值 $R_t$,条件方差 $(R_t+\rho R_t^2/k)/m$ | 两项:报告抽样、超传播 | 线性变换 |
| 4 | $\mathrm{Var}=\mathrm E\,\mathrm{Var}(\cdot\mid R_t)+\mathrm{Var}\,\mathrm E(\cdot\mid R_t)$ | 拆成"病例少"和"环境变"两部分 | 全方差公式,H4 |
| 5 | $V(m)=v_R+A/m$,$A=\overline R+\rho(\overline R^2+v_R)/k$ | $A$ 里是 $\overline R^2+v_R$ | $\mathrm E R_t^2=\overline R^2+v_R$ |
| 6 | $m_\times=A/v_R$,$V/v_R=1+m_\times/m$ | 两项相等的规模 | 代数 |
| 7 | $V'=-A/m^2$;翻倍降幅 $1/[2(1+m/m_\times)]$ | 过了 $m_\times$,翻倍降不到 25% | 求导、代数 |
| 8 | 目标1 误差 $\to0$;目标2 误差 $\ge v_R$ | 同一估计量,靶子不同 | Cramér–Rao,交叉项为零 |

### 1.1 第一步:数据生成机制

**板书**

$$X_{i,t}\mid R_t\ \overset{\text{iid}}{\sim}\ \mathrm{NB}\Big(k,\ \frac{k}{k+R_t}\Big),\qquad \mathrm E(X_{i,t}\mid R_t)=R_t,\quad \mathrm{Var}(X_{i,t}\mid R_t)=R_t+\frac{R_t^2}{k}$$

$$I_t=\sum_{i=1}^{n}X_{i,t},\qquad C_t\mid I_t\sim\mathrm{Bin}(I_t,\rho)$$

(符号验证 S2b)

**口述**

"第 $t$ 期上一代有 $n$ 个感染者。每个人传给几个人是随机的,用负二项刻画:均值是当期的 $R_t$,方差比均值多出 $R_t^2/k$,$k$ 越小,越是少数人传给了大多数人。新感染里每个人独立地以概率 $\rho$ 被报告,所以报告数是总感染数的二项稀疏。"

**依据**

- H1、H2:给定 $R_t$ 个体独立,同期共享 $R_t$。
- 负二项等价于"个体传染力 $\nu_i\sim\mathrm{Gamma}$(均值 $R_t$、形状 $k$),再在其上取泊松",这是 Lloyd-Smith 等 [3] 的超传播模型。被问"为什么方差是 $R+R^2/k$",用全方差一行即可:$\mathrm{Var}(X)=\mathrm E\nu+\mathrm{Var}\,\nu=R_t+R_t^2/k$。

### 1.2 第二步:用 PGF 证明负二项在求和与二项稀疏下保持族不变

**板书**

(a) 负二项的 PGF:

$$G(s)=\Big(\frac{p}{1-(1-p)s}\Big)^{r},\qquad X\sim\mathrm{NB}(r,p)$$

(b) 独立求和:$G_I(s)=G(s)^n=\Big(\dfrac{p}{1-(1-p)s}\Big)^{nk}$,即 $I_t\mid R_t\sim\mathrm{NB}(nk,\,p)$,$p=\dfrac{k}{k+R_t}$。

(c) 二项稀疏:

$$G_C(s)=\mathrm E\big[\mathrm E(s^{C_t}\mid I_t)\big]=\mathrm E\big[(1-\rho+\rho s)^{I_t}\big]=G_I(1-\rho+\rho s)$$

(d) 代数整理。记 $q=1-(1-p)(1-\rho)$,则分母 $1-(1-p)(1-\rho+\rho s)=q-(1-p)\rho s$,

$$G_C(s)=\Big(\frac{p}{q-(1-p)\rho s}\Big)^{nk}=\Bigg(\frac{p/q}{1-\frac{(1-p)\rho}{q}\,s}\Bigg)^{nk},\qquad 1-\frac pq=\frac{q-p}{q}=\frac{(1-p)\rho}{q}$$

所以 $G_C$ 正是 $\mathrm{NB}(nk,\,p/q)$ 的 PGF。

(e) 代入 $p=k/(k+R_t)$:

$$q=\frac{k+\rho R_t}{k+R_t},\qquad p'=\frac pq=\frac{k}{k+\rho R_t}$$

$$\boxed{\,C_t\mid n,R_t\sim\mathrm{NB}\Big(nk,\ \frac{k}{k+\rho R_t}\Big),\quad \mathrm E(C_t\mid n,R_t)=\rho nR_t,\quad \mathrm{Var}(C_t\mid n,R_t)=\rho nR_t+\frac{\rho^2nR_t^2}{k}\,}$$

(符号验证 S1、S2;模拟验证 MC1:从个体层面逐人抽后代再二项稀疏,2×10⁵ 次,均值相对误差 0.16%,方差相对误差 0.17%,与 $\mathrm{NB}(nk,p')$ 的全变差距离 0.0049)

**口述**

"判断是不是负二项,只看 PGF 的形状是不是 $\big(p/[1-(1-p)s]\big)^r$。求和就是 PGF 相乘,底数不变、指数从 $k$ 变成 $nk$。稀疏就是把 $s$ 换成 $1-\rho+\rho s$:一个人被报告贡献一个 $s$,没被报告贡献 1。换完以后分母还是 $s$ 的一次式,提出常数 $q$,形状不变,只是 $p$ 变成了 $p/q$。代进去,$p'=k/(k+\rho R_t)$,相当于把 $R_t$ 换成 $\rho R_t$,形状参数 $nk$ 不变。"

**依据**

- 独立随机变量和的 PGF 等于 PGF 之积。
- 条件期望的塔性质;二项分布 $\mathrm E(s^{C}\mid I)=(1-\rho+\rho s)^{I}$。
- PGF 唯一确定分布。
- 矩:$\mathrm E=G'(1)$,$\mathrm{Var}=G''(1)+G'(1)-G'(1)^2$;代入 $r=nk$、$p'$ 得 $\mathrm E=nk\cdot\rho R_t/k=\rho nR_t$,$\mathrm{Var}=nk\cdot\rho R_t(k+\rho R_t)/k^2=\rho nR_t+\rho^2nR_t^2/k$。

### 1.3 第三步:自然估计量及其条件均值与方差

**板书**

$$m\equiv\rho n,\qquad \widehat R_t=\frac{C_t}{m}$$

$$\mathrm E(\widehat R_t\mid R_t)=R_t,\qquad \mathrm{Var}(\widehat R_t\mid R_t)=\frac{\rho nR_t+\rho^2nR_t^2/k}{(\rho n)^2}=\underbrace{\frac{R_t}{\rho n}}_{\text{报告抽样}}+\underbrace{\frac{R_t^2}{kn}}_{\text{超传播}}=\frac{R_t+\rho R_t^2/k}{m}$$

相对方差:

$$\frac{\mathrm{Var}(C_t\mid n,R_t)}{\mathrm E(C_t\mid n,R_t)^2}=\frac{1}{\rho nR_t}+\frac{1}{nk}$$

(符号验证 S3)

**口述**

"估计量就是报告数除以 $m$。它对 $R_t$ 条件无偏。条件方差有两项:第一项来自报告抽样,提高 $\rho$ 能压;第二项来自超传播,分母里只有 $n$ 没有 $\rho$,报告再完整也压不掉,只能扩大覆盖。两项都按 $1/n$ 下降。"

**依据**

- 第二步的均值与方差;$\mathrm{Var}(aC)=a^2\mathrm{Var}(C)$。
- 第二项不含 $\rho$ 是论文命题 3 的来源(见 2.4 节)。

### 1.4 第四步:全方差公式

**板书**

$$\mathrm{Var}(\widehat R_t)=\underbrace{\mathrm E\big[\mathrm{Var}(\widehat R_t\mid R_t)\big]}_{\text{抽样与人口随机性}}+\underbrace{\mathrm{Var}\big[\mathrm E(\widehat R_t\mid R_t)\big]}_{\text{环境波动}}$$

又 $\mathrm E\widehat R_t=\mathrm E[\mathrm E(\widehat R_t\mid R_t)]=\overline R$,所以

$$\mathrm{Var}(\widehat R_t)=\mathrm E(\widehat R_t-\overline R)^2=\mathrm{Var}(\widehat R_t-\overline R)$$

**口述**

"现在 $R_t$ 本身也是随机的。全方差公式把总误差拆成两块:第一块是给定环境以后、因为病例有限而产生的误差,包括报告抽样和个体传播的随机性(生态学里叫人口随机性);第二块是环境本身让 $R_t$ 上下波动。估计量对 $\overline R$ 无偏,所以这里的方差就是估计目标2 的均方误差。"

**依据**

- 全方差公式(条件方差分解)。
- H4:给定 $n$ 时 $R_t$ 的均值和方差就是 $\overline R$ 和 $v_R$,否则外层期望要在 $R_t\mid n$ 的条件分布下取,结果不再是这两个常数。

### 1.5 第五步:闭式 $v_R+A/m$

**板书**

$$\mathrm E\big[\mathrm{Var}(\widehat R_t\mid R_t)\big]=\frac{\mathrm E R_t}{m}+\frac{\rho\,\mathrm E R_t^2}{km}=\frac{\overline R}{m}+\frac{\rho(\overline R^2+v_R)}{km}\equiv\frac{A}{m}$$

$$\mathrm{Var}\big[\mathrm E(\widehat R_t\mid R_t)\big]=\mathrm{Var}(R_t)=v_R$$

$$\boxed{\,V(m)=v_R+\frac{A}{m},\qquad A=\overline R+\frac{\rho(\overline R^2+v_R)}{k}\,}$$

论文的等价写法:$V=v_R+\dfrac{\overline R}{\rho n}+\dfrac{\overline R^2+v_R}{kn}$。

(符号验证 S5;模拟验证 MC3:$R_t\sim$ Gamma(均值 1.15,方差 0.04),$k=0.35$,$\rho=0.25$,6 个规模各 10⁶ 次,模拟方差与 $v_R+A/m$ 之比为 0.9988–1.0023,均值相对误差均小于 0.01%)

**口述**

"条件方差是 $R_t$ 的二次式,取期望只需要 $R_t$ 的一阶矩和二阶矩。注意 $A$ 里的二次项是 $\overline R^2+v_R$ 而不是 $\overline R^2$:超传播项是 $R_t^2$ 的期望,环境方差在这里也会出现一次。"

**依据**

- 期望的线性;$\mathrm E R_t^2=\mathrm{Var}(R_t)+(\mathrm E R_t)^2=v_R+\overline R^2$。
- 只用到 $R_t$ 的前两阶矩,对环境分布的形状不作假设。
- 数例(论文图 2 参数 $\overline R=1.15$,$v_R=0.04$,$k=0.35$,$\rho=0.25$):$A=1.15+0.25\times1.3625/0.35=2.1232$(精确计算 N1)。

### 1.6 第六步:交叉点 $m_\times=A/v_R$

**板书**

$$\frac{A}{m}=v_R\iff m=m_\times\equiv\frac{A}{v_R}$$

$$\frac{V(m)}{v_R}=1+\frac{m_\times}{m},\qquad \frac{A/m}{V(m)}=\frac{1}{1+m/m_\times},\qquad V(m_\times)=2v_R$$

(符号验证 S6;数例 $m_\times=2.1232/0.04=53.08$,精确计算 N1)

**口述**

"$m_\times$ 是两块误差一样大的规模。规模小于它,误差主要来自病例少;大于它,主要来自环境波动。用它做单位,总方差就是底板的 $1+m_\times/m$ 倍:在 $m_\times$ 处是底板的 2 倍;想把方差压到底板的 1.1 倍以内,要 $m=10\,m_\times$。"

**依据**

- 纯代数。要主动说明:$V''(m)=2A/m^3>0$,曲线处处凸,$m_\times$ 不是拐点,也不是最优规模(最优规模要引入成本,见 2.6 节)。

### 1.7 第七步:边际收益

**板书**

$$V'(m)=-\frac{A}{m^2}< 0,\qquad V''(m)=\frac{2A}{m^3}>0,\qquad \frac{m\,V'(m)}{V(m)}=-\frac{m_\times}{m+m_\times}$$

翻倍:

$$\frac{V(2m)}{V(m)}=\frac{2m+m_\times}{2(m+m_\times)},\qquad \frac{V(m)-V(2m)}{V(m)}=\frac{1}{2(1+m/m_\times)}$$

推广到扩大 $K$ 倍:

$$\frac{V(m)-V(Km)}{V(m)}=\frac{1-1/K}{1+m/m_\times}\ \xrightarrow{K\to\infty}\ \frac{1}{1+m/m_\times}$$

过了交叉点翻倍降不到 25%:记 $x=m/m_\times$,

$$\frac{1}{2(1+x)}-\frac14=\frac{1-x}{4(1+x)}< 0\iff x>1$$

(符号验证 S6;数例 $m=10$、$53.08$、$200$ 时翻倍降幅 42.1%、25.0%、10.5%,精确计算 N1;模拟验证 MC3:模拟降幅 42.03%、25.01%、10.19%,相对误差 0.1%、0.04%、2.8%)

**口述**

"边际收益是 $A/m^2$,按平方衰减。用弹性说:在 $m_\times$ 处规模增加 1%,方差只降 0.5%。最直观的是翻倍:降幅等于 $1/[2(1+m/m_\times)]$,在 $m_\times$ 处正好 25%,超过以后不到 25%。规模扩大无穷多倍,最多也只能拿走规模项那一份,即 $1/(1+m/m_\times)$。"

**依据**

- 求导;弹性定义 $\mathrm d\log V/\mathrm d\log m$。
- 论文命题 2(ii)–(iv)。

### 1.8 第八步:估计目标1 与估计目标2 的区分

**板书**

估计目标1(瞬时再生数,条件于 $R_t$):

$$\mathrm E\big[(\widehat R_t-R_t)^2\mid R_t\big]=\frac{R_t+\rho R_t^2/k}{m}=\frac{1}{\mathcal I(R_t)}\ \xrightarrow{m\to\infty}\ 0,\qquad \mathcal I(R_t)=\frac{n}{R_t/\rho+R_t^2/k}$$

估计目标2(跨期平均再生数,对环境边缘化):

$$\widehat R_t-\overline R=(\widehat R_t-R_t)+(R_t-\overline R),\qquad \mathrm E\big[(\widehat R_t-R_t)(R_t-\overline R)\big]=\mathrm E\big[(R_t-\overline R)\,\underbrace{\mathrm E(\widehat R_t-R_t\mid R_t)}_{=0}\big]=0$$

$$\mathrm E(\widehat R_t-\overline R)^2=\mathrm E\Big[\frac{1}{\mathcal I(R_t)}\Big]+v_R=\frac{A}{m}+v_R\ \ \ge v_R$$

下界命题:对任何满足 $\mathrm E(\delta\mid R_t)=R_t$ 的估计量 $\delta(C_t)$,

$$\mathrm E(\delta-\overline R)^2=\mathrm E\big[\mathrm{Var}(\delta\mid R_t)\big]+v_R\ \ge\ \mathrm E\Big[\frac{1}{\mathcal I(R_t)}\Big]+v_R=v_R+\frac{A}{m}$$

$\widehat R_t$ 取到等号。

(符号验证 S4、S7;模拟验证 MC2:固定 $R_t=1.15$,$m=5$、$53.08$、$200$ 各 10⁶ 次,模拟方差与 $1/\mathcal I(R_t)$ 之比为 0.998、0.999、1.001)

**口述**

"同一个估计量,换一个靶子。估计目标1 问的是这一期实际的 $R_t$,环境已经发生了,当作固定参数;此时误差就是 Cramér–Rao 下界,随规模趋于零,而且对每个有限 $n$ 都精确取到。估计目标2 问的是平均水平,误差多出 $R_t-\overline R$ 这一项。两项不相关,因为给定 $R_t$ 时第一项均值为零。所以目标2 的误差是目标1 的平均误差加上 $v_R$,规模再大也压不过 $v_R$。并且在所有对 $R_t$ 条件无偏的估计量里,$v_R+A/m$ 已经是最小的,所以底板不是估计量选得不好造成的。"

**依据**

- 命题 1:得分函数 $S(R_t)=\mathcal I(R_t)(\widehat R_t-R_t)$,这是 Cramér–Rao 不等式取等号的充要条件(见 2.1 节)。
- 交叉项为零:塔性质。
- 下界命题:逐点用 Cramér–Rao 不等式 $\mathrm{Var}(\delta\mid R_t)\ge1/\mathcal I(R_t)$,再对 $R_t$ 取期望;$\mathrm E[1/\mathcal I(R_t)]=\mathrm E[(R_t+\rho R_t^2/k)/m]=A/m$(符号验证 S7)。需要 H4。
- 限定:"条件无偏"是必要的限定。如果允许收缩到一个先验猜测(例如贝叶斯估计),对目标2 的均方误差可以低于 $v_R$,代价是对目标1 有偏。单期数据里没有关于 $\overline R$ 的额外信息,要压底板只能增加期数或汇总辖区(2.3、2.5 节)。

---

## 2 延伸推导:论文其余命题与推论

标注含义。现场必推:主讲时就写在白板上;被问再推:准备好三五行推导,导师问到再写;只需陈述:会说结论和依据即可,推导在附录。

### 2.1 命题 1:当期再生数的有效估计(被问再推)

结论:$\widehat R_t$ 是 MLE;无偏;方差等于 Cramér–Rao 下界且对每个有限 $n$ 都成立;是一致最小方差无偏估计(UMVUE)。

推导要点。记 $\theta=\rho R_t$,观测值为 $c$:

$$\ell(R_t)=\text{常数}+nk\log\frac{k}{k+\rho R_t}+c\log\frac{\rho R_t}{k+\rho R_t}$$

$$S(R_t)=\frac{c}{R_t}-\frac{(c+nk)\rho}{k+\rho R_t}=\frac{k\rho n}{R_t(k+\rho R_t)}\big(\widehat R_t-R_t\big)$$

$$\mathcal I(R_t)=\mathrm E\big[-\ell''(R_t)\big]=\frac{k\rho n}{R_t(k+\rho R_t)}=\frac{n}{R_t/\rho+R_t^2/k}=\frac{1}{\mathrm{Var}(\widehat R_t\mid R_t)}$$

(符号验证 S4)

- MLE:$c>0$ 时得分在 $\widehat R_t$ 左正右负;$c=0$ 时得分恒负,极大值在边界 0。
- 有限样本取等:得分函数是 $\widehat R_t-R_t$ 的倍数,这是 Cramér–Rao 取等号的充要条件,不需要 $n\to\infty$。
- UMVUE(只需陈述):$k$ 已知时 $C_t$ 的分布是单参数指数族,自然参数 $\eta=\log[\rho R_t/(k+\rho R_t)]$ 取遍 $(-\infty,0)$,$C_t$ 完备充分,由 Lehmann–Scheffé 定理得 [6]。

### 2.2 命题 2:跨期平均水平的方差(现场必推)

即主线 1.4–1.7 节。(i) $V\to v_R$;(ii) 规模项份额 $1/(1+m/m_\times)$;(iii) 翻倍降幅 $1/[2(1+m/m_\times)]$;(iv) 严格递减、严格凸、弹性 $-m_\times/(m+m_\times)$。全部符号验证 S5、S6。

### 2.3 空间汇总降低底板(被问再推)

$J$ 个辖区环境方差同为 $v_R$,两两相关系数平均为 $\bar c$,等权平均的环境项:

$$\mathrm{Var}\Big(\frac1J\sum_{j=1}^JR_{j}\Big)=\frac{Jv_R+J(J-1)\bar c\,v_R}{J^2}=v_R\Big[\bar c+\frac{1-\bar c}{J}\Big]$$

(符号验证 S9;模拟验证 MC5:$J=5$,$\bar c=0.34$,10⁶ 次,比值 0.9988)

口述要点:扰动不完全同步($\bar c< 1$)时汇总能压低底板,极限为 $\bar c\,v_R$;完全同步时无效。

### 2.4 命题 3:报告率与覆盖面不对称(被问再推)

把 $V$ 写成 $n$、$\rho$ 的函数:$V(n,\rho)=v_R+\overline R/(\rho n)+(\overline R^2+v_R)/(kn)$。

$$-\frac{\partial V}{\partial\log n}=\frac{\overline R}{\rho n}+\frac{\overline R^2+v_R}{kn}=\frac{A}{m},\qquad -\frac{\partial V}{\partial\log\rho}=\frac{\overline R}{\rho n}=\frac{\overline R}{m},\qquad \text{比值}=\frac{A}{\overline R}=1+\frac{\rho(\overline R^2+v_R)}{k\overline R}$$

- $\rho\to1$:$V\to v_R+\overline R/n+(\overline R^2+v_R)/(kn)>v_R$,超传播项还在。
- $n\to\infty$:$V\to v_R$。
- 漏报额外方差:$\overline R/(\rho n)=\overline R/n+(1-\rho)\overline R/(\rho n)$。

(符号验证 S8;数例:图 2 参数 $A/\overline R=1.85$;住院情景 $\overline R=1.67$、$k\in[0.2,0.5]$、$\rho\in[0.0056,0.021]$、$v_R\in[0.04,0.08]$ 时为 1.02–1.18,精确计算 N1、N2)

口述要点:$\rho$ 很小时 $A\approx\overline R$,两条途径效果几乎相同,选哪条看成本。

### 2.5 命题 4:多期预算分配(独立情形被问再推,AR(1) 情形只需陈述)

设 $T$ 期、每期规模 $m$、总量 $B=Tm$ 固定,用 $T^{-1}\sum_t\widehat R_t$ 估计 $\overline R$。对 $(R_1,\dots,R_T)$ 用全方差公式:

$$\frac{1}{T^2}\mathrm{Var}\Big(\sum_t\widehat R_t\Big)=\mathrm{Var}(\bar R_T)+\frac{1}{T^2}\sum_t\mathrm E\Big[\frac{R_t+\rho R_t^2/k}{m}\Big]=\mathrm{Var}(\bar R_T)+\frac{A}{B}$$

独立时 $\mathrm{Var}(\bar R_T)=v_R/T$。规模项 $A/B$ 只依赖边际分布,与怎么切分无关;环境项随 $T$ 下降,所以只看方差,期数越多越好。

AR(1) 情形:$\mathrm{Cov}(R_s,R_t)=v_Rr^{|s-t|}$,

$$\sum_{h=1}^{T-1}(T-h)r^h=\frac{r\,[T(1-r)-(1-r^T)]}{(1-r)^2}\quad\Rightarrow\quad \mathrm{Var}(\bar R_T)=\frac{v_R}{T}\cdot\frac{1+r}{1-r}-\frac{2r(1-r^T)v_R}{T^2(1-r)^2}$$

(符号验证 S10:恒等式对 $T=1,\dots,40$ 逐一核对;模拟验证 MC4:$T=10$、$r=0.8$、$m=20$,2×10⁵ 条路径,模拟方差与理论之比 1.0006)

- 有效期数近似 $T_{\mathrm{eff}}=T(1-r)/(1+r)$ 只取第一项,总是高估环境项:$r=0.8$ 时 $T=26$ 高估 20.5%,$T=10$ 高估 65.8%(精确计算 N3)。第二项与第一项之比约为 $2r/[T(1-r^2)]$,所以近似只在 $T\gg2r/(1-r^2)$ 时可用。
- 单调性(只需陈述):记 $S_T=T^2\mathrm{Var}(\bar R_T)$、增量 $\Delta_j=v_R(1+2\sum_{h\le j}r^h)$。$\Delta_j$ 是凹数列,由此得 $(2T+1)S_T-T^2\Delta_T\ge(T+1)(Tv_R-d/2)>0$,$d=\Delta_T-\Delta_0< 2Tv_R$。讲义逐行核对过附录这段不等式,无误;另在 $r\in\{0.2,0.5,0.8,0.95\}$、$T\le400$ 上数值核对严格递减(精确计算 E1)。

### 2.6 推论 1:最优单期规模(被问再推)

每期固定成本 $c_0$、每例边际成本 $c_1$、总经费 $\mathcal B$,$T=\mathcal B/(c_0+c_1m)$。独立情形:

$$f(m)=\frac{(c_0+c_1m)(v_R+A/m)}{\mathcal B}=\frac{c_0v_R+c_1A+c_1v_Rm+c_0A/m}{\mathcal B}$$

$$f'(m)=\frac{c_1v_R-c_0A/m^2}{\mathcal B}=0\ \Rightarrow\ m^*=\sqrt{\frac{c_0}{c_1}\cdot\frac{A}{v_R}}=\sqrt{\frac{c_0}{c_1}\,m_\times},\qquad f(m^*)=\frac{(\sqrt{c_0v_R}+\sqrt{c_1A})^2}{\mathcal B}$$

$f''=2c_0A/(m^3\mathcal B)>0$,驻点唯一。(符号验证 S11)

- 口述要点:最优单期规模是成本比与交叉点的几何平均。这和两阶段抽样的费用分配是同一个问题 [9]:期数对应初级单元,$v_R$ 对应单元间方差,$A$ 对应单元内方差。
- 数值(精确计算 N4、N5):图 2 参数下 $c_0/c_1=10$、$100$ 时 $m^*=23.0$、$72.9$;住院情景 $m_\times\in[21.3,49.2]$ 时分别为 14.6–22.2、46.1–70.1。取整例 $c_0=100$、$c_1=1$、$\mathcal B=600$:逐个整数 $T$ 比较,$T=3$、$m=100$ 最优,方差 0.02041。
- AR(1) 时把 $v_R$ 换成 $v_R(1+r)/(1-r)$,$m^*$ 约乘 $\sqrt{(1-r)/(1+r)}$;近似值 42.1($r=0.5$)、24.3($r=0.8$)可复现,论文给出的"精确最优"42.9、25.0 无法复现,见第 7 部分勘误 3。

### 2.7 命题 5:精确增长检验(只需陈述,单调似然比被问再推)

检验 $H_0\colon R_t\le1$ 对 $H_1\colon R_t>1$,拒绝域 $C_t\ge c_\alpha$。单调似然比一行:取 $R>R'$,

$$\log\frac{f(c;R)}{f(c;R')}=\text{常数}+c\,\log\frac{R(k+\rho R')}{R'(k+\rho R)},\qquad \frac{\mathrm d}{\mathrm dR}\log\frac{R}{k+\rho R}=\frac{k}{R(k+\rho R)}>0$$

所以对数似然比关于 $c$ 递增(符号验证 S12)。之后是 Karlin–Rubin 定理 [8]:水平上确界在 $R_t=1$ 处,非随机检验在其实际水平 $\alpha^*\le\alpha$ 下一致最优,功效为 $1-F_{\mathrm{NB}}(c_\alpha-1;\,nk,\,k/[k+\rho(1+\delta)])$。

论文数值全部复现(精确计算 N7、N8,$\rho=0.25$,单侧 5%):

- Wald 检验实际水平:$k=0.1$、$m=5$ 时 7.81%;$m< 40$ 内最大值 8.03%、8.75%、10.40%($k=0.1$、0.35、1);精确检验最大水平 0.04999。
- 达到 / 始终保持 80% 功效的 $n$:$k=0.35$ 时 $\delta=0.15$、0.3、0.5 为 2071/2107、568/581、229/235;$\delta=0.25$ 时 $k=1$ 为 568/585,$k=0.1$ 为 1660/1684;$k=0.35$、$\delta=0.3$ 时 $n$ 从 400 到 699 功效下降 82 次。
- 模拟验证 MC8:$n=581$、$c_\alpha=173$,4×10⁵ 次,功效 0.8016(精确 0.8022),水平 0.04636(精确 0.04634)。

### 2.8 注 1:时间序列中的信息集分解(被问再推)

更新过程里下一期的感染压力 $\Lambda_{t+1}=\sum_sw_sI_{t+1-s}$ 因漏报而不可观测。设给定 $(\Lambda_{t+1},R_{t+1})$ 时 $C_{t+1}$ 服从以 $\Lambda_{t+1}$ 代替 $n$ 的负二项,且在 $\mathcal F_t$ 下 $\Lambda_{t+1}$ 与 $R_{t+1}$ 独立。记 $\bar\Lambda=\mathrm E(\Lambda_{t+1}\mid\mathcal F_t)$,$m=\rho\bar\Lambda$。第一次全方差:

$$\mathrm{Var}(C_{t+1})=\underbrace{\mathrm E\Big(\rho\Lambda R+\frac{\rho^2\Lambda R^2}{k}\Big)}_{=mA}+\rho^2\,\mathrm{Var}(\Lambda R)$$

第二步,独立乘积的方差:

$$\mathrm{Var}(\Lambda R)=\mathrm E\Lambda^2\,\mathrm ER^2-\bar\Lambda^2\overline R^2=\bar\Lambda^2\big[v_R+\mathrm{CV}^2(\Lambda)(\overline R^2+v_R)\big]$$

相加除以 $m^2$:

$$\frac{\mathrm{Var}(C_{t+1}\mid\mathcal F_t)}{m^2}=v_R+\frac{A}{m}+\mathrm{CV}^2(\Lambda_{t+1}\mid\mathcal F_t)\,(\overline R^2+v_R)$$

(符号验证 S13;模拟验证 MC6:$\bar\Lambda=200$、$\mathrm{CV}^2=0.1$、$m=50$,10⁶ 次,比值 0.9994)

口述要点:多出的第三项来自分母不确定,与规模无关;$\Lambda$ 完全已知时退化为命题 2。

### 2.9 预测误差恒等式与均方误差分解(只需陈述)

$$\frac{(C_{t+1}-\overline RD_t)^2}{(\overline RD_t)^2}=\frac{(G_t-\overline R)^2}{\overline R^2},\qquad \mathrm E(G_t-\overline R)^2=\mathrm E\Big[\Big(\frac{\sigma_t}{D_t}\Big)^2\Big]+\mathrm E\Big[\Big(\frac{\mu_t}{D_t}-\overline R\Big)^2\Big]$$

前者是两边同除 $\overline RD_t$ 的恒等式(符号验证 S16);后者因 $D_t$ 由 $\mathcal F_t$ 决定,对条件均方误差"方差 + 偏差平方"再取期望即得。要会说的结论:第一项不必等于 $v_R+A/D_t$,所以单代公式在时间序列中只是参照曲线,不是下界。

### 2.10 分母噪声抬高斜率:式 (b-delta)(只需陈述)

给定真实感染史 $\mathcal H_t$,取 $m=\rho\Lambda_{t+1}$、$I_{t+1-s}\approx\Lambda_{t+1}$,令 $D_t=m(1+\delta)$,则 $\mathrm E\delta=0$,$\mathrm E\delta^2=c/m$,$c=(1-\rho)\sum_sw_s^2$。$X=C_{t+1}/m$ 与 $\delta$ 独立,$G_t=X/(1+\delta)$。用 $\mathrm E(1+\delta)^{-1}\approx1+c/m$、$\mathrm E(1+\delta)^{-2}\approx1+3c/m$:

$$\mathrm E(G_t\mid\mathcal H_t)\approx\overline R\Big(1+\frac cm\Big),\qquad \mathrm{Var}(G_t\mid\mathcal H_t)\approx v_R+\frac{A+(\overline R^2+3v_R)c}{m}$$

$$\frac{\mathrm{Var}(G_t\mid\mathcal H_t)}{[\mathrm E(G_t\mid\mathcal H_t)]^2}\approx\frac{v_R}{\overline R^2}+\frac{A+(1-\rho)(\overline R^2+v_R)\sum_sw_s^2}{\overline R^2\,m}$$

(符号验证 S14;数值:$\overline R=1.67$、$v_R=0.06$、$k=0.35$、$\rho=0.021$ 时 $A=1.8409$,三种权重的预测斜率 1.155、1.660、0.993,比值 1.44、0.86,无分母噪声时 0.660;以固定 $\overline R$ 归一化多出 0.021,约为斜率的 1.8%,精确计算 N9。模拟验证 MC7:10⁶ 次,$m=400$ 时模拟斜率 1.173 与 1.672,相对误差 1.6% 与 0.7%;$m=100$ 时 0.8% 与 3.1%,差距来自 $O(m^{-2})$ 项)

### 2.11 实证拟合形式 $a+b/D_t$(只需陈述)

单代模型下把式 (var-average) 除以 $\overline R^2$:$\mathrm E(L_t)\approx v_R/\overline R^2+A/(\overline R^2m)$,所以 $a=v_R/\overline R^2$,$b=A/\overline R^2$,$b/a=m_\times$。要会说的限定:实证的 $G_t$ 跨约两代,分母含噪(2.10 节)抬高 $b$,条件偏差(2.9 节)抬高 $a$,所以经验交叉点 $b/a$ 不是 $A/v_R$ 的估计,只检验"常数加规模反比"的形状。

---

## 3 与 Parag 等 (2022) 的理论连接

### 3.1 Parag 原文实际使用的量

以下均出自上传 PDF 的 Methods(期刊页码 591–592):

- 式 (9):泊松更新模型 $I_t\sim\mathrm{Pois}(\Lambda_tR_t)$,$\Lambda_t=\sum_{x}w_{t-x}I_x$ 为总感染力。
- 式 (10)–(11):对数似然 $\sum_tI_t\log R_t-\Lambda_tR_t$,MLE $\widehat R_t=I_t/\Lambda_t$,Fisher 信息 $\mathrm{FI}(R_t)=\Lambda_t/R_t$;平方根变换后 $\mathrm{FI}(2\sqrt{R_t})=\Lambda_t$,与未知的 $R_t$ 无关。
- Cramér–Rao 界:$\mathrm{var}(\tilde R_t)\ge\mathrm{FI}(R_t)^{-1}$,原文说它给出任何无偏估计"渐近可达"的最小不确定性(p591)。
- 漏报:$C_t\sim\mathrm{Bin}(I_t,\rho_t)$,于是 $C_t\sim\mathrm{Pois}(\rho_t\Lambda_tR_t)$;加上延迟后为式 (14) $C\mid R_t\sim\mathrm{Pois}(\rho_tF_{\tau-t}\Lambda_tR_t)$,式 (15) $F_C(R_t)=\rho_tF_{\tau-t}\Lambda_t/R_t$(p592)。
- 负二项:原文 p586 说有研究用负二项替代泊松,并称补充材料表明这不影响其关于数据流相对信息量的结论,但负二项"不易处理"。补充材料不在上传 PDF 中,这一说法无法核对。

### 3.2 对应关系

| Parag (2022) | 你的模型 |
|---|---|
| 总感染力 $\Lambda_t$ | 上一代人数 $n$(世代间隔集中在一期,$w_1=1$) |
| 延迟累积概率 $F_{\tau-t}$ | 1(无报告延迟) |
| 报告比例 $\rho_t$ | 常数 $\rho$(Parag 称 CONR) |
| 泊松后代 | 负二项后代,$k\to\infty$ 时退化为泊松 |
| 每期 $R_t$ 是固定未知参数 | $R_t$ 是随机的,均值 $\overline R$、方差 $v_R$ |

### 3.3 结论一:$k\to\infty$、$v_R=0$ 时两者一致

$$\lim_{k\to\infty}\mathcal I(R_t)=\lim_{k\to\infty}\frac{n}{R_t/\rho+R_t^2/k}=\frac{\rho n}{R_t}=\frac{m}{R_t}$$

这正是 Parag 式 (15) 在 $\Lambda_t=n$、$F=1$、$\rho_t=\rho$ 时的 $F_C(R_t)$。于是估计目标1 的方差 $R_t/m$ 就是 Parag 的 Cramér–Rao 下界。再令 $v_R=0$,$A\to\overline R$,

$$\lim_{k\to\infty}V(m)\Big|_{v_R=0}=\frac{\overline R}{m}=\frac{1}{F_C(\overline R)}$$

(符号验证 S15)也就是说,在泊松、无环境波动的极限下,你的 $V(m)$ 与 Parag 的 Cramér–Rao 下界逐式相同。还可以多说一句:在单期设定下这个界对有限样本就能取到,因为泊松和负二项都是以均值为参数的指数族,得分函数都是 $\widehat R_t-R_t$ 的倍数;Parag 原文的"渐近可达"是对一般情形的表述。

### 3.4 结论二:超传播下,漏报损失的信息比例小于泊松情形

报告完全时($\rho=1$)信息为 $n/(R_t+R_t^2/k)$,于是

$$\frac{\mathcal I_C(R_t)}{\mathcal I_I(R_t)}=\frac{\rho(1+R_t/k)}{1+\rho R_t/k}=\rho+\frac{\rho(1-\rho)R_t/k}{1+\rho R_t/k}\ \ge\ \rho$$

(符号验证 S15)泊松情形这个比例就是 $\rho$,即 Parag 的"漏报按比例 $\rho$ 损失信息"。负二项下保留的比例更高:图 2 参数($R_t=1.15$、$k=0.35$、$\rho=0.25$)下为 0.588,而泊松为 0.25(精确计算 E3)。原因是超传播带来的方差在稀疏前后都在,报告抽样只是叠加在它上面。这个结论只对单期、无延迟的设定成立,不能外推为对 Parag 多期结果的修正。

### 3.5 结论三:平方根变换在负二项下不再消去 $R_t$

由 Fisher 信息的变量替换,$\mathrm{FI}(2\sqrt{R_t})=\mathcal I(R_t)\cdot R_t$:

$$\mathrm{FI}(2\sqrt{R_t})=\frac{m}{1+\rho R_t/k}\ \xrightarrow{k\to\infty}\ m$$

(符号验证 S15)Parag 用这个变换使信息与未知 $R_t$ 无关;负二项下它仍依赖 $R_t$,图 2 参数下约为 $0.549\,m$(精确计算 E3)。

### 3.6 结论四:环境方差在 Fisher 信息框架之外,但可以写成它的期望加一项

Parag 的 Fisher 信息是关于固定参数 $R_t$ 的,对应你的估计目标1。估计目标2 的 $\overline R$ 不是条件似然里的参数,而你对环境只假设了前两阶矩,没有似然,也就没有对 $\overline R$ 的 Fisher 信息。能推出的是 1.8 节的关系:

$$V(m)=v_R+\mathrm E_{R_t}\Big[\frac{1}{\mathcal I(R_t)}\Big]$$

即估计目标2 的方差等于"Cramér–Rao 下界对环境取平均"再加环境方差,并且在条件无偏估计类中不可改进。

### 3.7 推不出的,不要说

- Parag 的核心结果是多期的总信息 $T(C)=\prod_t\sqrt{\rho_tF_{\tau-t}\Lambda_t}$ 和几何平均 $\theta=G(\rho_t)G(F_{\tau-t})$(式 (3)–(5)),处理的是时变报告率与延迟。你的模型没有延迟、$\rho$ 不随时间变,不能声称你的结果推广或修正了这些量。
- Parag 说负二项不改变其相对信息结论,依据在补充材料中,无法核对;讲义 3.4 节的比例只说明单期情形。
- "你的工作把 Parag 的结果推广到了负二项"这种说法不要讲,单期负二项的 Fisher 信息是标准结果,你的增量在环境方差、两个估计目标的区分和设计含义。

---

## 4 导师追问预案

**问 1:为什么用负二项,不用泊松?**
答:继发感染数严重过离散,负二项是超传播的标准模型 [3],等价于个体传染力服从 Gamma 再取泊松。技术上它有两个好处:独立求和与二项稀疏后仍是负二项(1.2 节),所以 $C_t$ 的分布有闭式;$k\to\infty$ 时退化为泊松,能直接和 Parag 的结果对上(3.3 节)。选负二项的代价只体现在 $A$ 里的 $\rho(\overline R^2+v_R)/k$ 一项。

**问 2:H1 的独立性不成立怎么办?比如聚集性传播。**
答:同期共享的环境已经由 $R_t$ 吸收(H2),这里说的是剩余的个体间相关。设同期后代数两两相关系数为 $\psi$,$\sigma^2=R_t+R_t^2/k$,则

$$\mathrm{Var}(\widehat R_t\mid R_t)=\frac{\sigma^2[1+(n-1)\psi]}{n}+\frac{(1-\rho)R_t}{\rho n}\ \xrightarrow{n\to\infty}\ \psi\sigma^2$$

(符号验证 S17)$\psi=0$ 时回到命题 1。$\psi>0$ 时条件方差也有一个不随规模消失的底板,作用和 $v_R$ 同向,会让实际交叉点比 $A/v_R$ 更小。

**问 3:$\rho$ 是已知的还是估计的?**
答:论文假设已知(H3)。若 $\rho$ 来自一项独立研究,$\hat\rho=\rho(1+\varepsilon)$,$\mathrm E\varepsilon=0$,$\mathrm E\varepsilon^2=\kappa$,一阶展开得

$$\mathrm{Var}\Big(\frac{C_t}{\hat\rho n}\Big)\approx v_R+\frac Am+\kappa\Big(\overline R^2+v_R+\frac Am\Big)$$

(符号验证 S19)多出的 $\kappa(\overline R^2+v_R)$ 也不随规模消失,相当于又一个底板。这是论文应在讨论中补充的一点。

**问 4:$\rho$ 设错了偏差有多大?**
答:用 $\tilde\rho$ 代替真值 $\rho$,估计量变为 $\lambda\widehat R_t$,$\lambda=\rho/\tilde\rho$。

$$\mathrm E(\lambda\widehat R_t-\overline R)^2=\lambda^2\Big(v_R+\frac Am\Big)+\overline R^2(\lambda-1)^2$$

(符号验证 S18)偏差是乘性的。$\rho$ 不随时间变时,相邻期的比值 $\widehat R_t/\widehat R_{t-1}$ 不受影响;但阈值检验 $R_t\le1$ 直接受影响,$\tilde\rho$ 偏小会把 $R_t$ 高估,检验水平膨胀。

**问 5:$R_t$ 平稳吗?不平稳时 $\overline R$ 指什么?**
答:H4 要求同一窗口内各期 $R_t$ 围绕同一均值波动,$\overline R$ 是窗口内的均值,因此估计目标2 总是相对于一个窗口定义的。均值漂移时,以窗口均值为基准会多出偏差平方项 $(\overline R_{\text{早}}-\overline R_{\text{峰}})^2$。论文实证正好给出了例子:达峰期若仍以初期均值为基准,偏差项占总损失的 88.9%(第 6.4 节)。这也是论文主分析只取流行初期的理由。

**问 6:$k$ 也要估计,会影响什么?**
答:估计量 $\widehat R_t=C_t/m$ 本身不含 $k$,无偏性不受影响。受影响的是三件事:方差公式中的 $A$、命题 1 的 UMVUE 结论(需要 $k$ 已知才是单参数指数族),以及增长检验的临界值 $c_\alpha$。$k$ 用数据估计后,精确检验的水平不再有精确保证,论文讨论部分已说明。

**问 7:单代分支过程和更新方程是什么关系?**
答:单代模型是更新方程在世代间隔集中于一期($w_1=1$)时的特例,此时 $\Lambda_t=I_{t-1}=n$,$\widehat R_t=C_t/(\rho n)$ 对应 Cori 等的 $I_t/\Lambda_t$ [4]。一般情形下 $\Lambda_{t+1}=\sum_sw_sI_{t+1-s}$ 因漏报不可观测,注 1(2.8 节)给出多出来的 $\mathrm{CV}^2(\Lambda)(\overline R^2+v_R)$ 项;实证中用的是带噪的 $D_t$,2.10 节说明它抬高斜率。所以单代公式在时间序列中是参照曲线,不是下界。

**问 8:和 EpiEstim(Cori 等 2013)的贝叶斯估计是什么关系?**
答:Cori 等用 Gamma 先验(形状 $a$、尺度 $b$)和泊松更新似然,假设窗口内 $R$ 不变。对数后验关于 $R$ 的导数为

$$\frac{a+\sum I_s-1}{R}-\Big(\frac1b+\sum\Lambda_s\Big)$$

所以后验是 Gamma(形状 $a+\sum I_s$,率 $1/b+\sum\Lambda_s$)(符号验证 S20)。先验很弱、窗口为一期时,后验均值约为 $I_t/\Lambda_t$,后验方差约为 $R_t/\Lambda_t$,就是你的 $\widehat R_t$ 与 $k\to\infty$、$\rho=1$ 时的 Cramér–Rao 下界。两点差别可以推出来:其一,EpiEstim 的泊松似然在超传播下低估方差,真实方差是泊松方差的 $1+\rho R_t/k$ 倍,图 2 参数下 1.82 倍,住院情景 1.02–1.18 倍(精确计算 E2);其二,窗口取 $\tau$ 期、各期规模相同且环境独立时,窗口平均对 $\overline R$ 的方差为 $(v_R+A/m)/\tau$(符号验证 S20),介于两个估计目标之间。

**问 9:为什么不像 Parag 那样用 Fisher 信息?**
答:估计目标1 用了,命题 1 就是 Fisher 信息与 Cramér–Rao 下界,而且精确取等。估计目标2 的 $\overline R$ 不是条件似然的参数,论文只假设环境的前两阶矩,没有似然可求 Fisher 信息;全方差公式只要两阶矩,假设更弱。两者的关系是 $V(m)=v_R+\mathrm E[1/\mathcal I(R_t)]$(3.6 节)。

**问 10:$m_\times$ 是不是最优监测规模?**
答:不是。$V(m)$ 处处凸,没有拐点,$m_\times$ 只是两类误差相等的规模。最优规模必须引入成本:$m^*=\sqrt{(c_0/c_1)\,m_\times}$(2.6 节)。所以题目里不宜写"最优监测规模",除非正文以推论 1 为主结果。

**问 11:每个辖区每期只有一个观测,$v_R$ 怎么估?**
答:各期独立、规模相同时,$\widehat R_t$ 的样本方差 $S^2$ 满足 $\mathrm ES^2=v_R+A/m$。$A$ 里含 $v_R$,解出

$$\hat v_R=\frac{S^2-(\hat{\overline R}+\rho\hat{\overline R}^2/k)/m}{1+\rho/(km)}$$

(符号验证 S21)规模不同时按 $1/m_t$ 加权同理。需要 $k$、$\rho$ 已知,且 $T$ 足够大;有时间相关时 $S^2$ 有偏,要按 AR(1) 公式修正。

**问 12:实证的 $b/a$ 能当作 $m_\times$ 的估计吗?**
答:不能。$a=v_R/\overline R^2$、$b=A/\overline R^2$ 只在单代、分母无噪声时成立。分母噪声只抬高 $b$(2.10 节),情景模拟中 $b/a=59.2$,而真实 $A/v_R=30.7$;条件偏差抬高 $a$(2.9 节)。所以实证只检验"常数加规模反比"的形状,论文已这样表述。更有鉴别力的证据是滞后权重改变时斜率的相对变化:预测 1.44、0.86,观测 1.40、0.86。

**问 13:命题 1、2 是教科书结论吧?你的贡献在哪里?**
答:命题 1 是单参数指数族的标准结果,命题 2 的推导只用全方差公式,数学上都不新,应当这样承认。贡献在于:把监测问题区分为两个估计目标,给出两者之间的交叉点 $m_\times=A/v_R$ 及其设计含义(报告率与覆盖面的不对称、预算下的最优单期规模、小样本增长检验),并说明这一结构在时间序列和美国住院数据中保留到什么程度。

---

## 5 15 分钟板书顺序

| 时间 | 板书 | 要说出口的一句话 |
|---|---|---|
| 0:00–1:00 | 写两个估计目标:$R_t$ 与 $\overline R=\mathrm ER_t$,$v_R=\mathrm{Var}R_t$ | 同一个估计量,两个靶子 |
| 1:00–2:00 | 1.1 节:个体负二项、求和、二项稀疏 | $k$ 越小超传播越强 |
| 2:00–4:00 | 1.2 节:PGF、$s\mapsto1-\rho+\rho s$、提出 $q$、得 $p'=k/(k+\rho R_t)$ | 稀疏后还是负二项,$R_t$ 换成 $\rho R_t$ |
| 4:00–5:30 | 1.3 节:$\widehat R_t=C_t/m$,条件方差两项 | 报告抽样项与超传播项 |
| 5:30–7:30 | 1.4–1.5 节:全方差公式,得 $v_R+A/m$,展开 $A$ | $A$ 里是 $\overline R^2+v_R$ |
| 7:30–9:00 | 1.6 节:$m_\times=A/v_R$,$V/v_R=1+m_\times/m$ | 两类误差相等的规模,不是拐点 |
| 9:00–11:00 | 1.7 节:$V'$、弹性、翻倍降幅,$x>1$ 时降幅不到 1/4 | 过了交叉点翻倍收益不到 25% |
| 11:00–13:30 | 1.8 节:误差拆分、交叉项为零、下界 | 目标1 无底板,目标2 底板 $v_R$ |
| 13:30–15:00 | 一行 $m^*=\sqrt{(c_0/c_1)m_\times}$;一行 $k\to\infty$ 时 $\mathcal I\to m/R_t$ | 最优规模要靠成本;泊松极限与 Parag 一致 |

练习建议:先只看速记卡默写一遍,再完全脱稿写一遍并计时。卡住最多的通常是 1.2 节的提出 $q$ 那一步和 1.8 节交叉项为零的理由。

---

## 6 一页速记卡

1. 稀疏:$G_C(s)=G_I(1-\rho+\rho s)$ ⇒ $C_t\mid n,R_t\sim\mathrm{NB}\big(nk,\ k/(k+\rho R_t)\big)$,$\mathrm E=\rho nR_t$,$\mathrm{Var}=\rho nR_t+\rho^2nR_t^2/k$
2. 估计目标1:$\mathrm{Var}(\widehat R_t\mid R_t)=\dfrac{R_t+\rho R_t^2/k}{m}=\dfrac{1}{\mathcal I(R_t)}$,$m=\rho n$
3. 全方差:$\mathrm{Var}(\widehat R_t)=\mathrm E\,\mathrm{Var}(\widehat R_t\mid R_t)+\mathrm{Var}(R_t)$
4. 估计目标2:$V(m)=v_R+\dfrac Am$,$A=\overline R+\dfrac{\rho(\overline R^2+v_R)}{k}$
5. 交叉点:$m_\times=\dfrac{A}{v_R}$,$\dfrac{V(m)}{v_R}=1+\dfrac{m_\times}{m}$
6. 翻倍降幅:$\dfrac{1}{2(1+m/m_\times)}$;弹性 $-\dfrac{m_\times}{m+m_\times}$
7. 下界:$\mathrm E(\delta-\overline R)^2\ge v_R+\mathrm E[1/\mathcal I(R_t)]=v_R+A/m$(对 $R_t$ 条件无偏的 $\delta$)
8. 最优单期规模:$m^*=\sqrt{\dfrac{c_0}{c_1}\,m_\times}$

数例(图 2 参数 $\overline R=1.15$、$v_R=0.04$、$k=0.35$、$\rho=0.25$):$A=2.1232$,$m_\times=53.1$,翻倍降幅 42.1% / 25.0% / 10.5%($m=10$ / 53.1 / 200)。

---

## 7 勘误

逐行核对了附录全部证明并用脚本复现了正文数值,没有发现推导错误。以下是数值或表述层面的问题,按影响从大到小排列。

**勘误 1:AR(1) 下"精确最优"的数值无法复现(design.tex:47)。**
原文:"仍取图示参数与 $c_0/c_1=100$,$r=0.5$ 时精确最优与近似值分别为 42.9 和 42.1,$r=0.8$ 时为 25.0 和 24.3。"
核对:近似值 $\sqrt{100\,m_\times}\sqrt{(1-r)/(1+r)}=42.1$、24.3 可复现。把 $T=\mathcal B/(c_0+c_1m)$ 视为连续、用式 (alloc-ar) 的精确环境项求最优:同段的 $\mathcal B=600$ 下为 66.8 和 96.3;没有任何单一 $\mathcal B$ 能同时给出 42.9 与 25.0($\mathcal B\approx10^4$ 时 $r=0.5$ 为 42.9,但 $r=0.8$ 为 25.8;$\mathcal B\approx2\times10^4$ 时 $r=0.8$ 为 25.0,但 $r=0.5$ 为 42.5)。
建议:写明计算"精确最优"所用的预算 $\mathcal B$ 和求解口径;若原意是大 $T$ 极限,应说明 $\mathcal B=600$ 时 $T$ 只有 3 期左右,近似不适用。依据:`verify_results.json` 中 N6。

**勘误 2:情景参数下 $A$ 与 $b$ 区间的上端(empirical.tex:58)。**
原文:"此时 $A$ 在 1.702--1.967 ……情景隐含的截距为 0.0143--0.0287,斜率为 0.610--0.705。"
正确:若 $k$、$\rho$、$v_R$ 在所给区间内同时变动,$A$ 的最大值在 $k=0.2$、$\rho=0.021$、$v_R=0.08$ 处,为 1.971,对应斜率上端 $1.971/1.67^2=0.707$。原文 1.967 是 $v_R=0.04$ 角点的值。$m_\times$ 区间 21.3–49.2、截距区间、倍数 3.2–3.7 的结论不受实质影响。依据:N2。

**勘误 3:"方括号内第一项"无所指(design.tex:26)。**
原文:"常用的有效期数近似 $T_{\mathrm{eff}}=T(1-r)/(1+r)$ 只保留了方括号内第一项"。式 (alloc-ar) 中没有方括号。
建议:改为"只保留了式 (alloc-ar) 的第一项"。数值 20.5%、65.8% 正确(N3)。

**勘误 4:$m$ 的口径前后不一(introduction.tex:12)。**
原文:"$m$ 是预计报告的病例数"。model.tex:22 的定义是"上一代感染者中预计被报告的人数",即 $m=\rho n$;当期预计报告的新病例数是 $\mathrm E(C_t)=\rho n\overline R=m\overline R$。
建议:引言改用 model.tex 的定义。

**勘误 5:粘贴分析中的公式与表述。**
- $X_i\sim\mathrm{NB}$、$C_t\mid I_t\sim\mathrm{Bin}(I_t,\rho)$、$m=\rho n$、$\widehat R_t=C_t/m$、$\mathrm{Var}(\widehat R_t-\overline R)=v_R+A/m$、$A=\overline R+\rho(\overline R^2+v_R)/k$、$m_\times=A/v_R$:全部正确(S1–S6)。
- 需补充的成立条件:$v_R+A/m$ 依赖 H4,只在单代、$n$ 与当期环境无关时成立;在时间序列中它只是参照曲线,不是下界(论文第 5.1 节,讲义 2.9 节)。
- "方差界":对估计目标2,$v_R+A/m$ 是自然估计量的精确方差;只有加上"对 $R_t$ 条件无偏的估计量"这一限定,它才是下界(1.8 节)。题目若用"方差界"需带这一限定,否则改为"方差结构"。
- "时点/条件有效再生数""潜在基线传播水平"不是领域术语,改为"瞬时再生数""跨期平均再生数"(0.3 节)。"封面文章"一说不成立,见精读报告 deep-read.md 第三部分。

---

## 8 验证记录

| 编号 | 内容 | 方法 | 结果 |
|---|---|---|---|
| S1 | 负二项求和与二项稀疏的 PGF 代数,$q$、$p'$ | sympy | 通过 |
| S2、S2b | 后代与报告数的均值、方差 | sympy(由 PGF 求导) | 通过 |
| S3 | $\widehat R_t$ 条件方差、相对方差 | sympy | 通过 |
| S4 | 得分函数分解、Fisher 信息、$1/\mathcal I=\mathrm{Var}$ | sympy | 通过 |
| S5 | 全方差公式得 $v_R+A/m$ | sympy | 通过 |
| S6 | 份额、翻倍与 $K$ 倍降幅、导数、弹性、$V(m_\times)=2v_R$ | sympy | 通过 |
| S7 | $\mathrm E[1/\mathcal I(R_t)]=A/m$ | sympy | 通过 |
| S8 | 命题 3 偏导与极限 | sympy | 通过 |
| S9 | 空间汇总底板 | sympy | 通过 |
| S10 | AR(1) 部分和恒等式($T\le40$)与环境项 | sympy | 通过 |
| S11 | 推论 1 的 $m^*$、$f(m^*)$、凸性 | sympy | 通过 |
| S12 | 单调似然比 | sympy | 通过 |
| S13 | 注 1 信息集分解 | sympy | 通过 |
| S14 | 分母噪声的 delta 展开(三种归一化) | sympy 级数 | 通过 |
| S15 | Parag 泊松极限、信息比、平方根变换 | sympy 极限 | 通过 |
| S16 | 预测误差恒等式 | sympy | 通过 |
| S17–S21 | 追问预案中的相关性底板、$\rho$ 设错、$\rho$ 估计、EpiEstim 共轭与窗口、$v_R$ 矩估计 | sympy | 通过 |
| N1–N9、E1–E3 | 论文正文数值、检验水平与功效、斜率预测 | numpy/scipy 精确计算 | 除勘误 1–2 所列外全部复现 |
| MC1 | 个体层面稀疏 vs 负二项,2×10⁵ 次 | 模拟 | 均值误差 0.16%,方差误差 0.17% |
| MC2 | 估计目标1 方差 vs Cramér–Rao 下界,3×10⁶ 次 | 模拟 | 比值 0.998–1.001 |
| MC3 | 估计目标2 $v_R+A/m$,6×10⁶ 次 | 模拟 | 比值 0.9988–1.0023 |
| MC4 | AR(1) 多期方差,2×10⁵ 条路径 | 模拟 | 比值 1.0006 |
| MC5 | 空间汇总,10⁶ 次 | 模拟 | 比值 0.9988 |
| MC6 | 注 1 信息集分解,10⁶ 次 | 模拟 | 比值 0.9994 |
| MC7 | 分母噪声斜率,4×10⁶ 次 | 模拟 | $m=400$ 时误差 0.7%–1.6% |
| MC8 | 增长检验功效与水平,4×10⁵ 次 | 模拟 | 与精确值差 0.0006 以内 |

复现:在仓库根目录运行 `python3 .work/case-count-bottleneck/derivation/verify_derivation.py`,约 11 秒。

---

## 参考文献

[1] 用户论文仓库 wangchi2068/case-count-inference-bottleneck,commit 8ff67a9。https://github.com/wangchi2068/case-count-inference-bottleneck

[2] Parag KV, Donnelly CA, Zarebski AE. Quantifying the information in noisy epidemic curves. Nature Computational Science, 2022, 2: 584–594. https://doi.org/10.1038/s43588-022-00313-1

[3] Lloyd-Smith JO, Schreiber SJ, Kopp PE, Getz WM. Superspreading and the effect of individual variation on disease emergence. Nature, 2005, 438: 355–359. https://doi.org/10.1038/nature04153

[4] Cori A, Ferguson NM, Fraser C, Cauchemez S. A new framework and software to estimate time-varying reproduction numbers during epidemics. American Journal of Epidemiology, 2013, 178(9): 1505–1512. https://doi.org/10.1093/aje/kwt133

[5] Fraser C. Estimating individual and household reproduction numbers in an emerging epidemic. PLoS ONE, 2007, 2(8): e758. https://doi.org/10.1371/journal.pone.0000758

[6] Lehmann EL, Casella G. Theory of Point Estimation. 2nd ed. New York: Springer, 1998.

[7] Casella G, Berger RL. Statistical Inference. 2nd ed. Pacific Grove: Duxbury, 2002.

[8] Karlin S, Rubin H. The theory of decision procedures for distributions with monotone likelihood ratio. Annals of Mathematical Statistics, 1956, 27(2): 272–299.

[9] Cochran WG. Sampling Techniques. 3rd ed. New York: Wiley, 1977.

[10] Hamilton JD. Time Series Analysis. Princeton: Princeton University Press, 1994.

---

## 9 第三轮新增推导

本部分对应第三轮理论升级,共四个新命题、一个推论和一个附注。命题 A 处理报告率在期间波动的情形,命题 B 讨论环境方差 $v_R$ 本身能估多准,命题 C 把两者合成设计原则,命题 D 修正一阶自回归下的预算设计。LaTeX 稿(陈述、附录级证明、图)在 `.work/case-count-bottleneck/derivation/r3/propositions_r3.tex`,可直接并入论文;验证脚本为同目录 `verify_r3.py`,43 项检查全部通过(固定种子 20261017,两核约 43 秒),结果写入 `verify_r3.json` 与 `verify_r3.log`。下文"检查 A.S2"之类的编号与脚本输出一一对应。

一句话版本:规模换来的是 $\overline R$ 的精度,期数换来的是对 $v_R$ 的认识,报告标准化去掉的是报告率波动带来的那一项方差。

### 9.0 新增记号与假设

| 记号 | 含义 |
|---|---|
| $p_t$ | 第 $t$ 期的实际报告率,随机 |
| $\rho=\mathrm E p_t$,$\sigma^2=\mathrm{Var}\,p_t$ | 报告率的均值与方差 |
| $\tau=\sigma/\rho$,$u_t=p_t/\rho$ | 报告率的相对波动与标准化报告率,$\mathrm E u_t=1$,$\mathrm{Var}\,u_t=\tau^2$ |
| $\nu$ | Beta 型报告率的集中度,$p_t\sim\mathrm{Beta}(\rho\nu,(1-\rho)\nu)$ |
| $\phi$ | $R_t$ 的一阶自回归系数(论文现稿写作 $r$,并稿时统一为 $\phi$) |
| $\psi$ | 报告率波动的一阶自回归系数 |
| $\kappa_T(x)$ | $1+2\sum_{h=1}^{T-1}(1-h/T)x^h$,即 $T^{-1}\sum_s\sum_t x^{\lvert s-t\rvert}$ |
| $\mathcal B$ | 总预算,$T(c_0+c_1m)=\mathcal B$ |

新增两条假设,替代 H1 中"报告率固定"的部分。

- H5:给定 $p_t$,每例新感染独立地以概率 $p_t$ 被报告;$\{p_t\}$ 平稳,与 $\{R_t\}$ 和 $n$ 独立。
- H6:给定全部 $R_t$ 与 $p_t$,各期报告数相互独立。

由论文式 (thinning) 的推导把 $\rho$ 换成 $p_t$,立刻得到 $C_t\mid n,R_t,p_t\sim\mathrm{NB}(nk,\,k/(k+p_tR_t))$。

报告率波动分两类,后面的结论在两类之间会分化。二项型来自报告率本身的抽样,$\sigma^2=\rho(1-\rho)/(\nu+1)$,报告率接近 1 时波动消失;制度型来自填报口径或检测政策的变化,$\tau$ 与 $\rho$ 无关,$\sigma^2=\rho^2\tau^2$。

### 9.1 命题 A:报告率波动下的方差三分量(现场必推)

结论:

$$\mathrm{Var}(\widehat R_t)=v_R+v_H+\frac{A_H}{m},\qquad v_H=\tau^2(\overline R^2+v_R),\qquad A_H=\overline R+\frac{\rho(1+\tau^2)(\overline R^2+v_R)}{k}$$

$v_H$ 不含 $n$,所以和 $v_R$ 一样不随规模下降。

**板书三步。**

第一步,给定 $(n,R_t,p_t)$。这就是原模型,报告率换成 $p_t$,由负二项均值方差直接写出:

$$\mathrm E(C_t\mid n,R_t,p_t)=p_tnR_t,\qquad \mathrm{Var}(C_t\mid n,R_t,p_t)=p_tnR_t+\frac{p_t^2nR_t^2}{k}$$

第二步,对 $p_t$ 用全方差公式。条件方差取期望要用 $\mathrm E p_t^2=\rho^2+\sigma^2$,条件均值的方差是 $\sigma^2n^2R_t^2$:

$$\mathrm{Var}(C_t\mid n,R_t)=\rho nR_t+\frac{(\rho^2+\sigma^2)nR_t^2}{k}+\sigma^2n^2R_t^2$$

(检查 A.S1)最后一项是 $n^2$ 阶,除以 $m^2=\rho^2n^2$ 后不随 $n$ 变小,这就是 $v_H$ 的来源。

第三步,对 $R_t$ 再用一次全方差公式,代入 $\mathrm E R_t^2=\overline R^2+v_R$,除以 $m^2$:

$$\mathrm{Var}(\widehat R_t)=v_R+\frac{\sigma^2}{\rho^2}(\overline R^2+v_R)+\frac{\overline R}{m}+\frac{\rho(1+\tau^2)(\overline R^2+v_R)}{km}$$

整理即为结论(检查 A.S2)。图示参数($\overline R=1.15$,$v_R=0.04$,$k=0.35$,$\rho=0.25$)取 $\tau=0.15$:$v_H=0.0307$,$A_H=2.145$;推广的交叉规模 $m_{\times,H}=A_H/(v_R+v_H)$ 从 53.1 降到 30.4;$m=1000$ 时方差 0.0728,原公式给 0.0421。蒙特卡洛在 $\tau\in\{0.15,0.30\}$、$m$ 从 3 到 3000 的 14 个格点上(每格 2×10⁵ 次)最大标准化偏差 1.64(检查 A.M1)。

**为什么 $v_H$ 里没有 $1/k$。** 超传播的噪声来自个体之间,$n$ 个感染者相加后相对方差按 $1/n$ 下降;报告率波动作用在整期报告数上,一期之内所有病例共用同一个 $p_t$,相加不会抵消。这一点和 $v_R$ 不随规模下降是同一个道理(同一期共用 $R_t$,即 H2)。

**下界(被问再推)。** 问题是:换一个更聪明的估计量,能不能把 $v_H$ 去掉?答案是不能。论证分两步。

第一步是数据处理不等式。$C_t$ 只经过乘积 $\theta_t=p_tR_t$ 依赖 $R_t$,即 $R_t\to\theta_t\to C_t$ 是马尔可夫链,所以 $C_t$ 关于 $R_t$ 的 Fisher 信息不超过 $\theta_t$ 关于 $R_t$ 的信息。$\theta_t/\rho=R_tu_t$ 是以 $R_t$ 为尺度参数的尺度族,其信息为 $\mathcal J_u/R_t^2$,$\mathcal J_u$ 只取决于 $u_t$ 的分布,与 $m$ 无关。对条件无偏估计量用 Cramér–Rao,再对 $R_t$ 取期望:

$$\mathrm E(\tilde\theta-\overline R)^2\ \geq\ v_R+\frac{\overline R^2+v_R}{\mathcal J_u}\qquad\text{对任意 } m$$

第二步是 Cauchy–Schwarz。记尺度族在 $R=1$ 处的得分函数为 $\ell'(u)$,对 $\mathrm E u_t=1$ 关于尺度参数求导得 $\mathrm E[\ell'(u_t)u_t]=1$,又 $\mathrm E\ell'(u_t)=0$,所以 $\mathrm{Cov}(\ell',u)=1\le\sqrt{\mathcal J_u}\,\tau$,即 $\mathcal J_u\ge1/\tau^2$。等号当且仅当得分函数是 $u$ 的仿射函数,解出来 $u_t$ 是 Gamma 分布(检查 A.S3)。

所以:$u_t$ 为 Gamma 分布时,下界恰好是 $v_R+v_H$,与 $m$ 无关,而 $\widehat R_t$ 在 $m\to\infty$ 时达到它;其他分布下下界略低于 $v_R+v_H$,对数正态时比值为 $\log(1+\tau^2)/\tau^2$,$\tau=0.15$ 时 0.989(检查 A.S3b)。数值上,$\tau=0.3$ 的 Gamma 波动下,$C_t$ 关于 $R_t$ 的信息在 $m=10$、100、1000 时为 2.98、7.11、8.25,单调趋近上界 8.40(检查 A.N2)。

**命题 3(iv) 的修正(现场必推)。** 原命题说扩大覆盖总比提高报告率有效,比值 1.85。把 $\tau^2$ 看成 $\rho$ 的函数重写方差:

$$V_H=v_R+\tau^2(\overline R^2+v_R)+\frac{\overline R}{\rho n}+\frac{(1+\tau^2)(\overline R^2+v_R)}{kn}$$

两种手段各提高一个相同的小比例,方差下降量分别是 $-\rho\,\partial V_H/\partial\rho$ 和 $-n\,\partial V_H/\partial n$。$\overline R/(\rho n)$ 一项在两者中相同,相减抵消。乘以 $kn/(\overline R^2+v_R)$ 后,"报告率减覆盖"为:

$$-\rho\,\frac{\mathrm d\tau^2}{\mathrm d\rho}\,(kn+1)-(1+\tau^2)$$

(检查 A.S7)它为正时提高报告率更有效。

- 二项型:$-\rho\,\mathrm d\tau^2/\mathrm d\rho=1/[\rho(\nu+1)]$,$1+\tau^2=(\rho\nu+1)/[\rho(\nu+1)]$,条件化为 $kn>\rho\nu$,即 $m>\rho^2\nu/k$(检查 A.S5)。$\nu=100$ 时阈值 17.9,$\nu=1000$ 时 178.6;$\nu\to\infty$ 时报告率不波动,阈值趋于无穷,回到原命题。
- 制度型:$\tau$ 与 $\rho$ 无关,导数为零,覆盖总是占优,比值为 $A_H/\overline R=1+\rho(1+\tau^2)(\overline R^2+v_R)/(k\overline R)$,$\tau=0.15$ 时 1.86(检查 A.S6)。但两种手段都动不了 $v_H$。

板书时一句话总结:报告率波动属于二项型时,提高报告率顺带压低波动,规模够大后它反超扩大覆盖;属于制度型时,原排序不变,但要去掉 $v_H$ 只能统一口径。

**观测到报告率时。** 若各期 $p_t$ 已知,用 $\tilde R_t=C_t/(p_tn)$,条件方差为 $R_t/(p_tn)+R_t^2/(kn)$,于是:

$$\mathrm E(\tilde R_t-\overline R)^2=v_R+\frac{\overline R\,\mathrm E(1/p_t)}{n}+\frac{\overline R^2+v_R}{kn}$$

不含 $v_H$(检查 A.S8、A.M2)。这就是第三条杠杆"报告标准化"的数学含义。Parag 等 (2022) [2] 第 588 页在报告率已知的设定下证明恒定报告率时信息量最大;这里处理的是报告率未知时波动的不可约部分,两者互补。

**不可识别(只需陈述,被问再推)。** 均值 $\overline R$ 与 $v_R$、$\tau^2$ 无关;方差的三项中,$v_R+v_H=U-\overline R^2$,$A_H=\overline R+\rho U/k$,其中 $U=(1+\tau^2)(\overline R^2+v_R)$。所以只看计数的前两阶矩,$(v_R,\tau^2)$ 沿 $U$ 的等值线移动时什么都看不出来(检查 A.S4)。论文里的仿射回归只用到前两阶矩,截距 $a$ 中"环境"与"报告"两部分无法拆开,拆开需要报告率的辅助数据。

**比值估计量中的报告噪声(被问再推)。** 设第 $j$ 个州 $p_{j,t}=\rho_ju_{j,t}$,$\rho_j$ 不随时间变化。$G_t=C_{t+1}/D_t$ 的分子分母各含一个 $\rho_j$,精确约去(检查 A.M3 中 const_only 场景的误差为机器精度)。真实感染数在滞后窗口内近似不变、无计数噪声时,令 $u=1+\epsilon$ 一阶展开:

$$\frac{G_t}{G_t^0}-1\approx\epsilon_{t+1}-\sum_{s\ge1}w_s\epsilon_{t+1-s}$$

其中 $G_t^0$ 是报告率恒为 $\rho_j$ 时的值。取方差,周间波动进入截距的量为 $\tau_w^2F(w,\psi)$:

$$F(w,\psi)=1-2\sum_{s\ge1}w_s\psi^{s}+\sum_{s\ge1}\sum_{s'\ge1}w_sw_{s'}\psi^{\lvert s-s'\rvert}$$

(检查 A.S9)主规格 $w=(0.65,0.25,0.10)$ 下 $\psi=0$ 时 $F=1.495$,$\psi=0.9$ 时 $F=0.217$。截距比只依赖 $\psi$,扫遍 $\psi\in[0,1)$ 得 $q_1\in[0.883,1.338]$、$q_2\in[0.892,1.373]$,与实证 0.688 [0.658, 0.727] 和 1.539 [1.420, 1.656] 都不相交(检查 A.N1)。结论:纯报告噪声解释不了截距随权重的变化。

### 9.2 命题 B:规模买不到 $v_R$ 的精度(现场必推前两步)

**第一步:矩估计。** 由命题 2,单期报告数的边缘方差为:

$$\mathrm{Var}(C_t)=m^2V(m)=m\overline R+\frac{\rho m}{k}(\overline R^2+v_R)+m^2v_R$$

(检查 B.S1)第三轮方案原文的矩式漏了 $m^2v_R$ 这一项,这里是修正后的版本。用样本均值 $\bar C$ 代替 $m\overline R$、样本方差 $S_C^2$ 代替 $\mathrm{Var}(C_t)$,对 $v_R$ 解出:

$$\hat v_R=\frac{S_C^2\,km-\bar C\,km-\rho\bar C^2}{m^2(km+\rho)}$$

(检查 B.S2)记 $Y_t=C_t/m$,它等价于 $\hat v_R=[S_Y^2-h(\bar Y)]/(1+\rho/(km))$,$h(y)=y/m+\rho y^2/(km)$。也就是"样本方差减去抽样噪声的估计"。

**第二步:为什么有平台。** $m\to\infty$ 时 $Y_t\to R_t$,$h\to0$,$\hat v_R$ 退化为 $R_1,\dots,R_T$ 的样本方差。后者的方差只取决于 $T$ 和 $R_t$ 的分布,与 $m$ 无关。这一步在白板上一句话就够了,精确版本是:

$$T\,\mathrm{Var}(\hat v_R)\to\Omega(m)=\Omega_\infty+\frac{c_1}{m}+O(m^{-2}),\qquad \Omega_\infty=\mathrm E(R_t-\overline R)^4-v_R^2$$

Gamma 环境下 $\Omega_\infty=v_R^2(2+6v_R/\overline R^2)$,$c_1=4v_RA+8v_R^2[k\overline R+3\rho(\overline R^2+v_R)]/(k\overline R^2)$(检查 B.S4、B.S4b)。图示参数下 $c_1/\Omega_\infty=108.6$,即 $m$ 要到 100 左右,有限规模的额外方差才和平台同量级:$m=10$、100、1000 时 $\Omega(m)/\Omega_\infty=37.5$、2.36、1.11(检查 B.N1)。$Y_t$ 的三、四阶矩由负二项阶乘矩 $\mathrm E[C_t(C_t-1)\cdots(C_t-j+1)\mid R_t]=(nk)(nk+1)\cdots(nk+j-1)(\rho R_t/k)^j$ 精确算出,不用模拟。

**第三步:任何估计量都过不了这个平台(被问再推)。** $v_R\to R_{1:T}\to C_{1:T}$ 是马尔可夫链,因为给定全部 $R_t$ 后报告数的分布不含 $v_R$。由数据处理不等式,报告数关于 $v_R$ 的 Fisher 信息不超过 $R_{1:T}$ 自身的信息,与 $m$ 和相关结构都无关。Gamma 环境(均值固定)下每期信息为:

$$\mathcal I_R(v_R)=\frac{\alpha[\alpha\psi_1(\alpha)-1]}{v_R^2},\qquad \alpha=\overline R^2/v_R$$

$\psi_1$ 为三伽马函数,图示参数下 315.6(检查 B.S5)。所以任一无偏估计的相对标准误不低于 $(0.505T)^{-1/2}$:

| $T$ | 3 | 5 | 10 | 20 | 50 | 100 |
|---|---|---|---|---|---|---|
| 相对标准误下界 | 0.81 | 0.63 | 0.44 | 0.31 | 0.20 | 0.14 |

单期报告数关于 $v_R$ 的信息在 $m=1$、10、100、1000、3000 时为 0.17、8.0、134.9、284.8、304.8,单调趋近 315.6(检查 B.N2)。蒙特卡洛覆盖 $\phi\in\{0,0.5,0.8\}$、$T$ 从 3 到 100、$m$ 从 3 到 $10^4$ 共 144 格(检查 B.M1–B.M3),$\phi=0$ 的 48 格上模拟方差与有限规模公式之比在 0.96 到 1.06 之间。相对均方根误差举例:

| | $m=3$ | $m=10$ | $m=100$ | $m=1000$ | $m=10^4$ |
|---|---|---|---|---|---|
| $T=3$ | 16.8 | 6.40 | 1.58 | 1.06 | 1.02 |
| $T=10$ | 8.13 | 3.02 | 0.75 | 0.52 | 0.49 |
| $T=50$ | 3.56 | 1.29 | 0.32 | 0.22 | 0.21 |

每一行从 $m=1000$ 起几乎不动,每一列随 $T$ 稳定下降。图见 `.work/case-count-bottleneck/derivation/r3/figures/fig_r3_01_vR_precision.pdf`。

**第四步:自相关下的有效期数(现场必推)。** 高斯一阶自回归、$\overline R$ 已知时,对正态变量有 $\mathrm{Cov}[(R_s-\overline R)^2,(R_t-\overline R)^2]=2v_R^2\phi^{2\lvert s-t\rvert}$。因此:

$$\mathrm{Var}\Big[\frac1T\sum_{t=1}^T(R_t-\overline R)^2\Big]=\frac{2v_R^2}{T^2}\sum_{s,t}\phi^{2\lvert s-t\rvert}=\frac{2v_R^2}{T}\kappa_T(\phi^2)$$

(检查 B.S7、B.M4)有效期数为 $T/\kappa_T(\phi^2)\approx T(1-\phi^2)/(1+\phi^2)$。和均值的有效期数 $T(1-\phi)/(1+\phi)$ 相比,平方序列的自相关是 $\phi^2$,衰减更快,所以有效期数更大:$\phi=0.8$、$T=26$ 时均值约 2.9,方差精确为 6.2;$T=100$ 时为 11.1 与 22.4。$\phi$ 已知时,高斯一阶自回归关于 $v_R$ 的信息为 $T/(2v_R^2)$,与 $\phi$ 无关(检查 B.S6),先预白化再估计就能达到。

**推论:季层面成分。** 设 $R_t=\overline R+\eta_{s(t)}+\varepsilon_t$,$\eta$ 是 $S$ 个流行季的共同成分,方差 $v_S$。同一条数据处理链 $v_S\to\eta_{1:S}\to R\to C$ 给出:任一无偏估计的相对标准误不低于 $\sqrt{2/S}$,季均值未知时为 $\sqrt{2/(S-1)}$。$S=3$ 时为 0.82 和 1.00,和州数、周数、病例数都无关。

注意这条推论的边界:它只说季层面成分无法由三季数据确定;季内成分仍可由大量州周估计。不要说成"16,218 个州周只有 3 个独立观测,所以 $v_R$ 估不准",这个说法与精读核验结果不符(截距 $a$ 的不确定性按季聚类与按州聚类差不多,问题在识别,不在样本量)。

### 9.3 命题 C:三种杠杆的分工(只需陈述,公式一行可推)

$T$ 期平均 $\bar R_T=T^{-1}\sum_tC_t/m$ 的误差拆成"给定 $R$ 与 $p$ 的抽样误差"和"$u_tR_t$ 的波动"两部分,二者不相关。第二部分的协方差因 $u$ 与 $R$ 独立而可分解:

$$\mathrm{Cov}(u_sR_s,u_tR_t)=v_R\varrho_R(h)+\tau^2\varrho_u(h)[\overline R^2+v_R\varrho_R(h)],\qquad h=\lvert s-t\rvert$$

(检查 C.S1)两者都是一阶自回归时得:

$$\mathrm E(\bar R_T-\overline R)^2=\frac{v_R\kappa_T(\phi)+\tau^2\overline R^2\kappa_T(\psi)+\tau^2v_R\kappa_T(\phi\psi)}{T}+\frac{A_H}{Tm}$$

读法:$m$ 只出现在最后一项;$T$ 压前三项,但报告偏差持续($\psi=1$)时报告项至少是 $\tau^2\overline R^2$,期数再多也压不下去;$\tau=0$ 或使用观测到的 $p_t$ 去掉报告项;$v_R$ 本身的精度只由 $T$ 决定(命题 B)。

数值($\phi=\psi=0.5$,$\tau=0.15$,单位 $10^{-3}$,每种设置 6×10⁴ 次模拟,最大标准化偏差 1.37,检查 C.M1):

| 设置 | 理论 | 模拟 | 说明 |
|---|---|---|---|
| 基线 $T=10$,$m=50$ | 22.54 | 22.63 | 环境 10.40,报告 7.85,抽样 4.29 |
| 规模×10 | 18.68 | 18.58 | 只压抽样项 |
| 期数×4 | 6.16 | 6.18 | 三项都降 |
| 统一口径 $\tau=0$ | 14.65 | 14.58 | 报告项归零 |
| 观测报告率 | 14.70 | 14.77 | 报告项归零 |
| $\psi=1$,$T=40$ | 33.79 | 33.50 | 报告项 29.8,期数无效 |

图见 `.work/case-count-bottleneck/derivation/r3/figures/fig_r3_02_levers_budget.pdf` 左栏。

### 9.4 命题 D:自相关下的预算设计(现场必推目标函数与一阶条件)

论文推论 1 之后有一句"环境服从一阶自回归时 $m^*$ 约需乘以 $\sqrt{(1-r)/(1+r)}$,正相关使最优方案偏向更多、更小的期"。这句只在预算很大时成立,预算小时方向相反。

**目标函数。** 预算约束 $T(c_0+c_1m)=\mathcal B$ 解出 $c_1mT=\mathcal B-c_0T$,代入 $T$ 期平均的方差:

$$F(T)=v_R\,e(T)+\frac{Ac_1}{\mathcal B-c_0T},\qquad e(T)=\frac{\kappa_T(\phi)}{T}$$

**一阶条件。** 记 $g_T(\phi)=-T^2e'(T)$,求导并代回 $\mathcal B-c_0T=c_1mT$:

$$v_R\,g_T(\phi)=\frac{c_0A}{c_1m^2}\quad\Longrightarrow\quad m^*=\frac{m_0^*}{\sqrt{g_{T^*}(\phi)}},\qquad m_0^*=\sqrt{\frac{c_0A}{c_1v_R}}$$

独立情形 $g\equiv1$,回到推论 1。显式地:

$$g_T(\phi)=\frac{1+\phi}{1-\phi}-\frac{2\phi}{(1-\phi)^2}\Big[\frac{2(1-\phi^T)}{T}+\phi^T\ln\phi\Big]$$

(检查 D.S1;脚本里这个量叫 lambda_T,论文里改用 $g_T$,因为 $\lambda$ 已用于收缩估计、$\Lambda$ 已用于感染压力。)

**关键事实:$g_T$ 从小于 1 单调增到大于 1。**

- 端点:$g_\infty=(1+\phi)/(1-\phi)>1$;$g_1-1=2\phi(\phi-1-\phi\ln\phi)/(1-\phi)^2$,而 $\phi(1-\ln\phi)$ 的导数 $-\ln\phi>0$、在 $\phi=1$ 处等于 1,所以 $g_1<1$(检查 D.S2、D.S3)。
- 单调:令 $x=-T\ln\phi$,$H(T)=2(1-\phi^T)/T+\phi^T\ln\phi$,直接求导得 $T^2H'(T)=q(x)-2$,$q(x)=e^{-x}(x^2+2x+2)$。$q(0)=2$,$q'(x)=-x^2e^{-x}<0$,所以 $H$ 递减、$g$ 递增(检查 D.S4)。
- 凸性(被问再推):$e''(T)=(2g_T-Tg_T')/T^3$,化简后要证 $(1-\phi^2)/\phi>L\,w(x)$,$L=-\ln\phi$,$w(x)=[6-e^{-x}(6+4x+x^2)]/x$。先证 $w\le2$:$z(x)=(6+4x+x^2)e^{-x}-6+2x$ 满足 $z(0)=0$、$z'\ge0$。再令 $y=1/\phi$,左边是 $y-1/y$,右边不超过 $2\ln y$,而 $y-1/y-2\ln y$ 在 $y=1$ 处为零、导数 $(1-1/y)^2>0$(检查 D.S5、D.S6)。

**结论。** $F$ 严格凸,最优 $T^*$ 唯一且随预算增加;$g_{T^\dagger}=1$ 的根 $T^\dagger$ 唯一,对应预算阈值 $\mathcal B^\dagger=T^\dagger(c_0+c_1m_0^*)$。

- $\mathcal B<\mathcal B^\dagger$:$T^*<T^\dagger$,$g<1$,$m^*>m_0^*$,应当更少、更大的期。
- $\mathcal B>\mathcal B^\dagger$:$m^*<m_0^*$,应当更多、更小的期;$\mathcal B\to\infty$ 时 $m^*\to m_0^*\sqrt{(1-\phi)/(1+\phi)}$,即原文那句近似。
- 整数解取 $\lfloor T^*\rfloor$ 或 $\lceil T^*\rceil$(凸性);$F'(1)\ge0$ 时取 $T=1$。

直观解释:期数很少时,多加一期带来的大部分是和上一期重复的信息,边际收益低于独立情形,所以先把每期做大;期数多了以后,相关的环境项成为主导,规模的边际收益下降,于是改为增加期数。

数值($c_0/c_1=100$,$m_0^*=72.9$,检查 D.N2 共 81 个设计全部符合):

| $\phi$ | $T^\dagger$ | $\mathcal B^\dagger$ | $g_1$ |
|---|---|---|---|
| 0.3 | 2.51 | 433 | 0.585 |
| 0.5 | 2.96 | 511 | 0.386 |
| 0.8 | 4.48 | 775 | 0.141 |
| 0.9 | 6.13 | 1060 | 0.068 |

$\phi=0.8$ 时:$\mathcal B=600$ 最优 $T^*=3.06$、$m^*=96.3$,整数解 $T=3$、$m=100$;$\mathcal B=2000$ 时 $m^*=36.0$;$\mathcal B=60000$ 时 $m^*=24.5$,接近近似值 24.3。$\mathcal B=600$ 时按原近似取 $T=5$、$m=20$,模拟方差 0.0504,最优方案 0.0403(检查 D.M1)。

**空间附注(只需陈述)。** 把期换成 $J$ 个辖区,辖区间平均相关 $\bar c$,论文式 (pooling) 加抽样项后对 $m$ 求导得 $m^*=\sqrt{c_0A/[c_1v_R(1-\bar c)]}$,随 $\bar c$ 上升:相关越强,越应在少数辖区加深监测(检查 D.S7)。第三轮方案原文写的方向相反,不采纳。

### 9.5 板书顺序(约 25 分钟)

1. 写 H5,一行写出 $C_t\mid p_t$ 的负二项分布(1 分钟)。
2. 两次全方差公式推出 $v_R+v_H+A_H/m$,圈出 $\sigma^2n^2R_t^2$ 这一项(5 分钟)。
3. 写"报告率减覆盖"的边际差,分二项型与制度型两行得到阈值 $m>\rho^2\nu/k$ 与比值 $A_H/\overline R$(4 分钟)。
4. 写 $\tilde R_t=C_t/(p_tn)$ 的方差,指出 $v_H$ 消失(1 分钟)。
5. 写 $\mathrm{Var}(C_t)$ 的三项,解出 $\hat v_R$;说明 $m\to\infty$ 时退化为 $R_t$ 的样本方差(4 分钟)。
6. 画 $v_R\to R_{1:T}\to C_{1:T}$ 的链,写数据处理不等式与相对标准误下界表(3 分钟)。
7. 写平方序列的协方差 $2v_R^2\phi^{2h}$,得 $T/\kappa_T(\phi^2)$(2 分钟)。
8. 写 $F(T)$、一阶条件 $m^*=m_0^*/\sqrt{g_T}$,画 $g_T$ 从 $g_1<1$ 增到 $(1+\phi)/(1-\phi)$ 的草图,标出 $T^\dagger$(5 分钟)。

收尾一句:规模换 $\overline R$ 的精度,期数换对 $v_R$ 的认识,报告标准化去掉 $v_H$。

下界的 Cauchy–Schwarz 一步、$\Omega(m)$ 的 $c_1$、$g_T$ 的凸性三处留到被问时再推。

### 9.6 导师追问预案

**问:$\tau$ 实际有多大,$v_H$ 是不是可以忽略?** 精读报告用 NHSN 填报医院数的周间比值估计过一个代理:比值方差 0.00118,对应 $\tau_w\approx0.034$,只占截距超出部分的 1.7%–2.9%。所以按这个代理,周间报告波动在实证截距里不重要;命题 A 的意义在于设计层面(若 $\tau=0.15$,交叉规模从 53 降到 30)与识别层面(截距里有一部分原则上可能来自报告)。代理只覆盖医院填报数,不覆盖检测行为,这一点要说明。

**问:原来的命题 3 错了吗?** 原命题在报告率固定的假设下正确。命题 A 给出它的适用范围:制度型波动下排序不变;二项型波动下,规模超过 $\rho^2\nu/k$ 后排序反转。

**问:下界依赖 Gamma 假设吗?** 一般下界是 $v_R+(\overline R^2+v_R)/\mathcal J_u$,对任何 $u_t$ 分布成立;Gamma 是唯一使它等于 $v_R+v_H$ 的情形。其他分布下最优估计量可能略好于 $C_t/m$,但改进有限,对数正态 $\tau=0.15$ 时只差 1.1%。

**问:用极大似然估 $v_R$ 会不会比矩估计好?** 数据处理不等式对所有无偏估计成立,渐近地也约束极大似然。极大似然在 $m$ 小时能更接近下界,但下界本身随 $m$ 增大只趋于 $R_{1:T}$ 的信息,平台依然存在。

**问:那三季数据是不是意味着 $v_R$ 根本估不了?** 不能这样说。推论只针对季层面的共同成分;州周层面的环境方差仍有大量单位可用。精读核验显示截距的不确定性按季聚类与按州聚类相近,难点在于识别(命题 A(vi)),与"只有 3 个观测"无关。

**问:非高斯自回归时 $T/\kappa_T(\phi^2)$ 还成立吗?** 不一定。平方序列的协方差会多出四阶累积量项。脚本只验证了高斯情形,论文中需写明。

**问:预算阈值依赖什么?** $T^\dagger$ 只依赖 $\phi$;$\mathcal B^\dagger$ 还依赖 $c_0$、$c_1$ 与 $m_0^*$。所以"多期小规模还是少期大规模"取决于预算与 $\mathcal B^\dagger$ 的相对位置,与固定费用占比有关。

**问:把 $T$ 当连续变量合法吗?** $F$ 严格凸,整数最优一定是连续最优点两侧的整数之一,所以只需比较两个值(检查 D.N2 对 81 个设计逐一核对)。

**问:报告噪声能不能解释截距随权重变化?** 不能。纯报告噪声给出的截距比随 $\psi$ 变化的整个范围($q_1$ 在 0.883 与 1.338 之间,$q_2$ 在 0.892 与 1.373 之间)都不包含实证值 0.688 和 1.539。

**问:这些结果哪些是你自己的?** 见下一节。

### 9.7 哪些是标准工具,哪些是新的

标准工具:全方差公式;Cramér–Rao 不等式与尺度族 Fisher 信息 [6][7];Fisher 信息的数据处理不等式 [11];样本自协方差的方差 [12];方差分量模型中组间方差的精度受组数限制 [13][9];恒定漏报不影响再生数估计 [14][15];报告率已知时恒定报告信息最大 [2];两阶段抽样的费用分配 [9];一阶自回归的方差和 [10]。

本文新增:本观测链下的三分量分解与推广交叉规模;两类报告波动下命题 3 排序的分化与反转阈值 $m>\rho^2\nu/k$;经由 $U$ 的不可识别性;比值估计量随滞后权重变化的截距特征 $F(w,\psi)$;修正矩估计的有限规模方差 $\Omega(m)$ 与 $1/m$ 系数 $c_1$;平方序列的精确有效期数 $T/\kappa_T(\phi^2)$;一阶自回归下的精确一阶条件、$g_T$ 的单调性与凸性、预算阈值 $\mathcal B^\dagger$。

### 9.8 第三轮验证记录

| 编号 | 内容 | 方法 | 结果 |
|---|---|---|---|
| A.S1–A.S2 | 条件方差、三分量分解 | sympy | 通过 |
| A.S3、A.S3b | Gamma 与对数正态尺度族信息 | sympy | 通过 |
| A.S4 | 经由 $U$ 的不可识别 | sympy | 通过 |
| A.S5–A.S7 | 两类波动的边际比较与一般准则 | sympy | 通过 |
| A.S8–A.S9 | 观测报告率的方差、$F(w,\psi)$ | sympy | 通过 |
| A.N1–A.N2 | 截距比范围、数值 Fisher 信息 | 数值积分 | 通过 |
| A.M1–A.M3 | 三分量、观测报告率、比值估计量 | 模拟 | 最大标准化偏差 1.64;比值估计量相对误差小于 6% |
| B.S1–B.S7、B.S4b | 边缘方差、矩估计、平台与 $c_1$、Fisher 信息、有效期数 | sympy | 通过 |
| B.N1–B.N2 | $\Omega(m)$ 单调与收敛速率、数值数据处理不等式 | 精确计算 | 通过 |
| B.M1–B.M4 | 144 格平台、有限规模公式、下界、自回归有效期数 | 模拟 | 无失败格 |
| C.S1–C.S2、C.N1 | 协方差分解、抽样项、杠杆分工 | sympy、精确计算 | 通过 |
| C.M1 | 六种杠杆设置 | 模拟 | 最大标准化偏差 1.37 |
| D.S1–D.S7 | $g_T$ 表达式、端点、单调、凸性、空间附注 | sympy | 通过 |
| D.N1–D.N2 | 网格上的凸性与单调、81 个设计 | 数值优化 | 通过 |
| D.M1 | 设计方差与 $\mathcal B=600$ 对比 | 模拟 | 通过 |

关于 B.N1 的一处判据调整:首轮判据要求 $m=10^5$ 时 $\Omega(m)$ 与极限的相对差小于 $10^{-3}$,而 $c_1/m$ 这一项在该处本身就是 $1.09\times10^{-3}$,判据比命题本身还严。命题的极限已由 B.S4 符号验证,因此补充 B.S4b 推出 $c_1$,并把 B.N1 改为"单调,且 $m(\Omega/\Omega_\infty-1)$ 与 $c_1/\Omega_\infty$ 相差小于 2%",实测比值 1.0025 和 1.0003。命题内容没有改动。

复现:在仓库根目录运行 `python3 .work/case-count-bottleneck/derivation/r3/verify_r3.py`,约 43 秒;图由同目录 `figures/make_figs_r3.py` 生成。用户仓库里的代码没有运行。

### 9.9 第三轮新增参考文献

[11] Zamir R. A proof of the Fisher information inequality via a data processing argument. IEEE Transactions on Information Theory, 1998, 44(3): 1246–1250. https://doi.org/10.1109/18.669301

[12] Bartlett MS. On the theoretical specification and sampling properties of autocorrelated time-series. Supplement to the Journal of the Royal Statistical Society, 1946, 8(1): 27–41. https://doi.org/10.2307/2983611

[13] Searle SR, Casella G, McCulloch CE. Variance Components. New York: Wiley, 1992. https://doi.org/10.1002/9780470316856

[14] Gostic KM, McGough L, Baskerville EB, et al. Practical considerations for measuring the effective reproductive number, Rt. PLoS Computational Biology, 2020, 16(12): e1008409. https://doi.org/10.1371/journal.pcbi.1008409

[15] Azmon A, Faes C, Hens N. On the estimation of the reproduction number based on misreported epidemic data. Statistics in Medicine, 2014, 33(7): 1176–1192. https://doi.org/10.1002/sim.6015
