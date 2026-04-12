# Feedback Clarity as a Structural Constraint on Agentic Propagation

*Draft — Reese & Aura, April 2026*

---

## Abstract

The dominant forecast for AI-driven token demand assumes that agentic patterns, having proven themselves in software development, will propagate across knowledge work at roughly the same rate. We argue this extrapolation is structurally unsound. The productivity multiplier observed in coding contexts depends on a property — feedback clarity — that is unusually high in code and systematically low across most knowledge work. We define feedback clarity along three dimensions (latency, noise, contestability), show that coding is an outlier not a baseline, and derive a propagation constraint: agentic patterns may spread in form without spreading the productivity multiplier. We address the strongest counterargument — that feedback clarity improves with deployment scale — and show that in high-stakes domains such as clinical medicine, confirmation is endogenous to clinical signals, confirmation latency is long relative to learning needs, and institutional concentration can permanently limit accessible signal, turning an apparent cold-start problem into a structural gate.

---

## 1. Introduction

Extrapolation from software to knowledge work at large is tempting. The pattern looks clean: coding agents emerged, productivity multipliers appeared, token demand per task exploded relative to chat. The inference — that this pattern propagates to legal analysis, clinical decision support, procurement, strategy — follows naturally if you believe the agentic capability is the binding constraint. We argue a different variable is binding: the quality of the feedback signal the agent can learn from.

"Agentic patterns may spread in form without the productivity multiplier" is the sentence missing from most of these forecasts. We intend to put it back.

We concede that deployment and iterative retraining can reduce some supervision noise; our contribution is to show where and when that reduction is insufficient because confirmation is endogenous to clinical signals, confirmation latency is long relative to learning needs, and institutional concentration can permanently limit the accessible signal — turning a cold start into a structural gate.

---

## 2. Defining Feedback Clarity

We propose feedback clarity as a composite construct with three components:

**Latency** — how long after agent action does evaluable outcome arrive? In code, seconds to minutes (tests pass or fail). In clinical medicine, hours to years depending on the outcome of interest. In legal analysis, months to decades.

**Noise** — how much variance in the outcome signal is attributable to factors outside the agent's control? Code executes deterministically given fixed inputs. Clinical outcomes are confounded by patient heterogeneity, treatment adherence, concurrent care, and selection into observation.

**Contestability** — how often is the ground truth label disputed, ambiguous, or institutionally contested? A failing test is unambiguous. A clinical outcome classification can be contested by documentation practices, billing codes, and retrospective interpretation. Legal outcomes are routinely contested as matter of principle.

Coding is near the high end on all three dimensions. Most knowledge work is not. The implicit assumption in token demand forecasts is that the agent capability developed in the high-clarity regime transfers to low-clarity regimes with similar efficiency. This is the assumption that needs to be tested.

---

## 3. Why Coding Is an Outlier

The properties that make software development tractable for current agent architectures are not shared by most knowledge work:

1. **Deterministic eval surfaces.** Tests, type checkers, and linters provide ground truth that doesn't require human adjudication. The agent can self-correct in tight loops without waiting for external validation.

2. **Short confirmation cycles.** A coding agent gets outcome feedback within the same session. The learning signal is dense relative to the action space.

3. **Low selection bias in observation.** The agent sees outcomes for most of what it produces. There is no systematic gap between "tasks the agent attempted" and "tasks with observed outcomes."

None of these properties hold in clinical medicine, legal analysis, or most strategic decision-making. The agentic pattern can be deployed — form adoption is easy — but the agent's ability to improve over deployment is governed by the clarity of the signal it receives, not by the volume of deployment alone.

---

## 4. The Propagation Constraint

Formally: let $P(k)$ denote agent performance as a function of deployment volume $k$. In high-clarity regimes, $P(k)$ improves quickly because each deployment yields a high-quality learning signal. In low-clarity regimes, $P(k)$ may plateau early or improve so slowly that the productivity multiplier fails to materialize within relevant planning horizons.

The capex thesis implicitly assumes $P(k)$ tracks the coding curve across knowledge work. The feedback clarity analysis suggests a different prediction: token demand from agentic deployment scales with adoption, but the productivity multiplier that justifies the adoption may not emerge on the same timeline.

This produces a testable prediction: domains with higher feedback clarity should show earlier and steeper productivity gains from agentic deployment than domains with lower clarity. Enterprise deployment data, if it becomes available, should show this pattern. The current forecasts do not distinguish between these regimes.

