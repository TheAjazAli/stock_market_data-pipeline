
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"

# Find the most recently created CSV file
csv_files = list(RAW_DIR.glob("RELIANCE_NS_*.csv"))

if not csv_files:
    raise FileNotFoundError("No Reliance CSV file found in data/raw.")

csv_path = max(csv_files, key=lambda file: file.stat().st_mtime)

df = pd.read_csv(csv_path)

print("=" * 50)
print("STOCK DATA VALIDATION REPORT")
print("=" * 50)

print(f"\nFile: {csv_path.name}")
print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")

print("\n1. COLUMN NAMES")
print(df.columns.tolist())

print("\n2. DATA TYPES")
print(df.dtypes.to_string())

print("\n3. MISSING VALUES")
print(df.isnull().sum().to_string())

print("\n4. DUPLICATE ROWS")
print(df.duplicated().sum())

# Check whether expected market-data columns exist
required_columns = ["Open", "High", "Low", "Close", "Volume"]
missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

print("\n5. REQUIRED COLUMN CHECK")
if missing_columns:
    print("Missing columns:", missing_columns)
else:
    print("All required market-data columns exist.")

    # Check for invalid negative prices or volumes
    price_columns = ["Open", "High", "Low", "Close"]
    negative_prices = (df[price_columns] < 0).any(axis=1).sum()
    negative_volumes = (df["Volume"] < 0).sum()

    # Check whether the daily high is below the daily low
    invalid_high_low = (df["High"] < df["Low"]).sum()

    print(f"Rows with negative prices: {negative_prices}")
    print(f"Rows with negative volumes: {negative_volumes}")
    print(f"Rows where High < Low: {invalid_high_low}")

print("\n6. FIRST FIVE RECORDS")
print(df.head().to_string(index=False))

print("\nValidation inspection completed.")
