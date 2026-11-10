
from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"

SYMBOL = "RELIANCE.NS"

# Load database credentials
load_dotenv(PROJECT_ROOT / ".env")

# Find latest Reliance CSV
csv_files = list(RAW_DIR.glob("RELIANCE_NS_*.csv"))

if not csv_files:
    raise FileNotFoundError("No Reliance CSV file found.")

csv_path = max(csv_files, key=lambda file: file.stat().st_mtime)

print(f"Reading file: {csv_path.name}")

# Read CSV
df = pd.read_csv(csv_path)

# Normalize column names
df.columns = [
    str(col).strip().lower().replace(" ", "_")
    for col in df.columns
]

# Identify date column
if "date" not in df.columns:
    date_column = df.columns[0]
    df = df.rename(columns={date_column: "date"})

# Validate required columns
required_columns = ["open", "high", "low", "close", "volume"]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

# Convert date
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Convert numeric columns
numeric_columns = [
    "open", "high", "low", "close",
    "adj_close", "volume", "dividends", "stock_splits"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove rows with invalid dates or missing essential values
df = df.dropna(
    subset=["date", "open", "high", "low", "close", "volume"]
)

# Prepare records for PostgreSQL
rows = []

for record in df.to_dict(orient="records"):
    def clean(value):
        if pd.isna(value):
            return None
        return value

    rows.append({
        "symbol": SYMBOL,
        "trade_date": record["date"].date(),
        "open": clean(record["open"]),
        "high": clean(record["high"]),
        "low": clean(record["low"]),
        "close": clean(record["close"]),
        "adj_close": clean(record.get("adj_close")),
        "volume": (
            int(record["volume"])
            if pd.notna(record["volume"])
            else None
        ),
        "dividends": clean(record.get("dividends", 0)),
        "stock_splits": clean(record.get("stock_splits", 0)),
        "source_file": csv_path.name
    })

if not rows:
    raise ValueError("No valid records available to load.")

# Create database connection
database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME")
)

engine = create_engine(database_url)

# Insert or update records
insert_query = text("""
    INSERT INTO stock_prices_staging (
        symbol, trade_date, open, high, low, close,
        adj_close, volume, dividends, stock_splits, source_file
    )
    VALUES (
        :symbol, :trade_date, :open, :high, :low, :close,
        :adj_close, :volume, :dividends, :stock_splits, :source_file
    )
    ON CONFLICT (symbol, trade_date)
    DO UPDATE SET
        open = EXCLUDED.open,
        high = EXCLUDED.high,
        low = EXCLUDED.low,
        close = EXCLUDED.close,
        adj_close = EXCLUDED.adj_close,
        volume = EXCLUDED.volume,
        dividends = EXCLUDED.dividends,
        stock_splits = EXCLUDED.stock_splits,
        source_file = EXCLUDED.source_file,
        loaded_at = CURRENT_TIMESTAMP;
""")

try:
    with engine.begin() as connection:
        connection.execute(insert_query, rows)

    print("\nData loading successful!")
    print(f"Source file: {csv_path.name}")
    print(f"Records processed: {len(rows)}")

except Exception as error:
    print(f"\nData loading failed: {error}")
    raise

finally:
    engine.dispose()
