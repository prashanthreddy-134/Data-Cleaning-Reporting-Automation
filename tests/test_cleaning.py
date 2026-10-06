import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from data_cleaning import clean_sales_data

def test_cleaning_removes_duplicates_and_missing_values(tmp_path):
    source = ROOT / "data" / "raw_sales_data.csv"
    output = tmp_path / "cleaned.csv"
    df, summary = clean_sales_data(source, output)

    assert summary["duplicate_rows_removed"] >= 1
    assert df.duplicated().sum() == 0
    assert df.isna().sum().sum() == 0
    assert (df["quantity"] > 0).all()
    assert (df["unit_price"] > 0).all()
    assert (df["sales"] > 0).all()

def test_sales_is_recalculated(tmp_path):
    source = ROOT / "data" / "raw_sales_data.csv"
    output = tmp_path / "cleaned.csv"
    df, _ = clean_sales_data(source, output)

    expected = (df["quantity"] * df["unit_price"]).round(2)
    assert (df["sales"] == expected).all()
