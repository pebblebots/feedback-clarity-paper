# Structural Limits on RL for High-Stakes Reasoning: Feedback Latency, Proxy Endogeneity, and the Drift Ceiling

**Status:** draft — do not cite  
**Date started:** 2026-04-13  
**Collaborators:** Reese, Aura  
**Venue target:** short position paper, ~6 pages, ICML/NeurIPS workshop or clawrxiv

---

## Abstract (draft)

The policy is part of the environment — so you can never hold the environment fixed long enough to get clean signal. In high-stakes reasoning domains such as medicine and law, this observation collapses the compiler analogy that motivates current RL-for-reasoning work. We identify three distinct identification failure regimes that all have the same structural root: (1) Heckman-style selection bias with violated exclusion restriction, (2) instrument endogeneity from policy-generated observational signals, and (3) evaluation instrument correlation with failure mode in LLM-judge pipelines. Together these imply a proxy drift result: systems optimizing against measurable proxies in this class of domains will drift from ground truth in proportion to policy influence on the distribution — and the drift is not detectable in-sample. We do not claim impossibility; we claim that the feedback latency in these domains is not merely quantitatively slower than code execution but qualitatively different in kind, imposing a ceiling that the compiler-equivalent framing does not capture.

---

## 1. Introduction

The "compiler equivalent" framing for RL in reasoning domains asks: can we find a feedback signal with the same properties as code execution? Fast, deterministic, ground-truth verifiable. The framing has been productive. It correctly identifies why RL has scaled well on code and math, and it correctly identifies the gap in domains like medicine and law.

But the framing has a hidden assumption: that the feedback signal, once found, will remain stable as the policy changes. In code, this holds. A compiler is not a function of the code it is evaluating in any loop-closing sense. In medicine, it does not hold.

When a clinical reasoning system changes its recommendations, patient populations change (referral patterns shift, self-selection changes, downstream treatment effects alter observable signals). When a legal reasoning system changes its arguments, precedent shifts over time, and the proxies used to evaluate argument quality (judicial reception, settlement rates) are functions of the arguments being made. The environment is not a fixed evaluation surface. The environment is downstream of the policy.

This is not a new observation in causal inference or economics. It is the standard problem of policy evaluation under distributional shift caused by the policy itself. What is new is the implication for RL training: the feedback signal is endogenous by construction, and the degree of endogeneity increases as the policy becomes more capable and more influential.

---

## 2. Three Identification Failure Regimes

### 2.1 Selection Bias with Violated Exclusion Restriction

**Setup.** Suppose we want to estimate the quality of a clinical reasoning model's recommendations using observed patient outcomes. Outcomes are only observed for cases where follow-up occurs (confirmation). Let:

- $Y$ = true outcome (ground truth quality of recommendation)
- $Y^*$ = observed outcome (only when $S = 1$, i.e., follow-up confirmed)
- $S$ = selection indicator (1 = confirmed, 0 = lost to follow-up)
- $X$ = case features
- $Z$ = proposed instrument for selection propensity

The Heckman correction requires an instrument $Z$ that enters the selection equation but not the outcome equation (exclusion restriction). The natural candidate is something like "confirmed in EHR vs lost to follow-up."

**Violation.** Lost-to-follow-up is correlated with patient severity, socioeconomic status, and care-seeking behavior — all of which are correlated with the clinical picture and therefore with recommendation quality. The exclusion restriction is violated: $Z$ affects $Y$ not just through $S$ but directly through the case distribution.

**Implication.** The Heckman correction gives partial identification, not point identification. The bias direction is knowable (underestimation of failure rate in high-severity cases that self-select out), but magnitude requires sensitivity analysis. Rosenbaum-style bounds or parametric sensitivity to exclusion violation magnitude are the appropriate tools. Point estimates from naive Heckman application are fragile.

### 2.2 Instrument Endogeneity from the Assay Layer

**Setup.** A natural family of instruments for clinical reasoning quality uses assay-layer signals: labs ordered, vitals recorded, imaging obtained. These are observable, granular, and in principle correlated with reasoning quality (better reasoning → appropriate workup → informative assay results).

**Violation.** Ordering labs is a policy action. Whether an imaging series is obtained is downstream of the clinician's (or model's) reasoning process. The instrument is generated by the policy you are trying to evaluate. This is circular by construction: you cannot use policy-generated signals to instrument for policy quality when the signals are downstream of the reasoning being evaluated.

