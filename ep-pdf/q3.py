# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
# from reportlab.pdfbase import pdfmetrics
# from reportlab.lib.units import inch
# import json

# def json_data(filename):
#     with open(filename, 'r') as file:
#         return json.load(file)

# data = json_data("./eP-pdf/ep.json")

# class pdfgenerator:
#     def __init__(self):
#         self.pdf = SimpleDocTemplate("ep_ans1.pdf", pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=40)
#         self.elements = []
#         self.style_sheet = getSampleStyleSheet()
        
#         # Define styles for title, headings, content, and numbering
#         self.heading2_style = ParagraphStyle(
#             'Heading2',
#             parent=self.style_sheet['Heading2'],
#             fontSize=12,
#             fontName='Times-Bold',
#             leftIndent=27,  
#         )
#         self.title_style = ParagraphStyle(
#             'Title',
#             parent=self.style_sheet['Heading2'],
#             fontSize=12,
#             fontName='Times-Bold',
#             alignment=TA_CENTER,
#             leftIndent=27,  
#         )
#         self.text_style = ParagraphStyle(
#             'Justified',
#             parent=self.style_sheet['BodyText'],
#             fontName='Times-Roman',
#             fontSize=12,
#             leading=20,
#             alignment=TA_JUSTIFY,
#         )
#         self.numbering_style = ParagraphStyle(
#             'Numbering',
#             fontName='Times-Roman',
#             fontSize=12,
#             leading=20,
#             alignment=TA_CENTER,
#         )

#     def get_line_width(self, text, font_name, font_size):
#         """Calculate the width of a string based on font settings."""
#         return pdfmetrics.stringWidth(text, font_name, font_size)

#     def wrap_text_with_numbering(self, text, max_width):
#         words = text.split()
#         line = ""
#         line_count = 1  # Start counting lines from 1

#         for word in words:
#             new_line = f"{line} {word}".strip()

#             # Check if the new line fits within the content width
#             if self.get_line_width(new_line, self.text_style.fontName, self.text_style.fontSize) < max_width:
#                 line = new_line  # Add the word to the current line
#             else:
#                 # Add the numbered line as a row in a table without breaking words
#                 row = [
#                     Paragraph(f"{line_count}.", self.numbering_style),  # Numbering on the left
#                     Paragraph(line, self.text_style)  # Fully justified text content
#                 ]
#                 table = Table([row], colWidths=[0.4 * inch, max_width])
#                 table.setStyle(TableStyle([
#                     ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
#                     ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#                     ('LEFTPADDING', (1, 0), (1, -1), 10),
#                 ]))
#                 self.elements.append(table)
#                 self.elements.append(Spacer(1, 4))  # Add space between lines

#                 line_count += 1
#                 line = word  # Start a new line with the current word

#         # Add any remaining text in the last line
#         if line:
#             row = [
#                     Paragraph(f"{line_count}.", self.numbering_style),
#                     Paragraph(line, self.text_style)
#             ]
#             table = Table([row], colWidths=[0.4 * inch, max_width])
#             table.setStyle(TableStyle([
#                 ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
#                 ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#                 ('LEFTPADDING', (1, 0), (1, -1), 10),
#             ]))
#             self.elements.append(table)

#     def convert_json_to_pdf_buffer(self, Data: dict):
#         # Add title
#         title_text = Data.get('title', {}).get('text', '').upper()
#         if title_text:
#             self.elements.append(Paragraph(title_text, self.title_style))
#             self.elements.append(Spacer(1, 12))

#         # Technical field text with numbering
#         technical_field_text = Data.get("technical_field", {}).get("text", "")
#         if technical_field_text:
#             self.elements.append(Paragraph("Technical Field", self.heading2_style))
#             self.wrap_text_with_numbering(technical_field_text, max_width=450)

#         # Background text
#         background_text = Data.get("background", {}).get("text", "")
#         if background_text:
#             self.elements.append(Paragraph("Background Art", self.heading2_style))
#             sections = background_text.split('\n\n')
#             for section in sections:
#                 self.wrap_text_with_numbering(section, max_width=450)

#         # Generate the PDF
#         self.pdf.build(self.elements)

# # Initialize and create the PDF
# pdf = pdfgenerator()
# pdf.convert_json_to_pdf_buffer(data)
# print("PDF generation completed successfully.")



