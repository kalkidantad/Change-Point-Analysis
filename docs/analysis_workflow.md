# Analysis Workflow: Brent Oil Price Change Point Analysis

**Project:** Birhan Energies — Change Point Analysis of Brent Oil Prices  
**Author:** Birhan Energies Data Science Team  
**Date:** July 2026

---

## 1. Executive Summary

This document outlines the planned analytical workflow for detecting and interpreting structural breaks in Brent crude oil prices (May 1987 – September 2022). The analysis combines Bayesian change point detection (PyMC), exploratory time series analysis, and a curated event dataset to generate hypotheses about how geopolitical, economic, and OPEC-related events may have shifted price dynamics. The workflow is designed for interim delivery of foundational work (Task 1) and subsequent modeling (Task 2) and dashboard development (Task 3).

---

## 2. Analysis Workflow

### Phase 1: Data Acquisition and Preparation

| Step | Action | Output |
|------|--------|--------|
| 1.1 | Load `BrentOilPrices.csv` (8,978 daily observations) | Raw DataFrame |
| 1.2 | Parse `Date` column (`%d-%b-%y`) to datetime | Typed time index |
| 1.3 | Handle missing values and validate price range | Clean series |
| 1.4 | Compute log returns: `log(P_t) - log(P_{t-1})` | Stationary derivative |
| 1.5 | Resample to monthly aggregates for trend visualization | Aggregated views |

### Phase 2: Exploratory Data Analysis (EDA)

| Step | Action | Purpose |
|------|--------|---------|
| 2.1 | Plot raw price series (1987–2022) | Identify major trends and shocks |
| 2.2 | Plot log returns | Observe volatility clustering |
| 2.3 | Compute rolling mean and rolling volatility (30/90-day windows) | Detect regime shifts visually |
| 2.4 | Augmented Dickey-Fuller (ADF) test on prices and log returns | Test stationarity |
| 2.5 | Summary statistics by decade | Contextualize regime changes |
| 2.6 | Overlay researched events on price chart | Visual correlation screening |

**Key EDA questions:**
- Is the price series non-stationary? (Expected: yes — strong upward trend 2002–2008, mean-reverting post-2014)
- Do log returns exhibit volatility clustering? (Expected: yes — GARCH-like behavior)
- Which visual breakpoints align with known events?

### Phase 3: Event Data Integration

| Step | Action | Output |
|------|--------|--------|
| 3.1 | Load `oil_market_events.csv` (15 curated events) | Event reference table |
| 3.2 | Define event window (±30 days around event date) | Analysis windows |
| 3.3 | Compute pre/post event price statistics (mean, % change) | Event impact summaries |
| 3.4 | Map events to detected change points (Task 2) | Event–breakpoint associations |

### Phase 4: Bayesian Change Point Modeling (PyMC)

**Model specification (single change point, mean shift):**

```
τ ~ DiscreteUniform(0, N-1)          # Switch point index
μ₁ ~ Normal(0, σ_μ)                    # Mean before τ
μ₂ ~ Normal(0, σ_μ)                    # Mean after τ
σ ~ HalfNormal(σ_σ)                    # Observation noise

μ_t = switch(t < τ, μ₁, μ₂)
P_t ~ Normal(μ_t, σ)
```

| Step | Action | Output |
|------|--------|--------|
| 4.1 | Build PyMC model on log returns (or prices) | Model object |
| 4.2 | Run MCMC: `pm.sample(2000, tune=1000, cores=2)` | Posterior samples |
| 4.3 | Check convergence: R-hat ≈ 1.0, trace plots | Diagnostics |
| 4.4 | Plot posterior of τ | Change point date distribution |
| 4.5 | Plot posteriors of μ₁, μ₂ | Before/after parameter estimates |
| 4.6 | Quantify impact: P(μ₂ > μ₁), % change | Probabilistic statements |

**Extensions (Task 2 advanced / future work):**
- Multiple change points (iterative or hierarchical model)
- Markov-switching volatility regimes
- VAR with macroeconomic covariates (GDP, USD index)

### Phase 5: Interpretation and Reporting

