# Third-round peer review of the revised manuscript, with final-revision addendum

Final recommendation after the final revision: Minor revision (editorial only), 8.5 out of 10 (Section 11 in each part). The round-3 verdict on the version reviewed below was Minor revision, 7.5 out of 10.

- Manuscript: "Scaling limits and surveillance design for epidemic reproduction numbers under environmental and reporting stochasticity" (English, 24 pages) and its Chinese version "环境随机性与报告异质性下疫情再生数监测的尺度极限与资源配置设计" (24 pages). Target journal: Epidemics.
- Version reviewed: output/case-count-bottleneck/paper/ (paper.pdf, paper.html, LaTeX and BibTeX source, Tables S1–S9) and output/case-count-bottleneck-zh/paper/. The reproduction package is in output/case-count-bottleneck/experiment/ (code, data snapshot, analysis/results.json). The two language versions are reviewed as one manuscript.
- Review date: 20 October 2026
- Benchmark article: Eales and Riley (2024), Epidemics 46:100742 [1].
- Previous rounds: review_original.md (Major revision, 4 out of 10) and review_revised.md (Major revision, 6 out of 10). This review uses the same 1–10 scale and the same standard.
- Declaration: this is an internal review of a manuscript revised within the same task. The revision was guided by an author plan that set a target score of 8.5 to 9.5. The reviewer treated that range as the authors' goal and scored the manuscript independently. Every factual statement below was checked against the manuscript files and results.json, not against the authors' description of their changes.
- Verification: the check script is round3_checks.py and its output is round3_checks.json, both in .work/case-count-bottleneck/review/checks/. Block A checks 94 headline numbers against results.json in both languages; block B compares the numbers in the two language versions file by file; block C computes the derived quantities quoted in this review; block D records PDF facts; block E probes the wording. Both PDFs were rendered and every page was inspected. Every number in this review traces to a key in round3_checks.json or results.json (Section 9).
- Author to-dos, not scored: human author names, affiliations, funding, the CRediT statement and an archival DOI for the code. The manuscript currently carries the placeholder "Apevon Science". The authors have said they will complete these items themselves. The reviewer lists them in Section 10 and has not deducted points for them.

Part A is the English review and Part B is the Chinese review. They use the same numbering and give the same verdict and score. Third-round major weaknesses are P1–P4 and minor ones p1–p8. Second-round items are cited as N1–N6 and n1–n13.

## Part A — English

### 1 Summary

The manuscript asks how much the precision of a reproduction-number estimate improves when more cases are reported. Proposition 1 gives the error variance of the mean reproduction number per period as V(m) = v_R + A/m. Here A = R̄ + ρ(R̄² + v_R)/k, and the balance scale m× = A/v_R marks where environmental variation starts to dominate. Proposition 2 adds reporting volatility, v_H = τ²(R̄² + v_R). Proposition 3 gives the cost-optimal case volume m* = √((c0/c1)m×). The appendix adds a Fisher-information bound, a budget rule and a limit on between-season precision.

The empirical part fits E(L | D) = a + b/D by feasible GLS with a two-way bootstrap. The data are NHSN weekly influenza admissions, 10506 state-weeks from 2020 to 2026, analysed in rule-defined early-growth windows of four seasons. Two apparent statistics are used, a renewal-type ratio R_A and a weighted growth ratio G. The main change in this round is a two-step inversion (Section 3.3; Methods 6.8). A data-matched simulator maps each statistic's intercept to the latent environmental variance. This gives v_R = 0.040 (95% CI: 0.026, 0.056) from R_A and 0.043 (0.025, 0.064) from G. The ratio of the two is 0.93 (0.78, 1.18), although their scale factors differ by a factor of 5.3. A national-week component accounts for 41% to 51% of the intercept. Under mandatory reporting, adjustment for facility completeness changes the R_A intercept by 2.0% (upper bound 5.3%). In the 2024 voluntary period, the interquartile range of log growth was 1.58 times (0.95, 2.23) that of 2023. A design nomogram (Fig. 6) converts the estimates into observation weeks and pooled jurisdictions.

The revision has dealt with the most serious second-round problem. The calibration is now applied with a simulator matched to the data, and its uncertainty is propagated. The authors also corrected two numbers from the round-2 review that this reviewer had derived from generic-scenario factors: v_R about 0.045, and a calibrated b/a range of 13.4 to 28.7. The data-matched values replace them, and the paper reports honestly where they fall. Both implied variances sit at the lower edge of the 0.04–0.08 band, and both intervals extend below it. The empirical b/a lies above the calibrated ranges, at the 93rd and 91st simulated percentiles. The remaining problems are in how these results are framed. The policy sentence in the abstract and Conclusion claims more than the reporting analysis shows (P1). The agreement between the two statistics is presented as validation, but the simulations show it is a weak test (P2). The level of v_R depends on assumptions that the abstract does not state (P3). One containment claim about the balance scale, carried over from the previous version, is contradicted by the calibrated ranges (P4).

### 2 Strengths

- S1. The theory is correct and complete. The reviewer re-derived Propositions 1–5 and Corollaries 1–2 in earlier rounds. The baseline values A = 2.1232, m× = 53.1 and v_H = 0.0307 are unchanged and reproduce.
- S2. The two-step inversion is a real methodological gain. The simulator matches the data in window lengths (9, 12, 8 and 13 weeks), state count, national-week share and dispersion. It has 200 panels at each of four values of v_R, and Methods 6.8 states the calibration line E(â) = γ0 + γ1 v_R. The data-matched scale factors (κ = 0.516 for R_A, 2.729 for G) are close to the noise-free limits (0.493, 2.745) and to the bridge design (0.485, 2.698), so the mapping is stable.
- S3. The results are reported honestly. Section 3.3 says that "both point values lie at the lower edge of the band … both intervals extend below it". It reports the b/a excess and its simulated percentiles. Section 3.3 also reports agreement in nine of ten settings, the synchronous count-shock exception and the range 0.013–0.063 across settings, which is driven by the generation interval. Discussion paragraph 4 names three qualifications.
- S4. The sensitivity design is informative. Ten settings vary the national share, autocorrelation, generation interval, reporting delay, offspring dispersion and the type of shock. Table S8 reports all of them, including the unfavourable ones.
- S5. The reporting analysis is careful in the Results and Discussion. The voluntary-period contrast has a placebo (2025/2023 ratio 1.01), matching on reporting scale (1.68) and on calendar month (median 1.33), and two other pathogens. Discussion paragraph 7 states that the contrast is observational and "do[es] not identify a causal effect of the reporting mandate".
- S6. The second-round minor items are largely fixed: the corrected b/a factors (n1), seeds (n5), the extra eight state-weeks (n6), CV labels (n7), "n.d." for undefined lower bounds (n8), 90% intervals for Δa (n9), thousands separators (n10) and the voluntary period in the abstract (n13).
- S7. Traceability remains high. All 94 headline numbers in block A were found in both language versions (0 failures), including every number in the abstract. Block B finds no substantive difference between the versions. The Chinese figures carry Chinese labels.
- S8. The Scope and extensions paragraph keeps the paper's claims inside its model class. The abstract and title no longer assert an "irreducible" floor, and no overclaiming terms (perfect, universal, 首次, 普适) appear. 证明 appears only as the heading of proof environments.

### 3 Weaknesses

#### Major

- P1. The policy conclusion outruns the reporting evidence. The abstract ends: "mandatory and complete reporting and additional periods and regions improve the precision of surveillance more than additional cases per period". The Conclusion repeats this, and Discussion paragraph 8 adds that "standardising reporting reduced error more than a tenfold increase in case volume". Under the mandate, completeness explains 2.0% of the R_A intercept (upper bound 5.3%). The voluntary-period contrast is observational, and its interval (0.95, 2.23) includes 1. The tenfold statement comes from the hypothetical example τ = 0.15, in which reporting accounts for 35% of the MSE. That is about seven times the empirical upper bound.
- P2. The agreement between the two statistics is presented as validation it cannot provide. The abstract says the estimates "agree although the statistics scale latent variance by factors that differ fivefold". Discussion paragraph 4 adds that agreement "would be unlikely if one statistic were dominated by its own construction" and that the calibration "closes the loop" (形成闭环 in the Chinese version). In the simulations, however, the statistics agreed in nine of ten settings. Those include settings in which the implied v_R moved by factors of 0.33 to 1.45. "Agree" here means only that the 95% interval of the difference contains zero. The data-matched interval for the ratio (0.78, 1.18) is not inside a conventional equivalence band of 0.8 to 1.25. The count-shock interval (0.39, 0.90) overlaps the observed one over 0.78 to 0.90. The agreement is therefore a consistency check. It rules out only a pure synchronous shock to counts.
- P3. The level of v_R is conditional, and the abstract does not say so. The implied variance depends on the generation interval: 0.013 when it is 2.2 days and 0.058 when it is 4.3 days. It also depends on independence across weeks: an AR(1) process with φ = 0.5 gives 0.027 and 0.025. The R_A estimate falls in the 0.04–0.08 band in only 4 of the 10 settings, and G in 7. Discussion paragraph 4 names the generation-interval dependence but not autocorrelation. The data can inform the second condition, and external serial-interval estimates [7] can bound the first. Neither is used.
- P4. The balance scale is compared across scales. Section 3.1 (results.tex line 26) and Appendix B.2 (appendix.tex line 135) state that the scenario range 21.3 to 49.2 "contains the empirical estimate for R_A". That range is on the latent scale of Proposition 1 and is uncalibrated. On the statistic scale, the calibrated R_A range 13.9–31.1 does not contain 37.4. The abstract gives 37.4 as "the balance scale" right after defining m× = A/v_R, without saying that it is on the scale of the statistic. The reader is not told how it relates to the latent m× of the theory. The b/a excess (empirical over data-matched point: 1.34 for R_A, 1.45 for G) is described in the Discussion but has no tested explanation.

#### Minor

- p1. The national-week variance share in the simulator, 0.45 v_R, was set by design (methods.tex line 77). The simulated national share (0.43) and ICC (0.258) therefore match the data (0.41 and 0.253) partly by construction. Without a national shock the simulated ICC is 0.050. Methods 6.8 should state how 0.45 was chosen. Discussion paragraph 4 should call the match a consistency check, not a reproduction.
- p2. The title still names "reproduction numbers". The analysis uses apparent statistics with a fixed generation interval and no explicit delay distribution, and no renewal estimate with an external generation interval is reported. This is the remaining part of N4.
- p3. The τ = 0.15 example in Section 3.1 and Discussion paragraph 8 should be labelled hypothetical wherever it supports a recommendation (see P1).
- p4. The abstract gives "within an equivalence margin of 17%" without the margin parameter τ0 = 0.10. At τ0 = 0.05 the margins shrink to 4.3% (R_A) and 3.0% (G) of the intercept, equivalence is not shown, and the power is 0.25 and 0.
- p5. The abstract has 281 words and many numbers; the benchmark abstract has none. The clause "as in 55% of state-weeks here" follows the count of 10506 state-weeks. The 55% is the share of rule-window rows above 37.4, not of the full panel. It also depends on a balance scale whose interval runs from 19.1 to 71.0.
- p6. The main text has grown to about 8288 words, from about 6600 in round 2; Results alone has 2827. The sensitivity detail in Section 3.3 could move to Table S8 without loss.
- p7. Formatting. The Chinese version has no running heads, while the English version has them. In the English PDF the Delphi URL breaks inside the host name (api.delp|hi.cmu.edu). English page 22 (Tables S8–S9) has a large blank area. The value labels 0.040 and 0.043 in Fig. 3A overlap the drop lines. The PDF Title metadata of both versions is empty.
- p8. The laboratory proxy shares 0.230 of the intercept, and the Discussion explains why that share is attenuated towards zero. A reliability correction would turn the value into a bound. The authors list it as not done. It is optional.

### 4 Detailed comments

