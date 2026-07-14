"""Data access layer for the dashboard API."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.data_loader import load_brent_prices, load_events

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"


def get_prices(start: str | None = None, end: str | None = None) -> list[dict]:
    prices = load_brent_prices()
    if start:
        prices = prices[prices.index >= pd.Timestamp(start)]
    if end:
        prices = prices[prices.index <= pd.Timestamp(end)]

    return [
        {"date": idx.strftime("%Y-%m-%d"), "price": round(float(row.price), 2)}
        for idx, row in prices.iterrows()
    ]


def get_events(category: str | None = None) -> list[dict]:
    events = load_events()
    if category:
        events = events[events["category"].str.lower() == category.lower()]

    return [
        {
            "event_id": int(row.event_id),
            "date": row.date.strftime("%Y-%m-%d"),
            "event_name": row.event_name,
            "category": row.category,
            "region": row.region,
            "description": row.description,
            "expected_price_impact": row.expected_price_impact,
        }
        for _, row in events.iterrows()
    ]


def get_change_points() -> list[dict]:
    path = OUTPUTS_DIR / "change_point_results.json"
    if not path.exists():
        return []
    with open(path) as f:
        return json.load(f)


def get_event_associations(analysis: str | None = None) -> list[dict]:
    path = OUTPUTS_DIR / "event_associations.csv"
    if not path.exists():
        return []

    df = pd.read_csv(path)
    if analysis:
        df = df[df["analysis"] == analysis]

    records = df.to_dict(orient="records")
    for row in records:
        row["within_hdi"] = bool(row.get("within_hdi"))
        row["within_window"] = bool(row.get("within_window"))
    return records


def get_event_metrics(event_id: int, window_days: int = 30) -> dict:
    prices = load_brent_prices()
    events = load_events()
    event = events[events["event_id"] == event_id]
    if event.empty:
        return {}

    event = event.iloc[0]
    event_date = event["date"]
    start = event_date - pd.Timedelta(days=window_days)
    end = event_date + pd.Timedelta(days=window_days)

    window = prices.loc[start:end].copy()
    pre = prices.loc[start:event_date, "price"]
    post = prices.loc[event_date:end, "price"]

    returns = prices["price"].pct_change().dropna()
    vol_window = returns.loc[start:end].std() * (252**0.5) * 100

    return {
        "event_id": int(event.event_id),
        "event_name": event.event_name,
        "event_date": event_date.strftime("%Y-%m-%d"),
        "category": event.category,
        "window_days": window_days,
        "pre_mean_price": round(float(pre.mean()), 2),
        "post_mean_price": round(float(post.mean()), 2),
        "pct_change": round(float((post.mean() - pre.mean()) / pre.mean() * 100), 2),
        "annualized_volatility": round(float(vol_window), 2),
        "window_prices": [
            {"date": idx.strftime("%Y-%m-%d"), "price": round(float(row.price), 2)}
            for idx, row in window.iterrows()
        ],
    }


def get_summary() -> dict:
    prices = load_brent_prices()
    returns = prices["price"].pct_change().dropna()

    return {
        "total_observations": len(prices),
        "date_range": {
            "start": prices.index.min().strftime("%Y-%m-%d"),
            "end": prices.index.max().strftime("%Y-%m-%d"),
        },
        "price_stats": {
            "min": round(float(prices["price"].min()), 2),
            "max": round(float(prices["price"].max()), 2),
            "mean": round(float(prices["price"].mean()), 2),
        },
        "annualized_volatility": round(float(returns.std() * (252**0.5) * 100), 2),
        "num_events": len(load_events()),
        "num_change_point_analyses": len(get_change_points()),
    }