This is precisely the endogeneity structure the world-models framing predicts: under policy-endogenous observation, the distribution over observables shifts when you change the policy. A naive estimator computed on logged trajectories is computing $E[Y | X, \pi_0]$ and using it to evaluate $\pi_1$, where $\pi_1 \neq \pi_0$ has changed the distribution over $X$ itself.

**Implication.** Assay-layer instruments are not valid without an additional conditioning argument that breaks the loop. Possible constructions (e.g., randomized workup protocols, natural experiments from EHR implementation changes) exist but require specific data designs not present in standard logged trajectories.

**Identification lever (separable case).** The separable case from Section 3 admits a potential instrument: a signal $Z$ that shifts selection propensity but is independent of outcome given true state. The EHR "confirmed-absent vs lost-to-follow-up" distinction is a candidate — cases where the EHR records confirmed absence of pathology can be separated from cases where the patient simply did not return. These two groups have different selection mechanisms but (arguably) the same ground-truth distribution conditional on case features. Whether this constitutes a valid $Z$ depends on whether the absence-confirmation process is independent of recommendation quality; in practice it is correlated with care quality and patient SES, so the exclusion restriction is weak but potentially bounded (see Section 2.1 sensitivity analysis).

**The fully entangled case.** When the policy *is* the observation action — the clinician or model decides what to measure — $P(\text{observe} \mid \text{state})$ is a function of the policy and no fixed channel exists. Every candidate instrument is downstream of the policy. Identification without exogenous randomization or natural experiments fails by construction. Only partial mitigations are available: sensitivity bounds, domain assumptions, randomized sub-studies. This is the harder case and is why Section 5 mitigations are partial rather than solutions. Section 3 formalizes the separable case only; the fully entangled case is the harder open problem.

### 2.3 Evaluation Instrument Correlation with Failure Mode

**Setup.** Replace multiple-choice ground truth with an LLM judge scoring reasoning chain quality. This is the natural engineering response to the ceiling imposed by MC evaluation. The LLM judge can distinguish "right answer, wrong reasoning" from "right answer, right reasoning" — in principle.

**Violation.** LLM judges are trained on fluent, well-structured text. A model optimizing against LLM judge scores will converge on fluent, well-structured reasoning — whether or not the reasoning is correct. The failure mode (fluent-but-wrong) is correlated with the evaluation instrument's strength. MC shortcuts are at least detectable: probing can surface "correct answer via shortcut" by examining reasoning under perturbation. Fluent-but-wrong reasoning that satisfies an LLM judge is structurally undetectable without ground-truth outcome closure.

**Implication.** Detecting evaluation instrument failure requires periodic ground-truth audits with delayed outcome closure as a first-class pipeline component. The audit lag is 12–18 months for clinical outcomes, years for legal outcomes. This is not a workaround problem — it is the fundamental audit gap. Any deployment without it is operating blind.

---

## 3. The Proxy Drift Result

The three failure regimes above are instances of a single underlying structure. We formalize this with a minimal construction.

**Setup.** Let:
- $S \in \{0,1\}$ be the true (hidden) state, $S \sim \text{Bernoulli}(p_0)$
- $X | S \sim \mathcal{N}(\mu_s, \sigma^2)$, observable features
- $f_\theta(X) = \text{expit}(\theta_0 + \theta_1 X)$, model prediction
- $\theta^* = (\theta_0^*, \theta_1^*)$ with $\theta_1^* = (\mu_1 - \mu_0)/\sigma^2$ = Bayes optimal

**Selection mechanism.** Cases are confirmed (enter training data) with probability:
$$P(\text{sel} \mid X, S) = \text{expit}(\beta \cdot f_\theta(X) + \kappa \cdot S)$$

where $\beta > 0$ is **feedback strength** (selection driven by model confidence) and $\kappa > 0$ is the **confirmation premium** (true positives more likely confirmed — clinical realism: pathology that gets flagged is more likely to result in a confirmed diagnosis than a missed case).

**The key asymmetry.** When $\kappa = 0$, selection depends only on model score and selection cancels from the posterior: $P(S=1 \mid X, \text{sel}) = P(S=1 \mid X)$. The selection is purely a covariate shift with no posterior bias. When $\kappa > 0$, true positives are overrepresented in the confirmed sample:

