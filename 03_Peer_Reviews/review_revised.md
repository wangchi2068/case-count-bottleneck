# Second-round peer review of the new manuscript

- Manuscript: "An irreducible error floor in reproduction number estimates from case counts under environmental and reporting variation" (English, 19 pages) and its Chinese version "基于病例数的再生数估计在环境变异与报告变异下的不可约误差下限" (20 pages). Target journal: Epidemics.
- Version reviewed: output/case-count-bottleneck/paper/ (paper.pdf, paper.html, LaTeX source, Tables S1–S7) and output/case-count-bottleneck-zh/paper/. The reproduction package is in output/case-count-bottleneck/experiment/ (code, the NHSN vintage retrieved on 2026-10-20, analysis/results.json). The English and Chinese versions are reviewed as one manuscript in two languages.
- Review date: 20 October 2026
- Benchmark article: Eales and Riley (2024), Epidemics 46:100742 [1], and the 25-rule style profile derived from it for this task.
- Previous round: review_original.md (Major revision, 4 out of 10). This review applies the same standard and the same 1–10 scale.
- Declaration: this is an internal review. The manuscript was written within the same task as this review, in response to the first-round comments. The reviewer gives no allowance for this. Every factual statement below was checked against the manuscript files, the tables and results.json, not against the authors' revision response.
- Verification: the check script is revised_checks.py and its output is revised_checks.json, both in .work/case-count-bottleneck/review/checks/. The script has five blocks: (A) 131 headline numbers formatted from results.json and located in the English and Chinese sources; (B) a file-by-file comparison of the numbers in the English and Chinese sections and tables; (C) quantities derived from the reported estimates; (D) PDF facts (pages, fonts, unresolved references); (E) style probes against the benchmark. The closed-form theory values were re-derived by hand. The full pipeline (run_all.sh) was not re-executed in this round, so reproducibility is assessed as traceability from results.json to the text.

Part A is the English review and Part B is the Chinese review. The two parts use the same numbering and give the same verdict and score. Second-round major weaknesses are numbered N1–N6 and minor ones n1–n13. First-round items are cited as "first-round M3" or "first-round m6".

## Part A — English

### 1 Summary

The manuscript asks how much the precision of a reproduction-number estimate improves when more cases are reported. Its answer depends on the target. Precision for the period-specific value keeps improving with case volume. Precision for the mean across periods, R̄, levels off at the environmental variance v_R. Proposition 1 gives the error variance of the period mean as V = v_R + A/m, where A = R̄ + ρ(R̄² + v_R)/k, and defines the balance scale m× = A/v_R. Proposition 2 shows that multiplicative reporting volatility with relative variance τ² adds v_H = τ²(R̄² + v_R) to the floor. Proposition 3 gives the cost-optimal case volume m* = √((c0/c1)m×). Corollary 1 states when coverage beats completeness. Appendix B adds a Fisher-information bound, a budget formula B† and a between-season precision result.

The empirical part uses NHSN weekly influenza hospital admissions for 50 states and the District of Columbia (21641 jurisdiction-weeks, 2020-08-08 to 2026-10-10). Two statistics are analysed: a weighted growth ratio G = C_{t+1}/D_t and a renewal-type ratio R_A = (1 + rθ)^α. An affine model E(L | D) = a + b/D is fitted by feasible GLS with a two-way (state × week) bootstrap. In rule-defined early-growth windows of four seasons, R_A gives a = 0.0150 (95% CI: 0.0100, 0.0208) and b/a = 37.4 (19.1, 71.0); G gives a = 0.0840 (0.0498, 0.1248) and b/a = 23.5 (8.4, 59.7). About half of the intercept is common to all states in a calendar week. A power law without a floor fits almost as well (p = 0.114 to 0.438). A known-truth simulation shows that neither statistic recovers v_R/R̄² as its intercept. Adjusting for facility reporting completeness changes the intercept by an amount that is equivalent to zero within pre-set margins at τ0 = 0.10, but not at τ0 = 0.05. Delphi laboratory data are added as a second proxy.

The revision is substantial and addresses most first-round comments. The theory is now placed against the ecological and sampling literature. Inference is two-way clustered throughout. The intercept is decomposed into national-week and state-season parts, and the floor is described as conditional on the affine form. The two language versions agree on all checked numbers. The remaining problems are concentrated in interpretation. The paper runs a simulation that calibrates the empirical intercepts but does not apply the calibration. When it is applied, two conclusions in the Discussion reverse (N1). The title still claims an irreducible floor that the paper itself says the data do not establish (N2). The reporting conclusion is worded more strongly than the equivalence test allows (N5). Positioning against Parag et al. [2], authorship and archiving remain incomplete (N3, N6).

### 2 Strengths

- S1. The theory is correct. The reviewer re-derived Propositions 1–3, Corollary 1 and Propositions 4–5 with Corollary 2. The baseline values A = 2.1232, m× = 53.1, v_H = 0.0307 (τ = 0.15) and m* = 14.6 to 22.2 (c0/c1 = 10) were reproduced from the stated formulas.
- S2. The contribution is now positioned against its antecedents. The Discussion names the ecological split of demographic and environmental variance [6, 7]. The Background states the two-stage sampling analogue [8]. The propositions are written in terms of (n, ρ), and Proposition 1(iv) limits the floor to conditionally unbiased estimators.
- S3. Inference is much stronger. Every interval is a two-way bootstrap percentile interval. The paper reports that the bootstrap standard deviation of a is 1.95 to 4.68 times the state-only value, which makes the first-round clustering problem visible rather than hidden.
- S4. The identification analysis is honest. Removing national-week effects reduces a by 41% to 52%, and the paper reports this in the main text. It also reports that the plateau test has no power and concludes that "the data are therefore consistent with a floor but do not establish one".
- S5. The known-truth simulation (Section 3.2, Fig. 3) is a valuable addition. It shows that apparent statistics do not recover v_R/R̄² and that b/a is recovered only on the statistic scale.
- S6. Multiplicity and power are handled explicitly: TOST with reported power, Holm and Benjamini–Hochberg corrections over 40 tests, and a no-environment null for the pathogen comparison. The null shows that q1 below 1 and q2 above 1 also occur without environmental variation, and the paper says so.
- S7. Traceability is high. All 131 headline numbers formatted from results.json were found in both the English and the Chinese sources (block A, 0 failures). The package contains one script per analysis block, figure and table builders, the raw data snapshot with its SHA-256, and run_all.sh.
- S8. The presentation follows the benchmark in most respects. The section order is Introduction, Background, Results, Discussion, Conclusion, Methods. The abstract (279 words in the PDF text) has no numbers. There are six data figures with bold outside panel letters, framed legends with titles and the Dark2 palette. Captions run to 119–141 words and carry no result numbers. There are no unresolved references, and all fonts are embedded.

### 3 Weaknesses

#### Major

- N1. The simulation calibration is reported but not used. Section 3.2 finds that the noise-free intercept is 2.68 × v_R/R̄² for G and 0.484 × v_R/R̄² for R_A. Section 3.3 and the Discussion still compare the empirical intercepts with the uncalibrated mapping. With the calibration applied, both statistics imply v_R ≈ 0.044–0.045. This lies inside the assumed range of 0.04 to 0.08, which contradicts the statement that the implied v_R is "below each of the values assumed". The intercept of G falls from 3.1–6.2 to 1.2–2.3 times the theory value. The calibrated theoretical b/a then contains the empirical value. The calibration itself rests on simulation settings that differ from the data, and its uncertainty is not propagated.
- N2. The title overstates the result. The floor for an estimate pooled over T periods is v_R/T, which falls with more periods. Proposition 1(iv) restricts the floor to conditionally unbiased estimators, and Appendix B.5 shows that shrinkage can go below it. The paper's own Discussion says the data do not establish a floor.
- N3. Positioning against the closest prior work is still incomplete. The Discussion describes the information-theoretic analyses of Parag and colleagues as Poisson models whose information grows with the number of cases. Parag, Donnelly and Zarebski (2022) [2] already include time-varying reporting fractions (Equation 5) and a negative-binomial extension. First-round D2 asked for this contrast.
- N4. The empirical target is still an apparent statistic. R_A is a Wallinga–Lipsitch transform of weekly growth [5], and Methods says it is "not a posterior estimate of R_t". The title and abstract nevertheless speak of reproduction number estimates. No renewal estimate with an admission delay is reported.
- N5. The reporting conclusion is stronger than the evidence. The equivalence margins at τ0 = 0.10 are 10% to 17% of the intercept, equivalence fails at τ0 = 0.05, and the test then has power 0 for G. The claim that the margins were "fixed before fitting" cannot be verified, and the margin formula uses the sample mean of the statistic. The laboratory proxy accounts for 0.230 (95% CI: 0.043, 0.418) of the R_A intercept. This number is ambiguous because laboratory growth carries its own noise. The voluntary-reporting period shows a 58% larger spread of log G.
- N6. Analysis history and submission compliance are incomplete. The window rule was revised during the analysis, and R_A was promoted to the primary statistic in this round. The earlier analysis rounds are documented only outside the paper. The author line and CRediT statement name "Apevon Science" with no human author. No archival DOI exists for the code.

#### Minor

