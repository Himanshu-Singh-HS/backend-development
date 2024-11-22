from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

def create_pdf_with_table(file_path):
   
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    
    # Define table data
    data = [
        ['Header 1', 'Header 2', 'Header 3'],
        ['Row 1 Col 1', 'Row 1 Col 2', 'Row 1 Col 3'],
        ['Row 2 Col 1', 'Row 2 Col 2', 'Row 2 Col 3'],
        ['Row 3 Col 1', 'Row 3 Col 2', 'Row 3 Col 3'],
    ]

    # Create Table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header row text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),         # Center align all text
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), # Header font bold
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),         # Header padding
        ('GRID', (0, 0), (-1, -1), 1, colors.black),    # Table grid
    ]))

    # Determine the table's position on the page
    table_width, table_height = table.wrap(0, 0)
    x = (width - table_width) / 2  # Center horizontally
    y = height - 200              # Position below the top margin
    
    # Draw the table on the canvas
    table.drawOn(c, x, y)

    # Save the canvas
    c.save()

# Generate the PDF
create_pdf_with_table("table_with_4_rows.pdf") 
