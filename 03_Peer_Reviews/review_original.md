# Peer review of the current manuscript

- Manuscript: "Limits to improving reproduction number estimates by increasing case counts: Environmental variability, reporting heterogeneity, and surveillance design" (single author; target journal: Epidemics)
- Version reviewed: English manuscript and supplement in the author's public repository (commit c2c859a, directory paper_en), compared against the Chinese version (paper_zh) and the released reproduction package
- Review date: 20 October 2026
- Benchmark article: Eales and Riley (2024), Epidemics 46:100742 [8]
- Verification: every numerical check reported below was recomputed by the reviewer. The scripts are theory_checks.py (closed-form quantities and a hierarchical Monte Carlo) and empirical_checks.py (re-analysis of the released derived panel of 10,303 state-weeks). Results quoted as "Verification" come from those scripts or from the independent reproduction audit of the released package.

Part A is the English review and Part B is the Chinese review. The two parts have the same numbering, the same verdict and the same score.

## Part A — English

### 1 Summary

The manuscript asks how much the precision of reproduction-number estimates improves when more cases are observed. It separates two inferential targets: the current transmission potential R_t (Target 1) and the cross-period mean transmission potential R̄ (Target 2). Under a negative-binomial branching process with binomial reporting, the author derives the mean squared error of a single-period estimator of R̄ as V(m) = v_R + A/m. Here v_R is the variance of R_t across periods (called environmental variance), A = R̄ + ρ(R̄² + v_R)/k, and m = ρn is the expected number of reported cases. The ratio m× = A/v_R is called the variance balance scale. Further propositions cover:

- multiplicative reporting heterogeneity, which adds a component v_H and lowers the balance scale (Proposition 3);
- budget allocation between the number of periods and the volume per period, with m* = √((c0/c1)m×) (Proposition 4);
- Fisher-information bounds for estimating v_R and a between-season variance (Proposition 5 and Corollary 2);
- a decomposition of design levers (Proposition 6);
- a budget threshold B† under AR(1) environments (Proposition 7).

The empirical part uses NHSN weekly influenza hospital admissions for 50 US states and Washington, D.C. In an early-expansion window of 1,267 state-weeks, the relative squared error of a weekly growth ratio G = C_{t+1}/D_t is regressed on 1/D_t. The fit gives an intercept a = 0.0991 and a slope b = 2.243 (b/a = 22.6), which the author reads as an empirical counterpart of v_R/R̄² and m×. The empirical part also includes:

- intercept-ratio diagnostics across denominator weightings (q1 = 0.688, q2 = 1.539);
- a reporting-completeness adjustment, with Δa = −0.0004 judged equivalent to zero by TOST with a ±0.0050 margin;
- cross-pathogen grading for COVID-19 and RSV;
- season-level and phase-level analyses;
- comparisons with ILINet, FluSurv-NET, FluSight forecasts and European COVID-19 data.

The practical conclusion is that once single-period volume reaches m×, resources should go to more observation periods, spatial pooling and standardised reporting rather than to more cases per period.

### 2 Strengths

S1. The question is relevant to Epidemics readers. Surveillance programmes routinely size systems by case counts, and the distinction between detecting a current change (Target 1) and estimating a stable mean (Target 2) is useful for design.

S2. The core algebra is correct. The reviewer reproduced A = 2.1232 and m× = 53.08 at the baseline parameters (R̄ = 1.15, v_R = 0.04, k = 0.35, ρ = 0.25), the doubling-gain formula 1/[2(1 + m/m×)], and v_H = 0.03066, A_H = 2.1451 and m×,H = 30.36 for τ = 0.15. A hierarchical Gamma–negative-binomial–binomial simulation matches V(n, ρ) to within Monte Carlo error at every design point tested (for example 0.2529 simulated against 0.2523 analytical at n = 40, ρ = 0.25).

S3. The design results are internally consistent and potentially useful. The levers decomposition reproduces (22.57, 18.71, 6.17 and 14.65 × 10⁻³ for baseline, tenfold volume, fourfold periods and τ = 0). The budget threshold B† = 775 is reproduced exactly at the baseline m× (T† = 4.48, m0* = 72.86). The optimal-volume ranges m* ∈ [14.6, 22.2] and [46.1, 70.1] are also reproduced.

S4. The empirical point estimates are reproducible. The reproduction audit recovered a = 0.0991, b = 2.243, b/a = 22.6 and N = 1,267 in three ways: from the archived output, by independent re-implementation, and from a fresh NHSN data vintage downloaded on 20 October 2026.

S5. The author reports many robustness checks and, in the Abstract and Limitations, concedes the two central identification limits: a plateau cannot be separated from slow decay, and the intercept cannot be uniquely attributed to environmental variance. This candour is a strength. The issue is that the title, the Results and the Conclusion do not follow these concessions (see M3 and m10).

S6. The surveillance setting is well chosen. The 2024 switch between mandatory and voluntary NHSN reporting is a rare natural variation in reporting completeness.

### 3 Weaknesses

#### Major

M1. The contribution is overstated against existing theory. V(m) = v_R + A/m is the law of total variance applied to an estimator that is conditionally unbiased for R_t. The resulting "floor" v_R is fixed by the choice of target (R̄) and of estimator class (single-period, conditionally unbiased for R_t). The same decomposition is the classical split of environmental and demographic stochasticity in population ecology: Var(growth) ≈ σ_e² + σ_d²/N, and the critical size σ_d²/σ_e² plays the role of m× [9, 10, 11]. The manuscript cites Engen et al. (1998) only as a terminological analogy. Proposition 3 overlaps with Parag et al. (2022), who already showed that variable reporting fractions reduce the information about R_t through their geometric mean [5]. Proposition 4 is, as the author notes, Neyman–Cochran allocation. Separately, V depends on (n, ρ) and not on m alone. When ascertainment ρ rises with n fixed, the error cannot fall below v_R + (R̄² + v_R)/(kn), which affects the design interpretation.

M2. The empirical statistic is not a reproduction-number estimate. G = C_{t+1}/D_t uses weekly weights (0.65, 0.25, 0.10), with a mean lookback of 10.2 days (Section 6.5, Eq. dt). These weights are not an influenza generation-interval distribution. G is therefore a weekly growth factor of a delay-convolved, downstream series, that is, an apparent quantity in the sense of Eales and Riley [8]. It is not R_t in the sense of Cori et al., Fraser or Wallinga and Lipsitch [1, 2, 3]. The Limitations paragraph concedes that weekly admissions span about two generations. Even so, the title and Abstract present the result as a limit on "reproduction number estimates", and Wallinga and Lipsitch (2007) is not cited.

M3. The intercept is not identified as environmental variance, and the plateau is not identified against slow decay. The manuscript's own Eq. (info-decomp) adds a component for infection-pressure uncertainty. The loss is measured against a single R̄ pooled over three seasons and 51 states. The selected early-expansion windows carry systematic growth trends. The reviewer found that 53% of the intercept is a national, week-synchronous component: adding week fixed effects reduces a from 0.0991 to 0.0464. The levelling-off rests on the two largest bins (N = 152 and 92). The power-law exponent p̂ = 0.273 is not distinguished from a plateau. b/a varies from 10.6 (top 1% trimmed) through 16.0–46.4 (leave one season out) to 119.2 (peak phase).

M4. The comparison of theory and data compares the ratio with the wrong quantity. Each parameter separately disagrees with theory: a is 3.5–6.9 times the scenario values and b is 3.2–3.7 times. Under the manuscript's own denominator-noise correction (Eq. b-delta), the scenario values of b/a are 38.9–83.5, not 21.3–49.2. The empirical 22.6 therefore falls below the corrected prediction rather than inside it. The Chinese version reports this direction (b/a overestimates m×; 59.2 against a true A/v_R of 30.7 in simulation), but the English version omits it.

M5. The confidence intervals ignore cross-state dependence within the same week. Resampling the 51 states treats states as independent. The quantity under study, however, is a shock shared within a period. In the released panel, the week-level intra-class correlation of growth deviations is 0.29. The week-clustered bootstrap standard deviation of a is 0.0171, twice the state-clustered value of 0.0084, and its 95% interval is [0.065, 0.131] rather than [0.084, 0.116]. The bibliography contains Cameron, Gelbach and Miller (2011) on multiway clustering, but the paper never cites or uses it.

M6. The reporting-heterogeneity conclusion depends on the proxy, a post hoc margin and an external benchmark. Facility reporting completeness measures participation, not case ascertainment. The ±0.0050 TOST margin equals 5% of the realised a and was fixed after a was known. For influenza in 2025–26, Δa is detectably non-zero (90% BCa 0.0020 to 0.0060) and is still declared equivalent, because a = 0.177 widens the margin to 0.0088. The "below 1% of the excess" statement rests on the exogenous benchmark v_R = 0.08. The power of the Δa test is at most 2.5% for κ ≤ 1 (Table S4).

M7. The analysis plan is not pre-registered in the usual sense, and there is no multiplicity control. The documents called "pre-registrations" (rounds r3 and r4, dated 17 and 18 October 2026) were written after the primary results were available. The grading rule changed between rounds without disclosure, and it moved influenza from "replicated" to "partial". Five grading variants give five different outcome vectors (Table S8). Three pathogens, two window types and several criteria are tested without adjustment. FluSurv-NET is described as corroborating although its q intervals span zero (q1 −3.61 to 3.92). FluSight forecasts target the same NHSN series and are not an independent check.

M8. The reproduction package is incomplete. The raw NHSN snapshot, two intermediate result files and the theory and simulation code are missing. The package has no plotting scripts for Figures 1–5; a figure builder exists only in the Chinese manuscript folder. Four scripts fail with FileNotFoundError, and paths are hard-coded. The Data and code availability statement nevertheless asserts completeness. The English version also lacks the generative-AI declaration and the Zenodo DOI that the Chinese version provides.

M9. The presentation prevents efficient assessment. The main text runs to 36 pages and about 7,700 words, with seven propositions and two corollaries. All English figures carry Chinese axis labels. The supplement contains 19 unresolved cross-references ("??"). Proof titles are misnumbered. Several captions contradict their panels. Page numbers overprint captions on pages 12, 21, 23 and 24.

#### Minor

