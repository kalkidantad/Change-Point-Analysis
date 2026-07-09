"""Time series analysis utilities."""

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller


def adf_test(series: pd.Series, name: str = "series") -> dict:
    """Run Augmented Dickey-Fuller stationarity test.

    Returns
    -------
    dict
        Test statistic, p-value, and interpretation.
    """
    result = adfuller(series.dropna(), autolag="AIC")
    p_value = result[1]
    stationary = p_value < 0.05

    return {
        "name": name,
        "adf_statistic": result[0],
        "p_value": p_value,
        "used_lag": result[2],
        "n_obs": result[3],
        "critical_values": result[4],
        "stationary": stationary,
        "interpretation": (
            f"Reject H0 (stationary) at 5% level"
            if stationary
            else "Fail to reject H0 (non-stationary) at 5% level"
        ),
    }


def summary_by_period(
    prices: pd.DataFrame, freq: str = "10YE"
) -> pd.DataFrame:
    """Compute summary statistics grouped by time period."""
    grouped = prices["price"].resample(freq).agg(["mean", "std", "min", "max", "count"])
    grouped.columns = ["mean_price", "std_price", "min_price", "max_price", "n_days"]
    return grouped


def event_window_stats(
    prices: pd.DataFrame,
    events: pd.DataFrame,
    window_days: int = 30,
) -> pd.DataFrame:
    """Compute pre/post price statistics around each event."""
    records = []
    for _, event in events.iterrows():
        event_date = event["date"]
        start = event_date - pd.Timedelta(days=window_days)
        end = event_date + pd.Timedelta(days=window_days)

        pre = prices.loc[start:event_date, "price"]
        post = prices.loc[event_date:end, "price"]

        if len(pre) < 5 or len(post) < 5:
            continue

        pre_mean = pre.mean()
        post_mean = post.mean()
        pct_change = ((post_mean - pre_mean) / pre_mean) * 100

        records.append(
            {
                "event_id": event["event_id"],
                "event_name": event["event_name"],
                "event_date": event_date,
                "pre_mean": round(pre_mean, 2),
                "post_mean": round(post_mean, 2),
                "pct_change": round(pct_change, 2),
                "category": event["category"],
            }
        )

    return pd.DataFrame(records)
