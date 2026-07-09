"""Bayesian change point detection utilities using PyMC."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import arviz as az
import numpy as np
import pandas as pd
import pymc as pm


@dataclass
class ChangePointResult:
    """Container for change point model outputs."""

    trace: az.InferenceData
    dates: pd.DatetimeIndex
    series: pd.Series
    summary: pd.DataFrame
    tau_summary: dict[str, Any]
    impact_summary: dict[str, Any]


def build_change_point_model(
    data: np.ndarray,
    sigma_prior: float = 1.0,
) -> pm.Model:
    """Build a single mean-shift change point model.

    Parameters
    ----------
    data : np.ndarray
        1-D observations (e.g., log returns).
    sigma_prior : float
        Scale for weakly informative Normal priors on segment means.

    Returns
    -------
    pm.Model
        PyMC model with switch point tau and segment means mu_1, mu_2.
    """
    n = len(data)

    with pm.Model() as model:
        tau = pm.DiscreteUniform("tau", lower=0, upper=n - 2)
        mu_1 = pm.Normal("mu_1", mu=0, sigma=sigma_prior)
        mu_2 = pm.Normal("mu_2", mu=0, sigma=sigma_prior)
        sigma = pm.HalfNormal("sigma", sigma=1)

        mu = pm.math.switch(tau >= np.arange(n), mu_1, mu_2)
        pm.Normal("obs", mu=mu, sigma=sigma, observed=data)

    return model


def fit_change_point_model(
    series: pd.Series,
    draws: int = 2000,
    tune: int = 1000,
    chains: int = 4,
    target_accept: float = 0.95,
    random_seed: int = 42,
) -> ChangePointResult:
    """Fit change point model and summarize posterior quantities."""
    data = series.values.astype(float)
    dates = series.index

    model = build_change_point_model(data)
    with model:
        trace = pm.sample(
            draws=draws,
            tune=tune,
            chains=chains,
            cores=min(chains, 4),
            target_accept=target_accept,
            random_seed=random_seed,
            progressbar=False,
        )

    summary = az.summary(trace, var_names=["tau", "mu_1", "mu_2", "sigma"])
    tau_samples = trace.posterior["tau"].values.flatten()
    mu1_samples = trace.posterior["mu_1"].values.flatten()
    mu2_samples = trace.posterior["mu_2"].values.flatten()

    tau_mode = int(pd.Series(tau_samples).mode().iloc[0])
    tau_median = int(np.median(tau_samples))
    tau_date_mode = dates[tau_mode]
    tau_date_median = dates[tau_median]
    hdi = az.hdi(trace, var_names=["tau"])["tau"].values

    prob_increase = float((mu2_samples > mu1_samples).mean())
    mean_diff = float((mu2_samples - mu1_samples).mean())
    pct_change = float((np.exp(mu2_samples) - np.exp(mu1_samples)).mean() / np.exp(mu1_samples).mean() * 100)

    tau_summary = {
        "tau_mode_index": tau_mode,
        "tau_median_index": tau_median,
        "tau_mode_date": str(tau_date_mode.date()),
        "tau_median_date": str(tau_date_median.date()),
        "tau_hdi_lower_index": int(hdi[0]),
        "tau_hdi_upper_index": int(hdi[1]),
        "tau_hdi_lower_date": str(dates[int(hdi[0])].date()),
        "tau_hdi_upper_date": str(dates[int(hdi[1])].date()),
    }

    impact_summary = {
        "mu_1_mean": float(mu1_samples.mean()),
        "mu_2_mean": float(mu2_samples.mean()),
        "mu_diff_mean": mean_diff,
        "prob_mu2_greater_mu1": prob_increase,
        "approx_daily_pct_change": pct_change,
    }

    return ChangePointResult(
        trace=trace,
        dates=dates,
        series=series,
        summary=summary,
        tau_summary=tau_summary,
        impact_summary=impact_summary,
    )


def associate_change_point_with_events(
    result: ChangePointResult,
    events: pd.DataFrame,
    window_days: int = 60,
) -> pd.DataFrame:
    """Find events nearest to the detected change point."""
    cp_date = pd.Timestamp(result.tau_summary["tau_median_date"])
    hdi_start = pd.Timestamp(result.tau_summary["tau_hdi_lower_date"])
    hdi_end = pd.Timestamp(result.tau_summary["tau_hdi_upper_date"])

    records = []
    for _, event in events.iterrows():
        event_date = event["date"]
        days_diff = abs((event_date - cp_date).days)
        in_hdi = hdi_start <= event_date <= hdi_end
        in_window = days_diff <= window_days

        records.append(
            {
                "event_id": event["event_id"],
                "event_name": event["event_name"],
                "event_date": event_date,
                "category": event["category"],
                "days_from_change_point": days_diff,
                "within_hdi": in_hdi,
                "within_window": in_window,
            }
        )

    return (
        pd.DataFrame(records)
        .sort_values("days_from_change_point")
        .reset_index(drop=True)
    )


def price_level_impact(
    prices: pd.DataFrame,
    result: ChangePointResult,
) -> dict[str, float]:
    """Translate log-return segment means to approximate price levels."""
    tau_idx = result.tau_summary["tau_median_index"]
    tau_date = pd.Timestamp(result.tau_summary["tau_median_date"])

    pre_prices = prices.loc[:tau_date, "price"]
    post_prices = prices.loc[tau_date:, "price"]

    pre_mean = float(pre_prices.mean()) if len(pre_prices) else np.nan
    post_mean = float(post_prices.mean()) if len(post_prices) else np.nan
    pct = ((post_mean - pre_mean) / pre_mean * 100) if pre_mean else np.nan

    return {
        "change_point_date": str(tau_date.date()),
        "pre_period_mean_price": round(pre_mean, 2),
        "post_period_mean_price": round(post_mean, 2),
        "price_pct_change": round(pct, 2),
    }
