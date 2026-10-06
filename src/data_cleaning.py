from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]

def clean_sales_data(input_path=None, output_path=None):
    input_path = Path(input_path or BASE_DIR / "data" / "raw_sales_data.csv")
    output_path = Path(output_path or BASE_DIR / "data" / "cleaned_sales_data.csv")

    df = pd.read_csv(input_path)
    original_rows = len(df)
    original_duplicates = int(df.duplicated().sum())
    missing_before = int(df.isna().sum().sum())

    # Standardize column names
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    # Standardize text fields
    text_cols = ["customer_name", "product", "category", "region", "payment_method"]
    for col in text_cols:
        df[col] = df[col].astype("string").str.strip()

    df["category"] = df["category"].str.title()
    df["region"] = df["region"].str.title()
    df["payment_method"] = df["payment_method"].str.title()

    # Dates and numeric fields
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    numeric_cols = ["quantity", "unit_price", "sales"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Missing text values
    df["customer_name"] = df["customer_name"].fillna("Unknown Customer")
    df["region"] = df["region"].fillna("Unknown Region")

    # Invalid numeric values become missing, then are repaired
    df.loc[df["quantity"] <= 0, "quantity"] = pd.NA
    df.loc[df["unit_price"] <= 0, "unit_price"] = pd.NA

    df["quantity"] = df["quantity"].fillna(df["quantity"].median()).round().astype("int64")
    df["unit_price"] = df["unit_price"].fillna(df["unit_price"].median())

    # Recalculate sales from cleaned quantity and unit price
    df["sales"] = (df["quantity"] * df["unit_price"]).round(2)

    # Sort and save
    df = df.sort_values("order_date").reset_index(drop=True)
    df.to_csv(output_path, index=False, date_format="%Y-%m-%d")

    summary = {
        "rows_before": original_rows,
        "duplicate_rows_removed": original_duplicates,
        "missing_cells_before": missing_before,
        "rows_after": len(df),
        "missing_cells_after": int(df.isna().sum().sum()),
        "columns": len(df.columns),
        "total_sales": round(float(df["sales"].sum()), 2),
    }
    return df, summary

if __name__ == "__main__":
    df, summary = clean_sales_data()
    print("Cleaning completed.")
    for k, v in summary.items():
        print(f"{k}: {v}")