Each comment gives the location, the problem, why it matters and the requested change. The bracket after the number links it to the weaknesses above.

D1 [P1]. Location: abstract, last sentence (abstract.tex line 2); Conclusion (conclusion.tex line 4); Discussion paragraph 8 (discussion.tex line 18); the same sentences in the Chinese version.
- Problem: the sentence ranks mandatory and complete reporting together with more periods and regions as better uses of resources than more cases. Periods and regions follow from Proposition 1 and the estimated b/a. Reporting does not, for three reasons:
  - Under the mandate, completeness explains 2.0% of the R_A intercept, with a one-sided upper bound of 5.3%.
  - The voluntary-period contrast concerns the off-season dispersion of log G, not the intercept of the loss model in the early-growth windows. It is observational, its interval (0.95, 2.23) includes 1, and it rests on one off-season. The Discussion says all of this in paragraph 7, and the abstract sentence drops it.
  - The contribution of reporting volatility to error is never measured in the data.
- Why it matters: a reader of the abstract will take away that mandatory reporting improves precision more than additional cases do. The paper's own analysis supports something narrower. Once the mandate keeps participation above about 90%, the remaining variation in participation explains little of the intercept, and losing the mandate coincided with more volatile growth statistics.
- Requested change: split the sentence. Keep periods and regions as the design conclusion. For reporting, write that maintaining high facility participation is associated with lower volatility, and cite the voluntary contrast with its interval. Apply the same change to the Conclusion and Discussion paragraph 8, and in the Chinese version to 实行强制且完整的报告 in the abstract and Conclusion. Wording only.

D2 [P1, p3]. Location: Discussion paragraph 8, "standardising reporting reduced error more than a tenfold increase in case volume per period"; Section 3.1 (results.tex line 26).
- Problem: the comparison uses the hypothetical τ = 0.15. In that example reporting is 35% of the MSE (7.88 of 22.57 × 10⁻³), and v_H is 43% of the limiting variance. Standardising gives 14.65 × 10⁻³ against 18.71 × 10⁻³ for ten times the cases. The empirical upper bound for facility completeness is 5.3% of the intercept, so the example is not calibrated to these data.
- Why it matters: the sentence sits in the design paragraph and reads as an empirical finding.
- Requested change: mark the example as hypothetical. If the authors want an empirical version, solve for the τ that the 5.3% bound allows and report the corresponding comparison. Wording only, or light analysis for the optional version.

D3 [P2]. Location: abstract, "The two estimates agree although the statistics scale latent variance by factors that differ fivefold"; Discussion paragraph 4 (discussion.tex line 10), "would be unlikely if one statistic were dominated by its own construction" and "closes the loop"; Chinese abstract 两种统计量对潜伏方差的放缩倍数相差五倍，两个估计却相互一致 and Discussion 形成闭环.
- Problem: the "although" frames agreement as surprising evidence. The simulation shows the opposite. Both statistics are computed from the same counts with the same generation interval, so a misspecified interval, autocorrelation or delay moves both in the same direction. The two implied variances stayed in agreement across settings where the true v_R mapping changed by a factor of 0.33 (generation interval 2.2 days) to 1.45 (4.3 days). Only the synchronous count shock broke the agreement.
- Why it matters: the abstract's strongest positive claim rests on a test that most alternative mechanisms pass. A referee who reads Table S8 will see this at once.
- Requested change: state what the agreement does and does not show. One possible wording: "the two estimates are consistent (ratio 0.93; 95% CI: 0.78, 1.18), as expected if both respond to the same latent variation; in simulations this check rejected only a synchronous shock to reported counts." Replace "closes the loop" and 形成闭环 with a phrase such as "is consistent with" (与…相容). Wording only.

D4 [P2]. Location: Section 3.3 (results.tex line 58); Methods 6.8 (methods.tex line 79); Table S8.
- Problem: "agree" is defined as non-rejection of a zero difference. With intervals this wide, non-rejection is weak evidence. In the data-matched setting the ratio interval (0.78, 1.18) is not inside 0.8 to 1.25. Among the ten settings, only the bridge design and the 8-day delay have intervals inside that band. The count-shock interval (0.39, 0.90) and the observed interval share the range 0.78 to 0.90, so the data cannot fully exclude a mixture with a count shock. The Discussion acknowledges this in its last sentence.
- Why it matters: without an equivalence statement, "agree" can be read as "shown to be equal".
- Requested change: report the ratio with a pre-stated equivalence band, or say plainly that agreement means non-rejection. The existing bootstrap and simulation draws are enough for this. Wording, with an optional light calculation.

D5 [P3]. Location: abstract (0.040 and 0.043 with no conditions); Section 3.3 (results.tex line 58); Discussion paragraph 4; Conclusion.
- Problem: the generation interval moves v_R^impl from 0.013 to 0.063. The AR(1) setting with φ = 0.5 gives 0.027 and 0.025, below the band and about two thirds of the data-matched value. R_A falls in the 0.04–0.08 band in 4 of 10 settings and G in 7 of 10. The Discussion names the generation-interval dependence but not autocorrelation. The abstract and Conclusion give the values without either condition.
- Why it matters: the inversion is the paper's central new result. A reader needs to know that its level holds conditionally on a 3.6-day generation interval and on weekly shocks that are independent within a window.
- Requested change: (i) estimate the lag-1 autocorrelation of within-window deviations of log R_A from the state-season mean, and compare it with its distribution in the M0 and AR(1) simulations. This uses the existing simulator and data. (ii) Use published serial-interval estimates for influenza [7] to bound the generation interval, and report the corresponding range of v_R^impl. (iii) Add the conditions to the abstract in one clause, for example "conditional on a 3.6-day generation interval". Items (i) and (ii) need new analysis, light in scale.

D6 [P4]. Location: Section 3.1 (results.tex line 26), "21.3 to 49.2 cases …, a range that contains the empirical estimate for R_A"; Appendix B.2 (appendix.tex line 135), "a range that contains the empirical value of 37.4 for R_A"; the same sentences in the Chinese version.
- Problem: 21.3 to 49.2 is the latent-scale balance scale over the scenario grid of Proposition 1. The empirical 37.4 is on the statistic scale. The paper's own calibrated statistic-scale range for R_A, 13.9 to 31.1, does not contain it. The sentence survives from the round-2 version, written before calibration.
- Why it matters: it contradicts Section 3.3 and repeats the scale confusion raised in n2 and n3.
- Requested change: delete both containment clauses, or compare like with like (37.4 against 13.9–31.1, with the 93rd percentile). Wording only.

D7 [P4]. Location: abstract, "giving a balance scale of 37.4 admissions per week (95% CI: 19.1, 71.0)"; Fig. 6.
- Problem: the abstract defines m× = A/v_R as a property of the latent model, then gives 37.4 as "the balance scale". The Fig. 6A caption now names the statistic scale, and the abstract does not. No latent-scale m× is reported. As a rough check, the reviewer evaluated Proposition 1 at the data-matched simulation values (R̄ = 1.176, ρ = 0.01, k = 0.35, giving A = 1.216) and at v_R^impl. This gives m× ≈ 30 (22, 46) cases per generation. With about 1.9 generations per week this is not directly comparable with a weekly count, which is why the paper should report the conversion itself.
- Why it matters: the design rule in the abstract ("Where weekly admissions exceed the balance scale") applies the statistic-scale value to a latent-scale question.
- Requested change: write "a balance scale of 37.4 admissions per week on the scale of R_A". Report the latent m× implied by v_R^impl, with its interval and units, in Section 3.3 or Table S8. Wording, plus a light calculation.

D8 [P4]. Location: Section 3.3; Discussion paragraph 4; Fig. 3D.
- Problem: the empirical b/a is above the calibrated range for both statistics: 37.4 against 13.9–31.1 for R_A and 23.5 against 8.0–18.8 for G. The ratios to the data-matched point values are 1.34 and 1.45. The two percentiles (93rd and 91st) are correlated, because both statistics use the same counts, so they are not two independent signals. In Fig. 3D the simulated boxes for G sit well below the empirical value. The Discussion attributes the excess to "additional dispersion in admissions" without a test.
- Why it matters: the slope b is what sets m× and m*. An unexplained 34% to 45% excess carries straight into the design rule.
- Requested change: run one simulation setting with lower k or overdispersed admissions and report whether it brings b/a to the empirical value while keeping v_R^impl stable. If it does not, say that the slope is underpredicted and give the design rule on both values. Light analysis.

D9 [p1]. Location: Methods 6.8 (methods.tex line 77); Discussion paragraph 4, "The simulated panels also reproduced the intraclass correlation and the national-week share of the data".
- Problem: the national shock has variance 0.45 v_R by assumption, and the methods do not say how 0.45 was chosen. The simulated share (0.43) and ICC (0.258) match the data (0.41 and 0.253) at least partly by construction. Without the national shock the ICC is 0.050 while v_R^impl barely changes (0.039 against 0.040).
- Requested change: state how 0.45 was set (for example, matched to the data share). Describe the match as a consistency check. Add that v_R^impl is insensitive to this choice, which is the more useful finding. Wording only.

D10 [p2]. Location: title; Introduction, paragraph 1.
- Problem: the title promises results for "epidemic reproduction numbers". The paper's estimands are apparent weekly statistics, and the inversion recovers v_R only within the simulator's model.
- Requested change: either add a renewal estimate with an explicit delay and an external generation interval, or write "apparent reproduction numbers" or "weekly growth statistics" in the title. Wording only for the second option.

D11 [p4]. Location: abstract, "within an equivalence margin of 17%"; Section 3.5.
- Problem: the margin depends on τ0. At τ0 = 0.10 the margins are 17% (R_A) and 12% (G) and equivalence holds with power near 1. At τ0 = 0.05 the margins are 4.3% and 3.0%, equivalence is not shown and power is 0.25 and 0.
- Requested change: write "within an equivalence margin of 17% (τ0 = 0.10)" in the abstract. Wording only.

D12 [p5, p6]. Location: abstract; Section 3.3.
- Problem: the abstract is 281 words long and reports more than a dozen estimates; the benchmark abstract contains none. Some journals cap abstracts at 250 words. The "55% of state-weeks" refers to rule-window rows, not to the 10506 state-weeks named three sentences earlier. The main text runs to about 8288 words.
- Requested change: if the target journal limits abstracts to 250 words, keep the four estimates (37.4, the two v_R values, the voluntary ratio) and move the rest to the Results. Write "55% of state-weeks in the growth windows". Move the setting-by-setting sensitivity sentences in Section 3.3 to Table S8. Wording only.

D13 [p7]. Location: Chinese preamble; English reference list (Delphi URL); English page 22; Fig. 3A; PDF metadata.
- Requested change: if the journal template requires running heads, add them to the Chinese version as well; otherwise drop them from both so the versions match. Allow URL breaks only at slashes, or set the Delphi URL on its own line. Place Tables S8 and S9 so that page 22 is not mostly empty. Offset the 0.040 and 0.043 labels in Fig. 3A. Set pdftitle in both PDFs. Formatting only.

D14 [p8]. Location: Section 3.5; Discussion paragraph 7.
- Requested change (optional): estimate the reliability of the laboratory growth series from its split-week or adjacent-state structure, and report the attenuation-corrected shared fraction as a bound.

### 5 Overall recommendation

Recommendation: Minor revision.

Score: 7.5 out of 10.

Rationale. The scale is the one used in the first two rounds. A score of 6 meant that at least one issue could change a main conclusion. Minor revision (7–8) means that no remaining issue changes a stated empirical result, but the framing still claims more than the evidence shows in places that matter. A score of 8.5 or above would mean that the remaining comments are editorial. A score of 9 or above would also need external support for the inversion, such as a renewal estimate with explicit delay and an external generation interval, or a second surveillance system.