- n1. The Discussion says b/a "changed by a factor of four" across specifications. The factor is 3.9 for R_A and 7.1 for G.
- n2. The design results (m*, B†) use the uncorrected calendar-window range of m×, although Section 3.3 argues for the corrected range.
- n3. Fig. 6D uses b/a = 37.4 on the statistic scale, while the simulation implies about 43 on the nominal scale.
- n4. The Fig. 6B caption calls a lower bound on the relative standard error a "lower bound on the precision".
- n5. Methods states one bootstrap seed, but the package uses four.
- n6. Sample sizes differ between R_A and G in the same windows (1748 against 1756; 1263 against 1267) without explanation.
- n7. Cross-validation is reported as leave-one-season-out in the text and as leave-one-state-out in Table S2.
- n8. Table S6 reports intervals for ratios of intercepts with negative lower bounds.
- n9. The text gives 95% intervals for Δa, while the equivalence test and Table S3 use 90% intervals. The Fig. 4B bin error bars ignore clustering.
- n10. Number formatting is inconsistent: thousands separators appear in tables but not in the text, and the code URL breaks inside the host name in the English PDF.
- n11. Alignment with the benchmark is incomplete in section proportions, length, use of "we", reference format, keywords and figure format.
- n12. The English and Chinese versions differ in running heads, the generative-AI declaration and the Chinese body font.
- n13. The only direct evidence on low reporting completeness (the voluntary period) points toward a reporting effect, and the abstract does not mention it.

### 4 Detailed comments

Each comment gives the location, the problem, why it matters, the requested change, and the verification method with its result. The bracket after the number links the comment to the weaknesses above.

D1 [N1]. Location: Section 3.3, last paragraph (results.tex line 58); Discussion, paragraph 4 (discussion.tex line 8); Section 3.2 and Fig. 3C.
- Problem: Section 3.2 reports that the median noise-free intercept is 2.68 × v_R/R̄² for G and 0.484 × v_R/R̄² for R_A. Section 3.3 then states that "the intercept of R_A implied v_R = 0.0217, below each assumed value of 0.04, 0.08 and 0.16". It also states that the empirical intercept of G was 3.1 to 6.2 times the theory value. Both comparisons ignore the calibration that the paper has just estimated. With it, the R_A intercept implies v_R = 0.0444 at R̄ = 1.2, or 0.0449 at the sample mean 1.206. The G intercept implies 0.0451. Alternative calibrations (the simulated slope, or scaling from the baseline scenario) give 0.0435 to 0.0445. The two statistics therefore agree with each other and imply a v_R between the assumed values 0.04 and 0.08. The G intercept becomes 1.2 to 2.3 times the theory value in rule windows and 1.3 to 2.6 times in calendar windows. Multiplying the corrected theoretical b/a by the simulated recovery ratio 0.328 gives 13.4 to 28.7 for rule windows and 12.8 to 27.4 for calendar windows. These ranges contain the empirical 23.5 and 22.6.
- Why it matters: the Discussion concludes that the excess over v_R "is not interpretable as unmodelled transmission variance". It also concludes that the empirical b/a fits only if non-environmental contributions are large. Applying the paper's own calibration reverses both conclusions.
- Requested change: apply the calibration in Section 3.3 and report the implied v_R with an interval that combines bootstrap and simulation uncertainty. Rewrite Discussion paragraph 4 and the limitation paragraph accordingly. If the authors judge the calibration unreliable (see D2), say so and give the uncalibrated and calibrated values side by side.
- Verification: block C of revised_checks.py. Inputs are a and R̄ from Table S1, the calibration factors 2.68 and 0.484 and the recovery ratio 0.328 from results.json. Outputs are R_A v_R = 0.0444 (R̄ = 1.2) and 0.0449 (R̄ = 1.206); G v_R = 0.0451; calibrated a/theory 1.16–2.33 (rule) and 1.29–2.58 (calendar); calibrated b/a 13.4–28.7 (rule) and 12.8–27.4 (calendar).

D2 [N1]. Location: Methods, simulation of apparent statistics (methods.tex, last paragraph); code s08_sim_apparent.py.
- Problem: the calibration rests on settings that differ from the data in four ways:
  - The simulation uses R̄ = 1.2. The mean of G in the rule windows is 1.724 (Table S1). The bias of a ratio statistic depends on the growth rate, so the factor 2.68 for G may not transfer. The mean of R_A (1.206) is close to the simulated value.
  - Weekly R is drawn independently for each state and week. The data show that 41% to 52% of the intercept is a national-week component, and the simulation has no common shock.
  - R_A is computed with the same generation interval that generated the data, so its calibration is optimistic.
  - The admission delay (mean 5.5 days, SD 3.0 days) is assumed. Each simulated window has six observation weeks.
- Why it matters: D1 shows that the main empirical conclusions turn on this calibration. The calibration needs to match the data well enough to be used, or it needs a stated uncertainty.
- Requested change: rerun the simulation with the empirical growth rates of each window, a national-week shock whose share matches the decomposition, a misspecified generation interval for R_A (the 2.2-day and 4.3-day variants already used), and the observed number of weeks per window. Report the calibration factors with their spread across replicates.
- Verification: the simulation design was read from methods.tex and s08_sim_apparent.py (Rw = rng.gamma(shp, RBAR/shp, (S, W)), independent across states and weeks; 500 states, 20 replicates, 17 scenarios, 4 warm-up and 6 observation weeks).

D3 [N2]. Location: title; Proposition 1(iv) (background.tex); Appendix B.5; Discussion paragraph 5 (discussion.tex line 10); Table S2 note.
- Problem: "irreducible" is not supported in three ways. First, the error of the mean pooled over T periods is v_R/T + A/(Tm), so the floor falls with more periods (Proposition 3). Second, the floor applies only to conditionally unbiased estimators (Proposition 1(iv)). Appendix B.5 shows that shrinkage beats v_R when Δ² is below v_R(1 + m/m×). Third, the plateau test gives p = 0.114, 0.438 and 0.418. The Table S2 note states that no fraction of the estimated a is detectable with 80% power. The Discussion itself concludes that the data "do not establish" a floor. The benchmark style profile also asks for a title that names the question rather than the conclusion.
- Why it matters: the title is what most readers will cite.
- Requested change: retitle in both languages. One option is "Case volume and the precision of reproduction number estimates under environmental and reporting variation". Remove "Error floor" from the keywords.
- Verification: reading of the cited locations. The p values and the power statement match results.json (block A).

D4 [N3]. Location: Discussion paragraph 3 (discussion.tex line 6); Introduction (citation of parag2022fundamental).
- Problem: the Discussion says that the analyses of Parag and colleagues "model incidence as Poisson given past incidence and conclude that information grows with the number of cases". In Parag, Donnelly and Zarebski (2022) [2], Equation 5 shows that the information in a noisy epidemic curve is scaled by the geometric mean of time-varying reporting fractions. Its Supplementary Note extends the result to negative-binomial noise. The description in the Discussion is therefore incomplete in the direction that inflates the novelty of Proposition 2. The added ecology [6, 7] and sampling [8] antecedents resolve the other half of first-round M1.
- Why it matters: Parag et al. [2] is the closest prior result on reporting noise and information. An Epidemics referee is likely to check this contrast first.
- Requested change: state that the effect of reporting fractions on information is already known [2]. Then contrast Proposition 2 with Equation 5 of [2] in three respects: the target (R̄ against R_t), the noise model (a mean-one multiplicative shock against a reporting fraction) and the consequence (an additive floor against an information ratio).
- Verification: comparison of discussion.tex line 6 with the first-round deep reading of [2], Equations 4–5 and the section "Ranking noise sources by their information loss".

D5 [N4]. Location: Methods Section 6.2 (definition of R_A); Appendix A.7; title and abstract.
- Problem: R_A = (1 + rθ)^α is the Wallinga–Lipsitch transform of weekly growth [5], with a gamma generation interval (mean 3.6 days, SD 1.6 days). Methods states correctly that it is "a transformation of observed growth and not a posterior estimate of R_t". The simulation shows that R_A attenuates environmental variance: its intercept is 0.484 of v_R/R̄². The title and abstract still refer to "reproduction number estimates", and no renewal-model estimate (for example EpiEstim [3]) with an admission delay is reported. First-round M2 asked for either a proper R_t estimate or a relabelled target. The revision relabels in Methods only.
- Why it matters: surveillance users will read the conclusions as applying to R_t estimates of the kind in Cori et al. [3] and Gostic et al. [4].
- Requested change: either add a renewal-model analysis with an infection-to-admission delay and report the intercept of its posterior means, or state in the title, abstract and conclusion that the empirical results concern growth-based statistics.
- Verification: methods.tex Section 6.2 and results.tex line 38.

D6 [N5]. Location: Abstract; Section 3.4 paragraph 1 (results.tex line 70); Discussion paragraph 6 (discussion.tex line 12); Methods Section 6.5; Table S3.
- Problem: the abstract and Discussion say that facility reporting completeness "explained a negligible part of the intercept". The evidence is narrower:
  - Δa is 0.0004 (95% CI: −0.0036, 0.0033) for G and 0.0003 (−0.0003, 0.0010) for R_A. Both are equivalent to zero at τ0 = 0.10. The margins at τ0 = 0.10 are 12% (G, rule), 10% (G, calendar) and 17% (R_A) of the intercept. The test therefore shows that the adjustment changes a by less than one-tenth to one-sixth.
  - At τ0 = 0.05 neither change is equivalent, and the power of the test at zero true change is 0 for G and 0.25 for R_A.
  - The margin δ = κ²τ0²(1 + v_R/R̄²) uses the sample mean of the statistic in the analysed windows, so it is not independent of the data. No dated record supports the statement that the margins were "fixed before fitting".
  - The adjustment divides counts by the share of hospitals reporting. It does not address changes in ascertainment within reporting hospitals, such as testing intensity or coding.
- Why it matters: "negligible" is a strong word for a test that can only rule out changes above 10% to 17% and has no power at the stricter margin.
- Requested change: replace "negligible" with the bound the test supports, for example "changed the intercept by less than 17% of its value". State that the margin depends on the sample mean. Either point to a dated record of the margins or remove "fixed before fitting". Add one sentence on within-hospital ascertainment.
- Verification: block C gives the margin shares 0.121 (G, rule), 0.102 (G, calendar) and 0.170 (R_A). The Δa intervals and power values match results.json (block A).