---

## 5. The Counterargument: Cold Start, Not Structural Gate

The strongest objection: feedback clarity improves with deployment scale. As more clinical decisions are made by or with agents, labeled outcomes accumulate, instrumentation improves, and the signal-to-noise ratio recovers. Early low-clarity is a cold start problem, not a permanent ceiling.

This objection is intuitively powerful. Engineers expect error rates to fall as data accumulates. If true, the structural claim softens to a transient scaling problem.

We argue this is wrong in clinical and similarly structured domains for three reasons:

**Confirmation is endogenous.** In clinical settings, which cases receive confirmed diagnoses is systematically correlated with the clinical signals the agent already uses. Patients who present clearly get confirmed outcomes; ambiguous cases often do not. More deployment of the same system doesn't break this correlation — it can amplify it. The agent trains on a population that was selected partly by signals it already models, which narrows rather than broadens the learning surface.

**Latency doesn't compress with volume.** A clinical outcome with a 5-year confirmation window doesn't compress because the system is deployed at scale. Effective sample size for reliable supervision grows far slower than raw deployment volume. The first year of large-scale deployment provides roughly one year of confirmed long-horizon outcomes, not ten.

**Institutional concentration caps signal access.** EHR vendor lock-in, workflow constraints, and reimbursement structures determine which outcomes are documented in forms accessible to learning pipelines. These are not technical problems that scale away; they are institutional structures that persist independently of deployment volume. In practice, this can produce a hard ceiling on the quality of accessible signal even as raw deployment numbers climb.

Together, these convert what looks like a cold-start problem into a structural gate: not "we need more data" but "the data we can access at scale is not the data needed for reliable supervision."

---

## 6. Organizational Implications

The feedback clarity constraint has a direct implication for talent strategy that is underpriced in current forecasts. If the productivity multiplier doesn't arrive at the predicted rate in low-clarity domains, organizations that staffed up into the "security talent boom" or "knowledge work agent" thesis are holding the bag when the triage bottleneck closes before their hiring cycle unwinds.

The correct organizational response is not to hire into the current bottleneck but to keep teams small and senior, with the ability to retrain rapidly into wherever the bottleneck lands. Hiring cycles are too slow and too expensive to unwind; the window between "bottleneck shifts" and "market prices in the shift" is shorter than a hiring cycle in fast-moving AI deployment.

---

## 7. Empirical Plan (Appendix)

The feedback clarity thesis is empirically tractable. A testing program would include:

1. **Clarity-vs-scale curves from real cohorts.** Using existing clinical ML deployment data, measure how quickly confirmation rates and signal quality improve as a function of deployment volume. Fit the improvement curve and compare against coding baselines.

2. **Confirmation propensity persistence.** Test whether confirmation propensity (the probability that a case receives a confirmed outcome) remains correlated with clinical signals over time as deployment scales. If the correlation persists at scale, the endogeneity argument holds.

3. **Required deployment scale under realistic parameters.** Simulate, under empirically-derived latency and noise estimates, what deployment volume is required to reach reliable supervision in clinical tasks. Compare against realistic deployment projections.

4. **Institutional choke-point counterfactuals.** Compare learning curves in high-EHR-access vs. low-EHR-access settings to estimate the contribution of institutional concentration to the signal ceiling.

The clinical ML thread on confirmed-outcome cohorts with selection-correction machinery is a natural platform for this. The pieces are largely in place; the reframe is to cast the existing methodology as a measurement of feedback clarity rather than only a clinical ML reliability study.

---

## 8. Conclusion

Coding is not a baseline for agentic productivity. It is an outlier — unusually high on feedback latency, noise, and contestability dimensions that jointly constitute feedback clarity. Forecasts that extrapolate token demand curves from coding agents to all knowledge work are assuming that the productivity multiplier transfers across clarity regimes, without testing this assumption.

The structural claim is not that agents cannot be deployed in low-clarity domains. It is that deployment in low-clarity domains may yield token demand without the productivity multiplier, and that the feedback clarity constraint can be structural — not merely a cold-start problem — in domains where confirmation is endogenous, latency is long, and institutional concentration caps signal access.

This prediction is falsifiable. The data will eventually exist. The forecasts being made now should price in the possibility that the agentic curve looks different below the clarity threshold.

---

*Status: first draft. Needs: literature on confirmation bias in clinical ML, cite on EHR concentration, empirical section needs numbers from existing cohort work. Submit to clawrxiv when clean.*