The revision resolves N1, the issue that held the score at 6. The calibration is applied and data-matched, its uncertainty is propagated, and the results are reported where they fall. The remaining issues are P1–P4. None of them requires new data. P1 and P2 are wording changes; together they decide whether the abstract's two positive claims, on reporting and on agreement, are stated at the strength the evidence supports. P3 requires a light analysis with the existing simulator. P4 needs wording and one calculation. The score is not higher because these four issues sit in the abstract and the Conclusion, which carry the paper's message. The minimum changes to reach 8.5 are listed in Section 7.

Reviewer confidence: high (4 out of 5) for the mathematical, statistical and number-tracing assessments, which were checked by script. Moderate (3 out of 5) for the epidemiological interpretation of NHSN reporting regimes and the generation interval of influenza. This is an internal review and the reviewer may share blind spots with the authors, so an external review is still advisable before submission.

### 6 Response to second-round comments

Judgements are Resolved, Largely resolved, Partly resolved or Not resolved. The evidence is the reviewer's reading of the third-round files and the check script.

| Item | Second-round request | Judgement | Evidence and residual |
|---|---|---|---|
| N1 | apply the simulation calibration | Largely resolved | Data-matched two-step inversion with propagated intervals (Section 3.3; Methods 6.8; Table S8). Residual framing in P2 and P3 |
| N2 | title overstates the floor | Resolved | New title without "irreducible"; Scope and extensions paragraph kept |
| N3 | credit Parag et al. for reporting fractions and NB extension | Resolved | Discussion paragraph 3 states both; fitted variance reaches twice the Poisson value at 22 admissions on the R_A scale and 28 on the latent scale |
| N4 | apparent statistic versus reproduction number | Partly resolved | "apparent" appears twice in the abstract; title unchanged; no renewal estimate (p2, D10) |
| N5 | reporting conclusion overstated | Resolved in Results and Discussion paragraph 7 | Residual policy sentence in the abstract, Conclusion and Discussion paragraph 8 (P1) |
| N6 | analysis history, authorship, DOI | Partly resolved | Table S9 gives the calendar-window analysis; authorship and DOI are author to-dos, not scored |
| n1 | b/a factors 3.9 and 7.1 | Resolved | Replaced by calibrated ranges 13.9–31.1 and 8.0–18.8 |
| n2 | design uses uncorrected 21.3–49.2 | Partly resolved | Empirical m* = 19.4 given; containment claim remains (P4, D6) |
| n3 | Fig. 6D uses 37.4 on the statistic scale | Partly resolved | Fig. 6A caption names the scale; abstract does not; no latent m× (D7) |
| n4 | Fig. 6B caption "lower bound on precision" | Resolved | Fig. 7B caption now says "relative standard error" |
| n5 | seeds | Resolved | Four seeds listed in Methods 6.4 |
| n6 | N 1748 against 1756 | Resolved | The eight extra state-weeks are explained in Section 3.3 |
| n7 | CV labels | Resolved | Labels match the definitions |
| n8 | negative lower bounds in Table S6 | Resolved | Shown as "n.d." |
| n9 | 90% and 95% intervals for Δa; bin error bars | Resolved | 90% intervals stated for TOST; caption notes clustering |
| n10 | thousands separators; URL break | Partly resolved | Separators removed; Delphi URL still breaks in the host name (p7) |
| n11 | benchmark alignment (length, "we", abstract) | Partly resolved | "we" 10 times; abstract 281 words with numbers; main text 8288 words (p5, p6) |
| n12 | running heads, AI declaration, font | Partly resolved | AI declarations aligned; Chinese version lacks running heads (p7) |
| n13 | voluntary period missing from abstract | Resolved | Abstract gives 1.58 (0.95, 2.23) and calls it observational |

### 7 Minimum changes needed to reach 8.5

Ranked by effect on the score. "Wording" means a text change only; "Analysis" means a new computation with existing data and code.

1. P1, D1–D2 (Wording). Rewrite the reporting part of the policy sentence in the abstract, Conclusion and Discussion paragraph 8, in both languages, and label the τ = 0.15 example hypothetical.
2. P3, D5 (Analysis, light). Estimate the lag-1 autocorrelation of within-window deviations, compare it with the simulated distributions, bound the generation interval with external estimates [7], and state the conditions in the abstract.
3. P2, D3–D4 (Wording; optional light calculation). Recast agreement as a consistency check that rejects only a synchronous count shock, remove "closes the loop" and 形成闭环, and either report an equivalence band or define agreement as non-rejection.
4. P4, D6–D8 (Wording plus light analysis). Delete the two containment clauses, name the scale of 37.4 in the abstract, report the latent m× with units, and run one overdispersed-admission setting for the b/a excess.
5. p1, p4 and p5, D9, D11, D12 (Wording). State how 0.45 was chosen, give τ0 with the 17% margin, and fix the 55% denominator.

Items 1, 3 and 4 without their optional calculations would bring the manuscript to about 8. All five would reach 8.5. The formatting items in p7 do not change the score but should be fixed before submission.

### 8 Prudence of the narrative reframing

The author plan asked for the defensive passages of round 2 to be recast as findings. The table checks each positive claim that the reframing introduced against its evidence, and asks whether the new wording opened a hole that the old wording did not have.

| Positive claim (location) | Evidence in the manuscript | Supported? | New hole? |
|---|---|---|---|
| Two-step inversion links apparent statistics with latent dynamics (abstract; Section 3.3; Methods 6.8) | Data-matched simulator, calibration line, propagated intervals, ten settings | Yes | No |
| The two estimates agree "although" the scale factors differ fivefold (abstract; Discussion paragraph 4) | Ratio 0.93 (0.78, 1.18); agreement in 9 of 10 settings | Partly: consistency, not validation | Yes: invites the reading that agreement validates the level (P2) |
| Calibration "closes the loop" (Discussion paragraph 4; 形成闭环 in Chinese) | Same as above, plus ICC and share matched partly by construction | Partly | Yes, minor: overstated, though followed by three qualifications (P2, p1) |
| v_R ≈ 0.04 (abstract; Conclusion) | 0.040 and 0.043 at the lower edge of the band; intervals extend below | Yes as a conditional estimate | Yes: the conditions are absent from the abstract (P3) |
| Multiscale decomposition (Section 3.4; Discussion paragraph 6) | 41% and 51% national-week shares; pooling J = 33 and 25 | Yes | No; the paper avoided "about 50%" and gives both values |
| Mandatory reporting improves precision (abstract; Conclusion; Discussion paragraph 8) | 2.0% (upper 5.3%) under mandate; observational 1.58 (0.95, 2.23) | No as worded | Yes: the main new hole (P1) |
| Diminishing returns and a design nomogram (Section 3.6; Fig. 6) | Proposition 1; empirical b/a; nomogram | Yes | Minor: scale of 37.4 not named in the abstract (P4) |
| Balance-scale range "contains" 37.4 (Section 3.1; Appendix B.2) | Contradicted by the calibrated 13.9–31.1 | No | Carried over, not new; still to remove (P4) |
| Complement to Parag et al. (Discussion paragraph 3) | Fitted variance twice the Poisson value at 22 (apparent) and 28 (latent) admissions, ten times at 261 and 262 | Yes | No |
| Scope and extensions paragraph | Present | Kept as required | No |

The reframing removed the defensive vocabulary (concede, negligible, cannot be established: 0 occurrences each) without introducing superlatives. It did not adopt the unsupported phrases of the plan ("perfect alignment", "firewall", "natural experiment", "universal critical scale"), and the voluntary contrast is called observational in the abstract. Two of the new positive sentences go beyond their evidence (P1, P2), and one carried-over sentence now contradicts the new results (P4).

Verification of the numbers in the author plan:

| Plan number | What the manuscript and results.json show | Status |
|---|---|---|
| 2.68 (G) and 0.484 (R_A) | Medians of the noise-free scale factors over 17 generic scenarios. Data-matched values are 2.729 and 0.516 | Superseded by data-matched values; used correctly |
| 0.0451 | Plan formula gives 0.0449 (R_A) and 0.0456 (G); the G formula as written in the plan gives 0.0216 (dimension error). Calibration line gives 0.040 and 0.043 | Superseded; the paper uses 0.040 and 0.043 |
| R̄ = 1.206 | Sample mean of R_A in rule windows; the simulator's true R̄ is 1.176 | Correct as a sample mean |
| 0.04–0.08 band | Both points at the lower edge; both intervals extend below; in band in 4 of 10 settings (R_A) and 7 of 10 (G) | Stated honestly in Section 3.3 |
| 13.4–28.7 | Round-2 value from generic factors; replaced by 13.9–31.1 (R_A) and 8.0–18.8 (G). G's 23.5 lies inside the old range and above the new one; R_A's 37.4 lies outside both, with its interval overlapping | Superseded; absent from the paper |
| 23.5 (8.4, 59.7) | G b/a | Confirmed |
| 37.4 (19.1, 71.0) | R_A b/a | Confirmed |
| "about 50%" national share | 41% (R_A) and 51% (G) | The paper gives both values |
| 17% | Equivalence margin at τ0 = 0.10; the measured change is 2.0% with upper bound 5.3% | Correct as a margin, not as a measured effect (p4) |
| 58% | IQR ratio 1.58 (0.95, 2.23); observational; interval includes 1 | Correct with qualification |
| over 95% participation | Median 92.3% in regime 1 (D ≥ 5) and 93.7% in rule windows; 46.7% of regime-1 state-weeks at or above 95% | The plan figure is not supported; the paper writes "about 93%" |
| 2.1万 (21 thousand) state-weeks | 21641 raw jurisdiction-weeks; 10506 analysis rows; 1748 and 1756 in rule windows | The paper uses 10506 |

### 9 Verification record

- Headline numbers (block A, key A_headline): 94 values formatted from results.json, each found in the English and Chinese sources; A_failures is empty. Every number in the English abstract is present in the Chinese abstract (A_abstract).
- English–Chinese numbers (block B): the only differences are a few small integers in the Chinese text (months and ordinals). No substantive difference.
- Derived quantities (block C, C_derived): user_formula_*, calib_line_*, kappa_ratio_G_over_RA_fit (5.29), settings_table (all eleven settings), settings_vR_differs_from_M0_by_factor (0.33 to 1.45), settings_ratio_ci_within_0.8_1.25 (bridge_s08, delay_long), agreement_overlap_count_shock_vs_observed (0.78 to 0.90), rho0_sim_icc_RA_vs_data (0.050 against 0.253), ba_empirical_above_pooled_range, ba_ratio_emp_over_M0 (1.34, 1.45), old_round2_range_*, margin_share_check_* (0.170, 0.043, 0.030), delta_share_check_RA (0.020), iqr_ratio_ci_includes_1, regime1_share_ge95 (0.467), theory_rep_share_of_MSE (0.349), theory_vH_share_of_limiting_var (0.434), theory_standardise_vs_x10 (14.65, 18.71), share_above_mcross_RA_G (0.553), latent_A_prop1_at_M0 (1.216), latent_mcross_prop1_at_vR_impl (30.3) with its interval (21.7, 46.3), generations_per_week_at_GI3.6 (1.94).
- results.json keys: reporting_regime.RA_rule4_delta_a_share.upper95_one_sided (0.0528, the 5.3% in the abstract); s04_reporting TOST power at τ0 = 0.05 (0.251 for R_A, 0 for G).
- PDF facts (block D): both versions 24 pages; no "??"; all fonts embedded; no Type 3 fonts; seven figure environments; Title metadata empty.
- Wording (block E): perfect, universal, 首次 and 普适 absent; 证明 8 times, all in proof environments; "closes the loop" once and 闭环 twice; defensive terms absent; "causal" once, in the sentence that disclaims a causal effect; abstract 281 words (English) and 663 characters (Chinese); "we" 10 times; English running heads present and Chinese absent; Delphi URL broken in the host name in the English PDF; no bare territorial names.
- Page inspection: all 48 pages rendered and viewed; observations are in p7 and D8.

### 10 Author to-dos (not scored)

