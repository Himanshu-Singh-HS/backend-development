from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.pdfbase import pdfmetrics  # Add this import
from io import BytesIO
import json

# Load JSON data
def json_data(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON data: {e}")
        return {}

# Load your JSON data
data = json_data("./eP-pdf/ep.json")
if not data:
    print("No data loaded from JSON.")
else:
    print("Data loaded successfully.")

class pdfgenerator:
    def __init__(self):
        self.pdf = SimpleDocTemplate("ep_ans1.pdf", pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=40)
        self.elements = []
        self.style_sheet = getSampleStyleSheet()
        self.heading2_style = ParagraphStyle(
            'Heading2',
            parent=self.style_sheet['Heading2'],
            fontSize=12,
            fontName='Times-Bold',
        )
        self.title_style = ParagraphStyle(
            'Title',
            parent=self.style_sheet['Heading2'],
            fontSize=12,
            fontName='Times-Bold',
            alignment=TA_CENTER
        )
        self.total_lines = 0

    def get_line_width(self, text, font_name, font_size):
        """Calculate the width of a string based on font settings."""
        ans=pdfmetrics.stringWidth(text, font_name, font_size)
        print("this is the line width-> ",ans)
        return ans

    # def add_justified_paragraph_with_numbering(self, text):
    #     words = text.split()  # Split the text into words
    #     line = ""
    #     line_count = 1  # Start counting lines from 1
        
    #     modified_style = ParagraphStyle(
    #         'Justified',
    #         parent=self.style_sheet['BodyText'],
    #         fontName='Times-Roman',
    #         fontSize=12,
    #         leading=20,
    #         alignment=TA_JUSTIFY,
    #     )
        
    #     max_width = self.pdf.width - self.pdf.leftMargin - self.pdf.rightMargin  # Calculate maximum width

    #     for word in words:
    #         # Construct line with the new word
    #         new_line = f"{line} {word}".strip()
    #         # Check if the new line fits in the paragraph
    #         if self.get_line_width(new_line, modified_style.fontName, modified_style.fontSize) < max_width:
    #             line = new_line  # If it fits, use the new line
    #         else:
    #             # If it doesn't fit, number the current line and add it to the elements
    #             if line:
    #                 self.elements.append(Paragraph(f"{line_count}. {line}", modified_style))
    #                 self.elements.append(Spacer(1, 12))
    #                 line_count += 1  # Increment line number
    #             line = word  # Start a new line with the current word
        
    #     # Add the last line if it exists
    #     if line:
    #         self.elements.append(Paragraph(f"{line_count}. {line}", modified_style))
    #         self.elements.append(Spacer(1, 12))

    #     self.total_lines += line_count  # Update total lines
    def add_justified_paragraph_with_numbering(self, text):
        words = text.split()  # Split the text into words
        line = ""
        line_count = 1  # Start counting lines from 1
        
        modified_style = ParagraphStyle(
            'Justified',
            parent=self.style_sheet['BodyText'],
            fontName='Times-Roman',
            fontSize=12,
            leading=20,
            alignment=TA_JUSTIFY,  # Ensure text is justified
        )
        
        max_width = self.pdf.width - self.pdf.leftMargin - self.pdf.rightMargin  # Calculate maximum width
        max_width=445
        for word in words:
            # Construct line with the new word
            new_line = f"{line} {word}".strip()
            # Check if the new line fits in the paragraph
            if self.get_line_width(new_line, modified_style.fontName, modified_style.fontSize) < max_width:
                line = new_line  # If it fits, use the new line
            else:
                # If it doesn't fit, number the current line and add it to the elements
                if line:
                    # Create a paragraph that is justified
                    self.elements.append(Paragraph(f"{line_count}. {line}", modified_style))
                  
                    line_count += 1  # Increment line number
                # Start a new line with the current word
                line = word
        
        # Add the last line if it exists
        if line:
            self.elements.append(Paragraph(f"{line_count}. {line}", modified_style))
            self.elements.append(Spacer(1, 12))

        self.total_lines += line_count  # Update total lines

    def convert_json_to_pdf_buffer(self, Data: dict) -> BytesIO:
        # Add title
        title_text = Data.get('title', {}).get('text', '').upper()
        if title_text:
            self.elements.append(Paragraph(title_text, self.title_style))
            self.elements.append(Spacer(1, 12))
            self.total_lines += 1  # Assuming the title takes 1 line
            print(f"Added title: {title_text}")
        else:
            print("No title found in JSON data.")

        # Technical field text with numbering
        technical_field_text = Data.get("technical_field", {}).get("text", "")
        if technical_field_text:
            self.elements.append(Paragraph("Technical field", self.heading2_style))
            self.total_lines += 1  # Heading line
            self.add_justified_paragraph_with_numbering(technical_field_text)
        else:
            print("No technical field text found in JSON data.")

        # Background text
        background_text = Data.get("background", {}).get("text", "")
        if background_text:
            self.elements.append(Paragraph("Background Art", self.heading2_style))
            self.total_lines += 1  # Heading line
            sections = background_text.split('\n\n')  # Split into sections
            for section in sections:
                self.add_justified_paragraph_with_numbering(section)
        else:
            print("No background text found in JSON data.")

        # Generate the PDF
        self.pdf.build(self.elements)
        print(f"Total number of lines in the document: {self.total_lines}")

# Initialize and create the PDF
pdf = pdfgenerator()
pdf.convert_json_to_pdf_buffer(data)
print("PDF generation completed successfully.")