D7 [N5]. Location: Section 3.4 (results.tex line 70); Methods Section 6.5; Table S4 note.
- Problem: in 44 states, laboratory growth "accounted for a share of 0.230 (95% CI: 0.043, 0.418) of the intercept of R_A". The correlation is 0.31. Laboratory growth contains transmission signal and its own sampling and testing noise. Under classical measurement error the shared share is attenuated toward zero [9]. The value 0.23 therefore cannot separate a small transmission share from a noisy proxy. The unexplained 77% cannot be attributed to environmental variance either. Seven jurisdictions (ak, dc, de, nh, ny, ri, ut) have no laboratory data.
- Why it matters: the proxy is used to support the conclusion that reporting is not the source of the intercept. Read either way, it is consistent with several explanations.
- Requested change: report the reliability of laboratory growth (for example a split-sample correlation) and an attenuation-corrected share. Describe 0.23 as a check that does not discriminate between the explanations. Report the main estimates restricted to the 44 states.
- Verification: data_decision.md and Table S4 note (Delphi clinical laboratory data, 1224 state-weeks).

D8 [N6]. Location: Methods Section 6.1; output/case-count-bottleneck/experiment/analysis/data_decision.md.
- Problem: the first version of the window rule ended windows at the season maximum. It was replaced on 2026-10-20, "before any intercept was fitted on the new windows" but after the first version had been used. In this round R_A became the primary statistic and calendar windows became secondary. The earlier analysis rounds (r3, r4) are described only in data_decision.md, which a journal reader will not see. Each choice is defensible. Together they form the garden of forking paths that first-round M7 raised [10].
- Why it matters: the reader needs to know which specifications were tried and in what order to judge the headline estimates.
- Requested change: add a short analysis-history table to the supplement. For each specification, give its role, when it was adopted, a and b/a. The headline estimates lie within each other's intervals, and the paper can say so.
- Verification: methods.tex Section 6.1; data_decision.md; the first-round manuscript analysed G only.

D9 [N6]. Location: author line (main.tex line 95); CRediT statement and Code availability (endmatter.tex).
- Problem: the only author is "Apevon Science", and the CRediT statement assigns all roles to "Apevon Science". Elsevier policy states that AI tools cannot be listed as authors and that authors are humans who take responsibility for the work [11]. Code availability points to a GitHub repository with no archival DOI. The revision response states this openly (first-round M8).
- Why it matters: both points block submission to Epidemics, whatever the scientific merit.
- Requested change: list the human authors with affiliations, ORCID identifiers and individual CRediT roles. Deposit the package on Zenodo or a similar archive and cite the DOI.
- Verification: main.tex, endmatter.tex and revision_response.md (M8 marked Partial).

D10 [n1]. Location: Discussion paragraph 5 (discussion.tex line 10); Section 3.3 paragraph 3.
- Problem: the Discussion says that b/a "changed by a factor of four" across specifications. For R_A the range is 24.7 to 97.1 (3.9 times); for G it is 12.2 to 86.8 (7.1 times).
- Requested change: give both factors.
- Verification: block C (RA_ba_range_factor = 3.93, G_ba_range_factor = 7.09).

D11 [n2]. Location: Section 3.1 paragraph 3; Fig. 2C; Appendix B.2; Table S7.
- Problem: m* (14.6 to 22.2 for c0/c1 = 10; 46.2 to 70.1 for c0/c1 = 100) and B† (655 to 763) use the uncorrected calendar-window range m× = 21.3 to 49.2. Section 3.3 argues that the denominator-corrected range (38.9 to 83.5) is the appropriate theory for G. With the corrected range, m* is 19.7 to 28.9 and 62.4 to 91.4.
- Requested change: state which range is used and why, or report both.
- Verification: block C (m_star_c10_using_delta_corrected_range, m_star_c100_using_delta_corrected_range).

D12 [n3]. Location: Fig. 6D and its caption.
- Problem: the design surface uses b/a = 37.4 for R_A on the statistic scale. With the simulated recovery ratio 0.849, the nominal-scale value is about 43. The caption calls the panel illustrative, but the scale is not named.
- Requested change: name the scale in the caption, or use the nominal value.
- Verification: block C (RA_ba_nominal_scale_via_sim_nom_ratio = 43.1).

D13 [n4]. Location: Fig. 6B caption.
- Problem: "Lower bound on the precision of an estimated between-season variance, expressed as a relative standard error". A lower bound on the relative standard error is an upper bound on precision.
- Requested change: "lower bound on the relative standard error of the estimated between-season variance".

D14 [n5]. Location: Methods (statement "seed 20261024"); s02_inference.py.
- Problem: the two-way bootstrap blocks use four seeds: 20261024 (R_A, rule), 20261124 (G, rule), 20261224 (G, calendar) and 20261324 (R_A, calendar).
- Requested change: state the seeding scheme.
- Verification: block C (seeds_twoway_blocks).

D15 [n6]. Location: Table S1; Section 3.3 paragraph 1.
- Problem: in the same rule windows, N is 1748 for R_A and 1756 for G; in calendar windows it is 1263 and 1267. The text does not explain the difference.
- Requested change: give the exclusion rule in the Table S1 note.
- Verification: Table S1 and results.json.

D16 [n7]. Location: Section 3.3 paragraph 3; Table S2.
- Problem: the text reports leave-one-season-out validation (two of four, none of four and three of three folds). The Table S2 column "CV folds" is leave-one-state-out (26/51, 19/51, 28/51). Methods mentions both.
- Requested change: report both in Table S2.

D17 [n8]. Location: Table S6.
- Problem: intercept ratios have intervals with negative lower bounds: COVID-19 calendar q1 = 0.73 (−0.32, 0.91) and RSV growth q2 = 1.69 (−0.22, 3.06). A ratio of intercepts that represent variances is positive. The negative bounds arise from bootstrap draws in which the denominator intercept is negative.
- Requested change: report the share of such draws and compute the intervals on the log scale over valid draws, or mark these intervals as undefined.

D18 [n9]. Location: Section 3.4 paragraph 1; Table S3; Fig. 4B.
- Problem: the text gives 95% intervals for Δa, while the test and Table S3 use 90% intervals. For R_A these are 0.29 (−0.22, 0.85) × 10⁻³ in Table S3 and 0.0003 (−0.0003, 0.0010) in the text. Both are labelled, but a reader will compare the 95% interval with the margin. The Fig. 4B bin error bars ignore clustering, as the caption and the limitations state.
- Requested change: give the 90% interval in the text next to the test result. Use two-way bootstrap bars in Fig. 4B, or remove them.

D19 [n10]. Location: Tables S1 and S6; Table S4 note; endmatter (Code availability).
- Problem: the tables print 1,748 and 2,707, while the text prints 1748 and 21641. The benchmark uses no thousands separators. The Table S4 note gives 0.23 (0.043, 0.42), while the text gives 0.230 (0.043, 0.418). In the English PDF the code URL breaks inside the host name ("https://github.c om/…"), so it does not survive copy and paste.
- Requested change: drop the separators, use the same number of digits, and let the URL break only at slashes.
- Verification: tab_s1_headline.tex lines 10–13 (1{,}748); visual inspection of the rendered end-matter page.

D20 [n11]. Location: whole manuscript.
- Problem: the comparison with the benchmark style profile is summarised below.

| Feature | Benchmark | New manuscript | Status |
|---|---|---|---|
| Title | sentence case, names the question | sentence case, 18 words, states a conclusion | not met (D3) |
| Abstract | 250–290 words, no numbers | 279 words (PDF text), no numbers | met |
| Keywords | 6–8, no repeat of title | 6, "Error floor" repeats the title | partly |
| Section order | Introduction to Methods, then end matter | same | met |
| Section shares | Discussion longest (about 30%), Results about 18% | Results 30.5%, Discussion 19.7% | not met |
| Main-text length | about 5700 words | 6600 words (detex count) | partly |
| Hedging | no "suggest" or "might" | none | met |
| First person | "we" about once per 150 words | 8 occurrences | partly |
| Numbers | no thousands separators | separators in tables | partly (D19) |
| Interval format | one format throughout | one format, labelled | met |
| Figures | data figures only, Dark2, framed legends, bold A–D | met, except a box schematic in Fig. 1A and raster Figs 1A and 6 | partly |
| Captions | 80–150 words, no result numbers | 119–141 words, interval levels only | met |
| In-text citations | Harvard author–year | author–year | met |
| Reference list | Surname, I.I., Year. Abbrev. J.; 30–45 entries; about 10% Epidemics | plainnat with full forenames and journal names; 43 entries; 4 from Epidemics (9%) | partly |
| End matter | Code, CRediT, competing interests, data, acknowledgements | present in this order, with an AI declaration | met |

- Why it matters: the benchmark gives most space to interpretation. In this manuscript the Results section is the longest, and much of the interpretation sits in Results paragraphs.
- Requested change: move interpretive sentences from Results to Discussion and shorten Results to about 1200 words. Cut about 900 words in total. Use the Elsevier Harvard reference style. Supply Figs 1A and 6 as vector files. Use Times or a metric-identical font in the figures; the figures embed Liberation Serif and the body uses Times New Roman.
- Verification: block E (word counts, shares, "we" count, caption lengths, bibliography count); block D (font list); visual inspection of the rendered pages.

D21 [n12]. Location: both PDFs; endmatter.
- Problem: block B finds that every difference in numbers between the language versions is explained. The Chinese text writes month names as numeric dates (introduction, methods, Table S4). The Chinese AI declaration mentions two image-2 timeouts and the TikZ fallback, which the English declaration omits. The Chinese appendix heading contains "超过 1". Table S6 in English contains "1 week" and "3 weeks" as words. Three non-numeric differences remain. The English PDF has running heads and the Chinese PDF has none. The AI declarations differ in content, as noted above. The Chinese body is set in Noto Serif CJK SC, not SimSun.
- Requested change: make the two AI declarations identical in content. Add running heads to the Chinese version. Use SimSun if the target is a Chinese-language venue that requires it.
- Verification: block B (per-file multisets of numbers); block D (pdffonts); visual inspection of pages 1–10 of each PDF.

