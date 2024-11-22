from reportlab.platypus import Table, TableStyle
from reportlab.lib.colors import black
from reportlab.lib import colors
from reportlab.platypus import Paragraph

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
# Importing third-party modules for PDF ===============================================
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer,PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from io import BytesIO
import json

class pdfgenerator:
    # Existing code remains the same
    
    def add_table(self, data):
        # Define the table data
        summaries = data.get("summaries", [])
        if not summaries:
            summaries = ["No data available"]  # Handle empty summaries gracefully

        table_data = [
            [Paragraph(f"<b>{summaries[0]}</b>", self.style_sheet['BodyText']), '', ''],  # Example row with centered header
            ['Row 2 Column 1', 'Row 2 Column 2', 'Row 2 Column 3'],
            ['Row 3 Column 1', 'Row 3 Column 2', 'Row 3 Column 3'],
        ]

        # Define table styles
        style = TableStyle([
            ('LINEBELOW', (0, 0), (-1, 0), 1, black),  # Line below the first row
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Middle align vertically
            ('FONTSIZE', (0, 0), (-1, -1), 10),  # Set font size
            ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Border around the table
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Grid lines
        ])

        # Calculate column widths dynamically
        left_margin = 72
        right_margin = 72
        available_width = self.pdf.pagesize[0] - left_margin - right_margin
        column_widths = [available_width / 3] * 3  # Divide width into 3 equal parts

        # Create the table
        table = Table(table_data, colWidths=column_widths)
        table.setStyle(style)

        # Add the table to elements
        self.elements.append(table)
        self.elements.append(Spacer(1, 12))