- m1. The bound (0.505T)^{-1/2} in Proposition 5(ii) holds only for one parameter set (ξ = R̄²/v_R = 33.06). It is not a general constant.
- m2. Corollary 2 is applied inconsistently: √(2/S) in Section 3.5 and √(2/(S−1)) in Section 3.6.
- m3. In Section 3.6 the interval −0.056 to 0.211 belongs to the pooled random-effects mean, not to the between-season variance. It is also attached to an S = 4 point estimate while coming from the S = 3 fit.
- m4. Proposition 7 does not define e(T) or g_T in the main text, does not state that B† is in units of c1, and does not report that B† depends on m×.
- m5. The levers decomposition reports 7.85 for the reporting term against 7.88 recomputed. The "72% against 17%" comparison mixes budgets (2,000 against 5,000 cases) and assumes a stationary R̄ over 40 weeks.
- m6. The Wald size and power numbers in Section 3.1 are not reproducible from the released code. A non-randomised discrete test is not exactly UMP at size α.
- m7. The shrinkage example uses oracle weights (δ* = 0.2787).
- m8. Counts and values are inconsistent between text and figures: 6,009/420 against 6,001/416, and 0.107 against 0.108. The value c̄ ≈ 0.34 is given without a derivation.
- m9. The voluntary-reporting contrast is confounded with season onset. The instrumental-variable exclusion restriction is not argued.
- m10. Wording overclaims: "decisively", "confirming", "corroborate", "must", and "100%" where the bootstrap share is 98.6–100%.
- m11. Bibliography hygiene: eleven uncited entries, one wrong author forename, and missing core references.
- m12. The D_t weights are ad hoc, and the treatment of the 504 imputed zeros needs to be stated in Methods.
- m13. The English and Chinese versions are not equivalent in several places.
- m14. Interval types (percentile, BCa, normal) are mixed without labels, and the paper reports two different intervals for a.

### 4 Detailed comments

Each comment gives the location, the problem, why it matters, the requested change, and, where possible, the verification method and its result. The bracket after the number links the comment to the weaknesses above.

D1 [M1]. Location: Introduction (introduction.tex line 10); Section 2.1 (background.tex line 43); Discussion, first paragraph (discussion.tex line 4).
- Problem: the decomposition v_R + A/m is presented as a new limit, with ecology mentioned only as an analogy. In the population-dynamics literature the variance of the growth rate is σ_e² + σ_d²/N, and the population size at which the two terms are equal, σ_d²/σ_e², is a standard quantity [9, 10, 11]. With σ_d² ↔ A and σ_e² ↔ v_R it is the same object as m×.
- Why it matters: Epidemics referees will judge novelty against this literature and against Parag et al. [5, 6, 7].
- Requested change: state the formal identity explicitly. Cite Lande, Engen and Sæther (2003) and Sæther and Engen (2002), which estimate σ_d² and σ_e² from data. Then describe the contribution as transferring a known decomposition to surveillance design, with reporting heterogeneity and budget allocation as the added parts.
- Verification: the bibliography entry for Engen et al. (1998) was checked: Biometrics 54:840–846, DOI 10.2307/2533838 [9].

D2 [M1]. Location: Section 2.3, Proposition 3; Introduction (introduction.tex lines 8 and 14).
- Problem: the manuscript cites Parag et al. (2022) only for the statement that Fisher information grows linearly with counts. The reviewer deep-read that paper. Its Equation 5 already shows that the information in a noisy epidemic curve is modulated by the geometric mean of time-varying reporting fractions, and its Supplementary Note extends this to negative-binomial noise [5]. Reporting variability lowering precision is therefore not new. The new element of Proposition 3 is that a multiplicative reporting shock enters the floor for R̄.
- Why it matters: positioning against the closest prior work is the main novelty test.
- Requested change: add a paragraph contrasting Proposition 3 with Equation 5 of [5]. The contrast concerns the target (R̄ against R_t), the noise model (mean-one multiplicative shock against Beta-distributed reporting fractions) and the consequence (an additive floor against an information ratio).
- Verification: deep reading of [5], Equations 4–5 and the section "Ranking noise sources by their information loss".

D3 [M1]. Location: Propositions 1(ii) and 2 (background.tex); proof of Proposition 2 (supp_proofs.tex line 60).
- Problem: the text describes the error as decaying "strictly as 1/m" and treats m as the design lever. However, V(n, ρ) = v_R + R̄/(ρn) + (R̄² + v_R)/(kn). The proof itself gives the limit as ρ → 1 with n fixed: v_R + R̄/n + (R̄² + v_R)/(kn), which is strictly greater than v_R. Better ascertainment cannot remove the demographic term. Only more ancestors, meaning more transmission or a larger population, can remove it.
- Why it matters: a surveillance programme controls ρ (testing and reporting), not n. The design advice in Section 3.5 and the Conclusion should be expressed for the lever that a programme actually controls.
- Requested change: state Propositions 1–2 in terms of (n, ρ), and give the floor in ρ separately from the floor in n.
- Verification: a Monte Carlo with 200,000 replicates at n = 40 gave V = 0.2529, 0.1949 and 0.1651 for ρ = 0.25, 0.5 and 1.0. The analytical values are 0.2523, 0.1948 and 0.1661, and the analytical limit 0.1661 is four times v_R = 0.04.

D4 [M1]. Location: Section 6.2 (methods.tex lines 14–18); Discussion (discussion.tex line 8).
- Problem: the class "conditionally unbiased for R_t" is used to define a lower bound for estimating R̄. An estimator that must track R_t cannot be closer to R̄ than R_t itself, so the floor v_R follows from the definition. Any multi-period or shrinkage estimator leaves the class. The Discussion acknowledges this, but the Abstract and Conclusion present the floor as a property of surveillance.
- Why it matters: the headline claim reads as a physical limit when it is a limit of a chosen estimator class.
- Requested change: move the estimator-class qualification into the statement of Proposition 2 and into the Abstract. Report the MSE of the obvious competitor (the T-period mean, Proposition 4) next to it.

D5 [M2]. Location: Section 6.3 (methods.tex lines 25–37); Section 6.5, Eq. (dt); title and Abstract.
- Problem: the weights (0.65, 0.25, 0.10) are labelled a three-week lookback, with a mean lag of 1.45 weeks (10.2 days). The influenza generation interval is roughly 3 days, and hospital admissions add an infection-to-admission delay. G therefore estimates a weekly multiplicative growth factor of a downstream series, of the order of R^{7/T_g}, not R_t. The relation between growth rate and R depends on the generation-interval distribution [3], and downstream series distort and lag R [8]. The practical recommendations of Gostic et al. [4] are to estimate R_t from a renewal model with explicit adjustment for observation delays.
- Why it matters: the scale of v_R, the value of R̄ = 1.67 and the balance scale all refer to the weekly growth factor. They cannot be read as properties of R_t estimators such as EpiEstim [1] or Fraser's method [2].
- Requested change: either (a) re-run the case study with a renewal-model R_t estimate (EpiEstim with an influenza generation interval, aggregated-data methods [12, 13, 14], an admission-delay kernel), or (b) retitle and reframe the empirical target as "weekly growth factor of admissions" and confine claims about R_t to the theoretical part. Option (a) is preferred.

D6 [M3]. Location: Section 6.3, Eq. (info-decomp) and line 30; Eq. (affine).
- Problem: Eq. (info-decomp) adds CV²(Λ_{t+1} | F_t)(R̄² + v_R), which the text calls scale-invariant. If that description holds, the term enters the intercept, and a = v_R/R̄² in Eq. (affine) does not follow. If it does not hold (under binomial thinning CV² of the latent pressure is roughly (1 − ρ)/C, which scales as 1/m), the term enters the slope, and b ≠ A/R̄². Either way the identification a ↔ v_R, b ↔ A is not implied by the model the paper writes down.
- Why it matters: this mapping is the bridge between the theory and the case study.
- Requested change: derive the expected intercept and slope from Eq. (info-decomp) under the stated reporting model, and carry the extra term through to Figure 2 and to the interpretation.

D7 [M3]. Location: Section 3.3 (results.tex lines 61–71); Figure 2.
- Problem: the loss is defined against one R̄ = 1.6706 pooled over three seasons, 51 states and 29 calendar weeks. Any systematic difference in mean growth between weeks, states or seasons therefore becomes "floor".
- Why it matters: a large part of the intercept is a common, predictable national component rather than state-level environmental variance.
- Requested change: decompose a into national-week, state-season and residual components with a hierarchical model, and report how much of the intercept each removes.
- Verification: the reviewer used the released derived panel (1,267 early-window state-weeks, about 45 states per week). Replacing the pooled R̄ by the cross-state mean growth of each week reduced the FGLS intercept from 0.0991 to 0.0464, a drop of 53% (state-clustered 95% interval 0.039–0.056). The slope changed little (2.243 to 1.927). The reproduction audit found that season, state and state-by-season means reduce a only to 0.0959, 0.0972 and 0.0910. The dominant common component is therefore weekly and national.

D8 [M3]. Location: Section 3.3 (results.tex line 63); Figure 2A–B; Section 3.2.
- Problem: "levels off at 0.103 and 0.105" rests on the two largest bins (N = 152 and 92). The power-law fit (p̂ = 0.273) is not distinguished from a plateau: the cross-validated deviance difference is 56.8 ± 27.2. The ratio b/a is fragile. It is 10.6 when the top 1% of losses are trimmed (these carry 19.5% of the total loss, and trimming gives a = 0.108 and b = 1.137). It is 16.0–46.4 when one season is left out, and 119.2 in the peak window.
- Why it matters: the balance scale is the paper's main applied number, and its empirical value is not stable.
- Requested change: pre-specify the plateau-versus-decay comparison, for example with a likelihood-ratio or cross-validation contrast and a stated minimum detectable difference. Report b/a as a range across these specifications, and drop the language that the plateau is established.

D9 [M4]. Location: Section 3.3 (results.tex line 71); Eq. (b-delta).
- Problem: the scenario slopes given in the text (0.610–0.707) are the naive A/R̄². Applying the manuscript's own Eq. (b-delta) with Σw² = 0.495 gives b = 1.11–1.21, and scenario values of b/a = 38.9–83.5. The empirical b/a = 22.6 is therefore below every corrected scenario. The statement that the ratio "aligns in magnitude" with m× = 21.3–49.2 compares against the uncorrected quantity, and the agreement arises because the errors in a and b cancel.
- Why it matters: this is the only quantitative link offered between the theory and the influenza data.
- Requested change: report the corrected prediction. State that a and b individually disagree with theory by factors of 3.5–6.9 and 1.9–2.0 (3.2–3.7 against the uncorrected slope), and restore the Chinese-version paragraph on the upward bias of b/a.
- Verification: closed-form evaluation over the grid v_R ∈ {0.04, 0.08}, k ∈ {0.2, 0.5}, ρ ∈ {0.0056, 0.021}, R̄ = 1.6706 (theory_checks.py, block empirical_scenarios).