D22 [n13]. Location: Abstract; Section 3.4 paragraph 1; Table S4.
- Problem: under voluntary reporting (median completeness 45.7%), the interquartile range of log G from May to October was 0.759 (95% CI: 0.479, 1.042), against 0.479 in 2023 and 0.483 in 2025. The FGLS intercept is unstable in that period, so this robust spread is the only direct evidence on low completeness. It points toward a reporting effect. The abstract reports only the mandatory-period equivalence.
- Requested change: report the voluntary-period result in the abstract and Discussion with the same weight as the mandatory-period result, noting that season and regime remain partly confounded.
- Verification: Table S4; results.json.

### 5 Overall recommendation

Recommendation: Major revision.

Score: 6 out of 10.

Rationale. The scale is the one used in the first round. A score of 4 meant a correct theory with an empirical part whose interpretation was not supported and needed new analyses. A score of 6 means that the analyses are now largely adequate, but at least one issue could change a main conclusion and the framing still claims more than the evidence shows. Minor revision (7–8) would require that no remaining issue can change a stated conclusion.

The revision has fixed most first-round problems: two-way clustering, the decomposition of the intercept, the known-truth simulation, multiplicity, positioning against the ecological and sampling antecedents, bibliography hygiene and the equivalence of the two language versions. Two of nine first-round major items are fully resolved, seven are partly resolved and none is unresolved (Section 6).

The score is not higher because of N1. The paper estimates a calibration and then does not use it, and the calibration reverses two statements in the Discussion. Fixing this requires a new simulation run and a rewritten Discussion paragraph, not wording changes alone. N2 and N5 need wording changes. N4 needs either a new analysis or a narrower claim. N6 needs actions that only the human authors can take (authorship, DOI).

Reviewer confidence: high (4 out of 5) for the mathematical, statistical and number-tracing assessments, which were checked by script. Moderate (3 out of 5) for the epidemiological interpretation of NHSN completeness and Delphi laboratory data. The internal nature of this review is a further limitation. The reviewer cannot rule out a shared blind spot with the authors of the manuscript, so an external review is still advisable before submission.

### 6 Response to first-round comments

Judgements are Resolved (已解决), Partly resolved (部分解决) or Not resolved (未解决). The evidence is the reviewer's own reading of the new manuscript and the check script, not the revision response.

| Item | First-round request | Judgement | Evidence |
|---|---|---|---|
| M1 | position against ecology and Parag et al. | Partly resolved | Ecology and sampling antecedents added (Discussion paragraph 2; Background); the Parag contrast omits reporting fractions (D4) |
| M2 | proper R_t estimate or relabelled target | Partly resolved | R_A added and relabelled in Methods; title and abstract unchanged; no renewal estimate (D5) |
| M3 | identification of the intercept and plateau | Resolved | Week and state-season decomposition, ICC, power-law test, cross-validation (Section 3.3; Table S2) |
| M4 | compare theory and data correctly | Partly resolved | Corrected b/a and a simulation added; the simulation calibration is not applied (D1, D2) |
| M5 | clustered inference | Resolved | FGLS with two-way bootstrap throughout; inflation 1.95 to 4.68 reported (Table S1) |
| M6 | reporting heterogeneity | Partly resolved | Renamed, TOST with power, laboratory proxy, voluntary period; conclusion overstated (D6, D7, D22) |
| M7 | pre-registration and multiplicity | Partly resolved | Holm and BH added; window revision disclosed; analysis history outside the paper (D8) |
| M8 | reproduction package | Partly resolved | Scripts, data snapshot with SHA-256, run_all.sh and figure builders present; no DOI; seeds incompletely stated (D9, D14); pipeline not re-executed by the reviewer |
| M9 | presentation | Partly resolved | Propositions 4–5 in Appendix B; English figures; no "??"; 6600 words and inverted section shares (D20) |
| m1 | constant 0.505 not general | Resolved | Appendix B.1 gives it at the baseline parameter set |
| m2 | √(2/(S−1)) used consistently | Resolved | Corollary 2; Section 3.4; Table S7 |
| m3 | S = 3 and S = 4 separated; correct interval | Resolved | Table S5; Q-profile interval (Methods Section 6.6) |
| m4 | define B† and its units | Resolved | Proposition 5, Eq. (B.2); the input range is questioned in D11 |
| m5 | lever comparison at equal budget | Resolved | Section 3.1; Table S7 (7.88) |
| m6 | Wald numbers and UMP claim | Resolved | Unreproducible Wald numbers removed; Appendix B.4 states the Karlin–Rubin result at the attained level |
| m7 | oracle shrinkage weight | Resolved | Appendix B.5 labels it an ideal bound and names empirical Bayes as the feasible analogue |
| m8 | inconsistent counts | Resolved | 6009, 420 and 4077 by regime agree across text and tables; a new R_A/G count difference is raised in D15 |
| m9 | voluntary period confounded; IV | Resolved | Calendar-matched comparison (Table S4); IV analysis removed |
| m10 | overclaiming wording | Partly resolved | "decisively", "confirming" and "must" removed; title, "negligible" and "not interpretable" remain (D3, D6, D1) |
| m11 | bibliography hygiene | Resolved | 43 entries, all cited; Mathis forename corrected; core references added; format differs from Elsevier (D20) |
| m12 | D_t weights and zero counts | Partly resolved | Zero-imputed counts excluded (Section 6.1); weights still not derived, and equal weights move b/a for G from 23.5 to 12.2 |
| m13 | English and Chinese equivalent | Resolved | 131 of 131 headline numbers in both; residual differences in D21 |
| m14 | interval types | Resolved | One percentile two-way interval, labelled; 90% and 95% for Δa noted in D18 |

Tally: major items 2 resolved, 7 partly resolved, 0 not resolved; minor items 12 resolved, 2 partly resolved, 0 not resolved.

### 7 Data decision

The authors kept the NHSN Weekly Hospital Respiratory Data vintage retrieved on 2026-10-20 and did not switch to another source. They added Delphi FluView clinical laboratory data as an auxiliary proxy (44 of 51 jurisdictions, 1224 state-weeks). FluSurv-NET was considered and not used, for lack of information at state level.

The reviewer agrees with keeping NHSN. The first-round problems lay in the definition of the statistic, the inference and the interpretation, not in the data. NHSN is the only source with weekly admissions for every state, together with the share of hospitals reporting, which the reporting analysis needs. A switch would have changed the object of study and broken the link to the first round.

Adding the laboratory proxy is useful but does not settle the reporting question, for the reasons in D7: measurement error in the proxy and seven missing jurisdictions. The voluntary-reporting period (D22) is a natural experiment already present in NHSN and deserves more weight than it receives.

### 8 Verification record

- Headline numbers (block A): 131 values formatted from results.json and the part files, each found in the English and Chinese sources; 0 failures.
- English–Chinese numbers (block B): all per-file differences are explained (month dates written as numbers in Chinese, the AI declaration, one appendix heading, two numbers written as words in English Table S6). No substantive difference.
- Derived quantities (block C): calibrated v_R, calibrated a/theory and b/a, margin shares, range factors, corrected m*, seeds and sample sizes, as quoted in D1, D6, D10–D15.
- PDF facts (block D): English 19 pages, Chinese 20 pages; all fonts embedded; no Type 3 fonts; no "??"; figure files fig_01_schematic.png, fig_01_theory.pdf, fig_02 to fig_05 as PDF, fig_06 as PNG; no digits in either abstract.
- Style probes (block E): as in the D20 table.
- Theory: Propositions 1–5 and Corollaries 1–2 re-derived by hand.

### References

[1] Eales O, Riley S. Differences between the true reproduction number and the apparent reproduction number of an epidemic time series. Epidemics 2024;46:100742. https://doi.org/10.1016/j.epidem.2024.100742

[2] Parag KV, Donnelly CA, Zarebski AE. Quantifying the information in noisy epidemic curves. Nature Computational Science 2022;2:584–594. https://doi.org/10.1038/s43588-022-00313-1

[3] Cori A, Ferguson NM, Fraser C, Cauchemez S. A new framework and software to estimate time-varying reproduction numbers during epidemics. American Journal of Epidemiology 2013;178:1505–1512. https://doi.org/10.1093/aje/kwt133

[4] Gostic KM, McGough L, Baskerville EB, et al. Practical considerations for measuring the effective reproductive number, Rt. PLOS Computational Biology 2020;16:e1008409. https://doi.org/10.1371/journal.pcbi.1008409

[5] Wallinga J, Lipsitch M. How generation intervals shape the relationship between growth rates and reproductive numbers. Proceedings of the Royal Society B 2007;274:599–604. https://doi.org/10.1098/rspb.2006.3754

[6] Lande R, Engen S, Sæther B-E. Stochastic Population Dynamics in Ecology and Conservation. Oxford University Press; 2003.

[7] Engen S, Bakke Ø, Islam A. Demographic and environmental stochasticity: concepts and definitions. Biometrics 1998;54:840–846. https://doi.org/10.2307/2533838

[8] Cochran WG. Sampling Techniques. 3rd ed. Wiley; 1977.

[9] Carroll RJ, Ruppert D, Stefanski LA, Crainiceanu CM. Measurement Error in Nonlinear Models: A Modern Perspective. 2nd ed. Chapman and Hall/CRC; 2006. https://doi.org/10.1201/9781420010138

[10] Gelman A, Loken E. The statistical crisis in science. American Scientist 2014;102:460–465. https://doi.org/10.1511/2014.111.460

