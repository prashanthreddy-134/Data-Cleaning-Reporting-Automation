# Automated Data Cleaning & Reporting System

## Task 4 – Data Cleaning & Reporting Automation

This project automates a complete data cleaning and reporting workflow using Python.

### Features

- Handles missing values
- Removes duplicate records
- Standardizes inconsistent text/category values
- Converts dates and numerical fields
- Detects and repairs invalid quantity/price values
- Recalculates sales values
- Generates a cleaned CSV automatically
- Generates Excel reports automatically
- Creates visual summaries
- Includes automated tests

## Project Workflow

```text
Raw Sales CSV
     ↓
Data Cleaning
     ↓
Validation
     ↓
Cleaned CSV
     ↓
Sales Analysis
     ↓
Excel Report + Charts
```

## Technologies

- Python
- Pandas
- Matplotlib
- OpenPyXL
- Pytest

## How to Run

### 1. Open the project

Open this folder in VS Code.

### 2. Create virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use:

```powershell
venv\Scripts\activate.bat
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run the complete automation

```powershell
python src/main.py
```

### 5. Run tests

```powershell
python -m pytest -v
```

## Generated Files

After running the program:

```text
data/
└── cleaned_sales_data.csv

reports/
├── sales_report.xlsx
├── cleaning_summary.txt
└── charts/
    ├── monthly_sales.png
    ├── category_sales.png
    ├── region_sales.png
    └── top_products.png
```

## Data Cleaning Operations

The raw dataset intentionally contains:

- Missing customer names
- Missing region values
- Duplicate records
- Inconsistent capitalization
- Extra spaces
- Negative quantities
- Negative sales
- Missing unit prices
- Inconsistent payment-method formatting

The automation repairs these issues and validates the final dataset.

## Report Contents

The Excel report contains:

1. Dashboard – KPIs and cleaning metrics
2. Cleaned Data – final processed dataset
3. Monthly Sales
4. Category Sales
5. Region Sales
6. Top Products

## Expected Outcome

The project demonstrates practical data preprocessing, automation, reporting, and visualization. It reduces manual cleaning and creates a repeatable reporting workflow from raw data to business-ready insights.

## Author

Prashanth Reddy S


## Enhanced Excel Dashboard

The automated Excel report now includes a professional dashboard with:

- Total Sales KPI
- Total Orders KPI
- Rows Cleaned KPI
- Duplicate Records Removed KPI
- Before/after data-quality summary
- Automated key insights
- Embedded monthly sales chart
- Embedded category sales chart
- Embedded regional sales chart
- Embedded top-products chart
- Separate detailed analysis sheets
