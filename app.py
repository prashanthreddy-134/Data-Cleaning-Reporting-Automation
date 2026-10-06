import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"

sys.path.insert(0, str(SRC_DIR))

from data_cleaning import clean_sales_data
from report_generation import generate_report


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Data Cleaning & Reporting Automation",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("📊 Data Cleaning & Reporting Automation")

st.markdown(
    "### Task 4 — Automated Data Cleaning, Analysis & Reporting"
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("⚙️ Controls")

run_button = st.sidebar.button(
    "🚀 Run Data Cleaning",
    use_container_width=True
)

st.sidebar.info(
    "This dashboard automatically cleans the raw sales dataset, "
    "generates analytics, creates visual summaries and produces "
    "an Excel report."
)


# =========================================================
# MAIN APPLICATION
# =========================================================

try:

    raw_file = BASE_DIR / "data" / "raw_sales_data.csv"
    cleaned_file = BASE_DIR / "data" / "cleaned_sales_data.csv"

    # -----------------------------------------------------
    # RUN CLEANING
    # -----------------------------------------------------

    if run_button or not cleaned_file.exists():

        with st.spinner(
            "Cleaning data and generating report..."
        ):

            df, summary = clean_sales_data()

            generate_report(
                df,
                summary
            )

        st.success(
            "✅ Data cleaning and reporting completed successfully!"
        )

    # -----------------------------------------------------
    # LOAD EXISTING CLEANED DATA
    # -----------------------------------------------------

    else:

        raw_df = pd.read_csv(raw_file)

        df = pd.read_csv(cleaned_file)

        df["order_date"] = pd.to_datetime(
            df["order_date"],
            errors="coerce"
        )

        # Calculate statistics dynamically
        rows_before = len(raw_df)

        duplicate_rows = int(
            raw_df.duplicated().sum()
        )

        missing_before = int(
            raw_df.isna().sum().sum()
        )

        rows_after = len(df)

        missing_after = int(
            df.isna().sum().sum()
        )

        summary = {
            "rows_before": rows_before,
            "duplicate_rows_removed": duplicate_rows,
            "missing_cells_before": missing_before,
            "rows_after": rows_after,
            "missing_cells_after": missing_after,
            "columns": len(df.columns),
            "total_sales": round(
                float(df["sales"].sum()),
                2
            )
        }


    # =====================================================
    # KPI SECTION
    # =====================================================

    st.subheader(
        "📌 Key Performance Indicators"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Sales",
            f"₹{df['sales'].sum():,.2f}"
        )

    with col2:

        st.metric(
            "Total Orders",
            f"{df['order_id'].nunique():,}"
        )

    with col3:

        st.metric(
            "Rows After Cleaning",
            f"{len(df):,}"
        )

    with col4:

        st.metric(
            "Duplicates Removed",
            f"{summary['duplicate_rows_removed']:,}"
        )


    st.divider()


    # =====================================================
    # DATA QUALITY
    # =====================================================

    st.subheader(
        "🧹 Data Quality Summary"
    )

    q1, q2, q3 = st.columns(3)

    with q1:

        st.metric(
            "Rows Before",
            summary["rows_before"]
        )

    with q2:

        st.metric(
            "Missing Cells Before",
            summary["missing_cells_before"]
        )

    with q3:

        st.metric(
            "Missing Cells After",
            summary["missing_cells_after"]
        )


    st.divider()


    # =====================================================
    # SALES ANALYSIS
    # =====================================================

    st.subheader(
        "📈 Sales Analysis"
    )

    chart_col1, chart_col2 = st.columns(2)


    # -----------------------------------------------------
    # MONTHLY SALES
    # -----------------------------------------------------

    monthly = (
        df.groupby(
            df["order_date"]
            .dt
            .to_period("M")
            .astype(str)
        )["sales"]
        .sum()
        .rename("Sales")
        .to_frame()
    )

    with chart_col1:

        st.markdown(
            "#### Monthly Sales"
        )

        st.line_chart(
            monthly
        )


    # -----------------------------------------------------
    # CATEGORY SALES
    # -----------------------------------------------------

    category = (
        df.groupby("category")["sales"]
        .sum()
        .sort_values(
            ascending=False
        )
        .rename("Sales")
        .to_frame()
    )

    with chart_col2:

        st.markdown(
            "#### Sales by Category"
        )

        st.bar_chart(
            category
        )


    # =====================================================
    # REGION + PRODUCT ANALYSIS
    # =====================================================

    chart_col3, chart_col4 = st.columns(2)


    # -----------------------------------------------------
    # REGION SALES
    # -----------------------------------------------------

    region = (
        df.groupby("region")["sales"]
        .sum()
        .sort_values(
            ascending=False
        )
        .rename("Sales")
        .to_frame()
    )

    with chart_col3:

        st.markdown(
            "#### Sales by Region"
        )

        st.bar_chart(
            region
        )


    # -----------------------------------------------------
    # TOP PRODUCTS
    # -----------------------------------------------------

    products = (
        df.groupby("product")["sales"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )

    with chart_col4:

        st.markdown(
            "#### Top 10 Products"
        )

        # Horizontal chart keeps product names readable.
        top_products = (
            products
            .sort_values(
                ascending=True
            )
            .rename("Sales")
            .to_frame()
        )

        st.bar_chart(
            top_products,
            horizontal=True
        )


    st.divider()


    # =====================================================
    # CLEANED DATASET
    # =====================================================

    st.subheader(
        "📋 Cleaned Dataset"
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # DOWNLOAD RESULTS
    # =====================================================

    st.subheader(
        "⬇️ Download Results"
    )


    # -----------------------------------------------------
    # CLEANED CSV
    # -----------------------------------------------------

    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "📥 Download Cleaned CSV",
        data=csv_data,
        file_name="cleaned_sales_data.csv",
        mime="text/csv"
    )


    # -----------------------------------------------------
    # EXCEL REPORT
    # -----------------------------------------------------

    excel_file = (
        BASE_DIR
        / "reports"
        / "sales_report.xlsx"
    )

    if excel_file.exists():

        with open(
            excel_file,
            "rb"
        ) as f:

            st.download_button(
                "📊 Download Excel Report",
                data=f,
                file_name="sales_report.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            )


    st.divider()


    # =====================================================
    # SUCCESS MESSAGE
    # =====================================================

    st.success(
        "✅ Automated data cleaning, analysis and reporting "
        "pipeline completed."
    )


# =========================================================
# ERROR HANDLING
# =========================================================

except Exception as e:

    st.error(
        "❌ An error occurred."
    )

    st.exception(e)