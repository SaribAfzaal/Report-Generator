from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

BRAND_COLOR = colors.HexColor("#2E5090")
LIGHT_GREY = colors.HexColor("#F2F2F2")

def build_title_section(report_title, generated_on, total_rows, styles):
    # Return the list of elements for the top of the page (title + quick facts).
    title_style = ParagraphStyle(
        "ReportTitle", parent=styles["Title"], textColor=BRAND_COLOR, spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        "ReportSubtitle", parent=styles["Normal"], textColor=colors.grey, fontSize=10
    )
    elements = [
        Paragraph(report_title, title_style),
        Paragraph(f"Generated on {generated_on} &bull; {total_rows} rows of source data", subtitle_style),
        Spacer(1, 0.3 * inch),
    ]
    return elements

def build_summary_table(summary, group_column, value_column):
    # Turn the summary DataFrame into a styled reportlab Table.
    # Table header row
    table_data = [[group_column, f"Total {value_column}", f"Average {value_column}", "Count"]]
    # Table body rows
    for _, row in summary.iterrows():
        table_data.append([
            str(row.iloc[0]),
            f"{row['Total']:,.2f}",
            f"{row['Average']:,.2f}",
            str(row["Count"]),
        ])
    table = Table(table_data, hAlign="LEFT", colWidths=[1.8 * inch, 1.6 * inch, 1.6 * inch, 1 * inch])
    table.setStyle(TableStyle([
        # Header row styling
        ("BACKGROUND", (0, 0), (-1, 0), BRAND_COLOR),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        # Body styling
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GREY]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
    ]))
    return table

def write_pdf_report(output_path, report_title, generated_on, summary, group_column, value_column, total_rows):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )
    elements = []
    elements += build_title_section(report_title, generated_on, total_rows, styles)
    elements.append(Paragraph("Summary by " + group_column, styles["Heading2"]))
    elements.append(Spacer(1, 0.15 * inch))
    elements.append(build_summary_table(summary, group_column, value_column))
    elements.append(Spacer(1, 0.3 * inch))
    footer_style = ParagraphStyle("Footer", parent=styles["Normal"], fontSize=8, textColor=colors.grey)
    elements.append(Paragraph("Generated automatically by Simple Report Generator.", footer_style))
    doc.build(elements)