D10 [M5]. Location: Section 6.6 (methods.tex line 72); all bootstrap intervals in Sections 3.3–3.6.
- Problem: the bootstrap resamples 51 states and so assumes independence across states. Growth deviations share a strong week component.
- Why it matters: the confidence intervals, the "100% of bootstrap replicates" statements and the TOST decisions all inherit the understated uncertainty.
- Requested change: use two-way clustering by state and by week [15], or a block bootstrap over weeks within season. Recompute every interval and the TOST.
- Verification: in the released panel the week-level intra-class correlation is 0.29. With 1,000 replicates, the state-clustered bootstrap gave SD(a) = 0.0084 (95% 0.084–0.116), and the week-clustered bootstrap gave SD(a) = 0.0171 (95% 0.065–0.131). This intra-class correlation also offers an empirical anchor for the c̄ ≈ 0.34 that Section 3.6 asserts without derivation.

D11 [M5, m14]. Location: Abstract; Section 3.3; Section 3.4 (results.tex line 79).
- Problem: two different intervals are reported for a (0.0837–0.1165 percentile and 0.0819–0.1144 BCa in one place; 0.0820–0.1146 in another), and interval types are not labelled consistently. "100% satisfied q1 < 1 < q2" is reported where the bootstrap share across pathogen-window combinations is 98.6–100%.
- Requested change: report one interval type throughout, labelled, with the seed and the number of replicates. Report the exact bootstrap shares.

D12 [M6]. Location: Section 3.4 (results.tex lines 77–79); Section 6.7 (methods.tex line 81).
- Problem: the adjustment uses the share of hospitals reporting, p̂_{s,t}. This proxy measures facility participation. It does not measure the probability that an infection becomes a recorded admission, which also depends on testing and coding. Under mandatory reporting, p̂ is nearly constant, so V_π is small by construction.
- Why it matters: the conclusion that reporting explains less than 1% of the intercept is a statement about this proxy, not about reporting heterogeneity.
- Requested change: rephrase the conclusion as a statement about facility completeness. If possible, add an ascertainment-sensitive proxy, such as test positivity or the number of tests from the same NHSN or NREVSS series, as a second check.

D13 [M6]. Location: Section 3.4; Table S4; prereg r3.
- Problem: the equivalence margin ±0.0050 equals 5% of the estimated a, and it was fixed after a was observed. Because the margin is proportional to a, the larger intercept in 2025–26 (a = 0.177) widens it to 0.0088. That season's Δa interval, 0.0020 to 0.0060, excludes zero and is still declared equivalent. Power is at most 2.5% for κ ≤ 1.
- Why it matters: an equivalence test with a data-dependent margin and low power cannot support a claim of negligibility [17].
- Requested change: fix the margin on substantive grounds before analysis, for example as a fraction of the theoretical slope contribution at the median D. Report the power at that margin, and report the excess under v_R = 0.04 and 0.16 as well as 0.08.
- Verification: with a = 0.0991, the excess is 0.0848, 0.0704 and 0.0418 for v_R = 0.04, 0.08 and 0.16. The v_R implied by a is 0.277, which is 3.5 times the benchmark.

D14 [M7]. Location: Section 3.4 (results.tex line 81); Table S8; Section 6.7.
- Problem: the r3 and r4 "pre-registrations" were written after the main estimates existed. The r3 to r4 change in the grading rule is not disclosed, and it moved influenza from "replicated" to "partial". The five grading variants in Table S8 produce the outcome vectors 0/4/3, 2/2/3, 4/1/2, 1/3/3 and 1/3/3.
- Why it matters: calling post hoc plans "pre-specified" overstates the confirmatory value of the replication.
- Requested change: call these analysis-plan amendments and give their dates. Show all grading variants in the main text, or choose one on stated a priori grounds. Control the family-wise error or false discovery rate over the pathogen × window × criterion family.

D15 [M7]. Location: Section 3.4 (results.tex line 81); Section 3.6 (results.tex line 145).
- Problem: "Independent outpatient ILINet surveillance (N = 1,479) and hospital FluSurv-NET (N = 364) corroborate the directional signature." For FluSurv-NET, q1 = 0.686 (−3.61 to 3.92) and q2 = 1.312 (−4.38 to 7.22), the directional share is 0.560, and only 14 sites are included. This is not corroboration. ILINet is a different system (outpatient ILI), but its lower BCa bound for one ratio is −29.3. FluSight forecasts are scored against the NHSN series, so their error is not an independent measurement of the floor. The European COVID-19 comparison (b/a = 124.7) uses a different pathogen, unit and reporting system.
- Requested change: report FluSurv-NET as uninformative. Present ILINet as a partially independent check with its intervals. Move FluSight and the European comparison to the supplement as descriptive context.

D16 [M8]. Location: Data and code availability (endmatter.tex); repository README.
- Problem: the reproduction audit found the following:
  - the raw NHSN snapshot CSV, empirical_stats.json, sim_theory.json and the theory and simulation code are missing, and the only plotting script in the package (r4_f_fig09.py) corresponds to an old figure number;
  - four scripts raise FileNotFoundError;
  - common.py hard-codes a relative path four directories up;
  - the README says the AR(1) simulation needs 200 replicates where 400 are used;
  - the README counts "23 scripts" where there are 21 entry points and 4 libraries;
  - the 24,815-comparison check compares the package with its own outputs;
  - reproduction_map.json predates round r4.
- Why it matters: Epidemics requires that results can be regenerated, and the availability statement is currently inaccurate.
- Requested change: deposit the dated raw snapshot (data.cdc.gov dataset ua7e-t2fy), all code that produces the numbers and figures, and a single command that rebuilds them. Then correct the statement.
- Verification: the point estimates reproduce from the released derived panel and from the 20 October 2026 data vintage. A re-seeded BCa interval for a is 0.0824–0.1138.

D17 [M8]. Location: endmatter of the English version.
- Problem: the Chinese version carries a generative-AI use declaration and a Zenodo DOI. The English version carries neither.
- Requested change: add both, following Elsevier's policy on generative AI in writing [18].

D18 [M9]. Location: whole manuscript; Figures 1–5.
- Problem: the main text runs to 36 pages and about 7,700 words, with seven propositions and two corollaries. The benchmark Epidemics article [8] has about 5,700 words, six figures and no tables. The eight English figure files are identical to the Chinese ones and carry Chinese labels; the figure builder (paper_zh/scripts/build_main_figures.py) hard-codes a Windows SimSun font path. Floats are stacked on pages 21–24, and page numbers overprint captions on pages 12, 21, 23 and 24.
- Requested change: move Propositions 5–7 and Corollary 2 to the supplement. Keep two or three theoretical results in the main text. Regenerate every English figure with English labels. Place figures near their first citation.

D19 [M9]. Location: figure captions.
- Problem: several captions contradict their figures:
  - the Figure 2B caption says the fit line is dashed, but it is solid;
  - the Figure 2D caption describes a grey band, but the band is teal;
  - the Figure 3B caption gives the ±0.0050 margin, but the band drawn is ±0.0013 on an axis that spans only ±0.002;
  - the Figure 4D caption calls m0* = 72.9 dashed, but it is drawn solid;
  - Figure 1A refers to a "bottom row" that does not exist;
  - the Figure 5A bar is clipped;
  - some panels carry double panel labels.
- Requested change: correct each caption or figure, and follow the benchmark style. That means panels lettered A–D at the upper left, captions of 80–150 words that describe content without restating results, and a consistent palette.

D20 [M9]. Location: supplement.
- Problem: there are 19 unresolved references ("??"). The proof titles are misnumbered: the proofs of main-text Propositions 4 and 5 are titled Propositions 5 and 6. Proposition 6 (levers) has no proof. References to S1.11 and S1.12 point to the wrong subsections. Table S1 overflows the page, and Table S8 is scaled too small to read in print.
- Requested change: compile the supplement together with the main text, using the xr package so that cross-references resolve. Renumber the proofs, and add the proof of the levers decomposition.

D21 [m1]. Location: Proposition 5(ii) (results.tex line 99); Supplementary Proposition S(b), Eq. (r3-IR).
- Problem: the constant 0.505 equals ξ[ξψ′(ξ) − 1] at ξ = R̄²/v_R = 33.06, that is, at the baseline parameters. It is a property of those parameters, not a universal constant. The constant is 0.645 at ξ = 1, 0.533 at ξ = 5 and 0.502 at ξ = 100, and its limit 0.5 recovers the Gaussian √(2/T).
- Requested change: state the bound as [T ξ(ξψ′(ξ) − 1)]^{-1/2} and give the baseline value as an example.
- Verification: trigamma evaluation with scipy; the stated values 0.81, 0.45 and 0.20 for T = 3, 10 and 50 are reproduced.

D22 [m2, m3]. Location: Section 3.5 (results.tex line 113); Section 3.6 (results.tex line 139); Limitations (discussion.tex line 14).
- Problem: Section 3.5 and the Limitations give lower bounds of 0.82 and 0.71 for S = 3 and 4, which are √(2/S). Section 3.6 invokes "the √(2/(S−1)) precision bound for S = 3", which equals 1.00. In addition, the between-season variance 0.0041 is the S = 4 estimate (including 2025–26), whereas the interval −0.056 to 0.211 is from the S = 3 random-effects fit. That interval is for the pooled mean intercept a_RE = 0.077, not for the variance; the S = 3 variance estimate is 0.0028.
- Requested change: use one version of the bound, the S − 1 version because the mean is estimated. Report the variance with its own interval, for example a profile-likelihood or Q-profile interval, and keep S = 3 and S = 4 results separate.

D23 [m4]. Location: Proposition 7 (results.tex line 130); proof (supp_proofs.tex line 170).
- Problem: e(T) and g_T are not defined in the main text, and the proof is a sketch. Reconstructing g_T = −T² e′(T) from the AR(1) variance gives T† = 4.48 for φ = 0.8, independent of c0/c1 and m×. Then B† = T†(c0 + c1 m0*), which is 775.0 only at m× = 53.08, in units of c1. Over the empirical range m× = 21.3–49.2, B† = 655–763.
- Requested change: define e(T) and g_T. State the units and the parameter dependence. Present B† as a formula, followed by the example.
- Verification: root-finding in theory_checks.py, block prop7. The closed-form AR(1) sum in the proof of Proposition 4 was confirmed: 31.3886 both directly and in closed form for φ = 0.8, T = 7.