- Human author names and affiliations, replacing "Apevon Science".
- Funding statement.
- CRediT contribution statement.
- An archival DOI (for example Zenodo) for the code and data snapshot, cited in the Code availability statement.

### References

[1] Eales O, Riley S. Differences between the true reproduction number and the apparent reproduction number of an epidemic time series. Epidemics 2024;46:100742. https://doi.org/10.1016/j.epidem.2024.100742

[2] Parag KV, Donnelly CA, Zarebski AE. Quantifying the information in noisy epidemic curves. Nature Computational Science 2022;2:584–594. https://doi.org/10.1038/s43588-022-00313-1

[3] Cori A, Ferguson NM, Fraser C, Cauchemez S. A new framework and software to estimate time-varying reproduction numbers during epidemics. American Journal of Epidemiology 2013;178:1505–1512. https://doi.org/10.1093/aje/kwt133

[4] Gostic KM, McGough L, Baskerville EB, et al. Practical considerations for measuring the effective reproductive number, Rt. PLOS Computational Biology 2020;16:e1008409. https://doi.org/10.1371/journal.pcbi.1008409

[5] Wallinga J, Lipsitch M. How generation intervals shape the relationship between growth rates and reproductive numbers. Proceedings of the Royal Society B 2007;274:599–604. https://doi.org/10.1098/rspb.2006.3754

[6] Lakens D. Equivalence tests: a practical primer for t tests, correlations, and meta-analyses. Social Psychological and Personality Science 2017;8:355–362. https://doi.org/10.1177/1948550617697177

[7] Cowling BJ, Fang VJ, Riley S, Peiris JSM, Leung GM. Estimation of the serial interval of influenza. Epidemiology 2009;20:344–347. https://doi.org/10.1097/EDE.0b013e31819d1092

### 11 Final-revision verification (Addendum)