[11] Elsevier. The use of generative AI and AI-assisted technologies in writing for Elsevier. https://www.elsevier.com/about/policies-and-standards/the-use-of-generative-ai-and-ai-assisted-technologies-in-writing-for-elsevier

[12] Lakens D. Equivalence tests: a practical primer for t tests, correlations, and meta-analyses. Social Psychological and Personality Science 2017;8:355–362. https://doi.org/10.1177/1948550617697177

## Part B — 中文

本部分为内部评审意见。被评稿件与本评审在同一任务内完成，是依据第一轮意见撰写的新稿；评审未因同源关系放宽标准。下文所有事实陈述均以稿件文件、附表和 results.json 为据，未采信作者修改说明中的自述。第二轮主要问题编号为 N1–N6，次要问题为 n1–n13，第一轮条目记作第一轮 M3、第一轮 m6 等。

### 1 简要概述

稿件讨论的问题是报告病例增多后再生数估计的精度能改善多少。结论取决于估计目标。对单期再生数，精度随病例量持续提高；对跨期均值 R̄，误差方差趋于环境方差 v_R 而停止下降。命题 1 给出单期均值的误差方差 V = v_R + A/m，其中 A = R̄ + ρ(R̄² + v_R)/k，并定义平衡规模 m× = A/v_R。命题 2 表明，相对方差为 τ² 的乘性报告波动会在下限上增加 v_H = τ²(R̄² + v_R)。命题 3 给出成本最优病例量 m* = √((c0/c1)m×)，推论 1 给出扩大覆盖优于提高完整度的条件。附录 B 另含 Fisher 信息界、预算公式 B† 与季间精度结果。

实证部分使用 NHSN 全美 50 州及哥伦比亚特区的流感周住院数（21641 个辖区周，2020-08-08 至 2026-10-10），分析两种统计量：加权增长比 G = C_{t+1}/D_t 与更新型比值 R_A = (1 + rθ)^α。仿射模型 E(L | D) = a + b/D 以可行广义最小二乘拟合，并采用州与周双向自助法。在四个季节按规则界定的早期增长窗口中，R_A 的 a = 0.0150（95% CI：0.0100，0.0208），b/a = 37.4（19.1，71.0）；G 的 a = 0.0840（0.0498，0.1248），b/a = 23.5（8.4，59.7）。截距约一半为同一日历周内各州共有的成分。不含下限的幂律拟合几乎同样好（p = 0.114 至 0.438）。已知真值的仿真表明，两种统计量的截距均不等于 v_R/R̄²。按医院报告完整度校正后，截距变化在 τ0 = 0.10 的预设界值内与零等效，在 τ0 = 0.05 时不等效。稿件另以 Delphi 实验室数据作第二代理变量。

本轮修改幅度大，回应了第一轮的大部分意见。理论已与生态学和抽样理论的先行工作对照；推断全程采用双向聚类；截距分解为全国周成分与州季成分，下限的成立被明确限定于仿射模型形式；中英两版在全部核查数字上一致。遗留问题集中在解释层面。稿件做了可校准实证截距的仿真却未加以应用，一旦应用，讨论部分有两项结论随之反转（N1）。标题仍声称存在不可约下限，稿件自身却承认数据未能确立这一下限（N2）。关于报告因素的结论措辞超出等效检验所能支持的范围（N5）。与 Parag 等 [2] 的定位、作者署名与代码归档仍不完整（N3、N6）。

### 2 优点

- S1。理论推导正确。评审逐一重推了命题 1–3、推论 1 以及命题 4–5 与推论 2，并依所给公式复现了基线取值 A = 2.1232、m× = 53.1、v_H = 0.0307（τ = 0.15）与 m* = 14.6 至 22.2（c0/c1 = 10）。
- S2。贡献定位已有改进。讨论部分点明了生态学中人口统计方差与环境方差的分解 [6, 7]，背景部分给出两阶段抽样的类比 [8]；各命题以 (n, ρ) 表述，命题 1(iv) 将下限限定于条件无偏估计量。
- S3。推断显著加强。全部区间均为双向自助法百分位区间。稿件报告 a 的自助标准差为仅按州重抽时的 1.95 至 4.68 倍，第一轮指出的聚类问题因此得以直接呈现。
- S4。识别分析如实陈述。剔除全国周效应后 a 下降 41% 至 52%，正文照实报告；稿件同时说明平台检验缺乏检验力，并得出数据与下限相容但未能确立下限的结论。
- S5。已知真值仿真（第 3.2 节，图 3）有重要价值。它表明表观统计量的截距不等于 v_R/R̄²，b/a 也只能在统计量自身尺度上得到恢复。
- S6。多重比较与检验力处理明确，包括报告检验力的双单侧等效检验、对 40 项检验的 Holm 与 Benjamini–Hochberg 校正，以及病原体比较中的无环境变异零模型。该零模型表明，q1 小于 1 且 q2 大于 1 的格局在没有环境变异时同样会出现，稿件对此也有说明。
- S7。可追溯性高。由 results.json 格式化得到的 131 个关键数字在中英文源文件中全部检出（A 段，0 项失败）。代码包含各分析模块脚本、图表生成脚本、附 SHA-256 的原始数据快照以及 run_all.sh。
- S8。版式大体符合范文。章节顺序为引言、背景、结果、讨论、结论、方法；摘要（PDF 文本 279 词）不含数字；六幅数据图采用面板外粗体字母、带标题的框内图例与 Dark2 配色；图注 119 至 141 词，不含结果数字；无未解析引用，字体全部嵌入。

### 3 缺点

#### 主要问题

- N1。仿真校准已报告而未使用。第 3.2 节得出无噪声截距对 G 为 v_R/R̄² 的 2.68 倍，对 R_A 为 0.484 倍；第 3.3 节与讨论部分却仍按未校准的对应关系比较实证截距。应用校准后，两种统计量所隐含的 v_R 均约为 0.044–0.045，落在假设区间 0.04 至 0.08 之内，与隐含 v_R 低于每一个假设值的表述相矛盾。G 的截距由理论值的 3.1–6.2 倍降至 1.2–2.3 倍，校准后的理论 b/a 区间也覆盖了实证值。校准本身依赖与数据有差别的仿真设定，其不确定性未被传递。
- N2。标题夸大了结论。跨 T 期合并估计的下限为 v_R/T，随期数增加而下降；命题 1(iv) 只对条件无偏估计量成立，附录 B.5 表明收缩估计可低于该下限；稿件的讨论部分也承认数据未能确立下限。
- N3。与最接近的先行工作的对照仍不完整。讨论部分把 Parag 等的信息论分析概括为泊松模型且信息随病例数增长。Parag、Donnelly 与 Zarebski（2022）[2] 的方程 5 已包含时变报告比例，补充说明中还推广到负二项噪声。第一轮 D2 已要求作此对照。
- N4。实证对象仍为表观统计量。R_A 是周增长率的 Wallinga–Lipsitch 变换 [5]，方法部分也写明它不是 R_t 的后验估计，标题与摘要却仍以再生数估计立论，且未报告含入院延迟的更新模型估计。
- N5。报告因素的结论强于证据。τ0 = 0.10 时的等效界值为截距的 10% 至 17%；τ0 = 0.05 时不等效，G 的检验力为 0。界值在拟合前确定的说法无从核实，界值公式还用到统计量的样本均值。实验室代理解释了 R_A 截距的 0.230（95% CI：0.043，0.418），由于实验室增长率自带噪声，这一数值含义不明。自愿报告时期 log G 的离散度高出 58%。
- N6。分析历程与投稿合规不完整。窗口规则在分析过程中修订过，本轮又把 R_A 提升为主统计量，此前各轮分析只记录在稿件之外。作者栏与 CRediT 声明仅署 Apevon Science，没有自然人作者；代码没有归档 DOI。

#### 次要问题

- n1。讨论称 b/a 在不同设定间相差四倍，实际 R_A 为 3.9 倍，G 为 7.1 倍。
- n2。设计结果（m*、B†）采用未经分母校正的日历窗口 m× 区间，而第 3.3 节主张校正后的区间才适用。
- n3。图 6D 采用统计量尺度上的 b/a = 37.4，仿真对应的名义尺度值约为 43。
- n4。图 6B 图注把相对标准误的下界称为精度的下界。
- n5。方法部分只写了一个自助法种子，代码实际使用四个。
- n6。同一窗口内 R_A 与 G 的样本量不同（1748 与 1756；1263 与 1267），正文未作说明。
- n7。交叉验证在正文中按季节留一报告，在表 S2 中按州留一报告。
- n8。表 S6 中截距比的区间下界出现负值。
- n9。正文给出 Δa 的 95% 区间，等效检验与表 S3 使用 90% 区间；图 4B 分箱误差棒未考虑聚类。
- n10。数字格式不统一，表格用千分位而正文不用；英文 PDF 中代码网址在主机名内部断行。
- n11。与范文在章节比例、篇幅、we 的用量、参考文献格式、关键词和图件格式上尚未完全对齐。
- n12。中英两版在页眉、生成式 AI 声明和中文正文字体上存在差异。
- n13。关于低报告完整度的唯一直接证据（自愿报告时期）指向报告效应，摘要未提及。

### 4 详细意见

每条意见依次给出位置、问题、重要性、修改要求以及核查方法与结果。编号后的方括号对应上文的缺点条目。