D24 [m5]. Location: Section 3.5 (results.tex line 126); Discussion (discussion.tex line 10).
- Problem: the reporting term recomputes to 7.88 × 10⁻³, not 7.85, from Eq. (r3-levers) with ψφ = 0.25 in the cross term. The total is 22.57. The "72% against 17%" contrast compares a design using 2,000 cases with one using 5,000 cases. It also assumes that R̄ is constant over 40 weeks, which is longer than an influenza season.
- Requested change: correct the value. Add a budget-matched comparison. State the stationarity assumption, or restrict T to within one season.

D25 [m6]. Location: Section 3.1 (results.tex line 44).
- Problem: the Wald test sizes (7.81% at m = 5, k = 0.1; 10.40% peak at k = 1) and the "drops 82 times" count cannot be regenerated from the released code. A non-randomised test based on a discrete statistic is UMP only at its attainable sizes.
- Requested change: release the code. State that the test is UMP among tests at the attained size, or use a randomised or mid-p version.

D26 [m7]. Location: Discussion (discussion.tex line 8); Supplement S1.11.
- Problem: the shrinkage illustration uses the oracle weight δ* = 0.2787, computed from the true v_R, which gives an MSE of 0.00892.
- Requested change: show the feasible empirical-Bayes weight and its MSE, or label the example as an oracle bound.

D27 [m8]. Location: Figure 3A against Section 6.5 (methods.tex line 65); Section 3.6.
- Problem: the regime sample sizes are 6,001 and 416 in Figure 3A and 6,009 and 420 in the text. The value 0.107 is computed as mean(a + b/max(D, 250)), while 0.108 appears elsewhere. The value c̄ ≈ 0.34 is inferred from the ratio of national to state loss without a derivation.
- Requested change: reconcile the numbers. Derive c̄ from the pooling formula or estimate it directly, for example from the week-level intra-class correlation in D10 (0.29).

D28 [m9]. Location: Section 3.6 (results.tex lines 143–145).
- Problem: the voluntary-reporting period (May–October 2024) is compared with mandatory periods, but only 55 of its state-weeks fall in October, at season onset. Season and regime are therefore confounded. The instrumental-variable regression uses lagged D_{t−3} to D_{t−5}, which plausibly affect current growth variability through the epidemic phase, and the exclusion restriction is not argued. A first-stage F of 1147 shows relevance, not validity. "Confirming that endogeneity does not drive the scale effect" is too strong.
- Requested change: argue the exclusion restriction or present the instrumental-variable result as a consistency check. Compare the regimes within matched calendar weeks.

D29 [m10]. Location: Abstract (abstract.tex line 2); results.tex lines 55, 57, 81, 145; discussion.tex line 14; conclusion.tex line 4.
- Problem: the Abstract opens with "Estimation errors in the reproduction number are frequently attributed to sample size", which is not supported by a citation. The text uses "decisively rejects", "decisively favor", "confirming", "corroborate", "must" and "100%" where the evidence is weaker. The Chinese version uses "compatible" (相容) in the same places.
- Requested change: align the English wording with the evidence and with the Chinese version. Follow the hedged register of the benchmark, for example "would likely", and avoid "confirms".

D30 [m11]. Location: bibliography.bib.
- Problem: eleven entries are never cited: breto2009time, cameron2011robust, carroll2006measurement, fuller1987measurement, hamilton1994time, lehmann1998point, koenker1978regression, bartlett1946theoretical, zamir1998proof, searle1992variance and dersimonian1986meta. The first author of mathis2024evaluation is Sarabeth M. Mathis, not "Shannon M" [16]. Core references are missing: Wallinga and Lipsitch (2007) [3], Lande, Engen and Sæther (2003) [10], Nash et al. (2023) [12], and Ogi-Gittins et al. (2024, 2025) [13, 14]. The last three address weekly aggregation and under-reporting in R_t estimation, which is exactly the setting of the case study. DerSimonian and Laird (1986) is in the bibliography but not cited, although a random-effects analysis is reported.
- Verification: a spot-check of seven entries by web search confirmed the authors, venue, year and DOI for Parag et al. 2022 (both papers), Parag et al. 2025, Steyn et al. 2025, Eales and Riley 2024, Engen et al. 1998 and Mathis et al. 2024 (forename wrong). For Parag et al. (2022, Nature Computational Science) the cited claim was also checked against the full text. Uncited entries were identified by matching every bibliography key against the citation commands in the source files.

D31 [m12]. Location: Section 6.5 (methods.tex lines 58–63).
- Problem: the weights (0.65, 0.25, 0.10) have no stated derivation. The 504 missing state-weeks are set to zero, and the paper does not say whether any enter the analysis window.
- Requested change: justify the weights, for example by deriving them from an influenza generation interval convolved with an admission delay, and report sensitivity to them. State explicitly that no imputed zeros enter the early window.
- Verification: the reviewer confirmed that none of the 1,267 early-window rows in the released panel is flagged as missing and none has G = 0. The zero imputation therefore does not affect the primary estimate.

D32 [m13]. Location: English against Chinese versions.
- Problem: the English version omits the following material that the Chinese version contains:
  - the influenza growth-window exception for q2 (BCa 1.686–2.261, above the null 1.578);
  - the grading-sensitivity table;
  - the paragraph on the upward bias of b/a;
  - three limitations (independence assumption H5, the instrumental-variable exclusion restriction, and the 504 zeros).

  It also describes the Δa power simulation in the opposite sense. The two Abstracts differ.
- Requested change: synchronise the versions, with English as the version of record, and keep a change log.

D33 [M2, M9]. Location: Introduction (introduction.tex line 12); Discussion (discussion.tex line 6); overall design. Comparison with the benchmark [8].
- Problem: Eales and Riley define the apparent reproduction number of a downstream series and show how convolution with delay distributions distorts and lags it. NHSN admissions are such a series, so the case-study G is an apparent growth quantity. The manuscript calls the two issues "conceptually distinct" when they interact. Delay convolution smooths week-to-week variation, which lowers the apparent v_R. Admission-delay heterogeneity across states adds variance.
- Requested change: discuss this interaction, ideally with a simulation in which R_t, the generation interval and the admission delay are known. Show how a and b of the apparent series relate to v_R and A.
- Presentation: for reference, the benchmark orders sections as Introduction, Background, Results, Discussion, Conclusion and Methods. Its Abstract is a single paragraph of about 280 words with no numbers. It has six figures and no tables, and its captions describe content rather than results. The manuscript already uses the same section order. Its main departures are length, the density of propositions, numerical results in the Abstract, and captions that restate numbers.

### 5 Overall recommendation

Recommendation: Major revision.

Score: 4 out of 10.

Rationale. The theoretical part is correct and clearly derived. Its novelty, however, is limited: the decomposition is the classical split of environmental and demographic variance, the allocation result is Neyman–Cochran, and the reporting result overlaps with Parag et al. (2022). The manuscript is not yet positioned honestly against this work (M1).

The empirical part is reproducible at the level of point estimates, but its interpretation is not supported. The statistic analysed is a weekly growth factor of a downstream series, not a reproduction-number estimate (M2). About half of the intercept is a nationally synchronous weekly component (M3). The headline agreement between b/a and m× is with the uncorrected prediction (M4). The confidence intervals are about half as wide as a week-clustered bootstrap gives (M5). The reporting-heterogeneity, replication and pre-registration claims rest on a narrow proxy, a post hoc margin and plans written after the results (M6, M7). The package does not yet regenerate the figures (M8). The presentation would need substantial work before an Epidemics referee could assess it efficiently (M9).

None of these problems is necessarily fatal. A re-framed paper could be publishable if it:

- presents the theory as a surveillance-design translation of known variance decompositions;
- estimates R_t properly or re-labels the empirical target;
- uses two-way clustered inference and a hierarchical decomposition of the intercept;
- reports the empirical balance scale as an uncertain range.

These changes amount to a substantial revision rather than a polish, hence the score of 4.

Reviewer confidence: high (4 out of 5) for the mathematical, statistical and reproducibility assessments, which were checked numerically. Moderate (3 out of 5) for the epidemiological interpretation of NHSN facility-completeness data, which the reviewer could not validate against external ascertainment data.

### References

[1] Cori A, Ferguson NM, Fraser C, Cauchemez S. A new framework and software to estimate time-varying reproduction numbers during epidemics. American Journal of Epidemiology 2013;178:1505–1512. https://doi.org/10.1093/aje/kwt133

[2] Fraser C. Estimating individual and household reproduction numbers in an emerging epidemic. PLOS ONE 2007;2:e758. https://doi.org/10.1371/journal.pone.0000758

[3] Wallinga J, Lipsitch M. How generation intervals shape the relationship between growth rates and reproductive numbers. Proceedings of the Royal Society B 2007;274:599–604. https://doi.org/10.1098/rspb.2006.3754

[4] Gostic KM, McGough L, Baskerville EB, et al. Practical considerations for measuring the effective reproductive number, Rt. PLOS Computational Biology 2020;16:e1008409. https://doi.org/10.1371/journal.pcbi.1008409

[5] Parag KV, Donnelly CA, Zarebski AE. Quantifying the information in noisy epidemic curves. Nature Computational Science 2022;2:584–594. https://doi.org/10.1038/s43588-022-00313-1

[6] Parag KV, Donnelly CA. Fundamental limits on inferring epidemic resurgence in real time using effective reproduction numbers. PLOS Computational Biology 2022;18:e1010004. https://doi.org/10.1371/journal.pcbi.1010004

[7] Parag KV, et al. Asymmetric limits on timely interventions from noisy epidemic data. Communications Physics 2025;8:450. https://doi.org/10.1038/s42005-025-02358-w

[8] Eales O, Riley S. Differences between the true reproduction number and the apparent reproduction number of an epidemic time series. Epidemics 2024;46:100742. https://doi.org/10.1016/j.epidem.2024.100742

[9] Engen S, Bakke Ø, Islam A. Demographic and environmental stochasticity: concepts and definitions. Biometrics 1998;54:840–846. https://doi.org/10.2307/2533838

[10] Lande R, Engen S, Sæther B-E. Stochastic Population Dynamics in Ecology and Conservation. Oxford University Press; 2003.