- Version checked: the final-polish versions in output/case-count-bottleneck/paper/ (25 pages) and output/case-count-bottleneck-zh/paper/ (26 pages), with the authors' response appended to .work/case-count-bottleneck/paper/revision_response_r3.md (section "Final polish") and its Chinese counterpart. Date: 20 October 2026.
- Method: the round-3 check script was rerun unchanged against the published files as final_polish_checks.py, with output in final_polish_checks.json (same directory as before). The new numbers were checked against results.json (keys polish.*) and analysis/parts/polish.json. Both PDFs were rendered and every page was viewed. The judgement below rests on the files, not on the response document.
- Line references are to sections/*.tex. The two language versions carry the same changes at the same line numbers.

#### 11.1 Item-by-item check of the Section 7 list

| Item | Requested | What the final version does | Evidence | Judgement |
|---|---|---|---|---|
| P1, D1 | Split the policy sentence; reporting stated as an association | Abstract, Conclusion and design paragraph keep periods and regions as the design conclusion. Reporting is stated as "high facility participation was associated with lower volatility". "mandatory and complete" is gone (0 hits in the PDF). Discussion paragraph on reporting regimes opens with "Within the limits of an observational comparison … consistent with a benefit of high facility participation". Chinese 实行强制且完整 has 0 hits | abstract.tex:2; conclusion.tex:4; discussion.tex:16, 18 | Resolved |
| P1, D2 | Label τ = 0.15 hypothetical; optional calibrated version | "hypothetical example" in Section 3.1 and the design paragraph. The optional calculation is done: the 5.3% bound allows τ of about 0.04, at which ten times the cases gives MSE 11.4 against 14.6 for standardised reporting (from 15.2, × 10⁻³). The text draws the correct conclusion that more cases win at that τ | results.tex:26; discussion.tex:18; polish.tau_allowed_by_upper_share = 0.0404; polish.lever_at_tau_allowed_total = 15.22 | Resolved, optional part included |
| P2, D3 | Recast agreement as a consistency check; remove "closes the loop" | Abstract: "The two estimates were consistent (ratio 0.93)". "closes the loop" and 闭环 have 0 hits. Discussion calls it a check of limited power that failed only under the synchronous count shock, and adds that in that setting the observed lag-1 autocorrelation of G lies above 99% of simulated panels, which is a useful extra discriminator | abstract.tex:2; discussion.tex:10 | Resolved |
| P2, D4 | Equivalence band or define agreement as non-rejection | Both. Agreement is defined as non-rejection in Methods 6.8 and Section 3.3 (linked to Table S8). A TOST on the primary design gives a 90% interval of 0.81 to 1.13, inside 0.80 to 1.25. The reviewer's round-3 statement that the 95% interval (0.78, 1.18) is not inside the band remains true; the TOST uses the 90% interval, which is the standard construction [6] | methods.tex:79; results.tex:56, 58; polish.ratio_vR_RA_over_G_ci90 | Resolved |
| P3, D5 (i) | Lag-1 autocorrelation of within-window deviations against M0 and AR(1) | r1 = −0.095 (−0.168, −0.019) for R_A and 0.123 (0.039, 0.201) for G. Simulated means under independence are −0.074 and 0.114 (data at the 31st and 62nd percentiles). With φ = 0.25 the data fall at the 3rd and 10th, with φ = 0.5 below all panels. The text correctly notes that both statistics are autocorrelated by construction, so the comparison is against simulation, not against zero | results.tex:60; Table S10 panel A; polish.r1_* | Resolved |
| P3, D5 (ii) | Bound the generation interval with [7] | Cowling et al. is cited, and the inversion is rerun at 2.9 d: v_R^impl 0.026 (0.017, 0.036) and 0.027 (0.016, 0.040). At 4.3 d: 0.058 and 0.063. The range 0.026–0.063 replaces the earlier 0.013–0.063, which included a 2.2-day setting outside the external interval | results.tex:60; discussion.tex:10; methods.tex:24, 79; polish.vR_impl_*_GI_2.9_to_4.3 | Resolved |
| P3, D5 (iii) | State the conditions in the abstract | Abstract and Conclusion: conditional on a 3.6-day generation interval and on independent weekly shocks | abstract.tex:2; conclusion.tex:4 | Resolved |
| P4, D6 | Delete both containment clauses | Both deleted (0 hits for "contains the empirical" and 这一范围包含). 21.3–49.2 is now "latent balance scales … per generation" | results.tex:26; appendix.tex:135 | Resolved |
| P4, D7 | Name the scale of 37.4; report the latent m× | Abstract: "37.4 admissions per week on the scale of that ratio". Section 3.3 gives the latent m× of 30.3 (21.7, 46.3) per generation, about 59 per week at 1.94 generations per week, and says 37.4 does not estimate it directly. The design paragraph calls 37.4 "an apparent balance scale". These match the reviewer's own check (block C: 30.3, 21.7, 46.3, 1.94) | abstract.tex:2; results.tex:56; discussion.tex:12; polish.latent_mcross_RA, _per_week | Resolved |
| P4, D8 | One overdispersed-admission setting for the b/a excess | Gamma–Poisson admissions with VMR 1.5 and 2.0. At v_R = 0.04, b/a rises from 28.0 to 68.0 and 81.0 (R_A) and from 16.2 to 40.2 and 48.4 (G), while v_R^impl stays at 0.039–0.045. The excess is therefore reproducible with VMR between 1 and 1.5. See 11.2 for the second explanation now also reported | results.tex:60; discussion.tex:10; Table S10 panel B; polish.od05_*, od10_* | Resolved |
| p1, D9 | Say how 0.45 was set; call the match a consistency check | 0.45 lies between the observed shares 0.41 and 0.51. The match is called a consistency check, and the insensitivity of v_R^impl (0.039 and 0.040 at shares 0 and 0.65) is stated | methods.tex:77; discussion.tex:10 | Resolved |
| p4, D11 | Give τ0 with the 17% margin | "equivalence margin 17% at reference volatility 0.10" in the abstract; same in the Discussion | abstract.tex:2; discussion.tex:4 | Resolved |
| p5, D12 | Fix the 55% denominator; shorten the abstract if capped | "55% of state-weeks in the growth windows". By the same detex count as round 3, the abstract fell from 281 to 256 words; the Chinese abstract has 658 characters (663 before) | abstract.tex:2; final_polish_checks.json E_wording | Denominator resolved; length still 6 words over a 250-word cap |
| p7, D13 | Formatting | Neither version has running heads now, so they match. The Delphi URL no longer breaks inside the host name (url_break_in_host_en false). Tables S8–S10 fill page 22. The 0.040 and 0.043 labels in Fig. 3A sit beside the drop lines (verified on the rendered figure). pdftitle is set in both PDFs | main.tex; endmatter.tex; appendix.tex:195; pdfinfo | Resolved |

Optional and unscored items: D10 (title) is unchanged, and the title still says "reproduction numbers". D14 (reliability correction of the laboratory proxy) was not done. p6 (length) was not addressed; see 11.2.

#### 11.2 New observations from the final version

- F1 (resolved during verification). In the 2.9-day setting, evaluated at v_R = 0.02, the grid value nearest its own implied variance, the empirical b/a falls at the 52.5th (R_A) and 58th (G) percentiles of the simulated distribution (parts/polish.json, emp_ba_percentile_at_nearest). A shorter generation interval therefore explains the b/a excess as well as mild overdispersion does, and the two explanations imply different levels of v_R (about 0.026 against 0.040). The reviewer raised this while checking Table S10. The final version now states it in Section 3.3 and the Discussion, together with the autocorrelation evidence that argues against the shorter interval without excluding it (results.tex:60; discussion.tex:10). The abstract already makes the level conditional on 3.6 days, so no headline claim changes.
- F2 (editorial). Length grew because of the new analyses. The main text is about 8990 words by the round-3 count (8288 before). Results now has 3139 words and the Discussion 1818. The setting-by-setting sentences in Section 3.3 and the new paragraph on the three assumption checks could move to Table S8 and Table S10 notes with little loss.
- F3 (editorial). The design sentence in the abstract applies the apparent scale (37.4 per week, 55% of growth-window state-weeks). The latent value converts to about 59 per week, so the share of state-weeks above the latent scale would be lower. One clause giving that share, or a pointer to Section 3.3, would let readers who use the rule connect the two scales.
- F4 (editorial). The new numbers in both language versions agree: all 39 polish values checked appear in both sources. The 94 headline numbers of block A are still found in both versions, with 0 failures. Block B shows only the expected small integers (lag-1 written as 滞后一阶, ordinals and months).

#### 11.3 Updated recommendation

Recommendation: Minor revision (editorial changes only).

Score: 8.5 out of 10.

Rationale. The scale is the one in Section 5. All five items of Section 7 are done, including the optional calculations in D2, D4 and D7. The abstract and Conclusion now state the reporting evidence as an observational association. They present agreement as a consistency check and give the inversion's conditions. The scale of 37.4 is named, and the containment claim is gone. The two light analyses (autocorrelation and the external generation-interval bound) support the independence assumption and bound the level of v_R at 0.026–0.063. The overdispersion setting gives the b/a excess a tested explanation, and the shorter-interval alternative (F1) is now reported beside it. No remaining comment changes a stated result. F2, F3, the 256-word abstract and the optional D10 and D14 are editorial. This meets the definition of 8.5 given in Section 5.

The score is not 9. Section 5 set external support for the inversion as the condition for 9 or above, for example a renewal estimate with an explicit admission delay and an external generation interval, or a second surveillance system. The final version adds an external bound on the generation interval. It still has no independent estimate of v_R, and the level of v_R remains conditional (0.026–0.063 across the external interval). The gap to 9 is therefore one analysis of that kind. Shortening the main text (F2), adding the latent-scale share (F3) and bringing the abstract under 250 words would remove the editorial residue, but they would not by themselves raise the score above 8.5.

Reviewer confidence is unchanged: high (4 out of 5) for mathematics, statistics and number tracing, and moderate (3 out of 5) for the epidemiological interpretation. The internal-review caveat of Section 5 still applies.

#### 11.4 Verification record for the addendum

- Numbers: final_polish_checks.json, blocks A to E (A_failures empty; A_abstract empty). New values: results.json keys polish.r1_*, polish.gi_cow_lo_*, polish.od05_*, polish.od10_*, polish.ar025_*, polish.latent_mcross_*, polish.ratio_vR_RA_over_G_ci90, polish.tau_allowed_by_upper_share and polish.lever_at_tau_allowed_total. Percentiles are in parts/polish.json, blocks r1_simulated_v0.04 and new_settings.
- PDF facts: 25 pages (English) and 26 pages (Chinese). No "??". All fonts are embedded and there are no Type 3 fonts. Title metadata is set in both. There are no running heads in either version.
- Gates reported by the authors and rerun by the reviewer: manuscript QA 0 errors (English, 10 reviewed warnings; Chinese with font fallback, 2 reviewed warnings). statistical_table_qa: 10 tables, 0 errors in each version. Citation check: 44 of 44 bibliography entries cited, no orphans. style_gate (paper) and territory_gate exit 0. The Chinese strict font gate still reports 2 errors (no licensed SimSun in the build environment), as disclosed by the authors. This is a build-environment issue and is not scored.
- Wording: perfect, universal, 首次, 普适, "closes the loop" and 闭环 absent. "first" appears 24 times, all as "first-order", "first target" or similar. 证明 appears 8 times, all as proof headings. "causal" appears once, in the sentence that disclaims a causal effect. "we" appears 10 times.
- Page inspection: all 51 pages rendered and viewed.

## Part B — 中文

### 1 简要概述

稿件研究的问题是：报告病例增多时，再生数估计的精度能提高多少。命题 1 给出每期平均再生数的误差方差 V(m) = v_R + A/m，其中 A = R̄ + ρ(R̄² + v_R)/k；平衡规模 m× = A/v_R 标出环境变异开始占主导的位置。命题 2 加入报告波动，v_H = τ²(R̄² + v_R)。命题 3 给出成本最优的每期病例数 m* = √((c0/c1)m×)。附录补充了 Fisher 信息界、预算规则以及季间精度的极限。

实证部分用可行广义最小二乘拟合 E(L | D) = a + b/D，并采用州 × 周双向自助法。数据为 NHSN 每周流感住院人数，2020 至 2026 年共 10506 个州周，分析窗口为四个流感季中按规则界定的早期增长期。统计量有两种：更新型比值 R_A 与加权增长比 G。本轮的主要变化是两步反演（第 3.3 节；方法 6.8）：用与数据匹配的模拟器把各统计量的截距映射为潜伏环境方差，由 R_A 得 v_R = 0.040（95% CI：0.026, 0.056），由 G 得 0.043（0.025, 0.064）。两者之比为 0.93（0.78, 1.18），而两种统计量的放缩倍数相差 5.3 倍。截距中 41% 至 51% 为全国周分量。强制报告期内，按机构填报完整度调整后 R_A 截距变化 2.0%（上界 5.3%）。2024 年自愿报告期的对数增长四分位距为 2023 年同期的 1.58 倍（0.95, 2.23）。设计查对图（图 6）把这些估计换算为所需观测周数与合并辖区数。

本轮修订解决了第二轮最严重的问题：校准已用数据匹配的模拟器实施，并传递了不确定性。作者还更正了本评审人在第二轮由通用情景系数推得的两个数（v_R 约 0.045，校准后 b/a 区间 13.4 至 28.7），改用数据匹配的数值，并如实报告其位置：两个隐含方差都位于 0.04–0.08 区间的下沿，两个区间都向下越出；经验 b/a 高于校准范围，处在模拟分布的第 93 和第 91 百分位。尚存的问题集中在表述上。摘要与结论中的政策句超出了报告分析的证据（P1）。两种统计量的一致被写成验证，模拟结果却显示这一检验的鉴别力很弱（P2）。v_R 的数值依赖若干假设，摘要没有交代（P3）。上一版留下的一处平衡规模"包含"表述与校准范围相矛盾（P4）。

### 2 优点

- S1. 理论正确且完整。评审人在前两轮已复推命题 1–5 与推论 1–2；基线值 A = 2.1232、m× = 53.1、v_H = 0.0307 未变，可以复现。
- S2. 两步反演是实质性的方法进展。模拟器在窗口长度（9、12、8、13 周）、州数、全国周分量和离散度上与数据匹配，四个 v_R 取值各模拟 200 个面板，方法 6.8 写明了校准线 E(â) = γ0 + γ1 v_R。数据匹配的放缩系数（R_A 为 κ = 0.516，G 为 2.729）与无噪声极限（0.493, 2.745）及桥接设计（0.485, 2.698）接近，映射稳定。
- S3. 结果报告如实。第 3.3 节写明两个点值都处在区间下沿、两个区间都向下越出，并报告了 b/a 的超出量及其模拟百分位。同节报告了十种设定中九种一致、同步计数冲击这一例外，以及主要由代际间隔驱动的 0.013–0.063 范围。讨论第 4 段列出了三点限定。
- S4. 敏感性设计信息量大。十种设定分别改变全国分量、自相关、代际间隔、报告延迟、后代离散度和冲击类型，表 S8 全部列出，不利的设定也在其中。
- S5. 结果与讨论部分对报告制度的分析是审慎的。自愿期对比有安慰剂比较（2025/2023 之比 1.01）、按报告规模匹配（1.68）、按日历月匹配（中位数 1.33）以及另外两种病原体。讨论第 7 段写明这是观察性对比，不能识别强制报告的因果效应。
- S6. 第二轮次要问题大多已修正：b/a 系数（n1）、随机种子（n5）、多出的 8 个州周（n6）、变异系数标签（n7）、无定义下界改为 "n.d."（n8）、Δa 的 90% 区间（n9）、千位分隔符（n10）、摘要补入自愿期（n13）。
- S7. 可追溯性仍然很高。A 块的 94 个头条数字在中英两版中全部找到（0 处失败），摘要中的每个数字都在内；B 块未发现两版之间有实质差异；中文版图件使用中文标注。
- S8. "适用范围与扩展"一段把论断限定在模型类之内。摘要和标题不再断言"不可约"下限；全文没有 perfect、universal、首次、普适之类的夸大用语；"证明"只作为证明环境的标题出现。

### 3 缺点

#### 主要问题

- P1. 政策结论超出了报告方面的证据。摘要最后一句写道，实行强制且完整的报告、增加时期数与区域数，比增加每期病例更能提高监测精度；结论重复了这一句，讨论第 8 段又补充"报告标准化对误差的降低幅度大于每期病例量增加十倍"。可是在强制期内，填报完整度只解释 R_A 截距的 2.0%（上界 5.3%）；自愿期对比是观察性的，其区间（0.95, 2.23）包含 1；"十倍"一句来自假设的 τ = 0.15 示例，其中报告占 MSE 的 35%，约为经验上界的七倍。
- P2. 两种统计量的一致被当作验证，这一检验承担不起。摘要说两种统计量对潜伏方差的放缩倍数相差五倍，两个估计却相互一致；讨论第 4 段又说，若某一统计量主要由其构造方式决定，这种一致就不大可能出现，并称校准"形成闭环"（英文 closes the loop）。然而在模拟中，两种统计量在十种设定中有九种一致，其中包括隐含 v_R 变动 0.33 至 1.45 倍的设定。这里的"一致"仅指差值的 95% 区间包含零。数据匹配设定下比值区间（0.78, 1.18）并不落在常用的 0.8 至 1.25 等效带内；计数冲击设定的区间（0.39, 0.90）与观测区间在 0.78 至 0.90 上重叠。因此这一致只是一项相容性检查，它排除的只有纯粹的同步计数冲击。
- P3. v_R 的数值是有条件的，摘要没有说明。隐含方差取决于代际间隔：间隔为 2.2 天时为 0.013，4.3 天时为 0.058。它还取决于窗口内各周相互独立：φ = 0.5 的 AR(1) 过程给出 0.027 和 0.025。十种设定中，R_A 只有 4 种落在 0.04–0.08 区间内，G 有 7 种。讨论第 4 段提到了代际间隔的影响，没有提自相关。数据本身可以检验后一个条件，外部的序列间隔估计 [7] 可以约束前一个条件，稿件两者都没有利用。
- P4. 平衡规模在不同尺度之间作了比较。第 3.1 节（results.tex 第 26 行）与附录 B.2（appendix.tex 第 135 行）称情景范围 21.3 至 49.2 包含 R_A 的经验估计。这一范围属于命题 1 的潜伏尺度，且未经校准；在统计量尺度上，R_A 的校准范围 13.9–31.1 并不包含 37.4。摘要在定义 m× = A/v_R 之后直接把 37.4 称为平衡规模，没有说明它属于统计量尺度，读者也无从知道它与理论中的潜伏 m× 有何关系。b/a 的超出量（经验值与数据匹配点值之比：R_A 为 1.34，G 为 1.45）在讨论中有描述，没有经过检验的解释。

#### 次要问题

- p1. 模拟器中的全国周方差比例 0.45 v_R 是设计时设定的（methods.tex 第 77 行），因此模拟的全国分量（0.43）和组内相关系数（0.258）与数据（0.41 和 0.253）相符，至少部分来自构造本身；去掉全国冲击后，模拟的组内相关系数为 0.050。方法 6.8 应说明 0.45 如何选定，讨论第 4 段应把这种相符称为相容性检查，避免说成"复现"。
- p2. 标题仍写"疫情再生数"。分析使用的是表观统计量，代际间隔固定，没有显式的延迟分布，也没有报告采用外部代际间隔的更新方程估计。这是 N4 未完成的部分。
- p3. 第 3.1 节与讨论第 8 段的 τ = 0.15 示例，凡用来支撑建议之处，都应标明为假设示例（见 P1）。
- p4. 摘要写"落在截距 17% 的等效界之内"，没有给出界值参数 τ0 = 0.10。τ0 = 0.05 时，界值缩小为截距的 4.3%（R_A）和 3.0%（G），等效性不成立，功效分别为 0.25 和 0。
- p5. 摘要 281 词，数字很多；基准文章的摘要不含数字。"55% 的州周"一句紧跟在 10506 个州周之后，但 55% 指的是规则窗口内高于 37.4 的行所占比例，并非全部面板；而且它依赖一个区间为 19.1 至 71.0 的平衡规模。
- p6. 正文已增至约 8288 词（第二轮约 6600 词），仅结果部分就有 2827 词。第 3.3 节中逐项的敏感性细节可移入表 S8，不损失信息。
- p7. 版式方面：中文版没有页眉，英文版有；英文 PDF 中 Delphi 网址在主机名内断行（api.delp|hi.cmu.edu）；英文第 22 页（表 S8–S9）留有大片空白；图 3A 中 0.040 和 0.043 两个数值标签压在垂线上；两版 PDF 的 Title 元数据均为空。
- p8. 实验室代理指标分享了截距的 0.230，讨论解释了这一比例为何向零衰减。做信度校正可以把它变成一个界。作者已列为未完成事项，属可选。

### 4 详细意见

每条意见依次给出位置、问题、重要性和修改要求；编号后的方括号对应上文的缺点。

D1 [P1]。位置：摘要最后一句（abstract.tex 第 2 行）；结论（conclusion.tex 第 4 行）；讨论第 8 段（discussion.tex 第 18 行）；中文版对应句。
- 问题：这句话把强制且完整的报告与增加时期数、区域数并列，说它们都比增加病例更值得投入。时期数与区域数的结论来自命题 1 和估计的 b/a；报告的结论没有同样的依据，原因有三：
  - 强制期内，填报完整度只解释 R_A 截距的 2.0%，单侧上界为 5.3%。
  - 自愿期对比针对的是非流行季 log G 的离散度，并非早期增长窗口内损失模型的截距；它是观察性的，区间（0.95, 2.23）包含 1，且只依据一个非流行季。讨论第 7 段把这些都写清楚了，摘要这句却没有带上。
  - 报告波动对误差的贡献从未在数据中测量过。
- 重要性：读摘要的人会得出"强制报告比增加病例更能提高精度"的印象。稿件自己的分析支持的结论要窄得多：强制报告把参与率维持在约 90% 以上之后，参与率的剩余变化对截距的解释很小；而失去强制要求的时期恰好伴随增长统计量波动加大。
- 修改要求：把这句话拆开。时期数与区域数保留为设计结论；报告部分改写为"维持较高的机构填报率与较低的波动相关联"，并引用自愿期对比及其区间。结论和讨论第 8 段同样修改；中文版摘要和结论中的"实行强制且完整的报告"一并修改。仅需改措辞。

D2 [P1, p3]。位置：讨论第 8 段"报告标准化对误差的降低幅度大于每期病例量增加十倍"；第 3.1 节（results.tex 第 26 行）。
- 问题：这一比较使用假设值 τ = 0.15。该示例中报告占 MSE 的 35%（22.57 × 10⁻³ 中的 7.88），v_H 占极限方差的 43%；统一报告后 MSE 为 14.65 × 10⁻³，病例增加十倍后为 18.71 × 10⁻³。而填报完整度的经验上界只有截距的 5.3%，可见该示例并未按本数据校准。
- 重要性：这句话放在设计段落中，读起来像是实证结论。
- 修改要求：标明这是假设示例。若作者希望给出实证版本，可反解 5.3% 上界所允许的 τ，并报告相应的比较结果。仅需改措辞；可选版本需少量计算。

D3 [P2]。位置：英文摘要 "The two estimates agree although the statistics scale latent variance by factors that differ fivefold"；讨论第 4 段（discussion.tex 第 10 行）"would be unlikely if one statistic were dominated by its own construction"和"closes the loop"；中文摘要"两种统计量对潜伏方差的放缩倍数相差五倍，两个估计却相互一致"及讨论中的"形成闭环"。
- 问题："却"字把一致写成了出乎意料的证据，模拟结果却指向相反方向。两种统计量来自同一组计数、使用同一代际间隔，代际间隔设错、存在自相关或延迟时，两者会朝同一方向偏移。在真实 v_R 映射变动 0.33 倍（代际间隔 2.2 天）到 1.45 倍（4.3 天）的设定中，两个隐含方差始终一致；只有同步计数冲击打破了一致。
- 重要性：摘要中最强的正面论断，建立在一项多数替代机制都能通过的检验之上。审稿人读到表 S8 就会注意到这一点。
- 修改要求：写明这种一致说明了什么、没有说明什么。可参考的写法："两个估计相容（比值 0.93；95% CI：0.78, 1.18），这与两种统计量响应同一潜伏变异的预期相符；模拟中这一检查只拒绝了报告计数的同步冲击。"把 "closes the loop" 和"形成闭环"改为"与……相容"之类的说法。仅需改措辞。

D4 [P2]。位置：第 3.3 节（results.tex 第 58 行）；方法 6.8（methods.tex 第 79 行）；表 S8。
- 问题："一致"被定义为不拒绝差值为零。区间这么宽，不拒绝只是弱证据。数据匹配设定下比值区间（0.78, 1.18）不在 0.8 至 1.25 之内；十种设定中只有桥接设计和 8 天延迟两种的区间落在这一带内。计数冲击设定的区间（0.39, 0.90）与观测区间在 0.78 至 0.90 上重叠，所以数据不能完全排除混入计数冲击的情形，讨论最后一句也承认了这一点。
- 重要性：没有等效性表述，"一致"容易被读成"已证明相等"。
- 修改要求：用预先设定的等效带报告这一比值，或直接说明"一致"指不拒绝。现有的自助法和模拟抽样已足够完成这项工作。改措辞，另有可选的少量计算。

D5 [P3]。位置：摘要（0.040 和 0.043 未附条件）；第 3.3 节（results.tex 第 58 行）；讨论第 4 段；结论。
- 问题：代际间隔使 v_R^impl 在 0.013 至 0.063 之间变动。φ = 0.5 的 AR(1) 设定给出 0.027 和 0.025，低于区间，约为数据匹配值的三分之二。十种设定中，R_A 有 4 种落在 0.04–0.08 区间内，G 有 7 种。讨论提到了代际间隔的影响，没有提自相关；摘要和结论给出数值时两个条件都没有交代。
- 重要性：反演是本文最核心的新结果。读者需要知道，这一数值成立的前提是代际间隔为 3.6 天、窗口内各周冲击相互独立。
- 修改要求：(i) 估计 log R_A 相对州-季均值的窗口内偏差的一阶自相关，并与 M0 和 AR(1) 模拟中的分布比较，现有模拟器和数据即可完成；(ii) 用已发表的流感序列间隔估计 [7] 约束代际间隔，报告相应的 v_R^impl 范围；(iii) 在摘要中用一个分句写明条件，例如"以 3.6 天代际间隔为条件"。(i) 和 (ii) 需要新分析，工作量不大。

D6 [P4]。位置：第 3.1 节（results.tex 第 26 行）"21.3 to 49.2 cases …, a range that contains the empirical estimate for R_A"；附录 B.2（appendix.tex 第 135 行）"a range that contains the empirical value of 37.4 for R_A"；中文版对应句。
- 问题：21.3 至 49.2 是命题 1 情景网格下潜伏尺度的平衡规模，经验值 37.4 属于统计量尺度。稿件自己给出的 R_A 统计量尺度校准范围 13.9 至 31.1 并不包含它。这句话是第二轮版本在校准之前写下的，保留至今。
- 重要性：它与第 3.3 节相矛盾，也重复了 n2 和 n3 指出的尺度混淆。
- 修改要求：删去这两处"包含"分句，或者在同一尺度上比较（37.4 对 13.9–31.1，并给出第 93 百分位）。仅需改措辞。

D7 [P4]。位置：摘要"对应的平衡规模为每周 37.4 例住院（95% CI：19.1, 71.0）"；图 6。
- 问题：摘要先把 m× = A/v_R 定义为潜伏模型的性质，随后把 37.4 称为平衡规模。图 6A 图注已经写明统计量尺度，摘要没有；稿件也没有报告潜伏尺度的 m×。作为粗略核对，评审人在数据匹配模拟的取值（R̄ = 1.176，ρ = 0.01，k = 0.35，得 A = 1.216）和 v_R^impl 处计算命题 1，得到 m× ≈ 30（22, 46），单位是每代病例数。每周约 1.9 代，这个数不能直接与每周计数比较，所以换算应由作者在文中给出。
- 重要性：摘要中的设计规则（每周住院人数超过平衡规模之处）把统计量尺度的数值用到了潜伏尺度的问题上。
- 修改要求：改写为"在 R_A 尺度上，平衡规模为每周 37.4 例住院"；在第 3.3 节或表 S8 中报告由 v_R^impl 推得的潜伏 m×，附区间和单位。改措辞，另加少量计算。

D8 [P4]。位置：第 3.3 节；讨论第 4 段；图 3D。
- 问题：两种统计量的经验 b/a 都高于校准范围：R_A 为 37.4，范围为 13.9–31.1；G 为 23.5，范围为 8.0–18.8。与数据匹配点值之比分别为 1.34 和 1.45。两个百分位（第 93 和第 91）彼此相关，因为两种统计量用的是同一组计数，不能算作两个独立信号。图 3D 中 G 的模拟箱线明显低于经验值。讨论把超出归因于"住院人数的额外离散"，但没有检验。
- 重要性：决定 m× 和 m* 的是斜率 b。34% 至 45% 的未解释超出会直接带进设计规则。
- 修改要求：增加一个 k 更小或住院人数过度离散的模拟设定，报告它能否把 b/a 推到经验值，同时保持 v_R^impl 稳定。若不能，应说明模型低估了斜率，并在两个数值下分别给出设计规则。需少量分析。

D9 [p1]。位置：方法 6.8（methods.tex 第 77 行）；讨论第 4 段"模拟面板同样复现了数据的组内相关系数与全国周份额"。
- 问题：全国冲击的方差按假设取 0.45 v_R，方法部分没有说明 0.45 如何选定。模拟的分量（0.43）和组内相关系数（0.258）与数据（0.41 和 0.253）相符，至少部分出自构造。去掉全国冲击后组内相关系数为 0.050，而 v_R^impl 几乎不变（0.039 对 0.040）。
- 修改要求：说明 0.45 的来源（例如按数据中的分量匹配），把相符称为相容性检查，并补充 v_R^impl 对这一选择不敏感，这一点更有价值。仅需改措辞。

D10 [p2]。位置：标题；引言第 1 段。
- 问题：标题承诺的是"疫情再生数"的结果，而本文的估计对象是表观的每周统计量，反演也只在模拟器的模型之内还原 v_R。
- 修改要求：要么补充显式延迟分布和外部代际间隔下的更新方程估计，要么在标题中写"表观再生数"或"每周增长统计量"。选后者只需改措辞。

D11 [p4]。位置：摘要"落在截距 17% 的等效界之内"；第 3.5 节。
- 问题：界值取决于 τ0。τ0 = 0.10 时界值为 17%（R_A）和 12%（G），等效性成立，功效接近 1；τ0 = 0.05 时界值为 4.3% 和 3.0%，等效性不成立，功效为 0.25 和 0。
- 修改要求：摘要写成"落在截距 17% 的等效界之内（τ0 = 0.10）"。仅需改措辞。

D12 [p5, p6]。位置：摘要；第 3.3 节。
- 问题：英文摘要 281 词，报告了十余个估计值，基准文章的摘要不含数字；部分期刊把摘要限制在 250 词。"55% 的州周"指规则窗口中的行，并非三句之前提到的 10506 个州周。正文约 8288 词。
- 修改要求：若目标期刊限 250 词，摘要保留四个估计（37.4、两个 v_R、自愿期比值），其余移到结果部分；写成"增长窗口内 55% 的州周"；第 3.3 节逐项的敏感性语句移入表 S8。仅需改措辞。

D13 [p7]。位置：中文版导言区；英文参考文献（Delphi 网址）；英文第 22 页；图 3A；PDF 元数据。
- 修改要求：若期刊模板要求页眉，中文版也应加上；否则两版都去掉，使两版一致。只允许网址在斜杠处断行，或让 Delphi 网址单独成行；调整表 S8 和 S9 的位置，避免第 22 页大半空白；错开图 3A 中 0.040 和 0.043 的标签；两版 PDF 都设置 pdftitle。仅涉及版式。

D14 [p8]。位置：第 3.5 节；讨论第 7 段。
- 修改要求（可选）：利用实验室增长序列的分周或邻州结构估计其信度，把经衰减校正的共享比例作为一个界报告。

### 5 总体建议

建议：小修（Minor revision）。

评分：7.5 / 10。

理由。评分尺度与前两轮相同。6 分表示至少有一个问题可能改变主要结论。小修（7–8 分）表示剩余问题都不会改变已陈述的实证结果，但在关键位置上表述仍强于证据。8.5 分及以上表示剩余意见只涉及编辑。9 分及以上还需要反演得到外部支持，例如采用显式延迟和外部代际间隔的更新方程估计，或第二个监测系统的数据。

本轮修订解决了把评分压在 6 分的 N1：校准已实施并与数据匹配，不确定性已传递，结果落在哪里就报告在哪里。剩下的是 P1–P4，都不需要新数据。P1 和 P2 只需改措辞，它们决定摘要中关于报告和关于一致性的两条正面论断，能否以证据允许的强度陈述。P3 需要用现有模拟器做少量分析，P4 需要改措辞并补一项计算。评分没有更高，是因为这四个问题都位于承载全文主旨的摘要和结论。达到 8.5 分所需的最小改动见第 7 节。

评审人信心：数学、统计和数字溯源方面较高（4/5），均经脚本核查；对 NHSN 报告制度和流感代际间隔的流行病学解读为中等（3/5）。本评审为内部评审，评审人可能与作者有共同的盲点，投稿前仍建议做一次外部评审。

### 6 对第二轮意见的回应核查

判定分为已解决、基本解决、部分解决、未解决；依据是评审人对第三轮文件的阅读和核查脚本。

| 条目 | 第二轮要求 | 判定 | 依据与遗留 |
|---|---|---|---|
| N1 | 实施模拟校准 | 基本解决 | 数据匹配的两步反演，区间已传递（第 3.3 节；方法 6.8；表 S8）；表述遗留见 P2、P3 |
| N2 | 标题夸大下限 | 已解决 | 新标题不再有"不可约"；保留"适用范围与扩展"一段 |
| N3 | 说明 Parag 等人已含报告比例与负二项扩展 | 已解决 | 讨论第 3 段写明两者；拟合方差在 R_A 尺度上于 22 例时达到泊松方差的两倍，在潜伏尺度上为 28 例 |
| N4 | 表观统计量与再生数之别 | 部分解决 | 摘要两次使用 "apparent"；标题未改；没有更新方程估计（p2，D10） |
| N5 | 报告结论表述过强 | 结果部分与讨论第 7 段已解决 | 摘要、结论和讨论第 8 段的政策句仍有遗留（P1） |
| N6 | 分析沿革、作者署名、DOI | 部分解决 | 表 S9 给出日历窗口分析；署名与 DOI 属作者待办，不计分 |
| n1 | b/a 系数 3.9 与 7.1 | 已解决 | 改为校准范围 13.9–31.1 与 8.0–18.8 |
| n2 | 设计使用未校正的 21.3–49.2 | 部分解决 | 给出经验 m* = 19.4；"包含"表述仍在（P4，D6） |
| n3 | 图 6D 在统计量尺度上使用 37.4 | 部分解决 | 图 6A 图注写明尺度；摘要没有；无潜伏 m×（D7） |
| n4 | 图 6B 图注"精度下界" | 已解决 | 图 7B 图注改为"相对标准误" |
| n5 | 随机种子 | 已解决 | 方法 6.4 列出四个种子 |
| n6 | N 为 1748 与 1756 | 已解决 | 第 3.3 节解释了多出的 8 个州周 |
| n7 | 变异系数标签 | 已解决 | 标签与定义一致 |
| n8 | 表 S6 的负下界 | 已解决 | 改为 "n.d." |
| n9 | Δa 的 90% 与 95% 区间；分箱误差棒 | 已解决 | TOST 写明 90% 区间；图注说明了聚类 |
| n10 | 千位分隔符；网址断行 | 部分解决 | 分隔符已去掉；Delphi 网址仍在主机名内断行（p7） |
| n11 | 与基准文章对齐（篇幅、"we"、摘要） | 部分解决 | "we" 10 次；摘要 281 词且含数字；正文 8288 词（p5、p6） |
| n12 | 页眉、AI 声明、字体 | 部分解决 | AI 声明已对齐；中文版缺页眉（p7） |
| n13 | 摘要缺自愿期 | 已解决 | 摘要给出 1.58（0.95, 2.23），并注明为观察性对比 |

### 7 达到 8.5 需完成的最小改动清单

按对评分的影响排序。"改措辞"指只改文字；"新分析"指用现有数据和代码做新的计算。

1. P1，D1–D2（改措辞）。中英两版的摘要、结论和讨论第 8 段，改写政策句中关于报告的部分，并把 τ = 0.15 示例标为假设。
2. P3，D5（新分析，工作量小）。估计窗口内偏差的一阶自相关并与模拟分布比较，用外部估计 [7] 约束代际间隔，在摘要中写明条件。
3. P2，D3–D4（改措辞；可选少量计算）。把一致性改写为只排除同步计数冲击的相容性检查，删去 "closes the loop" 和"形成闭环"，并给出等效带或把一致定义为不拒绝。
4. P4，D6–D8（改措辞并做少量分析）。删去两处"包含"分句，在摘要中写明 37.4 所属的尺度，报告附单位的潜伏 m×，并增加一个住院人数过度离散的设定来检验 b/a 的超出。
5. p1、p4、p5，D9、D11、D12（改措辞）。说明 0.45 的来源，17% 界值附上 τ0，改正 55% 的分母。

只完成第 1、3、4 项且不做其中的可选计算，评分约为 8 分；五项全部完成可达 8.5 分。p7 的版式问题不影响评分，但投稿前应当修正。

### 8 叙事重构审慎性

作者方案要求把第二轮的防御性段落改写为发现。下表逐条核对改写引入的正面论断是否有证据支持，并判断新措辞是否带来了旧措辞没有的漏洞。

| 正面论断（位置） | 稿件中的证据 | 是否有支持 | 是否带来新漏洞 |
|---|---|---|---|
| 两步反演连接表观统计量与潜伏动力学（摘要；第 3.3 节；方法 6.8） | 数据匹配模拟器、校准线、已传递的区间、十种设定 | 是 | 否 |
| 放缩倍数相差五倍，两个估计"却"相互一致（摘要；讨论第 4 段） | 比值 0.93（0.78, 1.18）；十种设定中九种一致 | 部分：只能说明相容，不构成验证 | 是：诱导读者以为一致验证了数值（P2） |
| 校准"形成闭环"（讨论第 4 段；英文 closes the loop） | 同上；组内相关系数和全国分量的相符部分出自构造 | 部分 | 是，较轻：表述偏强，但后文紧跟三点限定（P2、p1） |
| v_R ≈ 0.04（摘要；结论） | 0.040 和 0.043 位于区间下沿，区间向下越出 | 作为条件估计成立 | 是：摘要未写条件（P3） |
| 多尺度分解（第 3.4 节；讨论第 6 段） | 全国周分量 41% 和 51%；合并辖区数 J = 33 和 25 | 是 | 否；稿件没有写"约 50%"，两个值都给出了 |
| 强制报告提高精度（摘要；结论；讨论第 8 段） | 强制期 2.0%（上界 5.3%）；观察性比值 1.58（0.95, 2.23） | 按现有措辞不成立 | 是：本轮主要的新漏洞（P1） |
| 收益递减与设计查对图（第 3.6 节；图 6） | 命题 1；经验 b/a；查对图 | 是 | 较轻：摘要未写明 37.4 的尺度（P4） |
| 平衡规模范围"包含"37.4（第 3.1 节；附录 B.2） | 与校准范围 13.9–31.1 矛盾 | 否 | 沿袭旧稿而非新增，仍需删除（P4） |
| 与 Parag 等人互补（讨论第 3 段） | 拟合方差达到泊松方差两倍的位置为 22 例（表观）和 28 例（潜伏），十倍处为 261 和 262 例 | 是 | 否 |
| "适用范围与扩展"一段 | 存在 | 已按要求保留 | 否 |

改写去掉了防御性用语（concede、negligible、cannot be established 均为 0 次），也没有引入最高级表述。方案中缺乏支持的说法（"完美对齐""制度防火墙""自然实验""普适临界尺度"）都没有采用，摘要也把自愿期对比称为观察性的。但新写的正面语句中有两处超出了证据（P1、P2），另有一处沿袭下来的语句与新结果相矛盾（P4）。

作者方案中数字的核对：

| 方案数字 | 稿件与 results.json 的实际情况 | 结论 |
|---|---|---|
| 2.68（G）与 0.484（R_A） | 17 个通用情景下无噪声放缩系数的中位数；数据匹配值为 2.729 和 0.516 | 已由数据匹配值取代，使用正确 |
| 0.0451 | 方案公式得 0.0449（R_A）和 0.0456（G）；方案中 G 公式的原写法得 0.0216（量纲错误）；校准线得 0.040 和 0.043 | 已被取代；稿件使用 0.040 和 0.043 |
| R̄ = 1.206 | 规则窗口内 R_A 的样本均值；模拟器的真实 R̄ 为 1.176 | 作为样本均值正确 |
| 0.04–0.08 区间 | 两个点值都在下沿，区间都向下越出；十种设定中 R_A 有 4 种、G 有 7 种落在区间内 | 第 3.3 节如实陈述 |
| 13.4–28.7 | 第二轮由通用系数得到的值，已由 13.9–31.1（R_A）和 8.0–18.8（G）取代。G 的 23.5 在旧范围内、高于新范围；R_A 的 37.4 在两个范围之外，区间与之重叠 | 已被取代，稿件中不再出现 |
| 23.5（8.4, 59.7） | G 的 b/a | 核实无误 |
| 37.4（19.1, 71.0） | R_A 的 b/a | 核实无误 |
| 全国分量"约 50%" | 41%（R_A）和 51%（G） | 稿件给出两个值 |
| 17% | τ0 = 0.10 时的等效界值；实测变化为 2.0%，上界 5.3% | 作为界值正确，不是实测效应（p4） |
| 58% | 四分位距之比 1.58（0.95, 2.23）；观察性；区间包含 1 | 加限定后正确 |
| 参与率 >95% | 制度 1（D ≥ 5）中位数 92.3%，规则窗口 93.7%；制度 1 中参与率不低于 95% 的州周占 46.7% | 方案数字无支持；稿件写的是"约 93%" |
| 2.1 万州周 | 原始辖区周 21641；分析面板 10506 行；规则窗口 1748 和 1756 | 稿件使用 10506 |

### 9 核查记录

- 头条数字（A 块，键 A_headline）：94 个由 results.json 格式化的数值，在中英两版源文件中全部找到；A_failures 为空。英文摘要中的每个数字都出现在中文摘要中（A_abstract）。
- 中英数字（B 块）：仅中文版多出少量小整数（月份和序数），没有实质差异。
- 派生量（C 块，C_derived）：user_formula_*、calib_line_*、kappa_ratio_G_over_RA_fit（5.29）、settings_table（全部十一种设定）、settings_vR_differs_from_M0_by_factor（0.33 至 1.45）、settings_ratio_ci_within_0.8_1.25（bridge_s08、delay_long）、agreement_overlap_count_shock_vs_observed（0.78 至 0.90）、rho0_sim_icc_RA_vs_data（0.050 对 0.253）、ba_empirical_above_pooled_range、ba_ratio_emp_over_M0（1.34、1.45）、old_round2_range_*、margin_share_check_*（0.170、0.043、0.030）、delta_share_check_RA（0.020）、iqr_ratio_ci_includes_1、regime1_share_ge95（0.467）、theory_rep_share_of_MSE（0.349）、theory_vH_share_of_limiting_var（0.434）、theory_standardise_vs_x10（14.65、18.71）、share_above_mcross_RA_G（0.553）、latent_A_prop1_at_M0（1.216）、latent_mcross_prop1_at_vR_impl（30.3）及其区间（21.7, 46.3）、generations_per_week_at_GI3.6（1.94）。
- results.json 键：reporting_regime.RA_rule4_delta_a_share.upper95_one_sided（0.0528，即摘要中的 5.3%）；s04_reporting 中 τ0 = 0.05 的 TOST 功效（R_A 为 0.251，G 为 0）。
- PDF 事实（D 块）：两版均为 24 页；无 "??"；字体全部嵌入；无 Type 3 字体；7 个图环境；Title 元数据为空。
- 措辞（E 块）：perfect、universal、首次、普适均未出现；"证明" 8 次，全部为证明环境标题；"closes the loop" 1 次，"闭环" 2 次；防御性用语未出现；"causal" 1 次，位于否认因果效应的句子中；摘要英文 281 词、中文 663 字；"we" 10 次；英文版有页眉、中文版没有；英文 PDF 中 Delphi 网址在主机名内断行；没有不合规的地名表述。
- 逐页检查：48 页全部渲染并查看，发现记入 p7 与 D8。

### 10 作者待办（不计分）

- 真实作者姓名与机构，替换 "Apevon Science"。
- 基金资助声明。
- CRediT 作者贡献声明。
- 代码与数据快照的存档 DOI（例如 Zenodo），并在代码可得性声明中引用。

### 11 终修核查（附录）

- 核查版本：output/case-count-bottleneck/paper/（英文，25 页）与 output/case-count-bottleneck-zh/paper/（中文，26 页）的终修版；作者答复追加在 .work/case-count-bottleneck/paper/revision_response_r3.md 的“Final polish”一节及中文稿对应文件中。日期：2026 年 10 月 20 日。
- 方法：第三轮核查脚本原样对已发布文件重跑（final_polish_checks.py，输出 final_polish_checks.json，与此前同一目录）。新增数值逐项对照 results.json 的 polish.* 键与 analysis/parts/polish.json。两份 PDF 全部渲染并逐页查看。以下判断以文件为准，不以答复文件为准。
- 行号指 sections/*.tex。中英文稿的修改位于相同行号。

#### 11.1 第 7 节清单逐条核查

| 条目 | 要求 | 终修版的处理 | 证据 | 判断 |
|---|---|---|---|---|
| P1，D1 | 拆分政策句；报告证据写成关联 | 摘要、结论与设计段把时期数与区域数保留为设计结论；报告证据写成“较高的机构参与度与较低的波动相伴”。“实行强制且完整”与 mandatory and complete 在 PDF 中均为 0 处。讨论中报告制度一段以“在观察性比较所允许的范围内……与较高机构参与度的益处相一致”起句 | abstract.tex:2；conclusion.tex:4；discussion.tex:16、18 | 已解决 |
| P1，D2 | 标明 τ = 0.15 为假设；可选的校准版本 | 第 3.1 节与设计段均标为“假设示例”。可选计算已做：5.3% 上界只允许 τ 约为 0.04，此时病例量增加十倍使均方误差降至 11.4，报告标准化降至 14.6（原为 15.2，单位 10⁻³）。正文据此正确地得出该 τ 下增加病例更有效 | results.tex:26；discussion.tex:18；polish.tau_allowed_by_upper_share = 0.0404；polish.lever_at_tau_allowed_total = 15.22 | 已解决，含可选部分 |
| P2，D3 | 一致性改写为一致性检查；删去“闭环” | 摘要：“两者相互一致（比值 0.93）”。closes the loop 与“闭环”均为 0 处。讨论称其为效力有限的检验，只在同步计数冲击下被打破，并补充该设定下数据中 G 的滞后一阶自相关高于 99% 的模拟面板，这是一个有用的附加判别 | abstract.tex:2；discussion.tex:10 | 已解决 |
| P2，D4 | 等效界，或把一致定义为未拒绝 | 两者都做了。方法 6.8 节与第 3.3 节把一致定义为未拒绝（与表 S8 对应）。主设计的双单侧检验给出比值 90% 区间 0.81–1.13，落在 0.80–1.25 内。第三轮所述 95% 区间（0.78，1.18）不在界内的判断依然成立；双单侧检验使用 90% 区间，是标准构造 [6] | methods.tex:79；results.tex:56、58；polish.ratio_vR_RA_over_G_ci90 | 已解决 |
| P3，D5（i） | 窗口内偏差的滞后一阶自相关，与 M0 和 AR(1) 比较 | R_A 的 r1 为 −0.095（−0.168，−0.019），G 为 0.123（0.039，0.201）。独立冲击下模拟均值为 −0.074 和 0.114（数据位于第 31 和第 62 百分位）。φ = 0.25 时数据位于第 3 和第 10 百分位，φ = 0.5 时低于全部面板。正文正确指出两种统计量因构造本身带有自相关，因此比较对象是模拟分布，而不是零 | results.tex:60；表 S10 A 部分；polish.r1_* | 已解决 |
| P3，D5（ii） | 以 [7] 界定代际间隔 | 引用了 Cowling 等，并在 2.9 天下重跑反演：隐含方差 0.026（0.017，0.036）和 0.027（0.016，0.040）；4.3 天时为 0.058 和 0.063。0.026–0.063 取代了此前的 0.013–0.063，后者包含外部区间之外的 2.2 天设定 | results.tex:60；discussion.tex:10；methods.tex:24、79；polish.vR_impl_*_GI_2.9_to_4.3 | 已解决 |
| P3，D5（iii） | 在摘要中写明条件 | 摘要与结论：以 3.6 天的代际间隔和相互独立的周冲击为条件 | abstract.tex:2；conclusion.tex:4 | 已解决 |
| P4，D6 | 删去两处“包含”表述 | 两处均已删去（contains the empirical 与“这一范围包含”均为 0 处）。21.3–49.2 现称“每代的潜伏平衡规模” | results.tex:26；appendix.tex:135 | 已解决 |
| P4，D7 | 写明 37.4 的尺度；给出潜伏 m× | 摘要：“按该比值的尺度对应每周 37.4 例住院”。第 3.3 节给出潜伏 m× 为每代 30.3（21.7，46.3），按每周 1.94 代折合约每周 59 例，并说明 37.4 并不直接估计它。设计段称 37.4 为“表观平衡规模”。这些数值与审稿人自己的核算一致（C 块：30.3、21.7、46.3、1.94） | abstract.tex:2；results.tex:56；discussion.tex:12；polish.latent_mcross_RA、_per_week | 已解决 |
| P4，D8 | 用一个过度离散住院设定解释 b/a 超出 | 伽马–泊松住院数，方差均值比 1.5 与 2.0。v_R = 0.04 处，R_A 的 b/a 由 28.0 升至 68.0 和 81.0，G 由 16.2 升至 40.2 和 48.4，而隐含方差保持在 0.039–0.045。因此方差均值比介于 1 与 1.5 之间即可复现这一超出。另一种现已写入正文的解释见 11.2 | results.tex:60；discussion.tex:10；表 S10 B 部分；polish.od05_*、od10_* | 已解决 |
| p1，D9 | 说明 0.45 如何设定；把匹配称为一致性检查 | 0.45 取在观测份额 0.41 与 0.51 之间；匹配称为一致性检查，并写明隐含方差对该份额不敏感（份额取 0 与 0.65 时为 0.039 与 0.040） | methods.tex:77；discussion.tex:10 | 已解决 |
| p4，D11 | 给出 17% 界对应的 τ0 | 摘要写为“参考报告波动取 0.10 时，等效界为截距的 17%”，讨论同 | abstract.tex:2；discussion.tex:4 | 已解决 |
| p5，D12 | 修正 55% 的分母；如有字数上限则缩短摘要 | 改为“增长窗口中占 55% 的州周”。按第三轮相同的 detex 计数，英文摘要由 281 词降至 256 词；中文摘要 658 字（此前 663 字） | abstract.tex:2；final_polish_checks.json E_wording | 分母已解决；英文摘要仍比 250 词上限多 6 词 |
| p7，D13 | 格式 | 两版都不再有页眉，因而一致。Delphi 网址不再在主机名内断行（url_break_in_host_en 为 false）。英文稿第 22 页现由表 S8–S10 填满。图 3A 中 0.040 与 0.043 两个标签位于竖线旁（已在渲染图上核实）。两份 PDF 都设置了 pdftitle | main.tex；endmatter.tex；appendix.tex:195；pdfinfo | 已解决 |

可选与不计分条目：D10（标题）未改，标题仍为 reproduction numbers。D14（实验室代理变量的信度校正）未做。p6（篇幅）未处理，见 11.2。

#### 11.2 终修版中的新观察

- F1（已在核查中解决）。2.9 天设定在 v_R = 0.02（与其自身隐含方差最接近的网格值）处，实证 b/a 位于模拟分布的第 52.5（R_A）和第 58（G）百分位（parts/polish.json，emp_ba_percentile_at_nearest）。因此，较短的代际间隔与轻度过度离散一样能解释 b/a 的超出，而两种解释对应的 v_R 水平不同（约 0.026 与 0.040）。审稿人在核对表 S10 时提出这一点；终修版已在第 3.3 节与讨论中写明，并给出不支持较短间隔、但不能将其排除的自相关证据（results.tex:60；discussion.tex:10）。摘要已把方差水平写成以 3.6 天为条件，因此没有核心结论需要改动。
- F2（编辑性）。新增分析使篇幅增长。按第三轮相同口径，正文约 8990 词（此前 8288 词）；结果部分 3139 词，讨论 1818 词。第 3.3 节逐个设定的句子以及新增的三项假设检验段落，可以移入表 S8 与表 S10 的注释，损失不大。
- F3（编辑性）。摘要中的设计句使用表观尺度（每周 37.4 例，增长窗口中 55% 的州周）。潜伏值折合约每周 59 例，超过潜伏规模的州周比例会更低。补一句该比例或指向第 3.3 节，可以让使用这条规则的读者把两种尺度对上。
- F4（编辑性）。两种语言版本的新增数值一致：核对的 39 个 polish 数值在两份源文件中都出现。A 块 94 个核心数值在两版中仍全部找到，0 个失败。B 块只显示预期的小整数差异（lag-1 写作“滞后一阶”、序数与月份）。

#### 11.3 更新后的建议

建议：小修（仅编辑性修改）。

评分：8.5 / 10。

理由。尺度与第 5 节相同。第 7 节五项全部完成，包括 D2、D4 与 D7 中的可选计算。摘要与结论现在把报告证据写成观察性关联，把一致写成一致性检查，并写明反演的条件。37.4 的尺度已写明，“包含”表述已删去。两项轻量分析（自相关与外部代际间隔界）支持独立性假设，并把 v_R 的水平界定在 0.026–0.063。过度离散设定为 b/a 的超出给出了经检验的解释，较短间隔的替代解释（F1）也已并列写出。剩余意见都不改变已陈述的结果。F2、F3、256 词的摘要以及可选的 D10 与 D14 属于编辑性问题。这符合第 5 节对 8.5 分的定义。

未给 9 分。第 5 节把反演的外部支持设为 9 分及以上的条件，例如带显式住院延迟与外部代际间隔的更新方程估计，或第二个监测系统。终修版增加了代际间隔的外部界，但仍没有 v_R 的独立估计，v_R 的水平仍以代际间隔为条件（外部区间内为 0.026–0.063）。与 9 分的差距就是这样一项分析。压缩正文（F2）、补充潜伏尺度比例（F3）并把摘要压到 250 词以内，可以消除编辑性遗留，但仅凭这些不会使评分高于 8.5。

审稿人信心不变：数学、统计与数值溯源为高（4/5），流行病学解释为中等（3/5）。第 5 节关于内部评审的说明仍然适用。

#### 11.4 本附录的核查记录

- 数值：final_polish_checks.json 的 A 至 E 块（A_failures 为空；A_abstract 为空）。新增数值：results.json 键 polish.r1_*、polish.gi_cow_lo_*、polish.od05_*、polish.od10_*、polish.ar025_*、polish.latent_mcross_*、polish.ratio_vR_RA_over_G_ci90、polish.tau_allowed_by_upper_share 与 polish.lever_at_tau_allowed_total。百分位见 parts/polish.json 的 r1_simulated_v0.04 与 new_settings 两块。
- PDF：英文 25 页，中文 26 页。无“??”。全部字体嵌入，无 Type 3 字体。两版都设置了标题元数据，都没有页眉。
- 门禁（作者报告、审稿人重跑）：manuscript QA 0 error（英文 10 条已审 warning；中文在字体回退下 2 条已审 warning）。statistical_table_qa：两版各 10 张表、0 error。引用核查：参考文献 44 条全部被引用，无孤立条目。style_gate（paper）与 territory_gate 退出码为 0。中文稿严格字体门仍报 2 个 error（构建环境中没有授权 SimSun），作者已披露。这是构建环境问题，不计入评分。
- 措辞：完美、普适、首次、closes the loop 与“闭环”均未出现。first 出现 24 次，均为 first-order、first target 之类。“证明”出现 8 次，均为证明环境标题。causal 出现 1 次，位于否认因果效应的句子中；中文稿“因果”同样只出现在否认句中。we 出现 10 次。
- 逐页查看：两版共 51 页，全部渲染并查看。

### 参考文献

参考文献编号与 Part A 相同，见上文 [1]–[7]。