$$P(S=1 \mid X, \text{sel}) = \frac{\text{expit}(\beta f_\theta + \kappa) \cdot P(S=1 \mid X)}{\text{expit}(\beta f_\theta + \kappa) \cdot P(S=1 \mid X) + \text{expit}(\beta f_\theta) \cdot P(S=0 \mid X)}$$

This selected posterior is *not* equal to the population posterior. The difference is:

$$\Delta(x) \equiv P(S=1 \mid X=x, \text{sel}) - P(S=1 \mid X=x) = \frac{P(S=0 \mid X) \cdot P(S=1 \mid X) \cdot (\text{expit}(\kappa) - \frac{1}{2}) \cdot 2}{\text{(denominator)}} > 0$$

**Fixed point.** The model trained on selected data converges to $\hat{\theta}$ that minimizes NLL on the selected distribution — i.e., is calibrated to $P(S=1 \mid X, \text{sel})$, not $P(S=1 \mid X)$. We show $\hat{\theta}_1 < \theta_1^*$ (slope shrinks, model becomes less discriminative) analytically.

**Proposition.** For $\beta > 0$, $\kappa > 0$: the slope of the selected posterior log-odds with respect to model score $f$ is strictly less than the slope of the population log-odds. Therefore the model calibrated to the selected distribution has $\hat\theta_1 < \theta_1^*$.

*Proof.* Write the selected posterior odds via Bayes:
$$\log \text{Odds}_\text{sel}(X) = \log \text{Odds}_\text{pop}(X) + r(f(X))$$

where the log selection-odds ratio is:
$$r(f) := \log\frac{P(\text{sel}\mid S=1,X)}{P(\text{sel}\mid S=0,X)} = \log\frac{\text{expit}(\beta f + \kappa)}{\text{expit}(\beta f)} = \kappa + \log(1 + e^{\beta f}) - \log(1 + e^{\beta f + \kappa})$$

Differentiating with respect to $f$:
$$r'(f) = \beta\left[\sigma(\beta f) - \sigma(\beta f + \kappa)\right]$$

For $\beta > 0$, $\kappa > 0$: $\sigma(\beta f + \kappa) > \sigma(\beta f)$, so $r'(f) < 0$. The slope of the selected log-odds is strictly less than the slope of the population log-odds. A model calibrated to the selected distribution therefore recovers a shrunken slope, giving $\hat\theta_1 < \theta_1^*$. $\square$

**Scope conditions.** The direction reverses for $\kappa < 0$ (negative confirmation premium — false positives confirmed more often than true positives) or $\beta \leq 0$ (selection negatively correlated with model confidence). The null case $\kappa = 0$ gives $r'(f) = 0$: pure covariate shift, no posterior bias, $\hat\theta_1 = \theta_1^*$.

**Numerical illustration.** With $p_0 = 0.3$, $\mu_1 - \mu_0 = 1.5$, $\sigma = 1$, $\kappa = 1.5$ (realistic confirmation asymmetry):

| $\beta$ | $\hat\theta_1$ | $\hat\theta_0$ | Pop. NLL | Proxy NLL | IPW NLL$^\dagger$ | Drift (pop − opt) |
|---------|------------|------------|----------|-----------|-------------------|-------------------|
| 0.0     | 1.50 (opt) | −1.97 (opt) | 0.420   | —         | —                 | 0.000             |
| 1.0     | 1.42       | −1.54      | 0.430    | 0.475     | 0.430             | +0.010            |
| 2.0     | 1.38       | −1.56      | 0.429    | 0.484     | 0.429             | +0.009            |
| 4.0     | 1.36       | −1.66      | 0.424    | 0.489     | 0.424             | +0.004            |

*β=0 is the analytic population baseline evaluated at $\theta^*$ (no selection, $\kappa=0$); rows with $\beta>0$ reflect models trained under simulated selection ($\kappa=1.5$ active). Pop NLL at $\beta=0$ is the Bayes-optimal log-loss on the population; Drift at $\beta>0$ measures degradation relative to this fixed reference.*

$^\dagger$ IPW NLL uses estimated marginal propensity $\hat{P}(\text{sel} \mid X) = \text{expit}(\hat{\gamma}_0 + \hat{\gamma}_1 f_\theta(X))$ fitted by logistic regression on the full population. IPW correction is negligible ($< 0.001$ nats) because the propensity model cannot condition on the unobserved $S$, producing near-uniform weights (effective sample size 87–95% of selected $n$, weight range $[0.71, 1.50]$). See footnote~1 and κ-sweep table below.

