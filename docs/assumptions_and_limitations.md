# Assumptions and Limitations

**Project:** Birhan Energies — Brent Oil Price Change Point Analysis  
**Date:** July 2026

---

## 1. Assumptions

### Data Assumptions

| # | Assumption | Rationale |
|---|------------|-----------|
| A1 | **Brent spot price is a representative global oil benchmark** | Brent prices approximately two-thirds of internationally traded crude; suitable proxy for global oil market dynamics. |
| A2 | **Daily closing/spot prices accurately reflect market conditions** | EIA/FRED data is authoritative; intraday volatility is not captured. |
| A3 | **Missing values are missing at random** | Few missing observations in the dataset; forward-fill or interpolation is acceptable for gaps. |
| A4 | **The date range (May 1987 – Sep 2022) is sufficient** | Covers major modern oil market regimes including Gulf War, shale revolution, COVID, and Ukraine war. |
| A5 | **Event dates approximate the onset of market impact** | Events may affect prices days or weeks before/after the recorded date due to anticipation or delayed response. |

### Modeling Assumptions

| # | Assumption | Rationale |
|---|------------|-----------|
| M1 | **A single change point model captures one structural break at a time** | Simplifies interpretation; multiple breaks require iterative or multi-change-point models. |
| M2 | **Normal likelihood is adequate for log returns** | Computationally tractable; Student-t distribution may better handle fat tails (noted as limitation). |
| M3 | **Change points represent abrupt shifts, not gradual transitions** | Bayesian switch-point models assume instantaneous parameter changes; gradual shifts may be misidentified. |
| M4 | **Prior distributions are weakly informative** | Discrete uniform prior on τ; wide Normal priors on means allow data to dominate inference. |
| M5 | **MCMC convergence indicates reliable posterior estimates** | R-hat < 1.01 and sufficient effective sample size (ESS) required before interpreting results. |

### Analytical Assumptions

| # | Assumption | Rationale |
|---|------------|-----------|
| AN1 | **Temporal coincidence between a change point and an event suggests a plausible association** | Forms the basis for hypothesis generation, not causal proof. |
| AN2 | **Log returns are a more stationary target than raw prices** | Standard practice in financial time series analysis. |
| AN3 | **Major geopolitical and OPEC events are the primary drivers of structural breaks** | Other factors (technology, renewables, currency) are acknowledged but not modeled in the baseline analysis. |

---

## 2. Limitations

### Data Limitations

- **Single price series:** No multivariate data (volume, inventories, GDP, exchange rates) to control for confounders.
- **No intraday data:** Daily granularity misses within-day shocks and opening-gap effects.
- **Survivorship of benchmark:** Brent became the dominant benchmark over this period; earlier periods may reflect different market structures.
- **Event dataset subjectivity:** Event selection, dating, and categorization involve researcher judgment; alternative event lists could yield different associations.

### Methodological Limitations

- **Correlation vs. causation (critical):** Detecting a change point near an event date establishes **temporal correlation**, not **causal impact**. Multiple events may occur simultaneously (e.g., COVID pandemic and OPEC cuts in early 2020), making attribution ambiguous.
- **Single change point:** Real oil markets experience multiple overlapping regime changes; a one-break model oversimplifies.
- **Mean-only detection:** Changes in volatility (e.g., during crises) may not appear as mean shifts in log returns.
- **Linear/Gaussian framework:** Oil returns exhibit fat tails, asymmetry, and volatility clustering poorly captured by Normal likelihoods.
- **Uniform prior on τ:** Treats all dates as equally likely a priori; informative priors near known events would change results.

### Interpretation Limitations

- **Confounding:** Global macroeconomic conditions, USD strength, and interest rates simultaneously affect oil prices.
- **Endogeneity:** OPEC decisions respond to prices as well as causing price changes.
- **Hindsight bias:** Selecting events after observing price charts risks confirmation bias.
- **Generalizability:** Findings describe historical associations; predictive power for future events is limited.

---

## 3. Correlation vs. Causation

This is the most important limitation for stakeholders, particularly government bodies and policymakers.

### What This Analysis CAN Do

- Identify **when** statistical properties of oil prices changed (posterior over τ).
- Quantify **how much** parameters shifted (posterior over μ₁, μ₂).
- Highlight **temporal proximity** between detected breaks and documented events.
- Generate **testable hypotheses** (e.g., "The March 2020 change point is plausibly associated with COVID-19 demand destruction").

### What This Analysis CANNOT Do

- **Prove** that a specific event **caused** a price change.
- Rule out alternative explanations for a detected break.
- Isolate the individual effect of one event when multiple shocks overlap.
- Establish a causal directed acyclic graph (DAG) without additional data and methods.

### Recommended Language for Reporting

| Avoid | Prefer |
|-------|--------|
| "The Iraq War caused prices to rise 40%." | "A change point detected in March 2003 is temporally consistent with the onset of the Iraq War; the model estimates a mean log-return shift of X, with Y% posterior probability of an increase." |
| "OPEC cuts drove the recovery." | "The change point posterior mode aligns with the April 2020 OPEC+ agreement within a 30-day window, suggesting a plausible association that warrants further investigation." |
| "Sanctions on Iran increased prices." | "Following the May 2018 JCPOA withdrawal, prices exhibited a structural shift consistent with supply tightening, though concurrent factors (Venezuela collapse, strong demand) confound isolated attribution." |

### Strengthening Causal Claims (Future Work)

To move toward causal inference, future work should:

1. **Incorporate covariates** (GDP growth, USD index, inventory levels) in a multivariate model.
2. **Use difference-in-differences** or synthetic control methods for specific events.
3. **Apply Granger causality** or VAR models to test predictive relationships.
4. **Use instrumental variables** (e.g., exogenous supply disruptions unrelated to demand).
5. **Conduct placebo tests** — run change point models on periods without known events to calibrate false-positive rates.

---

## 4. Scope Boundaries

- This analysis covers **Brent crude spot prices only**; WTI, natural gas, and refined products are excluded.
- The **dashboard (Task 3)** presents associations for exploration; it does not imply causal links.
- **Forecasts** derived from change point models describe regime-specific behavior, not point predictions.

---

## 5. Risk Disclosure for Stakeholders

> **For investors:** Past structural breaks do not guarantee future regime behavior. Model outputs are probabilistic, not deterministic trading signals.

> **For policymakers:** Event–price associations should inform scenario planning, not sole justification for policy decisions. Complementary economic modeling is recommended.

> **For energy companies:** Operational decisions should incorporate multiple data sources beyond this single-series analysis.