D1 [N1]。位置：第 3.3 节末段（results.tex 第 58 行）；讨论第 4 段（discussion.tex 第 8 行）；第 3.2 节与图 3C。
- 问题：第 3.2 节报告，G 的无噪声截距中位数为 v_R/R̄² 的 2.68 倍，R_A 为 0.484 倍。第 3.3 节随后称 R_A 截距隐含 v_R = 0.0217，低于假设值 0.04、0.08 和 0.16 中的每一个，又称 G 的实证截距为理论值的 3.1 至 6.2 倍。两处比较都没有用到稿件刚刚估计出的校准系数。应用校准后，R_A 截距在 R̄ = 1.2 时隐含 v_R = 0.0444，按样本均值 1.206 计为 0.0449；G 截距隐含 0.0451；改用仿真斜率或按基线情景比例换算，结果为 0.0435 至 0.0445。两种统计量由此相互吻合，隐含的 v_R 位于假设值 0.04 与 0.08 之间。G 的截距在规则窗口中降为理论值的 1.2 至 2.3 倍，在日历窗口中为 1.3 至 2.6 倍。将经分母校正的理论 b/a 乘以仿真恢复比 0.328，规则窗口得 13.4 至 28.7，日历窗口得 12.8 至 27.4，均覆盖实证值 23.5 和 22.6。
- 重要性：讨论部分据此得出两项结论，一是超出 v_R 的部分不能解释为未建模的传播方差，二是实证 b/a 只有在非环境成分很大时才能吻合。按稿件自己的校准，这两项结论都会反转。
- 修改要求：在第 3.3 节应用校准，报告隐含 v_R 及合并了自助法与仿真不确定性的区间，并相应改写讨论第 4 段和局限性段落。若作者认为校准不可靠（见 D2），应明确说明，并将校准前后的数值并列给出。
- 核查：revised_checks.py 的 C 段。输入为表 S1 的 a 与 R̄，以及 results.json 中的校准系数 2.68、0.484 和恢复比 0.328。输出为 R_A 的 v_R = 0.0444（R̄ = 1.2）与 0.0449（R̄ = 1.206），G 的 v_R = 0.0451，校准后 a 与理论值之比 1.16–2.33（规则）和 1.29–2.58（日历），校准后 b/a 13.4–28.7（规则）和 12.8–27.4（日历）。

D2 [N1]。位置：方法部分表观统计量仿真一段（methods.tex 末段）；代码 s08_sim_apparent.py。
- 问题：校准所依赖的仿真设定在四方面与数据不同。
  - 仿真取 R̄ = 1.2，而规则窗口中 G 的均值为 1.724（表 S1）。比值统计量的偏差随增长率变化，G 的系数 2.68 未必可以直接套用；R_A 的均值 1.206 与仿真值接近。
  - 周 R 在州与周之间独立抽取。数据显示截距有 41% 至 52% 属于全国周成分，仿真中没有共同冲击。
  - R_A 使用的代际间隔与生成数据时相同，其校准因此偏乐观。
  - 入院延迟（均值 5.5 天，标准差 3.0 天）为假设值，每个仿真窗口只有六个观测周。
- 重要性：D1 表明主要实证结论取决于这一校准。校准须与数据足够匹配才能使用，否则需要给出其不确定性。
- 修改要求：按各窗口的实证增长率重新仿真，加入占比与分解结果一致的全国周冲击，对 R_A 使用误设的代际间隔（即已用过的 2.2 天和 4.3 天两种变体），并采用各窗口实际的观测周数；报告校准系数及其在重复间的离散程度。
- 核查：仿真设计取自 methods.tex 与 s08_sim_apparent.py（Rw = rng.gamma(shp, RBAR/shp, (S, W))，州与周之间独立；500 个州，20 次重复，17 个情景，预热 4 周，观测 6 周）。

D3 [N2]。位置：标题；命题 1(iv)（background.tex）；附录 B.5；讨论第 5 段（discussion.tex 第 10 行）；表 S2 注。
- 问题：不可约的说法在三方面缺乏支持。其一，跨 T 期合并的均值误差为 v_R/T + A/(Tm)，下限随期数增加而下降（命题 3）。其二，下限只对条件无偏估计量成立（命题 1(iv)），附录 B.5 表明，当 Δ² 小于 v_R(1 + m/m×) 时收缩估计可低于 v_R。其三，平台检验的 p 值为 0.114、0.438 和 0.418，表 S2 注说明估计截距的任何比例都无法以 80% 检验力检出，讨论部分也认为数据未能确立下限。范文风格要求标题陈述研究问题，不陈述结论。
- 重要性：标题是多数读者引用的依据。
- 修改要求：中英文标题同步修改，可考虑改为 Case volume and the precision of reproduction number estimates under environmental and reporting variation（环境变异与报告变异下病例量与再生数估计精度），并从关键词中删去 Error floor。
- 核查：逐处阅读上述位置；p 值与检验力表述与 results.json 一致（A 段）。

D4 [N3]。位置：讨论第 3 段（discussion.tex 第 6 行）；引言（引用 parag2022fundamental 处）。
- 问题：讨论部分称 Parag 等的分析以泊松分布刻画给定既往发病数下的发病数，并得出信息随病例数增长的结论。Parag、Donnelly 与 Zarebski（2022）[2] 的方程 5 表明，含噪流行曲线的信息量按时变报告比例的几何均值缩放，其补充说明还将结果推广到负二项噪声。讨论部分的概括有所遗漏，遗漏的方向恰好抬高了命题 2 的新颖性。新增的生态学 [6, 7] 与抽样理论 [8] 先行工作解决了第一轮 M1 的另一半。
- 重要性：[2] 是关于报告噪声与信息量最接近的已有结果，Epidemics 审稿人很可能首先核查这一对照。
- 修改要求：说明报告比例对信息量的影响已有结论 [2]，再从三方面将命题 2 与 [2] 的方程 5 对照，即估计目标（R̄ 与 R_t）、噪声模型（均值为 1 的乘性冲击与报告比例）以及后果（加性下限与信息比）。
- 核查：将 discussion.tex 第 6 行与第一轮对 [2] 方程 4–5 及 Ranking noise sources by their information loss 一节的精读结果对照。

D5 [N4]。位置：方法第 6.2 节（R_A 的定义）；附录 A.7；标题与摘要。
- 问题：R_A = (1 + rθ)^α 是周增长率的 Wallinga–Lipsitch 变换 [5]，代际间隔取伽马分布（均值 3.6 天，标准差 1.6 天）。方法部分正确地写明它是观测增长的变换，不是 R_t 的后验估计。仿真表明 R_A 会削弱环境方差，其截距仅为 v_R/R̄² 的 0.484 倍。标题与摘要仍称再生数估计，稿件也未报告含入院延迟的更新模型估计（如 EpiEstim [3]）。第一轮 M2 要求给出规范的 R_t 估计或重新标注实证对象，本轮仅在方法部分重新标注。
- 重要性：监测工作者会把结论理解为适用于 Cori 等 [3] 与 Gostic 等 [4] 所述类型的 R_t 估计。
- 修改要求：或者增加含感染至入院延迟的更新模型分析并报告其后验均值的截距，或者在标题、摘要和结论中写明实证结果针对的是基于增长率的统计量。
- 核查：methods.tex 第 6.2 节与 results.tex 第 38 行。

D6 [N5]。位置：摘要；第 3.4 节第 1 段（results.tex 第 70 行）；讨论第 6 段（discussion.tex 第 12 行）；方法第 6.5 节；表 S3。
- 问题：摘要与讨论称医院报告完整度只解释了截距中可忽略的部分，证据支持的范围更窄。
  - G 的 Δa 为 0.0004（95% CI：−0.0036，0.0033），R_A 为 0.0003（−0.0003，0.0010），两者在 τ0 = 0.10 时均与零等效。τ0 = 0.10 的界值分别为截距的 12%（G，规则窗口）、10%（G，日历窗口）和 17%（R_A），检验只能表明校正使 a 的变化小于其十分之一至六分之一。
  - τ0 = 0.05 时两者均不等效，真实变化为零时 G 的检验力为 0，R_A 为 0.25。
  - 界值 δ = κ²τ0²(1 + v_R/R̄²) 用到分析窗口内统计量的样本均值，并不独立于数据；界值在拟合前确定的说法也没有带日期的记录作支撑。
  - 校正方法是用报告医院占比去除病例数，不涉及报告医院内部的检出变化，例如检测强度或编码方式。
- 重要性：一个只能排除 10% 至 17% 以上变化、在更严界值下检验力为零的检验，不足以支持可忽略这样的强表述。
- 修改要求：将可忽略改为检验所支持的界限，例如截距变化小于其数值的 17%；说明界值依赖样本均值；提供界值确定时间的记录，或删去拟合前确定的说法；补充一句关于医院内部检出变化的讨论。
- 核查：C 段给出界值占比 0.121（G，规则）、0.102（G，日历）和 0.170（R_A）；Δa 区间与检验力数值与 results.json 一致（A 段）。

D7 [N5]。位置：第 3.4 节（results.tex 第 70 行）；方法第 6.5 节；表 S4 注。
- 问题：在有实验室数据的 44 个州中，实验室增长率解释了 R_A 截距的 0.230（95% CI：0.043，0.418），相关系数为 0.31。实验室增长率同时包含传播信号与其自身的抽样和检测噪声，在经典测量误差下，共有份额会向零衰减 [9]。0.23 因而无法区分传播份额确实较小与代理变量噪声较大这两种情形，余下的 77% 也不能直接归于环境方差。另有七个辖区（ak、dc、de、nh、ny、ri、ut）缺少实验室数据。
- 重要性：稿件以该代理变量支持报告因素不是截距来源的结论，而该结果与多种解释都相容。
- 修改要求：报告实验室增长率的信度（如分半相关）及经衰减校正的份额；把 0.23 表述为无法区分各种解释的核查结果；给出限定于这 44 个州的主要估计。
- 核查：data_decision.md 与表 S4 注（Delphi 临床实验室数据，1224 个州周）。

