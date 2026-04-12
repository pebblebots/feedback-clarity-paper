# Feedback Clarity as a Structural Constraint on Agentic Propagation
*Draft — Reese & Aura, April 2026*

## Abstract

The dominant forecasts for AI-driven token demand extrapolate agentic gains from software to the rest of knowledge work. We show this extrapolation is structurally fragile: the coding productivity multiplier depends on *feedback clarity* — a compound property (latency, noise, contestability) that is unusually high for code and systematically lower across most knowledge work. Coding is therefore an outlier, not a baseline. We formalize feedback clarity, present a propagation constraint (agentic form can spread without the productivity multiplier), and address the strongest objection — that scale resolves low clarity — by showing three structural failure modes in clinical domains: confirmation is endogenous to clinical signals, biological/operational latency does not compress with deployment, and institutional concentration (e.g., EHR vendor pathways) can cap accessible confirmation signal. We sketch an empirical plan (confirmed-outcome cohorts, Heckman-style selection correction for MNAR, vendor-variation counterfactuals) that makes the structural claim falsifiable.

## 1. Introduction

Extrapolation from software to knowledge work at large is tempting. Coding agents emerged, productivity multipliers appeared, token demand per task exploded relative to chat. The inference — that this propagates to legal analysis, clinical decision support, procurement, strategy — follows naturally if you believe the agentic capability is the binding constraint. We argue a different variable is binding: the quality of the feedback signal the agent can learn from.

*Agentic patterns may spread in form without the productivity multiplier* is the sentence missing from most of these forecasts. We intend to put it back.

We acknowledge deployment and iterative retraining can reduce supervision noise. Our contribution is to identify when such reductions are insufficient: confirmation can be endogenous to signals the agent already uses, confirmation latency may be long relative to learning requirements, and institutional concentration can permanently limit accessible confirmation — converting a cold start into a structural gate.

## 2. Defining Feedback Clarity

Define feedback clarity by three measurable components: (1) **Latency** — distribution of confirmation delays (e.g., median/percentiles): seconds for unit tests, days–years for many clinical outcomes. (2) **Noise** — signal-to-noise ratio of outcome conditional on agent action (variance attributable to unobserved confounders, adherence, concurrent interventions). (3) **Contestability** — probability that independently credible evaluators disagree about outcome label (inter-rater disagreement, billing/documentation ambiguity). These components admit empirical measurement and should be reported per domain/task.

## 3. Why Coding Is an Outlier

Deterministic eval surfaces (tests, linters); short confirmation cycles (same session); low selection bias in observation (agent sees outcomes for most of what it produces). None of these hold in clinical medicine, legal analysis, or strategic decision-making. The coding context combines near-zero latency, near-zero contestability for most tasks, and a noise floor set only by test coverage — a conjunction that is unusual across knowledge work, not representative of it.

## 4. The Propagation Constraint

Let P(k) be measurable performance (accuracy, utility) vs deployment volume k. In high-clarity regimes dP/dk is large at low k; in low-clarity regimes P(k) may plateau or improve only slowly. Operational prediction: plot P(k) for comparable tasks across domains using the same evaluation metric; higher measured clarity (as above) should correlate with earlier/steeper gains. Report confidence intervals and corrected estimates using selection models (see Section 7).

Token demand scales with adoption; the productivity multiplier that justifies adoption may not emerge on the same timeline. Forecasts that treat current coding-agent token intensity as a template for all knowledge work are implicitly assuming P(k) behaves identically across clarity regimes. That assumption is not tested.

## 5. The Counterargument: Cold Start, Not Structural Gate

The strongest objection: clarity improves with scale, so early low-clarity is transient. We argue this fails in clinical domains for three reasons:

(1) **Confirmation is endogenous**: confirmation propensity correlates with clinical signals used by models; deployment can magnify this selection bias rather than repair it (Obermeyer, Z., Powers, B., Vogeli, C., & Mullainathan, S. (2019). Dissecting racial bias in an algorithm used to manage the health of populations. *Science*, 366(6464), 447–453). Which cases get confirmed diagnoses is correlated with the signals the agent already uses, so more deployment amplifies rather than breaks this feedback loop.

(2) **Latency is time-bound**: biological and operational confirmation windows (months–years) do not compress with compute or user volume — they set a lower bound on the rate at which deployed agents can get high-quality supervision. A 5-year confirmation window does not compress at deployment scale. Feedback latency in clinical tasks is bounded by biological time, not compute or deployment volume, and is therefore structurally decoupled from the scaling curve the counterargument assumes.

(3) **Institutional concentration caps access**: EHR vendor pathways, coding/reimbursement incentives, and documentation practices create durable ceilings on which outcomes are both recordable and usable; empirical identification often requires vendor-variation or external linkage. [EHR vendor concentration citation needed — ONC Health IT Dashboard / KLAS 2023–2024 EHR market share report]. These constraints persist independently of deployment volume and can produce a hard ceiling on accessible signal quality.

## 6. Organizational Implications

The correct response is not to hire into the current bottleneck but to keep teams small and senior with rapid retraining capacity. Hiring cycles are too slow to unwind; the window between "bottleneck shifts" and "market prices it in" is shorter than a hiring cycle. The orgs that win probably aren't the ones who hire fastest into the spike but the ones who stay lean and retrain into wherever the bottleneck lands — which is the opposite of what companies actually do when a talent-boom narrative takes hold.

## 7. Empirical Plan

1. **Measure clarity**: construct confirmed-outcome cohorts and report latency distributions, SNR estimates, and inter-rater contestability metrics per domain/task.
2. **Estimate P(k)**: replicate agent deployment at incremental k in observational or simulated environments; plot corrected and naive P(k).
3. **Test persistence of confirmation propensity**: model selection-on-observables using Heckman-style MNAR correction (compare to IPW); test whether confirmation propensity remains correlated with agent-accessible signals at scale.
4. **Counterfactuals**: exploit vendor-variation or linked registries to simulate relaxing institutional caps (Epic-concentrated vs low-concentration settings).
5. **Simulations**: Monte Carlo models parameterized by observed latency/noise to estimate required deployment scale for targeted performance gains under realistic clarity conditions.

Confirmed-outcome cohort work with selection-correction machinery is the natural platform — reframe it as measuring feedback clarity. [Cohort numbers: placeholder — populate from confirmed-outcome cohort results when available.]

## 8. Conclusion

Coding is an outlier, not a default. Forecasts that extrapolate token demand should explicitly condition on feedback clarity; without that, they risk overestimating the pace and magnitude of agentic productivity gains. Our structural claim is falsifiable with the confirmed-outcome + selection-correction program described above; forecasts should incorporate uncertainty about clarity-driven propagation constraints.

---

*Open citations: (1) Obermeyer et al. 2019 — inserted in Sec 5.1. (2) EHR vendor concentration — ONC/KLAS placeholder in Sec 5.3, needs specific report citation. (3) Confirmed-outcome cohort numbers — placeholder in Sec 7, populate when available.*
