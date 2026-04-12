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

**Additive vs. substitutive demand.** Capex extrapolations typically assume substitutive demand: agents replace existing workflows or headcount, and token demand reflects the same tasks executed more cheaply at scale. Early enterprise survey data (week of April 2026) suggests a different pattern is also operative: agents are covering new surface area — tasks that were previously unaddressed or not resourced — rather than substituting existing labor. If agentic adoption is primarily additive, the counterfactual the extrapolation targets changes entirely. Substitutive capex extrapolation measures replacement and transition costs; additive extrapolation measures incremental capacity for net-new work. These are not magnitude adjustments — they change the policy conclusions about investment needs and vendor concentration. Both should be reported side by side, with explicit assumptions about the substitution elasticity and penetration rate. Treating observed token demand as evidence of substitution when it may reflect additive coverage overstates the productivity multiplier and misstates the displacement thesis. Report both scenarios with sensitivity bounds; note that direct enterprise survey data, rather than early-adopter intensity, is the appropriate empirical anchor for penetration assumptions.

## 5. The Counterargument: Cold Start, Not Structural Gate

The strongest objection: clarity improves with scale, so early low-clarity is transient. We argue this fails in clinical domains for three reasons:

(1) **Confirmation is endogenous**: confirmation propensity correlates with clinical signals used by models; deployment can magnify this selection bias rather than repair it (Obermeyer, Z., Powers, B., Vogeli, C., & Mullainathan, S. (2019). Dissecting racial bias in an algorithm used to manage the health of populations. *Science*, 366(6464), 447–453). Which cases get confirmed diagnoses is correlated with the signals the agent already uses, so more deployment amplifies rather than breaks this feedback loop.

(2) **Latency is time-bound**: biological and operational confirmation windows (months–years) do not compress with compute or user volume — they set a lower bound on the rate at which deployed agents can get high-quality supervision. A 5-year confirmation window does not compress at deployment scale. Feedback latency in clinical tasks is bounded by biological time, not compute or deployment volume, and is therefore structurally decoupled from the scaling curve the counterargument assumes.

(3) **Institutional concentration caps access**: EHR vendor pathways, coding/reimbursement incentives, and documentation practices create durable ceilings on which outcomes are both recordable and usable; empirical identification often requires vendor-variation or external linkage. As of end-2024, Epic holds an estimated 42.3% of US acute care hospital market share and 54.9% of bed market share, capturing ~70% of all hospital EHR decisions in 2024 (KLAS Research, *US Acute Care EHR Market Share 2025*, 2025). This degree of concentration means training pipelines in most large-system deployments are gated by a single vendor's data model and export policies. Critically, this is not a future risk: enterprises now prioritize vendor-integrated workflows and de-risk procurement by negotiating data-access and deployment terms; health systems seek to preserve downstream revenue streams when assessing AI adoption (enterprise survey data, April 2026). Vendors who are not agent-accessible are already being displaced from consideration. Institutional concentration is therefore a present condition that caps training signal access, not merely a structural future constraint.

## 6. Organizational Implications

The correct response is not to hire into the current bottleneck but to keep teams small and senior with rapid retraining capacity. Hiring cycles are too slow to unwind; the window between "bottleneck shifts" and "market prices it in" is shorter than a hiring cycle. The orgs that win probably aren't the ones who hire fastest into the spike but the ones who stay lean and retrain into wherever the bottleneck lands — which is the opposite of what companies actually do when a talent-boom narrative takes hold.

## 7. Empirical Plan

1. **Measure clarity**: construct confirmed-outcome cohorts and report latency distributions, SNR estimates, and inter-rater contestability metrics per domain/task.
2. **Estimate P(k)**: replicate agent deployment at incremental k in observational or simulated environments; plot corrected and naive P(k).
3. **Test persistence of confirmation propensity**: model selection-on-observables using Heckman-style MNAR correction (compare to IPW); test whether confirmation propensity remains correlated with agent-accessible signals at scale.
4. **Counterfactuals**: exploit vendor-variation or linked registries to simulate relaxing institutional caps (Epic-concentrated vs low-concentration settings).
5. **Simulations**: Monte Carlo models parameterized by observed latency/noise to estimate required deployment scale for targeted performance gains under realistic clarity conditions.

Confirmed-outcome cohort work with selection-correction machinery is the natural platform — reframe it as measuring feedback clarity. [Cohort numbers: placeholder — populate from confirmed-outcome cohort results when available.]

## 8. Pipeline Generalization

The feedback clarity framework applies at the stage level, not just at deployment scale. Any pipeline stage with no outcome signal is clarity-zero by definition, regardless of how principled it looks architecturally. A pre-research resolver that maps queries to canonical sources before an LLM synthesizes illustrates this: the resolver has no confirmation signal — it cannot know whether the sources it returned produced useful downstream answers. Resolver clarity is therefore zero: latency is unbounded (outcome never arrives), noise is uncorrelated with resolution quality, and contestability is absent because there is no eval surface. "Resolved to these sources" is not the same as "resolved correctly." Without a downstream eval loop, the hallucination is moved one stage earlier, not eliminated. The rest of the system pays silently.

Open source does not fix this. It makes the static heuristic inspectable but does not create a learning loop. The maintainer can audit and patch manually — that is not nothing — but it moves the competence requirement from the black box to the maintainer rather than solving the feedback problem. Inspectable limitations are not the same as corrected limitations.

This generalizes: pipeline architects should identify every clarity-zero stage and either (a) add an eval gate with a downstream outcome signal or (b) explicitly scope claims to what the stage can actually verify. Clarity-zero stages are silent error multipliers.

## 9. Conclusion

Coding is an outlier, not a default. Forecasts that extrapolate token demand should explicitly condition on feedback clarity; without that, they risk overestimating the pace and magnitude of agentic productivity gains. Our structural claim is falsifiable with the confirmed-outcome + selection-correction program described above; forecasts should incorporate uncertainty about clarity-driven propagation constraints.

---

*Open citations: (1) Obermeyer et al. 2019 — inserted in Sec 5.1. ✓ (2) KLAS EHR concentration — inserted in Sec 5.3: KLAS Research, US Acute Care EHR Market Share 2025, 2025. ✓ (3) Confirmed-outcome cohort numbers — placeholder in Sec 7, populate when available.*