D8 [N6]。位置：方法第 6.1 节；output/case-count-bottleneck/experiment/analysis/data_decision.md。
- 问题：窗口规则的第一版以季节最大值为窗口终点，于 2026-10-20 被替换。稿件称替换发生在新窗口上拟合任何截距之前，但第一版此前已经用过。本轮又把 R_A 定为主统计量，把日历窗口降为次要设定。此前的分析轮次（r3、r4）只记录在 data_decision.md 中，期刊读者看不到。每项选择单独看都有道理，合在一起便构成第一轮 M7 所指的分岔路径问题 [10]。
- 重要性：判断关键估计时需要知道尝试过哪些设定以及先后顺序。
- 修改要求：在补充材料中加一张分析历程表，逐项列出各设定的角色、采用时间、a 与 b/a。关键估计彼此落在对方的区间内，稿件可以直接说明这一点。
- 核查：methods.tex 第 6.1 节；data_decision.md；第一轮稿件只分析了 G。

D9 [N6]。位置：作者栏（main.tex 第 95 行）；CRediT 声明与代码可得性声明（endmatter.tex）。
- 问题：唯一作者为 Apevon Science，CRediT 声明也把全部角色归于 Apevon Science。Elsevier 政策规定 AI 工具不得列为作者，作者须为对研究负责的自然人 [11]。代码可得性声明指向 GitHub 仓库，没有归档 DOI，修改说明对此已有坦白（第一轮 M8）。
- 重要性：无论学术质量如何，这两点都会妨碍向 Epidemics 投稿。
- 修改要求：列出自然人作者及其单位、ORCID 和各自的 CRediT 角色；将代码包存入 Zenodo 或同类归档库并引用其 DOI。
- 核查：main.tex、endmatter.tex 与 revision_response.md（M8 标为部分完成）。

D10 [n1]。位置：讨论第 5 段（discussion.tex 第 10 行）；第 3.3 节第 3 段。
- 问题：讨论称 b/a 在不同设定间相差四倍。R_A 的范围为 24.7 至 97.1（3.9 倍），G 为 12.2 至 86.8（7.1 倍）。
- 修改要求：分别给出两个倍数。
- 核查：C 段（RA_ba_range_factor = 3.93，G_ba_range_factor = 7.09）。

D11 [n2]。位置：第 3.1 节第 3 段；图 2C；附录 B.2；表 S7。
- 问题：m*（c0/c1 = 10 时为 14.6 至 22.2，c0/c1 = 100 时为 46.2 至 70.1）与 B†（655 至 763）采用未经校正的日历窗口区间 m× = 21.3 至 49.2，而第 3.3 节主张经分母校正的区间（38.9 至 83.5）才是适用于 G 的理论值。按校正区间计算，m* 为 19.7 至 28.9 和 62.4 至 91.4。
- 修改要求：说明所用区间及理由，或两者并列。
- 核查：C 段（m_star_c10_using_delta_corrected_range，m_star_c100_using_delta_corrected_range）。

D12 [n3]。位置：图 6D 及其图注。
- 问题：设计曲面采用统计量尺度上 R_A 的 b/a = 37.4，按仿真恢复比 0.849 换算，名义尺度值约为 43。图注称该面板仅作示意，但未说明所用尺度。
- 修改要求：在图注中注明尺度，或改用名义尺度值。
- 核查：C 段（RA_ba_nominal_scale_via_sim_nom_ratio = 43.1）。

D13 [n4]。位置：图 6B 图注。
- 问题：图注将以相对标准误表示的量称为季间方差估计精度的下界。相对标准误的下界对应精度的上界。
- 修改要求：改为季间方差估计值相对标准误的下界。

D14 [n5]。位置：方法部分（种子 20261024 的表述）；s02_inference.py。
- 问题：双向自助法各模块使用四个种子，即 20261024（R_A，规则）、20261124（G，规则）、20261224（G，日历）和 20261324（R_A，日历）。
- 修改要求：说明种子设置方案。
- 核查：C 段（seeds_twoway_blocks）。

D15 [n6]。位置：表 S1；第 3.3 节第 1 段。
- 问题：同一规则窗口内 R_A 的 N 为 1748，G 为 1756；日历窗口中分别为 1263 和 1267。正文未解释差异。
- 修改要求：在表 S1 注中给出剔除规则。
- 核查：表 S1 与 results.json。

D16 [n7]。位置：第 3.3 节第 3 段；表 S2。
- 问题：正文报告按季节留一的验证结果（四折中两折、四折中零折、三折中三折），表 S2 的 CV folds 一列却是按州留一（26/51、19/51、28/51）。方法部分两者都有提及。
- 修改要求：在表 S2 中同时列出两种结果。

D17 [n8]。位置：表 S6。
- 问题：部分截距比的区间下界为负，如 COVID-19 日历窗口 q1 = 0.73（−0.32，0.91）、RSV 增长窗口 q2 = 1.69（−0.22，3.06）。代表方差的截距之比应为正值，负下界来自分母截距为负的自助样本。
- 修改要求：报告此类样本的比例，并在有效样本上于对数尺度计算区间，或将这些区间标为无定义。

D18 [n9]。位置：第 3.4 节第 1 段；表 S3；图 4B。
- 问题：正文给出 Δa 的 95% 区间，检验与表 S3 使用 90% 区间。以 R_A 为例，表 S3 为 0.29（−0.22，0.85）× 10⁻³，正文为 0.0003（−0.0003，0.0010）。两者虽都有标注，但正文读者会拿 95% 区间与界值比较。图 4B 分箱误差棒未考虑聚类，图注与局限性部分对此已有说明。
- 修改要求：正文在检验结果旁给出 90% 区间；图 4B 改用双向自助法误差棒，或删去误差棒。

D19 [n10]。位置：表 S1 与表 S6；表 S4 注；尾部代码可得性声明。
- 问题：表格印作 1,748 和 2,707，正文则写 1748 和 21641，范文不用千分位。表 S4 注写作 0.23（0.043，0.42），正文写作 0.230（0.043，0.418）。英文 PDF 中代码网址在主机名内部断行（https://github.c om/…），复制后无法使用。
- 修改要求：去掉千分位，统一有效位数，网址只在斜杠处断行。
- 核查：tab_s1_headline.tex 第 10–13 行（1{,}748）；逐页查看渲染后的尾部页面。

D20 [n11]。位置：全文。
- 问题：与范文风格档案的比较见下表。

| 项目 | 范文 | 新稿 | 结论 |
|---|---|---|---|
| 标题 | 句首大写，陈述研究问题 | 句首大写，18 词，陈述结论 | 未达到（D3） |
| 摘要 | 250–290 词，不含数字 | 279 词（PDF 文本），不含数字 | 达到 |
| 关键词 | 6–8 个，不重复标题 | 6 个，Error floor 与标题重复 | 部分达到 |
| 章节顺序 | 引言至方法，再接尾部模块 | 相同 | 达到 |
| 章节比例 | 讨论最长（约 30%），结果约 18% | 结果 30.5%，讨论 19.7% | 未达到 |
| 正文篇幅 | 约 5700 词 | 6600 词（detex 计数） | 部分达到 |
| 限定语 | 不用 suggest 与 might | 未出现 | 达到 |
| 第一人称 | 约每 150 词一次 we | 共 8 次 | 部分达到 |
| 数字 | 不用千分位 | 表格使用千分位 | 部分达到（D19） |
| 区间格式 | 全文统一 | 统一并有标注 | 达到 |
| 图 | 仅数据图，Dark2，带框图例，粗体 A–D | 符合，但图 1A 为方框示意图，图 1A 与图 6 为位图 | 部分达到 |
| 图注 | 80–150 词，不含结果数字 | 119–141 词，仅含区间水平 | 达到 |
| 文内引用 | Harvard 作者–年份制 | 作者–年份制 | 达到 |
| 参考文献表 | Surname, I.I., Year. Abbrev. J.；30–45 条；Epidemics 约占 10% | plainnat 格式，名字与刊名均为全称；43 条；Epidemics 4 条（9%） | 部分达到 |
| 尾部模块 | 代码、CRediT、利益冲突、数据、致谢 | 按此顺序齐备，另含 AI 声明 | 达到 |

- 重要性：范文把最多篇幅留给解释，本稿篇幅最长的是结果部分，相当一部分解释性文字写在结果段落中。
- 修改要求：把解释性语句从结果移到讨论，结果部分压缩到约 1200 词，全文删减约 900 词；参考文献改用 Elsevier Harvard 格式；图 1A 与图 6 提供矢量文件；图中字体改用 Times 或度量相同的字体（目前图中嵌入 Liberation Serif，正文为 Times New Roman）。
- 核查：E 段（词数、比例、we 计数、图注长度、文献条数）；D 段（字体列表）；逐页查看渲染页面。

D21 [n12]。位置：两版 PDF；尾部模块。
- 问题：B 段发现两版之间所有数字差异均可解释，包括中文把月份写成数字日期（引言、方法、表 S4），中文 AI 声明提到两次 image-2 超时及改用 TikZ 的过程而英文未提，中文附录有一处标题含超过 1，英文表 S6 把 1 week 和 3 weeks 写成文字。非数字层面仍有三处差异：英文 PDF 有页眉而中文没有；两版 AI 声明内容不同；中文正文使用 Noto Serif CJK SC 而非宋体。
- 修改要求：统一两版 AI 声明的内容；中文版补上页眉；若目标为要求宋体的中文期刊，正文改用宋体。
- 核查：B 段（逐文件数字多重集比较）；D 段（pdffonts）；两版 PDF 前十页逐页查看。

D22 [n13]。位置：摘要；第 3.4 节第 1 段；表 S4。
- 问题：自愿报告时期（报告完整度中位数 45.7%）5 至 10 月 log G 的四分位距为 0.759（95% CI：0.479，1.042），2023 年和 2025 年分别为 0.479 和 0.483。该时期 FGLS 截距不稳定，这一稳健离散度因而是关于低报告完整度的唯一直接证据，而它指向存在报告效应。摘要只报告了强制报告时期的等效结果。
- 修改要求：在摘要和讨论中以与强制报告时期结果同等的分量报告自愿报告时期的结果，并说明季节与报告制度仍部分混杂。
- 核查：表 S4；results.json。