| Step | Action | Audience |
|------|--------|----------|
| 5.1 | Compare τ posterior mode/median with event dates | Internal analysts |
| 5.2 | Write quantified impact statements | Investors, policymakers |
| 5.3 | Document limitations (correlation ≠ causation) | Government stakeholders |
| 5.4 | Produce blog-style final report with visualizations | Public / Medium |
| 5.5 | Build interactive dashboard (Task 3) | All stakeholders |

---

## 3. Change Point Models: Purpose and Expected Outputs

### Purpose

Change point models identify **structural breaks** — moments when the statistical properties of a time series (mean, variance, trend) shift abruptly. For Brent oil prices, these breaks may correspond to:

- Supply shocks (wars, sanctions, OPEC decisions)
- Demand shocks (financial crises, pandemics)
- Market regime changes (shale revolution, energy transition)

Unlike simple before/after comparisons, Bayesian change point detection provides:
- A **posterior distribution** over the change date (quantifying uncertainty)
- **Probabilistic estimates** of parameter shifts
- Natural handling of noise and overlapping effects

### Expected Outputs

| Output | Description | Example |
|--------|-------------|---------|
| τ (switch point) | Posterior over most likely change date | "90% CI: March 2020 – May 2020" |
| μ₁, μ₂ | Mean parameters before/after | "μ₁ = $62, μ₂ = $45" |
| Impact magnitude | Difference and % change | "14% decrease (94% probability)" |
| Convergence metrics | R-hat, ESS | "All R-hat < 1.01" |

### Model Limitations

- **Single change point** models detect only one break; multiple events may require multiple models or hierarchical approaches.
- **Mean-only shifts** ignore volatility changes; a crisis may increase variance without shifting the mean.
- **Temporal proximity ≠ causation** — a detected break near an event is evidence for a hypothesis, not proof of causality.
- **Confounding events** — overlapping shocks (e.g., COVID + OPEC cuts in 2020) cannot be disentangled without multivariate models.

---

## 4. Time Series Properties and Modeling Implications

Based on initial EDA (see `notebooks/01_eda.ipynb`):

| Property | Finding | Modeling Implication |
|----------|---------|---------------------|
| **Trend** | Strong non-stationary trend; prices rose from ~$18 (1987) to peaks above $140 (2008, 2022) | Model log returns or detrended series; change points on returns capture level shifts |
| **Stationarity** | ADF test rejects stationarity for prices; log returns closer to stationary | Apply change point model to log returns |
| **Volatility** | Clear clustering: high vol during 2008, 2014–2016, 2020, 2022 | Consider extending to variance change point models |
| **Seasonality** | Weak annual seasonality in prices | Not a primary modeling concern |
| **Distribution** | Returns show fat tails (leptokurtosis) | Normal likelihood is a simplifying assumption; Student-t likelihood as extension |

---

## 5. Communication Plan

| Stakeholder | Format | Key Messages |
|-------------|--------|--------------|
| **Investors** | Dashboard + executive summary | Risk regimes, event-driven volatility, probabilistic forecasts |
| **Policymakers** | Formal report (PDF/blog) | Energy security implications, sanction impacts, supply diversification |
| **Energy companies** | Interactive dashboard | Operational planning windows, cost sensitivity around events |
| **Government bodies** | Structured report with limitations section | Evidence-based hypotheses, explicit causation caveats |

---

## 6. Timeline

| Milestone | Date | Deliverables |
|-----------|------|--------------|
| Interim submission | 12 Jul 2026 | Task 1: workflow doc, events CSV, EDA notebook |
| Task 2 completion | 13 Jul 2026 | PyMC change point notebook, interpretations |
| Task 3 completion | 14 Jul 2026 | Flask API + React dashboard |
| Final submission | 14 Jul 2026 | Full report, code, dashboard screenshots |

---

## References

- PyMC Change Point Detection: https://www.pymc.io/projects/examples/en/latest/gaussian_processes/GP-ChangePoint.html
- Forecastegy Change Point Guide: https://forecastegy.com/posts/change-point-detection-time-series-python/
- Data Science Workflow: https://www.datascience-pm.com/data-science-workflow/
