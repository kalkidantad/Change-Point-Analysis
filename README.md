# Change Point Analysis — Brent Oil Prices

**10 Academy AI Mastery | Week 10 Challenge**  
**Client:** Birhan Energies  
**Objective:** Detect structural breaks in Brent crude oil prices and associate them with geopolitical, economic, and OPEC events using Bayesian change point analysis.

---

## Project Overview

This project analyzes how major political and economic events affect Brent oil prices (May 1987 – September 2022) using:

- **Exploratory time series analysis** (trend, stationarity, volatility)
- **Bayesian change point detection** (PyMC MCMC)
- **Event correlation** with a curated dataset of 15 key market events
- **Interactive dashboard** (Flask + React) for stakeholder exploration

---

## Repository Structure

```
├── data/
│   ├── BrentOilPrices.csv          # Daily Brent prices (8,978 obs)
│   └── oil_market_events.csv       # 15 curated market events
├── docs/
│   ├── analysis_workflow.md        # Task 1: Planned analysis steps
│   └── assumptions_and_limitations.md
├── notebooks/
│   ├── 01_eda.ipynb                # Task 1: Initial EDA
│   └── 02_change_point_model.ipynb # Task 2: PyMC modeling (TODO)
├── scripts/
│   └── download_data.py            # Data download utility
├── src/
│   ├── data_loader.py              # Data loading utilities
│   └── analysis.py                 # Time series analysis helpers
├── tests/
│   └── test_data_loader.py
└── requirements.txt
```

---

## Quick Start

```bash
git clone <your-repo-url>
cd Change-Point-Analysis
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v
jupyter notebook notebooks/01_eda.ipynb
```

---

## Task 1 Deliverables (Interim — 12 Jul 2026)

| Deliverable | Location |
|-------------|----------|
| Analysis workflow (1–2 pages) | [`docs/analysis_workflow.md`](docs/analysis_workflow.md) |
| Events dataset (15 events) | [`data/oil_market_events.csv`](data/oil_market_events.csv) |
| Assumptions & limitations | [`docs/assumptions_and_limitations.md`](docs/assumptions_and_limitations.md) |
| Initial EDA findings | [`notebooks/01_eda.ipynb`](notebooks/01_eda.ipynb) |

### Key EDA Findings

- **8,978 daily observations** from May 1987 to September 2022
- **Price range:** $9.10 – $143.95 (mean: $48.26)
- **Prices are non-stationary** (ADF p=0.26); **log returns are stationary** (ADF p≈0)
- **Annualized volatility:** ~41% with clear clustering during crises
- **Major regime shifts** visible around Gulf War (1990), Financial Crisis (2008), OPEC price war (2014), COVID (2020), Ukraine war (2022)

---

## Upcoming Tasks

- [ ] **Task 2:** Bayesian change point modeling with PyMC
- [ ] **Task 3:** Flask API + React interactive dashboard

---

## Data Sources

| Dataset | Source |
|---------|--------|
| Brent Oil Prices | [EIA via datahub.io](https://datahub.io/core/oil-prices) |
| Market Events | Curated from historical records (OPEC, EIA, news archives) |

---

## Team & Support

- **Slack:** #all-week10
- **Office hours:** Mon–Fri, 08:00–15:00 UTC
- **Tutors:** Kerod, Feven, Mahbubah
# Change-Point-Analysis
# Terminal 1 — Flask API
source venv/bin/activate
python -m backend.app

# Terminal 2 — React frontend
cd frontend && npm install && npm run dev
