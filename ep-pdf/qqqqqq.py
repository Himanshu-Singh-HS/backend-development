import fitz  # PyMuPDF
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.units import inch
from io import BytesIO
import json
import requests

def json_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

data = json_data("./eP-pdf/ep.json")

class PDFGenerator:
    def __init__(self):
        self.pdf_file_path = "ep-pdf.pdf"
        self.pdf = SimpleDocTemplate(self.pdf_file_path, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=40)
        self.elements = []
        self.style_sheet = getSampleStyleSheet()

        # Define styles
        self.heading2_style = ParagraphStyle(
            'Heading2',
            parent=self.style_sheet['Heading2'],
            fontSize=12,
            fontName='Times-Bold',
        )
        self.title_style = ParagraphStyle(
            'Heading2',
            parent=self.style_sheet['Heading2'],
            fontSize=12,
            fontName='Times-Bold',
            alignment=TA_CENTER
        )

    def add_justified_paragraph_with_numbering(self, text, first_Line_Indent=0):
        modified_style = ParagraphStyle(
            'Justified',
            parent=self.style_sheet['BodyText'],
            fontName='Times-Roman',
            fontSize=12,
            leading=20,
            alignment=TA_JUSTIFY,
            firstLineIndent=first_Line_Indent
        )
        self.elements.append(Paragraph(text, modified_style))
        self.elements.append(Spacer(1, 12))

    def download_image(self, img_url):
        """Downloads an image from a URL and returns it as a BytesIO object."""
        try:
            response = requests.get(img_url)
            if response.status_code == 200:
                return BytesIO(response.content)
            else:
                print(f"Failed to download the image from {img_url}")
        except Exception as e:
            print(f"Error downloading image: {e}")
        return None

    def convert_json_to_pdf_buffer(self, Data: dict) -> BytesIO:
        # Add title
        title_text = Data['title']['text'].upper()
        self.elements.append(Paragraph(title_text, self.title_style))
        self.elements.append(Spacer(1, 12))

        # Add various sections (technical field, background, etc.) as you did before
        # This section will be similar to your existing method without changes

        # Build PDF
        self.pdf.build(self.elements)

        # Add line numbers after PDF creation
        self.add_line_numbers()

    def add_line_numbers(self):
        """Add line numbers to the generated PDF using PyMuPDF."""
        # Open the existing PDF in update mode
        pdf_document = fitz.open(self.pdf_file_path)

        # Loop through each page
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            print(f"--- Page {page_num + 1} ---")

            # Get text as a dictionary to retrieve details about each line
            text_dict = page.get_text("dict")

            # Initialize the line index for the current page
            line_index = 1

            # Loop through each block of text
            for block in text_dict['blocks']:
                if block['type'] == 0:  # Ensure it's a text block
                    for line in block['lines']:
                        # Loop through each span (segment) in the line
                        for span in line['spans']:
                            # Calculate the y position for the line number
                            bbox = span['bbox']
                            y_position = bbox[1]  # Use the top of the bounding box for positioning
                            x_offset = bbox[0] - 30  # Positioning to the left of the text

                            # Insert the line number at the calculated position
                            page.insert_text((x_offset, y_position), f"{line_index}: ", fontsize=10, color=(0, 0, 0))

                        line_index += 1  # Increment line index after each line

        # # Save the modified PDF
        pdf_document.save(self.pdf_file_path.replace('.pdf', '-numberedqqq.pdf'))
        pdf_document.close()

# Usage
pdf = PDFGenerator()
pdf.convert_json_to_pdf_buffer(data)
