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
        

pdf = pdfgenerator()
pdf.convert_json_to_pdf_buffer(data)
