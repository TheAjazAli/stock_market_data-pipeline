
from pathlib import Path
from datetime import datetime, timezone
import json

import pandas as pd
import yfinance as yf


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"

# Start with one NSE-listed stock
SYMBOL = "RELIANCE.NS"


def extract_stock_data(symbol: str) -> None:
    """Download a small historical batch and preserve the source output."""

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Starting extraction for {symbol}...")

    # Download approximately one month of daily market data.
    stock = yf.Ticker(symbol)
    df = stock.history(
        period="1mo",
        interval="1d",
        auto_adjust=False
    )

    # Fail visibly if the provider returns no usable rows.
    if df.empty:
        raise RuntimeError(
            f"No data returned for {symbol}. "
            "Check the symbol, connectivity and data-source availability."
        )

    # Keep the returned columns and values intact in the CSV snapshot.
    # This is a downloaded data snapshot, not the original HTTP response.
    timestamp = datetime.now(timezone.utc)
    run_timestamp = timestamp.strftime("%Y%m%dT%H%M%SZ")

    csv_path = RAW_DIR / f"{symbol.replace('.', '_')}_{run_timestamp}.csv"
    metadata_path = RAW_DIR / f"{symbol.replace('.', '_')}_{run_timestamp}.json"

    df.to_csv(csv_path, index=True)

    metadata = {
        "symbol": symbol,
        "source": "Yahoo Finance via yfinance",
        "retrieved_at_utc": timestamp.isoformat(),
        "requested_period": "1mo",
        "requested_interval": "1d",
        "records_returned": int(len(df)),
        "columns": [str(column) for column in df.columns],
        "file": csv_path.name
    }

    metadata_path.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8"
    )

    print("\nExtraction successful.")
    print(f"Symbol: {symbol}")
    print(f"Records returned: {len(df)}")
    print(f"CSV saved to: {csv_path}")
    print(f"Metadata saved to: {metadata_path}")

    print("\nLatest available records:")
    print(df.tail(5).to_string())


if __name__ == "__main__":
    extract_stock_data(SYMBOL)