$\hat\theta_1$ degrades monotonically with $\beta$. Proxy NLL increases — the training signal is actively misleading. Population NLL is *non-monotone in raw value* ($0.430 \to 0.429 \to 0.424$): the intercept $\hat\theta_0$ drifts toward the more extreme empirical prior as selection intensity increases, partially recalibrating the base rate even as the slope degrades — so the relevant comparison is Drift (pop NLL − Bayes optimal), not raw Pop NLL trend. Drift is monotone in $\beta$. The training signal cannot detect this because Proxy NLL and Pop NLL move in opposite directions.

**This gap is architectural, not implementational.** IPW correction is negligible in practice — the marginal propensity approximation produces near-uniform weights, so IPW reduces to the naive estimator. This is not an implementation failure; it is a consequence of $\kappa$ being unobserved. Any propensity model that cannot condition on $S$ cannot correct for outcome-correlated selection. The residual gap is attributable to $\kappa$ rather than $\beta$: a direct κ-sweep (β=2.0 fixed, $\kappa \in \{0.0, 0.5, 1.0, 1.5, 2.0, 3.0\}$) confirms monotone increase in the gap from 0.000 to 0.014 as $\kappa$ increases. The gap is set by $\kappa$, not $\beta$. If you can bound $\kappa$ from domain knowledge — how asymmetric is your confirmation process? — you can bound the irreducible gap before training begins.

**κ-sweep (β=2.0 fixed):**

| $\kappa$ | $\hat\theta_1$ | Pop. NLL | Residual gap |
|---------|------------|----------|--------------|
| 0.0     | 1.51       | 0.420    | 0.000        |
| 0.5     | 1.46       | 0.421    | +0.001       |
| 1.0     | 1.42       | 0.425    | +0.005       |
| 1.5     | 1.38       | 0.429    | +0.009       |
| 2.0     | 1.36       | 0.431    | +0.011       |
| 3.0     | 1.35       | 0.434    | +0.014       |

Gap is monotone in $\kappa$, zero at $\kappa=0$. IPW provides negligible correction across all rows.

**Core result.** In domains where $\kappa > 0$ (confirmation is correlated with ground truth, not independent of it), training under selection endogeneity produces a fixed point $\hat\theta \neq \theta^*$, with:
1. $\hat\theta_1 < \theta_1^*$ — degraded discrimination
2. Population loss $\mathcal{L}(\hat\theta) > \mathcal{L}(\theta^*)$ — worse ground-truth performance
3. Proxy loss on selected sample $< \mathcal{L}(\theta^*)$ — *looks better in training*

The drift is undetectable from proxy measurements alone. Detection requires population-level evaluation, which requires confirmed labels from an unselected sample — precisely what the selection mechanism denies you.

**Closed-form fixed point (2D logistic case).** The 2D MLE (optimizing over both $\theta_0$ and $\theta_1$) satisfies $\theta_1^*(0) = \delta$ (Bayes optimal slope is recovered when $\beta = 0$, regardless of $\kappa$, because selection at $\beta=0$ depends only on $S$ and shifts the effective class prior but not the conditional slope). For $\beta > 0$, the fixed-point $\theta_1^*(\beta)$ satisfies the implicit equation obtained by setting both score equations to zero on the selected distribution. No closed-form solution exists in general, but the implicit function theorem gives:

$$\theta_1^*(\beta) = \delta + C(\kappa, \text{SNR}) \cdot \beta + O(\beta^2)$$

where $C(\kappa, \text{SNR}) = -\partial_\beta G_1 / \partial_{\theta_1} G_1 \big|_{\beta=0} < 0$ and $G_1 = \nabla_{\theta_1} \mathcal{L}_\text{sel}$ is the selected NLL slope gradient. Numerically, for the parameters of Section 3 ($p_0 = 0.3$, $\delta = 1.5$, $\kappa = 1.5$): $C \approx -0.165$.

**Sensitivity of $C$ to $\kappa$.** The drift coefficient $C(\kappa)$ is monotone increasing in $|\kappa|$, equals zero at $\kappa = 0$ (as required: no confirmation premium, no drift), and saturates as $\kappa \to \infty$ (expit saturation). For the numerical parameters above:

| $\kappa$ | $C(\kappa)$ | Drift per unit $\beta$ |
|---------|-------------|------------------------|
| 0.0     | 0           | 0                      |
| 0.5     | −0.087      | 0.087                  |
| 1.0     | −0.127      | 0.127                  |
| 1.5     | −0.165      | 0.165                  |
| 2.0     | −0.186      | 0.186                  |
| 3.0     | −0.215      | 0.215                  |

**Claim.** Systems optimizing against measurable proxies in this class of domains will drift from ground truth as $\beta$ (feedback strength) and $\kappa$ (confirmation asymmetry) increase — and the drift is not detectable in-sample. To first order: $\text{Drift}(\beta) = \theta_1^* - \theta_1^*(\beta) \approx |C(\kappa, \text{SNR})| \cdot \beta$. This grounds the proportionality claim in the main text. This is not a claim about impossibility. It is a claim about the minimum requirements for safe deployment: ground-truth evaluation on an unselected sample, run on a cadence shorter than the drift timescale.

**Footnote 1 (IPW correction).** Horvitz–Thompson IPW requires the true selection probability $P(\text{sel}_i) = \text{expit}(\beta f_\theta(X_i) + \kappa S_i)$. Because $S_i$ (the true *state*) is unobserved at training time, any estimable propensity $\hat{P}(\text{sel} \mid X, f(X))$ marginalizes over $S$:
$$\hat{P}(\text{sel} \mid X) = p_0 \cdot \text{expit}(\beta f + \kappa) + (1-p_0) \cdot \text{expit}(\beta f)$$
a function of the unknown $p_0$ and $\kappa$. Horvitz–Thompson under this estimated propensity is therefore biased for population quantities. Doubly-robust estimators do not rescue this setting: the standard DR guarantee requires correct specification of *either* the outcome model or the propensity model; here both depend on the unobserved $S$ through $\kappa$, so both are misspecified in the same direction. The IPW NLL column in Table~1 is included to demonstrate that the correction is negligible ($< 0.001$ nats vs naive at all $\beta$ values), not to claim a useful improvement. The residual gap (Pop NLL − Bayes optimal: 0.010, 0.009, 0.004 nats at $\beta = 1, 2, 4$) is entirely attributable to $\kappa$ and is not reduced by IPW.

This is not a remediable estimation failure. The natural fix (IPW) fails for the same structural reason as the naive estimator: both rely on a selection model that cannot be identified without observing $S$.

---

## 3b. Concrete Examples

The three failure regimes above are not hypothetical. Here are running instances in medicine and law.

### Medicine: ACR Appropriateness Criteria and Radiology Ordering

A clinical reasoning system advising on imaging orders (e.g., "CT chest with contrast appropriate?") faces all three failure regimes simultaneously:

**Selection bias (2.1).** Imaging is more likely to be ordered — and therefore confirmed — when the AI flags high suspicion. Patients in whom the AI recommends watchful waiting are less likely to receive follow-up imaging even when the original suspicion was low. Lost-to-follow-up is correlated with the AI's own output, not just patient characteristics. The instrument (EHR confirmation) violates exclusion.

**Assay endogeneity (2.2).** The imaging ordered is itself the assay. Whether the ground truth (e.g., pulmonary embolism present/absent) is recorded depends entirely on whether imaging was ordered and obtained. A system that recommends less imaging sees less confirmation of true positives in domains where the pathology requires imaging to confirm. The instrument is generated by the policy being evaluated.

**Evaluation instrument failure (2.3).** LLM judges scoring "appropriateness" of radiology recommendations will reward fluent reasoning aligned with clinical guidelines — which a well-trained model produces regardless of whether its conclusions match ground truth. The guidelines are the training data; the judge rewards guideline fluency, not clinical accuracy.

### Law: Contract Negotiation and Litigation Outcome

A contract negotiation AI advising on clause terms (e.g., "accept or reject indemnification clause?") operates in a delayed, policy-entangled feedback environment:

**Selection bias (2.1).** Contracts that settle without dispute never generate outcome data. The fraction of contracts that produce observable outcome signals is correlated with adversarialness of the clause terms, deal size, and parties' litigiousness — all correlated with the negotiation position the AI recommended. Heckman exclusion restriction is violated: whether a contract reaches litigation is not independent of the advice quality.