[11] Sæther B-E, Engen S. Pattern of variation in avian population growth rates. Philosophical Transactions of the Royal Society B 2002;357:1185–1195. https://doi.org/10.1098/rstb.2002.1119

[12] Nash RK, Bhatt S, Cori A, Nouvellet P. Estimating the epidemic reproduction number from temporally aggregated incidence data: a statistical modelling approach and software tool. PLOS Computational Biology 2023;19:e1011439. https://doi.org/10.1371/journal.pcbi.1011439

[13] Ogi-Gittins I, et al. A simulation-based approach for estimating the time-dependent reproduction number from temporally aggregated disease incidence time series data. Epidemics 2024;47:100773. https://doi.org/10.1016/j.epidem.2024.100773

[14] Ogi-Gittins I, et al. Simulation-based inference of the time-dependent reproduction number from temporally aggregated and under-reported disease incidence time series data. Philosophical Transactions of the Royal Society A 2025;383:20240412. https://doi.org/10.1098/rsta.2024.0412

[15] Cameron AC, Gelbach JB, Miller DL. Robust inference with multiway clustering. Journal of Business and Economic Statistics 2011;29:238–249. https://doi.org/10.1198/jbes.2010.07136

[16] Mathis SM, Webber AE, León TM, et al. Evaluation of FluSight influenza forecasting in the 2021–22 and 2022–23 seasons with a new target laboratory-confirmed influenza hospitalizations. Nature Communications 2024;15:6289. https://doi.org/10.1038/s41467-024-50601-9

[17] Lakens D. Equivalence tests: a practical primer for t tests, correlations, and meta-analyses. Social Psychological and Personality Science 2017;8:355–362. https://doi.org/10.1177/1948550617697177

[18] Elsevier. The use of generative AI and AI-assisted technologies in writing for Elsevier. https://www.elsevier.com/about/policies-and-standards/the-use-of-generative-ai-and-ai-assisted-technologies-in-writing-for-elsevier

## Part B — 中文

### 1 简要概述

稿件研究的问题是：观测病例数增加之后，再生数估计的精度能提高多少。作者区分两个推断目标，即当期传播潜力 R_t（目标 1）和跨期平均传播潜力 R̄（目标 2）。在带二项报告的负二项分支过程下，作者推导出单期 R̄ 估计量的均方误差 V(m) = v_R + A/m。其中 v_R 为 R_t 的跨期方差（稿件称为环境方差），A = R̄ + ρ(R̄² + v_R)/k，m = ρn 为期望报告病例数，比值 m× = A/v_R 称为方差平衡尺度。其余命题包括：

- 乘性报告异质性带来附加分量 v_H，并降低平衡尺度（命题 3）；
- 观测期数与单期病例量之间的预算分配，最优单期量 m* = √((c0/c1)m×)（命题 4）；
- 估计 v_R 与季间方差的 Fisher 信息界（命题 5 与推论 2）；
- 设计杠杆分解（命题 6）；
- AR(1) 环境下的预算阈值 B†（命题 7）。

实证部分使用 NHSN 对美国 50 个州及华盛顿特区的每周流感住院数据。在 1,267 个早期扩张州周中，作者把周增长比 G = C_{t+1}/D_t 的相对平方误差对 1/D_t 回归，得到截距 a = 0.0991、斜率 b = 2.243（b/a = 22.6），并将二者解读为 v_R/R̄² 与 m× 的经验对应量。实证部分还包括：

- 不同分母加权下的截距比诊断（q1 = 0.688，q2 = 1.539）；
- 报告完整度调整，以 ±0.0050 为界的 TOST 判定 Δa = −0.0004 与零等价；
- 对 COVID-19 和 RSV 的跨病原分级；
- 季别与阶段分析；
- 与 ILINet、FluSurv-NET、FluSight 预测以及欧洲 COVID-19 数据的比较。

稿件的实践结论为：单期病例量达到 m× 之后，资源应投向更多观测期、空间汇总与标准化报告，继续增加单期病例量的收益有限。

### 2 优点

S1. 研究问题与 Epidemics 读者相关。监测项目常按病例数确定系统规模。区分检测当期变化（目标 1）与估计稳定均值（目标 2），对监测设计有实际用处。

S2. 核心代数正确。审稿人在基线参数（R̄ = 1.15，v_R = 0.04，k = 0.35，ρ = 0.25）下复现了以下结果：

- A = 2.1232、m× = 53.08；
- 倍增收益公式 1/[2(1 + m/m×)]；
- τ = 0.15 时的 v_H = 0.03066、A_H = 2.1451、m×,H = 30.36。

Gamma–负二项–二项分层模拟在所有测试设计点上与 V(n, ρ) 的差异都在蒙特卡罗误差之内，例如 n = 40、ρ = 0.25 时模拟值 0.2529，解析值 0.2523。

S3. 设计结果内部一致，具有潜在用处。审稿人复现了以下结果：

- 杠杆分解：基线、单期量放大十倍、期数放大四倍、τ = 0 四种情形分别为 22.57、18.71、6.17、14.65（× 10⁻³）；
- 基线 m× 下的预算阈值 B† = 775（T† = 4.48，m0* = 72.86）；
- 最优单期量区间 m* ∈ [14.6, 22.2] 与 [46.1, 70.1]。

S4. 实证点估计可复现。复现审计用三条路径得到 a = 0.0991、b = 2.243、b/a = 22.6 与 N = 1,267：存档输出、独立重写的计算，以及 2026 年 10 月 20 日重新下载的 NHSN 数据版本。

S5. 稿件报告了大量稳健性检验。摘要与局限部分承认两项核心识别限制：平台与缓慢衰减无法区分，截距也无法唯一归因于环境方差。这种坦率值得肯定。问题在于标题、结果与结论部分没有按这两项让步调整措辞（见 M3 与 m10）。

S6. 监测场景选得好。2024 年 NHSN 在强制报告与自愿报告之间的切换，为报告完整度提供了少见的自然变异。

### 3 缺点

#### 主要问题

M1. 相对已有理论，稿件高估了自身贡献。

- 对 R_t 条件无偏的估计量应用全方差公式，即得 V(m) = v_R + A/m。所谓下限 v_R 由两项选择决定：目标取 R̄，估计量类取单期、对 R_t 条件无偏。
- 种群生态学中环境随机性与人口随机性的经典分解与此相同：增长率方差约为 σ_e² + σ_d²/N，临界规模 σ_d²/σ_e² 的作用对应 m× [9, 10, 11]。稿件引用 Engen 等（1998）时只把它当作术语类比。
- 命题 3 与 Parag 等（2022）重叠。该文已证明，随时间变化的报告比例通过其几何均值降低关于 R_t 的信息 [5]。
- 作者本人也指出，命题 4 即 Neyman–Cochran 分配。

此外，V 取决于 (n, ρ)，单凭 m 不能确定。n 固定而只提高检出率 ρ 时，误差不会低于 v_R + (R̄² + v_R)/(kn)，这会改变设计解读。

M2. 实证统计量与再生数估计之间存在概念差距。G = C_{t+1}/D_t 使用周权重 (0.65, 0.25, 0.10)，平均回看 10.2 天（6.5 节，式 dt）。这组权重与流感的代际间隔分布没有对应关系。G 因此是经延迟卷积的下游序列的周增长因子，属于 Eales 与 Riley 意义上的表观量 [8]，与 Cori 等、Fraser 以及 Wallinga 与 Lipsitch 意义上的 R_t 有别 [1, 2, 3]。局限段承认每周住院约跨两代，但标题和摘要仍把结论表述为对再生数估计的限制。稿件也未引用 Wallinga 与 Lipsitch（2007）。

M3. 截距未被识别为环境方差，平台也未与缓慢衰减区分开。

- 稿件自己的式（info-decomp）多出一项感染压力不确定性分量。
- 损失以合并三季、51 个州得到的单一 R̄ 为基准，而所选早期扩张窗本身带有系统性增长趋势。审稿人发现截距的 53% 来自全国同步的周分量：加入周固定效应后，a 由 0.0991 降为 0.0464。
- "趋于平稳"的判断只依靠最大的两个分箱（N = 152 与 92）。幂律指数 p̂ = 0.273 与平台无法区分。
- b/a 在不同设定下差异很大：剔除损失最大的 1% 为 10.6，留一季为 16.0–46.4，高峰阶段为 119.2。

M4. 理论与数据的比较把比值与错误的量相比。两个参数各自都与理论不符：a 是情景值的 3.5–6.9 倍，b 是 3.2–3.7 倍。按稿件自己的分母噪声修正（式 b-delta），b/a 的情景值为 38.9–83.5，原稿给出的 21.3–49.2 没有经过这一修正。实证值 22.6 因此低于修正后的预测，不在区间之内。中文稿报告了这一方向（b/a 高估 m×；模拟中 59.2 对真实 A/v_R = 30.7），英文稿删去了这段。

M5. 置信区间忽略了同一周内各州之间的相关。按 51 个州重抽样相当于假定州间独立，而研究对象恰是期内共享的冲击。在公开面板中：

- 增长偏差的周层面组内相关系数为 0.29；
- 按周聚类的 bootstrap 给出 a 的标准差 0.0171，是按州聚类（0.0084）的两倍；
- 按周聚类的 95% 区间为 [0.065, 0.131]，按州聚类为 [0.084, 0.116]。

参考文献表列有 Cameron、Gelbach 与 Miller（2011）的多维聚类方法，正文未引用也未使用。

M6. 报告异质性结论依赖代理变量、事后设定的界限和外部基准。

- 设施填报完整度衡量的是参与率，与病例检出率不同。
- TOST 界限 ±0.0050 等于实现值 a 的 5%，在 a 已知之后确定。
- 流感 2025–26 季的 Δa 可检测地偏离零（90% BCa 0.0020 至 0.0060），但因 a = 0.177 使界限放宽到 0.0088，仍被判为等价。
- "低于超额部分的 1%"依赖外生基准 v_R = 0.08。
- κ ≤ 1 时 Δa 检验的功效不超过 2.5%（表 S4）。

M7. 分析计划不属于通常意义上的预注册，也没有多重比较控制。

- 称作"预注册"的文件（r3 与 r4 轮，日期为 2026 年 10 月 17 日与 18 日）写于主要结果产出之后。
- 两轮之间的分级规则有改动且未披露，改动使流感由"复现"降为"部分复现"。五种分级变体给出五组不同结果（表 S8）。
- 三种病原、两类窗口与多项判据同时检验，未作校正。
- FluSurv-NET 的 q 区间跨越零（q1 为 −3.61 至 3.92），正文却称其印证了方向特征。
- FluSight 预测以同一 NHSN 序列为目标，不构成独立核验。

