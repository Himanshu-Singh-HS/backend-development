# Importing third-party modules for PDF ===============================================
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
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
        self.total_lines = 0  
        self.lines_per_page = self.calculate_max_lines_per_page()  
        self.lines_on_current_page = 0   
        print(f"total line in page { self.lines_per_page}")

    def calculate_max_lines_per_page(self):
        """Calculate the maximum number of lines that can fit on a page."""
        page_height = letter[1] - 112   
        line_height = 20   
        return int(page_height // line_height)
    

    def estimate_paragraph_lines(self, text, style):
        # Estimate the number of lines for the paragraph by dividing its height by line height
        line_height = style.leading
        width, height = letter[0] - 144, letter[1] - 112  # Page size minus margins (left+right and top+bottom)
        
        # Create a temporary Paragraph to measure text height
        para = Paragraph(text, style)
        text_height = para.wrap(width, height)[1]  # Get the height the text will occupy 
        
        #i want to check here so that we can findout exact lines ,check line by line function so that accurate get result rather than whole text 
        # if self.check_total_lines_on_currentpage()
        num_lines = text_height // line_height  # Estimate number of lines
        print(f"Estimating lines for text: '{text[:50]}...' - Estimated Height: {text_height}, Line Height: {line_height}, Estimated Lines: {num_lines}")
        print()
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
        
        print(f"Added {lines} lines for paragraph: '{text[:50]}...'")   
        # Check if the current page has exceeded the maximum lines
        self.check_total_lines_on_currentpage()
    
    def check_total_lines_on_currentpage(self):
        if self.lines_on_current_page >= self.lines_per_page:
            print(f"Page limit reached: {self.lines_on_current_page} lines on this page.")
            print(f"Total lines on this page: {self.lines_on_current_page}")
            self.elements.append(Paragraph(str(self.lines_on_current_page)))
            self.lines_on_current_page = 0  
    
  

    def convert_json_to_pdf_buffer(self, Data: dict) -> BytesIO:
        # Add title
        title_text = Data['title']['text'].upper()
        print(f"Processing title: '{title_text}'")
        self.elements.append(Paragraph(title_text, self.title_style))
        self.elements.append(Spacer(1, 12))  
        lines=self.estimate_paragraph_lines(title_text,self.title_style)
        self.total_lines += lines
        self.lines_on_current_page+=lines
        
        # Technical field text with numbering
        technical_field_heading = "Technical field"
        print(f"Processing heading: '{technical_field_heading}'")
        lines=self.estimate_paragraph_lines(technical_field_heading,self.heading2_style)
        self.total_lines += lines
        self.lines_on_current_page+=lines
        self.elements.append(Paragraph(technical_field_heading, self.heading2_style))
        self.add_justified_paragraph_with_numbering(Data["technical_field"]["text"])
        
        background_heading = "Background Art"
        print(f"Processing heading: '{background_heading}'")
      
        lines=self.estimate_paragraph_lines(background_heading,self.heading2_style)
        self.total_lines += lines
        self.lines_on_current_page+=lines
        self.elements.append(Paragraph(background_heading, self.heading2_style))
        
        # Background text
        background_text = Data["background"]["text"]
        sections = background_text.split('\n\n')
        for section in sections:
            print(f"Processing background section: '{section[:50]}...'")
            self.add_justified_paragraph_with_numbering(section)
                
        self.pdf.build(self.elements)
        
        # Final page summary if there are remaining lines
        if self.lines_on_current_page > 0:
            print(f"Total lines on the last page: {self.lines_on_current_page}")
        
        print(f"Total number of lines in the document (including all  title and headings everything ): {self.total_lines}")

pdf = pdfgenerator()
pdf.convert_json_to_pdf_buffer(data)
