import pdfplumber
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfWriter, PdfReader

def add_line_numbers_to_pdf(input_pdf_path, output_pdf_path):
    # Create a temporary PDF to hold the line numbers
    temp_pdf_path = "temp_with_line_numbers.pdf"
    c = canvas.Canvas(temp_pdf_path, pagesize=letter)
    
    # Open the input PDF
    with pdfplumber.open(input_pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                # Split text into lines and process
                lines = text.splitlines()
                line_number = 1
                
                for line in lines:
                    # Consider only truthy lines
                    if line.strip():  # Check if line is not empty
                        # Draw line number and text on the temporary PDF
                        # Note: This assumes the original page has some consistent line height.
                        c.drawString(10, 750 - 20 * line_number, f"{line_number}: {line.strip()}")
                        line_number += 1
            
            # Finish the current page
            c.showPage()
    
    c.save()