M8. 复现包不完整。原始 NHSN 快照、两个中间结果文件以及理论与模拟代码缺失。包内没有图 1–5 的作图脚本，作图程序只出现在中文稿目录下。四个脚本报 FileNotFoundError，路径为硬编码。数据与代码可得性声明仍称包是完整的。英文稿还缺少中文稿已有的生成式 AI 使用声明和 Zenodo DOI。

M9. 呈现方式妨碍高效评审。正文 36 页、约 7,700 词，含七个命题与两个推论。存在以下问题：

- 英文稿全部图件使用中文坐标标签；
- 补充材料有 19 处未解析的交叉引用（"??"）；
- 证明标题编号错位；
- 多处图注与面板内容矛盾；
- 第 12、21、23、24 页的页码压在图注上。

#### 次要问题

- m1. 命题 5(ii) 的界 (0.505T)^{-1/2} 只在一组参数（ξ = R̄²/v_R = 33.06）下成立，不能作为通用常数。
- m2. 推论 2 的用法前后不一：3.5 节取 √(2/S)，3.6 节取 √(2/(S−1))。
- m3. 3.6 节的区间 −0.056 至 0.211 属于合并随机效应均值，与季间方差无关。该区间来自 S = 3 拟合，却配在 S = 4 的点估计后面。
- m4. 命题 7 在正文中没有定义 e(T) 与 g_T，没有说明 B† 以 c1 为单位，也没有说明 B† 随 m× 变化。
- m5. 杠杆分解中报告项写作 7.85，复算为 7.88。"72% 对 17%"的比较混用了不同预算（2,000 例对 5,000 例），并假定 R̄ 在 40 周内平稳。
- m6. 3.1 节的 Wald 检验水平与功效数值无法用公开代码重现。基于离散统计量的非随机化检验在名义水平 α 下并不严格 UMP。
- m7. 收缩估计示例使用了理想权重（δ* = 0.2787）。
- m8. 正文与图件的计数和数值不一致：6,009/420 对 6,001/416，0.107 对 0.108。c̄ ≈ 0.34 没有推导。
- m9. 自愿报告期的对比与流行季起点混淆。工具变量的排除性约束没有论证。
- m10. 措辞过度："decisively""confirming""corroborate""must"，以及 bootstrap 比例实为 98.6%–100% 处写作"100%"。
- m11. 参考文献管理：十一条未引用条目，一位作者名字有误，缺少核心文献。
- m12. D_t 权重为人为设定。504 个以零填补的周如何处理，需要在方法部分写明。
- m13. 英文稿与中文稿多处不等价。
- m14. 区间类型（百分位、BCa、正态）混用且未标注，a 有两套不同的区间。

### 4 详细意见

每条意见依次给出位置、问题、影响、修改要求，并在可核验时给出核验方法与结果。编号后的方括号对应上文的缺点条目。

D1 [M1]。位置：引言（introduction.tex 第 10 行）；2.1 节（background.tex 第 43 行）；讨论第一段（discussion.tex 第 4 行）。
- 问题：稿件把分解 v_R + A/m 作为新的极限提出，对生态学只作类比式提及。种群动态文献中增长率方差为 σ_e² + σ_d²/N，两项相等时的种群规模 σ_d²/σ_e² 是标准量 [9, 10, 11]。令 σ_d² 对应 A、σ_e² 对应 v_R，该量与 m× 是同一对象。
- 影响：Epidemics 审稿人会对照这类文献以及 Parag 等的工作 [5, 6, 7] 判断新颖性。
- 修改要求：明确写出这一形式等同。引用 Lande、Engen 与 Sæther（2003）以及 Sæther 与 Engen（2002），后两者已从数据估计 σ_d² 与 σ_e²。再把贡献表述为将已知分解迁移到监测设计，新增部分为报告异质性与预算分配。
- 核验：Engen 等（1998）的书目信息经核对无误，见 Biometrics 54:840–846，DOI 10.2307/2533838 [9]。

D2 [M1]。位置：2.3 节命题 3；引言（introduction.tex 第 8 行与第 14 行）。
- 问题：稿件引用 Parag 等（2022）只是为了说明 Fisher 信息随病例数线性增长。审稿人深读了该文。其式 5 已表明，含噪流行曲线中的信息受时变报告比例几何均值的调节，补充说明又把结论推广到负二项噪声 [5]。报告波动降低精度这一点因此不新。命题 3 的新意在于乘性报告冲击进入 R̄ 的下限。
- 影响：与最接近的已有工作的定位，是新颖性评判的主要依据。
- 修改要求：增加一段，将命题 3 与 [5] 的式 5 对照。对照从三方面展开：目标（R̄ 与 R_t），噪声模型（均值为一的乘性冲击与 Beta 分布的报告比例），结论形式（加性下限与信息比）。
- 核验：深读 [5] 的式 4–5 及 "Ranking noise sources by their information loss" 一节。

D3 [M1]。位置：命题 1(ii) 与命题 2（background.tex）；命题 2 的证明（supp_proofs.tex 第 60 行）。
- 问题：正文称误差"严格按 1/m"衰减，并以 m 作为设计杠杆。按模型推导，V(n, ρ) = v_R + R̄/(ρn) + (R̄² + v_R)/(kn)。证明本身给出 n 固定、ρ → 1 时的极限 v_R + R̄/n + (R̄² + v_R)/(kn)，严格大于 v_R。提高检出率不能消除人口随机项，只有更多祖代（即更多传播或更大人群）才能消除。
- 影响：监测项目能控制的是 ρ（检测与报告），控制不了 n。3.5 节与结论中的设计建议应以项目实际可控的杠杆表述。
- 修改要求：用 (n, ρ) 表述命题 1–2，并分别给出 ρ 方向与 n 方向的下限。
- 核验：n = 40 时以 200,000 次重复作蒙特卡罗，ρ = 0.25、0.5、1.0 对应 V = 0.2529、0.1949、0.1651；解析值为 0.2523、0.1948、0.1661，解析极限 0.1661 为 v_R = 0.04 的四倍。

D4 [M1]。位置：6.2 节（methods.tex 第 14–18 行）；讨论（discussion.tex 第 8 行）。
- 问题：稿件用"对 R_t 条件无偏"这一估计量类给 R̄ 的估计设定下界。必须跟踪 R_t 的估计量，离 R̄ 的距离不可能小于 R_t 本身，所以下限 v_R 由定义直接得出。任何多期估计量或收缩估计量都不属于这个类。讨论部分承认这一点，但摘要和结论把该下限表述为监测本身的性质。
- 影响：核心结论读起来像物理极限，实际是所选估计量类的极限。
- 修改要求：把估计量类的限定写进命题 2 的陈述和摘要。同时报告最直接的竞争者（命题 4 的 T 期均值）的均方误差。

D5 [M2]。位置：6.3 节（methods.tex 第 25–37 行）；6.5 节式（dt）；标题与摘要。
- 问题：权重 (0.65, 0.25, 0.10) 被称为三周回看，平均滞后 1.45 周（10.2 天）。流感代际间隔约 3 天，住院数据还叠加了感染到入院的延迟。G 估计的因此是下游序列的周乘性增长因子，量级约为 R^{7/T_g}，与 R_t 不同。增长率与 R 的关系取决于代际间隔分布 [3]，下游序列会使 R 失真并滞后 [8]。Gostic 等的实务建议 [4] 是用更新方程模型估计 R_t，并显式校正观测延迟。
- 影响：v_R 的尺度、R̄ = 1.67 的取值和平衡尺度都针对周增长因子而言，不能解读为 EpiEstim [1] 或 Fraser 方法 [2] 一类 R_t 估计量的性质。
- 修改要求：两种方案任选其一。(a) 用更新方程模型的 R_t 估计重做案例，例如 EpiEstim 加流感代际间隔、处理聚合数据的方法 [12, 13, 14] 以及入院延迟核。(b) 修改标题，把实证目标重新定义为"住院的周增长因子"，并把关于 R_t 的结论限于理论部分。审稿人建议采用 (a)。

D6 [M3]。位置：6.3 节式（info-decomp）及第 30 行；式（affine）。
- 问题：式（info-decomp）多出一项 CV²(Λ_{t+1} | F_t)(R̄² + v_R)，正文称其与尺度无关。若这一描述成立，该项进入截距，式（affine）中的 a = v_R/R̄² 就不成立。若不成立（二项稀释下潜在压力的 CV² 约为 (1 − ρ)/C，按 1/m 变化），该项进入斜率，则 b ≠ A/R̄²。两种情形下，a ↔ v_R、b ↔ A 的对应都不能从稿件写出的模型推出。
- 影响：这一对应关系是理论与案例之间的桥梁。
- 修改要求：在给定报告模型下由式（info-decomp）推导截距与斜率的期望值，并把多出的这一项贯彻到图 2 和结果解读中。

D7 [M3]。位置：3.3 节（results.tex 第 61–71 行）；图 2。
- 问题：损失以单一 R̄ = 1.6706 为基准，该值合并了三季、51 个州与 29 个日历周。各周、各州或各季之间平均增长的系统差异，因此都被计入"下限"。
- 影响：截距的很大部分是全国共有、可预测的分量，州层面的环境方差只占其余部分。
- 修改要求：用分层模型把 a 分解为全国周分量、州-季分量和残差分量，并报告每一层各去掉多少截距。
- 核验：审稿人使用公开派生面板（1,267 个早期窗州周，每周约 45 个州），把合并的 R̄ 换成每周的跨州平均增长后，FGLS 截距由 0.0991 降至 0.0464，降幅 53%（按州聚类 95% 区间 0.039–0.056）。斜率变化不大，由 2.243 变为 1.927。复现审计发现，以季、州、州×季均值为基准时，a 只降至 0.0959、0.0972、0.0910。占主导的共同分量因此是全国性的周分量。

D8 [M3]。位置：3.3 节（results.tex 第 63 行）；图 2A–B；3.2 节。
- 问题："levels off at 0.103 and 0.105"只依靠最大的两个分箱（N = 152 与 92）。幂律拟合（p̂ = 0.273）与平台无法区分，交叉验证偏差差值为 56.8 ± 27.2。b/a 很不稳定：
  - 剔除损失最大的 1% 时为 10.6。这部分观测占总损失的 19.5%，剔除后 a = 0.108、b = 1.137。
  - 留一季时为 16.0–46.4。
  - 高峰窗为 119.2。
