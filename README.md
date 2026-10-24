# Simple Report Generator

A small Python script that takes a CSV file and turns it into two report files:
an Excel spreadsheet and a PDF, both with a summary table built in.

I made this because I kept manually building the same kind of summary tables
in Excel every time I had a new batch of data. This just automates that.

## What it does

Give it a CSV with some category column (like Region or Product) and a number
column (like Sales), and it will:

- Group the data and calculate totals, averages, and counts
- Build a formatted Excel report with a summary sheet and the raw data
- Build a PDF report with the same summary, ready to print or send

## Setup

You need Python installed, then run:

## How to use it


This creates `your_data_report.xlsx` and `your_data_report.pdf` in the same folder.

If it picks the wrong columns to group by, you can tell it exactly which ones to use:


You can also change the output file name:


## Files

- `report_generator.py` — the main script, run this one
- `excel_report.py` — handles building the Excel file
- `pdf_report.py` — handles building the PDF file
- `sample_sales.csv` — example data you can test with

## Example


Try it with the included sample file to see what the output looks like before
using your own data.