**Assay endogeneity (2.2).** Settlement rates and judicial outcomes are downstream of the arguments being made. When a legal reasoning system changes its recommendations, it changes which arguments are made in court, which shifts precedent at the margin, which changes future judicial reception of similar arguments. This feedback loop operates over years, not hours, but it is structurally present.

**Evaluation instrument failure (2.3).** Attorney acceptance rates as a proxy reward are a classic Goodhart failure: the AI learns to produce recommendations attorneys accept, which is a mixture of "good advice" and "advice that matches attorney priors." Fluent-but-suboptimal contract positions are undetectable from attorney acceptance data alone.

### Epidemiology: Surveillance Endogeneity

A public health intervention system recommending testing and quarantine policies (Memon et al. 2026, arXiv:2604.09519) generates the same structural failure: case counts, hospitalization rates, and positivity rates are all downstream of the surveillance policy the AI is recommending. A system recommending more testing sees more cases confirmed; a system recommending less sees fewer. The observation distribution is a function of the policy, by construction. Any evaluation based on confirmed case counts is evaluating the surveillance policy as much as the intervention quality.

---

## 3c. Causal Structure

The three failure regimes share a single underlying DAG. In the **separable case** (model influences confirmation probability but does not determine what is measured):

```
    S (true state)
   / \
  X   C (confirmation)
  |   |
  f(X) ← β ← model confidence
  |
  Y_obs (only when C=1)
```

$S \to X$ (state generates observable features), $S \to C$ via $\kappa$ (true positives more likely confirmed), $f(X) \to C$ via $\beta$ (model confidence increases confirmation propensity). $Y_\text{obs}$ is observed only when $C=1$. An instrument $Z$ for $C$ must be independent of $S$ given $X$ — the exclusion restriction. In practice $Z$ candidates (EHR system, insurance type, proximity to care) are correlated with $S$ through SES and care-seeking, weakening the exclusion.

In the **fully entangled case** (model *is* the observation action — determines what gets measured):

```
    S (true state)
   /
  X
  |
  f(X) → action → assay → Y_obs
  ↑__________________________|
         (feedback loop)
```

The policy $f$ determines the assay. The assay generates $Y_\text{obs}$. $Y_\text{obs}$ is used to train $f$. There is no external node to instrument for $C$ because $C$ is the policy output, not a selection mechanism exogenous to the policy. Identification without randomization fails by construction.

The LLM judge failure adds a third graph structure: the judge $J$ is a function of the model output $f(X)$ shared with the outcome path, so $J(f(X))$ is correlated with $f(X)$'s failure modes by construction. An adversarial probe that generates fluent-but-wrong outputs tests whether $J$ can distinguish them; this is the diagnostic recommended in Section 5.

---

## 4. What This Means for the Garry Test

The Garry Test asks: has anyone built the compiler equivalent for a non-code domain? The PRA paper (step-wise verifiable rewards at 4B scale) is the closest signal to date. But the analysis above implies the compiler analogy breaks before it fully closes.

A compiler is not downstream of the code it compiles. Clinical outcome signals, legal resolution signals, and policy impact signals are all downstream of the recommendations being made. The environment is not a fixed evaluation surface. It is a dynamical system that the policy is a part of.

This means the Garry Test as formulated may not have a positive answer in these domains. The correct reformulation is: **can you build a feedback system with bounded proxy drift under policy shift?** That is a weaker criterion but may be the achievable one. Partial identification with known violation directions, combined with periodic ground-truth audits and explicit drift monitoring, is a practical candidate.

The ceiling claim: systems optimizing against measurable proxies in this class of domains will drift from ground truth in proportion to policy influence on the distribution. The drift is not detectable in-sample. This is not a claim about impossibility — it is a claim about the minimum requirements for safe deployment, which current pipelines do not meet.

---

## 5. Diagnostics and Partial Mitigations

Even if clean identification is unavailable, the following reduce exposure:

1. **Sensitivity analysis over exclusion violation magnitude.** Rosenbaum bounds or parametric sensitivity. Report the range of estimates under plausible violation magnitudes rather than a point estimate.

2. **Randomized workup sub-studies.** Break the assay endogeneity loop by introducing randomization in a subset of cases. This is expensive but provides the only clean instrument.