- 影响：平衡尺度是稿件最主要的应用数字，其经验值并不稳定。
- 修改要求：事先设定平台与衰减的比较方法，例如似然比或交叉验证对比，并给出最小可检测差异。把 b/a 报告为跨这些设定的区间，删去平台已经成立的表述。

D9 [M4]。位置：3.3 节（results.tex 第 71 行）；式（b-delta）。
- 问题：正文给出的情景斜率 0.610–0.707 是未修正的 A/R̄²。代入稿件自己的式（b-delta），取 Σw² = 0.495，得 b = 1.11–1.21，b/a 的情景值为 38.9–83.5。实证 b/a = 22.6 因此低于所有修正后的情景值。正文说该比值与 m× = 21.3–49.2 "aligns in magnitude"，比较对象是未修正的量，而吻合来自 a 与 b 两处误差相互抵消。
- 影响：这是稿件在理论与流感数据之间给出的唯一定量联系。
- 修改要求：报告修正后的预测。说明 a 与 b 各自偏离理论 3.5–6.9 倍和 1.9–2.0 倍（相对未修正斜率为 3.2–3.7 倍），并恢复中文稿中关于 b/a 向上偏倚的段落。
- 核验：在 v_R ∈ {0.04, 0.08}、k ∈ {0.2, 0.5}、ρ ∈ {0.0056, 0.021}、R̄ = 1.6706 的网格上作闭式计算（theory_checks.py 的 empirical_scenarios 部分）。

D10 [M5]。位置：6.6 节（methods.tex 第 72 行）；3.3–3.6 节的全部 bootstrap 区间。
- 问题：bootstrap 对 51 个州重抽样，隐含州间独立的假设，而增长偏差含有很强的周分量。
- 影响：置信区间、"100% of bootstrap replicates"的说法以及 TOST 判定都沿用了被低估的不确定性。
- 修改要求：按州与周双向聚类 [15]，或在季内按周作块 bootstrap，并重算全部区间与 TOST。
- 核验：公开面板中周层面组内相关系数为 0.29。各作 1,000 次重复：按州聚类 SD(a) = 0.0084（95% 区间 0.084–0.116），按周聚类 SD(a) = 0.0171（95% 区间 0.065–0.131）。这一组内相关系数也为 3.6 节未经推导给出的 c̄ ≈ 0.34 提供了经验参照。

D11 [M5, m14]。位置：摘要；3.3 节；3.4 节（results.tex 第 79 行）。
- 问题：a 有两套区间，一处为百分位 0.0837–0.1165 与 BCa 0.0819–0.1144，另一处为 0.0820–0.1146，区间类型的标注也不统一。在病原-窗口组合上，bootstrap 中满足 q1 小于 1 小于 q2 的比例为 98.6%–100%，正文写作"100%"。
- 修改要求：全文使用一种区间并注明类型、种子和重复次数，报告 bootstrap 比例的确切值。

D12 [M6]。位置：3.4 节（results.tex 第 77–79 行）；6.7 节（methods.tex 第 81 行）。
- 问题：调整使用填报医院比例 p̂_{s,t}。这一代理变量衡量设施参与程度，与感染成为住院记录的概率不同，后者还取决于检测与编码。强制报告期内 p̂ 几乎不变，V_π 因而按构造就很小。
- 影响："报告解释不到截距的 1%"只针对这一代理变量成立，不能推广到报告异质性本身。
- 修改要求：把结论改写为关于设施完整度的陈述。如有可能，增加对检出率敏感的代理变量作第二项核验，例如同一 NHSN 或 NREVSS 序列中的检测阳性率或检测数。

D13 [M6]。位置：3.4 节；表 S4；r3 轮计划。
- 问题：等价界 ±0.0050 等于 a 估计值的 5%，在观测到 a 之后确定。界限与 a 成比例，因此 2025–26 季较大的截距（a = 0.177）把界限放宽到 0.0088。该季 Δa 的区间 0.0020 至 0.0060 不含零，仍被判为等价。κ ≤ 1 时功效至多 2.5%。
- 影响：界限依赖数据、功效又低的等价检验，不能支持"可忽略"的结论 [17]。
- 修改要求：在分析前依据实质理由确定界限，例如取中位 D 处理论斜率贡献的某一比例。报告该界限下的功效，并同时报告 v_R = 0.04、0.08、0.16 三种基准下的超额部分。
- 核验：取 a = 0.0991 时，v_R = 0.04、0.08、0.16 对应的超额部分为 0.0848、0.0704、0.0418。由 a 反推的 v_R 为 0.277，是基准值的 3.5 倍。

D14 [M7]。位置：3.4 节（results.tex 第 81 行）；表 S8；6.7 节。
- 问题：r3 与 r4 轮"预注册"写于主要估计产出之后。两轮之间分级规则的改动没有披露，改动使流感由"复现"降为"部分复现"。表 S8 的五种分级变体给出 0/4/3、2/2/3、4/1/2、1/3/3、1/3/3 五组结果。
- 影响：把事后计划称为"预先设定"，夸大了复现部分的验证价值。
- 修改要求：将这些文件称为分析计划修订并注明日期。在正文展示全部分级变体，或依据事先说明的理由只取一种。对病原 × 窗口 × 判据这一检验族控制族错误率或错误发现率。

D15 [M7]。位置：3.4 节（results.tex 第 81 行）；3.6 节（results.tex 第 145 行）。
- 问题：正文写道 "Independent outpatient ILINet surveillance (N = 1,479) and hospital FluSurv-NET (N = 364) corroborate the directional signature"。四个数据源的情况如下：
  - FluSurv-NET 的 q1 = 0.686（−3.61 至 3.92），q2 = 1.312（−4.38 至 7.22），方向一致比例 0.560，且只含 14 个站点，不构成印证。
  - ILINet 属于另一套系统（门诊 ILI），但其中一个比值的 BCa 下限为 −29.3。
  - FluSight 预测以 NHSN 序列为评分对象，其误差不能作为对下限的独立测量。
  - 欧洲 COVID-19 的比较（b/a = 124.7）病原、单位和报告体系都不同。
- 修改要求：把 FluSurv-NET 报告为信息不足。ILINet 作为部分独立的核验并附区间。FluSight 与欧洲比较移入补充材料，作为描述性背景。

D16 [M8]。位置：数据与代码可得性声明（endmatter.tex）；仓库 README。
- 问题：复现审计发现以下问题：
  - 原始 NHSN 快照 CSV、empirical_stats.json、sim_theory.json 以及理论与模拟代码缺失，包内唯一的作图脚本（r4_f_fig09.py）对应旧的图号；
  - 四个脚本报 FileNotFoundError；
  - common.py 硬编码了向上四级目录的相对路径；
  - README 称 AR(1) 模拟需 200 次重复，实际为 400 次；
  - README 称"23 个脚本"，实际为 21 个入口脚本加 4 个库；
  - 24,815 项比较的核对是用包本身的输出对照自己；
  - reproduction_map.json 早于 r4 轮。
- 影响：Epidemics 要求结果可以重新生成，而现有可得性声明与实际不符。
- 修改要求：存放带日期的原始快照（data.cdc.gov 数据集 ua7e-t2fy）、生成全部数值与图件的代码，以及一条重建全部结果的命令，再据实修改声明。
- 核验：点估计可由公开派生面板和 2026 年 10 月 20 日的数据版本复现。换种子重抽得到的 a 的 BCa 区间为 0.0824–0.1138。

D17 [M8]。位置：英文稿末尾声明部分。
- 问题：中文稿有生成式 AI 使用声明和 Zenodo DOI，英文稿两者皆无。
- 修改要求：按 Elsevier 关于写作中使用生成式 AI 的政策补充这两项 [18]。

D18 [M9]。位置：全文；图 1–5。
- 问题：
  - 篇幅：正文 36 页、约 7,700 词，含七个命题与两个推论。作为基准的 Epidemics 论文 [8] 约 5,700 词，六幅图，无表。
  - 图件：英文稿八个图件文件与中文稿完全相同，带中文标签；作图程序（paper_zh/scripts/build_main_figures.py）硬编码了 Windows 下的 SimSun 字体路径。
  - 版面：第 21–24 页浮动体堆叠，第 12、21、23、24 页页码压在图注上。
- 修改要求：将命题 5–7 与推论 2 移入补充材料，正文保留两到三项理论结果。用英文标签重新生成全部英文图件，并把图放在首次引用处附近。

D19 [M9]。位置：图注。
- 问题：多处图注与图件矛盾：
  - 图 2B 图注称拟合线为虚线，实为实线；
  - 图 2D 图注描述灰色带，实际为青色；
  - 图 3B 图注给出 ±0.0050 的界限，图中所画为 ±0.0013，且坐标轴只覆盖 ±0.002；
  - 图 4D 图注称 m0* = 72.9 为虚线，实际画成实线；
  - 图 1A 提到不存在的"下排"；
  - 图 5A 的柱条被截断；
  - 部分面板有双重面板标记。
- 修改要求：逐处修正图注或图件，并参照基准论文的风格：面板以 A–D 标在左上角，图注 80–150 词，描述内容而不复述结果，配色统一。

D20 [M9]。位置：补充材料。
- 问题：
  - 有 19 处未解析的引用（"??"）。
  - 证明标题编号错位：正文命题 4 与命题 5 的证明分别题为命题 5 与命题 6。
  - 命题 6（杠杆分解）没有证明。
  - 对 S1.11 与 S1.12 的引用指向错误的小节。
  - 表 S1 超出版心，表 S8 缩放过小，打印后无法阅读。
- 修改要求：与正文一起编译补充材料，用 xr 宏包解析交叉引用。重排证明编号，并补上杠杆分解的证明。

D21 [m1]。位置：命题 5(ii)（results.tex 第 99 行）；补充命题 S(b)，式（r3-IR）。
- 问题：常数 0.505 等于 ξ = R̄²/v_R = 33.06（即基线参数）时 ξ[ξψ′(ξ) − 1] 的值，属于这组参数的性质，不能作为通用常数使用。ξ = 1 时为 0.645，ξ = 5 时为 0.533，ξ = 100 时为 0.502；极限 0.5 对应高斯情形的 √(2/T)。
- 修改要求：把界写成 [T ξ(ξψ′(ξ) − 1)]^{-1/2}，基线值作为示例给出。
- 核验：用 scipy 计算三伽马函数，复现了正文中 T = 3、10、50 时的 0.81、0.45、0.20。

