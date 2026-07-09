"""Download and prepare Brent oil price data."""

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "BrentOilPrices.csv"
SOURCE_URL = (
    "https://raw.githubusercontent.com/datasets/oil-prices/main/data/brent-daily.csv"
)


def download_and_prepare(output_path: Path = DATA_PATH) -> pd.DataFrame:
    """Download Brent daily prices and save in challenge format."""
    df = pd.read_csv(SOURCE_URL)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df[(df["Date"] >= "1987-05-20") & (df["Date"] <= "2022-09-30")]
    df = df.dropna(subset=["Price"])
    df["Date"] = df["Date"].dt.strftime("%d-%b-%y")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} rows to {output_path}")
    return df


if __name__ == "__main__":
    download_and_prepare()