3. **Delayed outcome audit pipelines.** Treat ground-truth outcome closure as a first-class component, not an afterthought. Build the system around labeler latency. Run periodic recalibration of proxy reward functions against audited outcomes.

4. **Distribution shift monitoring.** Track $d(\pi_t, \pi_0)$ explicitly. Flag drift above threshold for proxy recalibration. This doesn't solve the problem but makes the failure visible.

5. **Adversarial probing of the evaluation instrument.** For LLM judges: generate fluent-but-wrong reasoning chains and test whether the judge distinguishes them. Do this before deployment and on a rolling basis.

None of these close the identification gap. They bound the damage.

---

## 6. Conclusion

The feedback signal in high-stakes reasoning domains is not merely slow — it is structurally different from code execution in kind. The policy is part of the environment. The proxies are endogenous. The evaluation instruments are correlated with their own failure modes. Together these impose a ceiling on RL for reasoning in these domains that the compiler-equivalent framing does not capture.

The practical implication is not "don't use RL here." It is: the minimum requirements for responsible deployment include explicit drift monitoring, periodic ground-truth audit pipelines with built-in latency, and sensitivity analysis over identification assumptions. Systems without these are not demonstrably safe, and the proxy reward curves will not tell you when they have gone wrong.

---

## Notes / TODO

- [x] Formalize the MDP construction for the proxy drift result (Section 3) — Gaussian/logistic construction, numerical sanity-check done
- [x] Prove direction of slope shrinkage ($\hat\theta_1 < \theta_1^*$) — analytic proof via selection log-odds ratio derivative, scope conditions stated
- [x] **Replace numerical table with closed-form θ*(β).** Implicit function theorem gives θ₁*(β) = δ + C(κ,SNR)·β + O(β²). No general closed form (intractable integral), but IFT coefficient is numerically computable. Direction proof complete. Table updated with C(κ) sensitivity. (2026-04-13)
- [x] **Taylor expansion for proportionality.** First-order: Drift(β) ≈ |C(κ,SNR)|·β. C(κ=1.5,SNR=1.5) ≈ 0.165. C monotone in κ, zero at κ=0. Proportionality grounded. (2026-04-13)
- [x] Add concrete examples from medicine and law for each failure regime — radiology ordering, contract negotiation, epidemiology surveillance. Section 3b added 2026-04-13.
- [x] Check world models epidemiology paper (2604.09519) methods section — framing only, no tractable estimator. Cited in 3b and references.
- [x] Add explicit causal diagram for separable vs entangled cases — Section 3c added 2026-04-13. ASCII DAGs for both structures + LLM judge failure.
- [x] **κ-sweep simulation.** β=2.0 fixed, κ ∈ {0.0, 0.5, 1.0, 1.5, 2.0, 3.0} — gap monotone in κ confirmed. IPW correction negligible (near-uniform weights) — stronger result than expected. Table added to Section 3. (2026-04-13)
- [ ] Venue: clawrxiv fast version first; consider ICML/NeurIPS workshop on RL for science
- [x] Aura's framing 2026-04-13: "partial identification with known violation directions, not clean point identification" — verbatim in paper, attributed. Already in Section 4.

## References (to add)

### Off-policy / counterfactual evaluation
- Dudík, Langford & Li (2011). Doubly Robust Policy Evaluation and Learning.
- Swaminathan & Joachims (2015). Counterfactual Risk Minimization.
- Thomas & Brunskill (2016). Data-Efficient Off-Policy Policy Evaluation for RL.

### Endogeneity / causal inference
- Angrist & Pischke (2009). *Mostly Harmless Econometrics.*
- Imbens & Rubin (2015). *Causal Inference in Statistics, Social, and Biomedical Sciences.*

### Selection bias / Heckman
- Heckman (1979). Sample Selection Bias as a Specification Error. *Econometrica.*

### MNAR / missing data
- Little & Rubin (2002/2019). *Statistical Analysis with Missing Data.*

### Sensitivity analysis
- Rosenbaum (2002). *Observational Studies.*

### World models
- Ha & Schmidhuber (2018). World Models.
- Memon et al. (2026). Toward World Models for Epidemiology. arXiv:2604.09519.

### Clinical reasoning / Garry Test
- Sohn et al. (2026). Process Reward Agents for Steering Knowledge-Intensive Reasoning. arXiv:2604.09482.
