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
├── figures/                        # EDA and posterior visualizations
├── notebooks/
│   ├── 01_eda.ipynb                # Task 1: Initial EDA
│   └── 02_change_point_model.ipynb # Task 2: PyMC modeling
├── outputs/                        # Model results (JSON/CSV)
├── scripts/
│   ├── download_data.py            # Data download utility
│   └── run_change_point_analysis.py
├── src/
│   ├── data_loader.py              # Data loading utilities
│   ├── analysis.py                 # Time series analysis helpers
│   └── change_point_model.py       # PyMC change point model
├── tests/
│   ├── test_data_loader.py
│   └── test_change_point_model.py
└── requirements.txt
```

---

## Quick Start

### 1. Clone and set up environment

```bash
git clone <your-repo-url>
cd Change-Point-Analysis
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### 2. Run tests

```bash
pytest tests/ -v
```

### 3. Run EDA notebook

```bash
jupyter notebook notebooks/01_eda.ipynb
```

### 4. Run change point analysis

```bash
python scripts/run_change_point_analysis.py
jupyter notebook notebooks/02_change_point_model.ipynb
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

## Task 2 — Change Point Modeling (Complete)

| Deliverable | Location |
|-------------|----------|
| PyMC change point notebook | [`notebooks/02_change_point_model.ipynb`](notebooks/02_change_point_model.ipynb) |
| Model utilities | [`src/change_point_model.py`](src/change_point_model.py) |
| Analysis script | [`scripts/run_change_point_analysis.py`](scripts/run_change_point_analysis.py) |
| Exported results (JSON/CSV) | [`outputs/`](outputs/) |
| Posterior visualizations | [`figures/cp_*.png`](figures/) |

### Key Findings

| Period | Change Point | Price Impact | Nearest Event |
|--------|-------------|--------------|---------------|
| COVID 2020 | 2020-04-21 | $45 → $40 (−10%) | OPEC+ cuts (9 days) |
| Financial Crisis | 2008-12-10 | $100 → $50 (−50%) | Lehman collapse (86 days) |
| Ukraine War | 2022-04-21 | $102 → $107 (+6%) | OPEC+ decision (21 days) |
| Gulf War | 1990-10-05 | $24 → $27 (+9%) | Iraq invasion (64 days) |
| OPEC Price War | 2016-01-19 | $66 → $41 (−39%) | Near market bottom |

---

## Task 3 — Interactive Dashboard (Complete)

| Deliverable | Location |
|-------------|----------|
| Flask API backend | [`backend/`](backend/) |
| React frontend | [`frontend/`](frontend/) |
| API tests | [`tests/test_api.py`](tests/test_api.py) |
| Dashboard screenshots | [`docs/screenshots/`](docs/screenshots/) |

### Run the dashboard

```bash
# Change-Point-Analysis
# Terminal 1 — Flask API
source venv/bin/activate
python -m backend.app

# Terminal 2 — React frontend
cd frontend && npm install && npm run dev
```

Open `http://localhost:3000`.

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/prices` | Historical Brent prices (filter by `start`, `end`) |
| `GET /api/events` | Curated market events |
| `GET /api/change-points` | PyMC model results |
| `GET /api/event-associations` | Event–change point mapping |
| `GET /api/events/<id>/metrics` | Pre/post event impact metrics |
| `GET /api/summary` | Dataset summary statistics |

---

## Data Sources

| Dataset | Source |
|---------|--------|
| Brent Oil Prices | [EIA via datahub.io](https://datahub.io/core/oil-prices) (DCOILBRENTEU / FRED) |
| Market Events | Curated from historical records (OPEC, EIA, news archives) |

---

## References

- [PyMC Change Point Examples](https://www.pymc.io/projects/examples/en/latest/)
- [Change Point Detection Guide](https://forecastegy.com/posts/change-point-detection-time-series-python/)
- [Bayesian Time Series Analysis](https://www.embecosm.com/2021/12/18/forget-arima-going-bayesian-with-time-series-analysis/)

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
