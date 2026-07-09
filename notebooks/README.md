# Notebooks

This directory contains Jupyter notebooks for the Brent oil price change point analysis.

| Notebook | Description | Task |
|----------|-------------|------|
| `01_eda.ipynb` | Exploratory data analysis: trends, stationarity, volatility | Task 1 (Interim) |
| `02_change_point_model.ipynb` | Bayesian change point detection with PyMC | Task 2 (Final) |

## Running Notebooks

```bash
# From project root
pip install -r requirements.txt
jupyter notebook notebooks/
```

Ensure the kernel uses the project virtual environment so `src/` imports resolve correctly.
