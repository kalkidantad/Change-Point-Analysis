"""Data loading and preprocessing utilities for Brent oil price analysis."""

from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_brent_prices(filepath: Path | None = None) -> pd.DataFrame:
    """Load Brent oil prices and parse dates.

    Parameters
    ----------
    filepath : Path, optional
        Path to CSV file. Defaults to data/BrentOilPrices.csv.

    Returns
    -------
    pd.DataFrame
        DataFrame with datetime index and 'price' column.
    """
    if filepath is None:
        filepath = DATA_DIR / "BrentOilPrices.csv"

    df = pd.read_csv(filepath)
    df.columns = [c.lower() for c in df.columns]
    df["date"] = pd.to_datetime(df["date"], format="%d-%b-%y")
    df = df.set_index("date").sort_index()
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["price"])
    return df


def load_events(filepath: Path | None = None) -> pd.DataFrame:
    """Load curated oil market events.

    Parameters
    ----------
    filepath : Path, optional
        Path to events CSV. Defaults to data/oil_market_events.csv.

    Returns
    -------
    pd.DataFrame
        Events with parsed date column.
    """
    if filepath is None:
        filepath = DATA_DIR / "oil_market_events.csv"

    events = pd.read_csv(filepath)
    events["date"] = pd.to_datetime(events["date"])
    return events


def compute_log_returns(prices: pd.DataFrame) -> pd.Series:
    """Compute daily log returns from price series."""
    price = prices["price"].astype(float)
    return np.log(price / price.shift(1)).dropna().rename("log_return")


def compute_rolling_volatility(
    log_returns: pd.Series, window: int = 30
) -> pd.Series:
    """Compute rolling standard deviation of log returns."""
    return log_returns.rolling(window=window).std()
