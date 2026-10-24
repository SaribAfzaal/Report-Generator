import argparse
import os
from datetime import datetime
import pandas as pd
from excel_report import write_excel_report
from pdf_report import write_pdf_report

def guess_group_column(df):
    # Pick a text column to group by, if the user didn't specify one.
    for column_name in df.columns:
        if not pd.api.types.is_numeric_dtype(df[column_name]):
            return column_name
    return None

def guess_value_column(df):
    # Pick a number column to summarize, if the user didn't specify one.
    for column_name in df.columns:
        if pd.api.types.is_numeric_dtype(df[column_name]):
            return column_name
    return None

def build_summary(df, group_column, value_column):
    """
    Turn the raw data into a small summary table.

    Example: if group_column is "Region" and value_column is "Sales",
    this returns one row per region with the total, average, and count
    of sales in that region.
    """
    summary = df.groupby(group_column)[value_column].agg(["sum", "mean", "count"])
    summary = summary.rename(columns={"sum": "Total", "mean": "Average", "count": "Count"})
    summary["Average"] = summary["Average"].round(2)
    summary = summary.sort_values("Total", ascending=False)
    summary = summary.reset_index()
    return summary

def main():
    parser = argparse.ArgumentParser(description="Generate Excel and PDF reports from a CSV file.")
    parser.add_argument("input_file", help="Path to the input CSV file")
    parser.add_argument("--group-by", help="Column to group rows by (default: auto-detected)")
    parser.add_argument("--value", help="Numeric column to summarize (default: auto-detected)")
    parser.add_argument("--output-name", help="Base name for the report files (default: based on input file)")
    args = parser.parse_args()
    # Step 1: Load the data
    if not os.path.exists(args.input_file):
        print(f"Error: could not find the file '{args.input_file}'")
        return
    df = pd.read_csv(args.input_file)
    if df.empty:
        print("Error: the input file has no data rows.")
        return
    # Step 2: Work out which columns to use
    group_column = args.group_by or guess_group_column(df)
    value_column = args.value or guess_value_column(df)
    if group_column is None or value_column is None:
        print("Error: couldn't find a text column to group by and a number column to summarize.")
        print("Try specifying them manually, e.g. --group-by Region --value Sales")
        return
    print(f"Grouping by: {group_column}")
    print(f"Summarizing: {value_column}")
    # Step 3: Build the summary table
    summary = build_summary(df, group_column, value_column)
    # Step 4: Work out output file names
    base_name = args.output_name or os.path.splitext(os.path.basename(args.input_file))[0]
    excel_path = f"{base_name}_report.xlsx"
    pdf_path = f"{base_name}_report.pdf"
    report_title = f"Report: {base_name}"
    generated_on = datetime.now().strftime("%Y-%m-%d %H:%M")
    # Step 5: Write the reports
    write_excel_report(
        excel_path,
        report_title=report_title,
        generated_on=generated_on,
        raw_data=df,
        summary=summary,
        group_column=group_column,
        value_column=value_column,
    )
    print(f"Created Excel report: {excel_path}")
    write_pdf_report(
        pdf_path,
        report_title=report_title,
        generated_on=generated_on,
        summary=summary,
        group_column=group_column,
        value_column=value_column,
        total_rows=len(df),
    )
    print(f"Created PDF report: {pdf_path}")
if __name__ == "__main__":
    main()