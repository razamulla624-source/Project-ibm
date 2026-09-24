"""
data_loader.py
--------------
Step 1 & 2: Load the CSV dataset and perform data quality checks.
Step 3: Validate / recalculate Sales = Quantity × Unit Price.
"""

import os
import pandas as pd

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "supermarket_data.csv")


def load_data() -> pd.DataFrame:
    """Load the CSV and return a clean DataFrame."""
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    return df


def check_data_quality(df: pd.DataFrame) -> dict:
    """
    Inspect the DataFrame for:
      - Missing values per column
      - Duplicate Invoice IDs
      - Negative numeric values (Quantity, Unit Price, Sales)
      - Sales mismatch: stored Sales vs recalculated Quantity × Unit Price
    Returns a dict summary of findings.
    """
    report = {}

    # --- Missing values ---
    missing = df.isnull().sum()
    report["missing_values"] = missing[missing > 0].to_dict()
    report["total_missing"] = int(missing.sum())

    # --- Duplicate invoices ---
    dupes = df.duplicated(subset=["Invoice ID"]).sum()
    report["duplicate_invoice_ids"] = int(dupes)

    # --- Negative numeric fields ---
    neg_qty = int((df["Quantity"] < 0).sum())
    neg_price = int((df["Unit Price"] < 0).sum())
    neg_sales = int((df["Sales"] < 0).sum())
    report["negative_quantity"] = neg_qty
    report["negative_unit_price"] = neg_price
    report["negative_sales"] = neg_sales

    # --- Sales recalculation check ---
    df["_Computed_Sales"] = (df["Quantity"] * df["Unit Price"]).round(2)
    mismatch = (df["Sales"].round(2) != df["_Computed_Sales"]).sum()
    report["sales_mismatch_rows"] = int(mismatch)
    df.drop(columns=["_Computed_Sales"], inplace=True)

    return report


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply minimal cleaning:
      - Drop fully-duplicate rows
      - Drop rows where Quantity or Unit Price is missing/zero/negative
      - Recalculate Sales = Quantity × Unit Price (authoritative)
      - Add helper columns: Month, Month-Year label, Quarter
    Returns the cleaned DataFrame.
    """
    # Drop fully-duplicate rows
    df = df.drop_duplicates()

    # Keep rows with valid Quantity and Unit Price
    df = df[(df["Quantity"] > 0) & (df["Unit Price"] > 0)]

    # Recalculate Sales (ensures consistency)
    df = df.copy()
    df["Sales"] = (df["Quantity"] * df["Unit Price"]).round(2)

    # Derived time columns
    df["Month"] = df["Date"].dt.month
    df["Month_Label"] = df["Date"].dt.to_period("M").astype(str)
    df["Quarter"] = df["Date"].dt.to_period("Q").astype(str)
    df["Day_of_Week"] = df["Date"].dt.day_name()

    return df.reset_index(drop=True)


def get_clean_dataframe() -> tuple[pd.DataFrame, dict]:
    """Convenience wrapper: load → quality-check → clean."""
    raw = load_data()
    quality_report = check_data_quality(raw.copy())
    clean = clean_data(raw.copy())
    return clean, quality_report
