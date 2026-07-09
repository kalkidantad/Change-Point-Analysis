"""Tests for data loading utilities."""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data_loader import compute_log_returns, load_brent_prices, load_events


def test_load_brent_prices():
    df = load_brent_prices()
    assert isinstance(df.index, pd.DatetimeIndex)
    assert "price" in df.columns
    assert len(df) > 8000
    assert df["price"].min() > 0


def test_load_events():
    events = load_events()
    assert len(events) >= 10
    assert "event_name" in events.columns
    assert "date" in events.columns


def test_compute_log_returns():
    df = load_brent_prices()
    returns = compute_log_returns(df)
    assert len(returns) == len(df) - 1
    assert returns.std() > 0