### 5 总体建议

建议：大修（Major revision）。

评分：6 分（满分 10 分）。

理由。评分尺度与第一轮相同。第一轮的 4 分对应理论正确、实证解释缺乏支持且需补做新分析的状态。6 分表示分析已基本到位，但仍至少有一个问题可能改变主要结论，且立论框架仍超出证据。小修（7–8 分）要求剩余问题均不足以改变已陈述的结论。

本轮修改解决了第一轮的大部分问题，包括双向聚类、截距分解、已知真值仿真、多重比较、与生态学和抽样理论先行工作的对照、文献整理以及中英两版的一致性。第一轮九项主要问题中，两项已解决，七项部分解决，没有未解决项（见第 6 节）。

分数未能更高，主要原因在 N1。稿件估计了校准系数却未使用，而应用后讨论部分的两项表述随之反转。修正需要重新运行仿真并改写讨论段落，单靠调整措辞不够。N2 与 N5 需要修改措辞；N4 需要补做分析或收窄结论；N6 所需的署名与 DOI 只能由自然人作者完成。

评审信心：数学、统计与数字溯源方面为高（4/5），均经脚本核查；NHSN 报告完整度与 Delphi 实验室数据的流行病学解释方面为中等（3/5）。本评审属内部评审，这本身也是一项局限，评审无法排除与稿件作者存在共同盲点，投稿前仍宜征求外部评审意见。

### 6 对第一轮意见的回应核查

判定分为已解决、部分解决、未解决三级。证据来自评审对新稿的阅读与核查脚本，未采信修改说明的自述。

| 条目 | 第一轮要求 | 判定 | 证据 |
|---|---|---|---|
| M1 | 与生态学及 Parag 等的工作对照定位 | 部分解决 | 已补生态学与抽样理论先行工作（讨论第 2 段；背景部分）；与 Parag 的对照遗漏报告比例（D4） |
| M2 | 给出规范的 R_t 估计或重新标注对象 | 部分解决 | 新增 R_A 并在方法部分重新标注；标题与摘要未改；无更新模型估计（D5） |
| M3 | 截距与平台的识别 | 已解决 | 周与州季分解、ICC、幂律检验、交叉验证（第 3.3 节；表 S2） |
| M4 | 正确比较理论与数据 | 部分解决 | 已补校正后的 b/a 与仿真；仿真校准未应用（D1、D2） |
| M5 | 聚类推断 | 已解决 | 全程 FGLS 加双向自助法；报告方差膨胀 1.95 至 4.68 倍（表 S1） |
| M6 | 报告异质性 | 部分解决 | 已更名，补等效检验及检验力、实验室代理、自愿报告时期；结论措辞过强（D6、D7、D22） |
| M7 | 预注册与多重比较 | 部分解决 | 已补 Holm 与 BH 校正；披露窗口修订；分析历程在稿件之外（D8） |
| M8 | 复现包 | 部分解决 | 脚本、带 SHA-256 的数据快照、run_all.sh 与作图脚本齐备；无 DOI；种子说明不全（D9、D14）；评审未重新运行全流程 |
| M9 | 呈现方式 | 部分解决 | 命题 4–5 移入附录 B；英文图件；无 ??；正文 6600 词且章节比例倒置（D20） |
| m1 | 常数 0.505 并非普适 | 已解决 | 附录 B.1 写明其对应基线参数组 |
| m2 | 统一使用 √(2/(S−1)) | 已解决 | 推论 2；第 3.4 节；表 S7 |
| m3 | 区分 S = 3 与 S = 4 并使用正确区间 | 已解决 | 表 S5；Q-profile 区间（方法第 6.6 节） |
| m4 | 定义 B† 及其单位 | 已解决 | 命题 5，式 (B.2)；输入区间的选择见 D11 |
| m5 | 等预算下比较各杠杆 | 已解决 | 第 3.1 节；表 S7（7.88） |
| m6 | Wald 数值与一致最优势检验表述 | 已解决 | 删除无法复现的 Wald 数值；附录 B.4 在可达水平上给出 Karlin–Rubin 结论 |
| m7 | 收缩示例使用先知权重 | 已解决 | 附录 B.5 标为理想界，并指出经验贝叶斯为可行替代 |
| m8 | 计数不一致 | 已解决 | 各报告制度的 6009、420、4077 在正文与表格中一致；新出现的 R_A 与 G 计数差异见 D15 |
| m9 | 自愿报告时期存在混杂；工具变量 | 已解决 | 日历匹配比较（表 S4）；已删除工具变量分析 |
| m10 | 措辞过度 | 部分解决 | decisively、confirming、must 等已删；标题、negligible 与 not interpretable 仍在（D3、D6、D1） |
| m11 | 文献整理 | 已解决 | 43 条全部被引；Mathis 名字已更正；核心文献已补；格式与 Elsevier 不同（D20） |
| m12 | D_t 权重与零值 | 部分解决 | 零值插补数据已排除（第 6.1 节）；权重仍无推导，改用等权重时 G 的 b/a 由 23.5 变为 12.2 |
| m13 | 中英文等价 | 已解决 | 131 个关键数字两版全部一致；剩余差异见 D21 |
| m14 | 区间类型 | 已解决 | 统一为双向自助法百分位区间并标注；Δa 的 90% 与 95% 区间问题见 D18 |

合计：主要问题已解决 2 项、部分解决 7 项、未解决 0 项；次要问题已解决 12 项、部分解决 2 项、未解决 0 项。

### 7 数据决策评价

作者保留了 2026-10-20 获取的 NHSN Weekly Hospital Respiratory Data 版本，没有更换数据源，另以 Delphi FluView 临床实验室数据作为辅助代理变量（51 个辖区中的 44 个，1224 个州周）。FluSurv-NET 经评估后因缺少州级信息而未采用。

评审赞同保留 NHSN。第一轮的问题出在统计量定义、推断与解释上，与数据本身无关。NHSN 是唯一同时提供各州周住院数和报告医院占比的数据源，报告分析离不开后者。更换数据源会改变研究对象，也会切断与第一轮结果的衔接。

新增实验室代理变量有用，但不能定论报告问题，原因见 D7，即代理变量自身的测量误差与七个辖区的缺失。自愿报告时期（D22）是 NHSN 中现成的自然实验，应获得比现稿更多的分量。

### 8 核查记录

- 关键数字（A 段）：由 results.json 及分模块文件格式化得到的 131 个数值，在中英文源文件中逐一检出，0 项失败。
- 中英文数字（B 段）：逐文件差异均可解释（中文把月份写成数字日期、AI 声明、附录一处标题、英文表 S6 两处以文字书写的数字），无实质差异。
- 派生量（C 段）：校准后的 v_R、校准后的 a 与理论值之比及 b/a、界值占比、范围倍数、校正后的 m*、种子与样本量，见 D1、D6、D10–D15。
- PDF 事实（D 段）：英文 19 页，中文 20 页；字体全部嵌入；无 Type 3 字体；无 ??；图件为 fig_01_schematic.png、fig_01_theory.pdf、fig_02 至 fig_05 的 PDF 与 fig_06 的 PNG；两版摘要均不含数字。
- 风格探针（E 段）：见 D20 表。
- 理论：命题 1–5 与推论 1–2 经人工重推。

### 参考文献

[1] Eales O, Riley S. Differences between the true reproduction number and the apparent reproduction number of an epidemic time series. Epidemics 2024;46:100742. https://doi.org/10.1016/j.epidem.2024.100742

[2] Parag KV, Donnelly CA, Zarebski AE. Quantifying the information in noisy epidemic curves. Nature Computational Science 2022;2:584–594. https://doi.org/10.1038/s43588-022-00313-1

[3] Cori A, Ferguson NM, Fraser C, Cauchemez S. A new framework and software to estimate time-varying reproduction numbers during epidemics. American Journal of Epidemiology 2013;178:1505–1512. https://doi.org/10.1093/aje/kwt133

[4] Gostic KM, McGough L, Baskerville EB, et al. Practical considerations for measuring the effective reproductive number, Rt. PLOS Computational Biology 2020;16:e1008409. https://doi.org/10.1371/journal.pcbi.1008409

[5] Wallinga J, Lipsitch M. How generation intervals shape the relationship between growth rates and reproductive numbers. Proceedings of the Royal Society B 2007;274:599–604. https://doi.org/10.1098/rspb.2006.3754

[6] Lande R, Engen S, Sæther B-E. Stochastic Population Dynamics in Ecology and Conservation. Oxford University Press; 2003.

[7] Engen S, Bakke Ø, Islam A. Demographic and environmental stochasticity: concepts and definitions. Biometrics 1998;54:840–846. https://doi.org/10.2307/2533838

[8] Cochran WG. Sampling Techniques. 3rd ed. Wiley; 1977.

[9] Carroll RJ, Ruppert D, Stefanski LA, Crainiceanu CM. Measurement Error in Nonlinear Models: A Modern Perspective. 2nd ed. Chapman and Hall/CRC; 2006. https://doi.org/10.1201/9781420010138

[10] Gelman A, Loken E. The statistical crisis in science. American Scientist 2014;102:460–465. https://doi.org/10.1511/2014.111.460

[11] Elsevier. The use of generative AI and AI-assisted technologies in writing for Elsevier. https://www.elsevier.com/about/policies-and-standards/the-use-of-generative-ai-and-ai-assisted-technologies-in-writing-for-elsevier

[12] Lakens D. Equivalence tests: a practical primer for t tests, correlations, and meta-analyses. Social Psychological and Personality Science 2017;8:355–362. https://doi.org/10.1177/1948550617697177