from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch
from reportlab.platypus.flowables import PageBreak
from io import BytesIO
import json

def json_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

data = json_data("./eP-pdf/ep.json")

class pdfgenerator:
    def __init__(self):
        self.pdf = SimpleDocTemplate("ep_ans1.pdf", pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=40)
        self.elements = []
        self.style_sheet = getSampleStyleSheet()
        
        # Define styles for title, headings, content, and numbering
        self.heading2_style = ParagraphStyle(
            'Heading2',
            parent=self.style_sheet['Heading2'],
            fontSize=12,
            fontName='Times-Bold',
            leftIndent=27,  
        )
        self.title_style = ParagraphStyle(
            'Title',
            parent=self.style_sheet['Heading2'],
            fontSize=12,
            fontName='Times-Bold',
            alignment=TA_CENTER,
            leftIndent=27,  
        )
        self.text_style = ParagraphStyle(
            'Justified',
            parent=self.style_sheet['BodyText'],
            fontName='Times-Roman',
            fontSize=12,
            leading=20,
            alignment=TA_JUSTIFY,
        )
        self.numbering_style = ParagraphStyle(
            'Numbering',
            fontName='Times-Roman',
            fontSize=12,
            leading=20,
            alignment=TA_CENTER,
        )
        self.line_count = 1  # Initialize line count for page

    def get_line_width(self, text, font_name, font_size):
        """Calculate the width of a string based on font settings."""
        return pdfmetrics.stringWidth(text, font_name, font_size)

    def add_numbered_paragraph(self, text):
        """Adds a numbered paragraph and resets numbering on each new page."""
        words = text.split()
        line = ""

        max_width = 470  # Set maximum width for the content column
        for word in words:
            new_line = f"{line} {word}".strip()

            # Check if the new line fits within the content width
            if self.get_line_width(new_line, self.text_style.fontName, self.text_style.fontSize) < max_width:
                line = new_line  # If it fits, continue building the line
            else:
                # If it doesn't fit, add the current line with numbering to the elements
                if line:
                    # Add a row with numbering in the first column and the text in the second column
                    row = [
                        Paragraph(f"{self.line_count}.", self.numbering_style),  # Numbering on the left
                        Paragraph(line, self.text_style)  # Justified text on the right
                    ]
                    table = Table([row], colWidths=[0.4 * inch, max_width])
                    table.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('LEFTPADDING', (1, 0), (1, -1), 10),
                    ]))
                    self.elements.append(table)
                    self.line_count += 1  # Increment line number
                line = word  # Start a new line with the current word

        # Add any remaining text in the last line
        if line:
            row = [
                Paragraph(f"{self.line_count}.", self.numbering_style),
                Paragraph(line, self.text_style)
            ]
            table = Table([row], colWidths=[0.4 * inch, max_width])
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (1, 0), (1, -1), 10),
            ]))
            self.elements.append(table)

    def on_new_page(self, canvas, doc):
        """Reset numbering on each new page."""
        self.line_count = 1  # Reset line count for the new page

    def convert_json_to_pdf_buffer(self, Data: dict):
        # Set up the on-page function to reset numbering
        self.pdf.build(self.elements, onFirstPage=self.on_new_page, onLaterPages=self.on_new_page)

        # Add title
        title_text = Data.get('title', {}).get('text', '').upper()
        if title_text:
            self.elements.append(Paragraph(title_text, self.title_style))
            self.elements.append(Spacer(1, 12))

        # Technical field text with numbering
        technical_field_text = Data.get("technical_field", {}).get("text", "")
        if technical_field_text:
            self.elements.append(Paragraph("Technical Field", self.heading2_style))
            self.add_numbered_paragraph(technical_field_text)

        # Background text
        background_text = Data.get("background", {}).get("text", "")
        if background_text:
            self.elements.append(Paragraph("Background Art", self.heading2_style))
            sections = background_text.split('\n\n')
            for section in sections:
                self.add_numbered_paragraph(section)

        # Generate the PDF
        self.pdf.build(self.elements, onFirstPage=self.on_new_page, onLaterPages=self.on_new_page)

# Initialize and create the PDF
pdf = pdfgenerator()
pdf.convert_json_to_pdf_buffer(data)
print("PDF generation completed successfully.")
