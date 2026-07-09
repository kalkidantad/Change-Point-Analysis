"""Smoke tests for change point model (fast MCMC)."""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.change_point_model import build_change_point_model, fit_change_point_model
from src.data_loader import load_brent_prices, compute_log_returns


def test_build_change_point_model():
    data = np.random.randn(50)
    model = build_change_point_model(data)
    assert model is not None


def test_fit_change_point_model_smoke():
    prices = load_brent_prices()
    returns = compute_log_returns(prices)["2020-01-01":"2020-03-31"]
    result = fit_change_point_model(returns, draws=100, tune=100, chains=2)
    assert result.tau_summary["tau_median_date"] is not None
    assert 0 <= result.impact_summary["prob_mu2_greater_mu1"] <= 1