D22 [m2, m3]。位置：3.5 节（results.tex 第 113 行）；3.6 节（results.tex 第 139 行）；局限（discussion.tex 第 14 行）。
- 问题：3.5 节与局限部分给出 S = 3、4 时的下界 0.82 与 0.71，即 √(2/S)。3.6 节援引 "the √(2/(S−1)) precision bound for S = 3"，其值为 1.00。此外，季间方差 0.0041 是 S = 4 的估计（含 2025–26 季），区间 −0.056 至 0.211 却来自 S = 3 的随机效应拟合。这一区间属于合并均值截距 a_RE = 0.077，与方差无关；S = 3 的方差估计为 0.0028。
- 修改要求：统一使用一种界。均值需要估计，应取 S − 1 的形式。给方差报告其自身的区间，例如轮廓似然区间或 Q-profile 区间，并把 S = 3 与 S = 4 的结果分开报告。

D23 [m4]。位置：命题 7（results.tex 第 130 行）；证明（supp_proofs.tex 第 170 行）。
- 问题：正文未定义 e(T) 与 g_T，证明只是概要。由 AR(1) 方差重建 g_T = −T² e′(T)，可得 φ = 0.8 时 T† = 4.48，与 c0/c1 和 m× 无关。于是 B† = T†(c0 + c1 m0*)，只有在 m× = 53.08 时才等于 775.0（以 c1 为单位）。在经验区间 m× = 21.3–49.2 上，B† = 655–763。
- 修改要求：定义 e(T) 与 g_T，写明单位和参数依赖，先给出 B† 的公式，再给示例。
- 核验：见 theory_checks.py 中 prop7 部分的求根。命题 4 证明中的 AR(1) 和式闭式解经核对无误：φ = 0.8、T = 7 时直接求和与闭式都得 31.3886。

D24 [m5]。位置：3.5 节（results.tex 第 126 行）；讨论（discussion.tex 第 10 行）。
- 问题：按式（r3-levers）、交叉项取 ψφ = 0.25 复算，报告项为 7.88 × 10⁻³，正文为 7.85，合计 22.57。"72% 对 17%"的对比把使用 2,000 例的设计与使用 5,000 例的设计相比，还假定 R̄ 在 40 周内不变，而 40 周长于一个流感季。
- 修改要求：更正数值，增加预算相同条件下的比较，写明平稳性假定，或把 T 限制在一个季内。

D25 [m6]。位置：3.1 节（results.tex 第 44 行）。
- 问题：Wald 检验水平（m = 5、k = 0.1 时 7.81%；k = 1 时峰值 10.40%）以及 n 从 400 增至 699 期间功效"下降 82 次"的计数，都无法用公开代码重新生成，所依赖的 sim_theory.json 缺失。基于离散统计量的非随机化检验只在可达水平上是 UMP。
- 修改要求：公开相关代码。说明该检验在实际达到的水平下是 UMP，或改用随机化检验或 mid-p 检验。

D26 [m7]。位置：讨论（discussion.tex 第 8 行）；补充 S1.11。
- 问题：收缩示例使用由真实 v_R 计算的理想权重 δ* = 0.2787，得到均方误差 0.00892。
- 修改要求：给出可行的经验贝叶斯权重及其均方误差，或把该例标明为理想情形下的界。

D27 [m8]。位置：图 3A 与 6.5 节（methods.tex 第 65 行）；3.6 节。
- 问题：两种制度下的样本量在图 3A 中为 6,001 与 416，在正文中为 6,009 与 420。0.107 按 mean(a + b/max(D, 250)) 计算，别处又出现 0.108（模型值 a + b/250）。c̄ ≈ 0.34 由全国损失与州损失之比推出，没有给出推导。
- 修改要求：统一数字。由汇总公式推导 c̄，或直接估计，例如采用 D10 中的周层面组内相关系数（0.29）。

D28 [m9]。位置：3.6 节（results.tex 第 143–145 行）。
- 问题：自愿报告期（2024 年 5 月 1 日至 10 月 31 日）与强制报告期作比较，但前者只有 10 月份的 55 个州周落在流行季起点，季节与制度完全混淆。工具变量回归使用滞后量 D_{t−3} 至 D_{t−5}，这些量很可能通过流行阶段影响当期增长的波动，排除性约束没有论证。第一阶段 F = 1147 只说明相关性，不能说明有效性。"Confirming that endogeneity does not drive the scale effect"的措辞过强。
- 修改要求：论证排除性约束，或把工具变量结果作为一致性检验呈现。在日历周匹配的条件下比较两种制度。

D29 [m10]。位置：摘要（abstract.tex 第 2 行）；results.tex 第 55、57、81、145 行；discussion.tex 第 14 行；conclusion.tex 第 4 行。
- 问题：摘要首句 "Estimation errors in the reproduction number are frequently attributed to sample size" 没有文献支持。正文在证据较弱之处使用 "decisively rejects""decisively favor""confirming""corroborate""must" 和"100%"。中文稿在相同位置用的是"相容"。
- 修改要求：英文措辞应与证据和中文稿一致，采用基准论文那种有所保留的语气（如 "would likely"），避免 "confirms"。

D30 [m11]。位置：bibliography.bib。
- 问题：
  - 十一条条目从未被引用：breto2009time、cameron2011robust、carroll2006measurement、fuller1987measurement、hamilton1994time、lehmann1998point、koenker1978regression、bartlett1946theoretical、zamir1998proof、searle1992variance 和 dersimonian1986meta。
  - mathis2024evaluation 的第一作者为 Sarabeth M. Mathis，条目写作 "Shannon M" [16]。
  - 缺少核心文献：Wallinga 与 Lipsitch（2007）[3]，Lande、Engen 与 Sæther（2003）[10]，Nash 等（2023）[12]，Ogi-Gittins 等（2024、2025）[13, 14]。后三项处理 R_t 估计中的周聚合与漏报，正是案例研究的情境。
  - 稿件报告了随机效应分析，DerSimonian 与 Laird（1986）列在文献表中却未被引用。
- 核验：通过网络检索抽查七条条目，确认了 Parag 等 2022（两篇）、Parag 等 2025、Steyn 等 2025、Eales 与 Riley 2024、Engen 等 1998 以及 Mathis 等 2024（名字有误）的作者、刊物、年份与 DOI。对 Parag 等（2022，Nature Computational Science），还对照全文核对了被引内容。未引用条目由文献表全部键名与源文件中的引用命令逐一比对得出。

D31 [m12]。位置：6.5 节（methods.tex 第 58–63 行）。
- 问题：权重 (0.65, 0.25, 0.10) 没有给出来源。504 个缺失州周被设为零，稿件没有说明其中是否有进入分析窗口的。
- 修改要求：说明权重的依据，例如由流感代际间隔与入院延迟卷积导出，并报告对权重的敏感性。明确写出早期窗内没有填补的零值。
- 核验：审稿人确认，公开面板中 1,267 个早期窗行无一标记为缺失，也无一 G = 0。零值填补因此不影响主要估计。

D32 [m13]。位置：英文稿与中文稿对照。
- 问题：英文稿缺少中文稿中的以下内容：
  - 流感增长期窗中 q2 的例外（BCa 1.686–2.261，高于零假设上限 1.578）；
  - 分级敏感性表；
  - 关于 b/a 向上偏倚的段落；
  - 三项局限（独立性假设 H5、工具变量排除性约束、504 个零值）。

  英文稿对 Δa 功效模拟的描述方向与中文稿相反，两版摘要也不相同。
- 修改要求：以英文稿为记录版本同步两版，并保留修改日志。

D33 [M2, M9]。位置：引言（introduction.tex 第 12 行）；讨论（discussion.tex 第 6 行）；整体设计。与基准论文 [8] 的比较。
- 问题：Eales 与 Riley 定义了下游序列的表观再生数，并说明与延迟分布卷积如何使其失真和滞后。NHSN 住院数据正是这类序列，案例中的 G 因此是表观增长量。稿件称两个问题"conceptually distinct"，但二者存在相互作用：延迟卷积平滑周间变化，使表观 v_R 降低；各州入院延迟的异质性又增加方差。
- 修改要求：讨论这种相互作用，最好用 R_t、代际间隔和入院延迟均已知的模拟来说明表观序列的 a、b 与 v_R、A 之间的关系。
- 呈现方式：作为参照，基准论文的章节顺序为引言、背景、结果、讨论、结论、方法；摘要为一段约 280 词、不含数字；六幅图，无表；图注描述内容，不复述结果。稿件已经采用相同的章节顺序。主要差别在篇幅、命题密度、摘要中的数值结果，以及复述数字的图注。

### 5 总体建议

建议：大修（Major revision）。

评分：4 分（满分 10 分）。

理由如下。理论部分正确，推导清楚，但新颖性有限：分解即环境方差与人口方差的经典划分，分配结果即 Neyman–Cochran，报告结果与 Parag 等（2022）重叠。稿件尚未如实地相对这些工作定位自身（M1）。

实证部分在点估计层面可复现，但解读缺乏支持。

- 所分析的统计量是下游序列的周增长因子，与再生数估计不同（M2）。
- 截距约一半是全国同步的周分量（M3）。
- b/a 与 m× 的核心吻合是相对未修正预测而言（M4）。
- 置信区间约为按周聚类 bootstrap 结果的一半宽（M5）。
- 报告异质性、复现与预注册三项结论分别依赖一个窄的代理变量、一个事后设定的界限，以及在结果之后写成的计划（M6、M7）。
- 复现包尚不能重新生成图件（M8）。
- 呈现方式需要大幅修改，Epidemics 审稿人才能高效评审（M9）。

这些问题都未必是致命的。若重新定位后满足以下条件，稿件有望达到发表水平：

- 把理论表述为已知方差分解在监测设计中的转化；
- 正确估计 R_t，或重新命名实证目标；
- 采用双向聚类推断和截距的分层分解；
- 把经验平衡尺度报告为一个有不确定性的区间。

上述修改属于实质性修订，远超润色范围，故给 4 分。

审稿人置信度：数学、统计与可复现性评估均经数值核验，置信度高（5 分制 4 分）。对 NHSN 设施完整度数据的流行病学解读，审稿人未能用外部检出率数据验证，置信度中等（5 分制 3 分）。

### 参考文献

参考文献编号与 Part A 相同，书目信息见 Part A 的参考文献表。
