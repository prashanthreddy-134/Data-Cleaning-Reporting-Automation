from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from data_cleaning import clean_sales_data
from report_generation import generate_report

def main():
    print("=" * 60)
    print("AUTOMATED DATA CLEANING & REPORTING SYSTEM")
    print("=" * 60)

    print("\n[1/3] Cleaning raw sales data...")
    df, summary = clean_sales_data()

    print("[2/3] Generating visual reports...")
    report_path = generate_report(df, summary)

    print("[3/3] Completed successfully.")
    print("\nCleaning Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")

    print(f"\nCleaned data: data/cleaned_sales_data.csv")
    print(f"Excel report: {report_path.relative_to(ROOT)}")
    print("Charts: reports/charts/")
    print("\nTask 4 automation completed successfully.")

if __name__ == "__main__":
    main()
