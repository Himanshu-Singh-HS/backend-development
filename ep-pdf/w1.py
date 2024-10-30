# Importing third-party modules for PDF ===============================================
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer,PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from io import BytesIO
import json

def json_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

data = json_data("./eP-pdf/ep.json")

class pdfgenerator:
    def __init__(self):
        self.pdf = SimpleDocTemplate("ep_ans.pdf", pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=40)
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
        self.total_lines = 0  # Counter to keep track of total lines
        self.lines_per_page = self.calculate_max_lines_per_page()  # Calculate max lines per page
        self.lines_on_current_page = 0  # Track lines on the current page

    def calculate_max_lines_per_page(self):
        """Calculate the maximum number of lines that can fit on a page."""
        page_height = letter[1] - 112  # Page height minus top and bottom margins
        line_height = 20  # Line height (adjust based on your style settings)
        return int(page_height // line_height)

    def estimate_paragraph_lines(self, text, style):
        # Estimate the number of lines for the paragraph by dividing its height by line height
        line_height = style.leading
        width, height = letter[0] - 144, letter[1] - 112  # Page size minus margins (left+right and top+bottom)
        
        # Create a temporary Paragraph to measure text height
        para = Paragraph(text, style)
        text_height = para.wrap(width, height)[1]  # Get the height the text will occupy
        
        num_lines = text_height // line_height  # Estimate number of lines
        print(f"Estimating lines for text: '{text[:50]}...' - Estimated Height: {text_height}, Line Height: {line_height}, Estimated Lines: {num_lines}")
        return int(num_lines)

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
        
        # Estimate the number of lines for the added paragraph
        lines = self.estimate_paragraph_lines(text, modified_style)
        self.total_lines += lines
        self.lines_on_current_page += lines
        
        print(f"Added {lines} lines for paragraph: '{text[:50]}...'")  # Print number of lines added
        
        # Check if the current page has exceeded the maximum lines
        if self.lines_on_current_page >= self.lines_per_page:
            print(f"Page limit reached: {self.lines_on_current_page} lines on this page.")
            self.print_page_summary()  # Print the summary for the current page
            self.lines_on_current_page = 0  # Reset for the next page

    def print_page_summary(self):
        """Print the summary of lines for the current page."""
        print(f"Total lines on this page: {self.lines_on_current_page}")
        print()
        print()

    def convert_json_to_pdf_buffer(self, Data: dict) -> BytesIO:
        # Add title
        title_text = Data['title']['text'].upper()
        print(f"Processing title: '{title_text}'")
        self.elements.append(Paragraph(title_text, self.title_style))
        self.elements.append(Spacer(1, 12))  
        # No line counting for title
        print(f"Title '{title_text}' added (not counted).")
        
        # Technical field text with numbering
        technical_field_heading = "Technical field"
        print(f"Processing heading: '{technical_field_heading}'")
        self.elements.append(Paragraph(technical_field_heading, self.heading2_style))
        # No line counting for headings
        print(f"Heading '{technical_field_heading}' added (not counted).")
        
        self.add_justified_paragraph_with_numbering(Data["technical_field"]["text"])
        
        background_heading = "Background Art"
        print(f"Processing heading: '{background_heading}'")
        self.elements.append(Paragraph(background_heading, self.heading2_style))
        # No line counting for headings
        print(f"Heading '{background_heading}' added (not counted).")
        
        # Background text
        background_text = Data["background"]["text"]
        sections = background_text.split('\n\n')
        for section in sections:
            print(f"Processing background section: '{section[:50]}...'")
            self.add_justified_paragraph_with_numbering(section)
        
        # Brief summary text
        self.elements.append(Paragraph("Summary of the invention", self.heading2_style))
        self.elements.append(Spacer(1, 12))
        summary_text = Data["summary"]["text"]
        sections = summary_text.split('\n\n')
        for section in sections:
            counter = self.add_justified_paragraph_with_numbering(section)
            
        #FIGIURES LIST
        self.elements.append(Paragraph("Brief description of the drawings",self.heading2_style))
        self.elements.append(Spacer(1, 12))
        figure_list=Data["list_of_figures"]
        for figure in figure_list:
            counter=self.add_justified_paragraph_with_numbering(figure)
        
        #Detailed Description   
        self.elements.append(Paragraph("Detailed description",self.heading2_style))
        self.elements.append(Spacer(1,12))
        # Method description
        method_desc_text = Data["description"]["method_desc"]["text"]
        method_desc_sections = method_desc_text.split('\n\n')
        for section in method_desc_sections:
            counter =  self.add_justified_paragraph_with_numbering(section)

        # System description
        system_desc_text_list = Data["description"]["system_desc"]["text_list"]
        for section in system_desc_text_list:
            counter = self.add_justified_paragraph_with_numbering(section)

        # Invention Description
        invention_desc_text = Data["description"]["invention_desc"]["text"]
        invention_desc_sections = invention_desc_text.split('\n\n')
        for section in invention_desc_sections:
            counter =  self.add_justified_paragraph_with_numbering(section)
        
        claims_style = ParagraphStyle(
        'Claims',
        parent=self.style_sheet['BodyText'],
        fontName='Times-Roman',
        fontSize=12,
        leading=20,
        alignment=TA_JUSTIFY,
    )   
        
        # Claims section
        self.elements.append(PageBreak())
        self.elements.append(Paragraph("Claims", self.heading2_style))
        self.elements.append(Spacer(1, 12))
        for index, claim in enumerate(Data['claims'], start=1):
            claim_text = f"{index}. {claim['text']}"
            claim_text = f"{index}.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{claim['text']}"
            claim_parts = claim_text.split("\n")
            for part in claim_parts:
                self.elements.append(Paragraph(part,claims_style))

        # Abstract section
        self.elements.append(PageBreak())
        self.elements.append(Paragraph("Abstract", self.heading2_style))
        self.elements.append(Spacer(1, 12))
        abstract_text = Data["abstract"]["text"]
        abstract_sections = abstract_text.split('\n\n')
        for section in abstract_sections:
            counter =  self.add_justified_paragraph_with_numbering(section)      
        self.pdf.build(self.elements)
        
        # Final page summary if there are remaining lines
        if self.lines_on_current_page > 0:
            print(f"Total lines on the last page: {self.lines_on_current_page}")
        
        print(f"Total number of lines in the document (excluding title and headings): {self.total_lines}")

pdf = pdfgenerator()
pdf.convert_json_to_pdf_buffer(data)
