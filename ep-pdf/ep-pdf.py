
# importing third-party modules  for pdf ===============================================
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak,Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER
from reportlab.lib.units import inch
from io import BytesIO
import json,requests

def json_data(filename):
    with open (filename,'r') as file:
        return json.load(file)
data=json_data("./eP-pdf/ep.json")
 

class PDFGenerator:
    def __init__(self):

        self.pdf = SimpleDocTemplate("ep-pdf.pdf", pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=40)
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
    # Function to add justified paragraphs with numbering
    def add_justified_paragraph_with_numbering(self,text,first_Line_Indent=0):
        
        modified_style = ParagraphStyle(
        'Justified',
        parent=self.style_sheet['BodyText'],
        fontName='Times-Roman',
        fontSize=12,
        leading=20,
        alignment=TA_JUSTIFY,
        firstLineIndent=first_Line_Indent)                                  
        self.elements.append(Paragraph(text, modified_style))
        self.elements.append(Spacer(1, 12))  
       
        
    def download_image(self,img_url):
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
    
    def add_page_number(self,canvas, doc,):
        """This method is called to add the page numberto each page."""
        page_num = canvas.getPageNumber()
        text = f"{page_num}"
        # Add the page number  
        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
        canvas.drawCentredString(4.25 * inch, 10.5 * inch, text)
        canvas.restoreState()
        
    # Add page numbering and handle line numbering
    def add_page_number_and_line_count(self, canvas, doc, start_line=1):
        """This method adds the page number and draws the line numbers in sets of five on the left side."""
        page_num = canvas.getPageNumber()
        text = f" {page_num}"
        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
        canvas.drawCentredString(4.25 * inch, 10.5 * inch, text)

       
        y_position = 10.2 * inch   
        line_height = 14  
        for i in range(1, 45):  
            if (start_line + i - 1) % 5 == 0:   
                canvas.drawString(50, y_position, str(start_line + i - 1))
            y_position -= line_height

        canvas.restoreState()
         
 
        
    def convert_json_to_pdf_buffer(self,Data: dict)-> BytesIO:
      
        # Add title
        title_text = Data['title']['text'].upper()
        self.elements.append(Paragraph(title_text,self.title_style))
        self.elements.append(Spacer(1, 12)) 
            
        # Technical field text with numbering
        self.elements.append(Paragraph("Technical field", self.heading2_style))

        counter = self.add_justified_paragraph_with_numbering(Data["technical_field"]["text"])
        self.elements.append(Paragraph("Background Art", self.heading2_style))
        # Background text
        background_text = Data["background"]["text"]
        sections = background_text.split('\n\n')
        for section in sections:
            counter = self.add_justified_paragraph_with_numbering(section)

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
            
        #image section
        self.elements.append(PageBreak())
        self.elements.append(Paragraph("Figures", self.heading2_style))
        sorted_claims = sorted(Data["claims"], key=lambda x: x.get("claim_type") == "system")
        for claim in sorted_claims:
            if claim.get("generated_figures_data") and claim["generated_figures_data"].get("latex_details"):
                for latex_detail in claim["generated_figures_data"]["latex_details"]:
                    if "images_urls" in latex_detail:
                        for img_url in latex_detail["images_urls"]:
                            print("**************generating pdf*********")
                            img_stream = self.download_image(img_url)
                            if img_stream:
                                img = Image(img_stream)
                                img_width = img.drawWidth
                                img_height = img.drawHeight 
                                max_width = 5 * inch   
                                max_height = 5 * inch  
                                scale_factor = min(max_width / img_width, max_height / img_height)
                                if scale_factor < 1:
                                    img.drawWidth = img_width * scale_factor
                                    img.drawHeight = img_height * scale_factor
                                self.elements.append(img) 
                            else:
                                print(f"Could not download image from {img_url}")
        self.pdf.build(self.elements, onFirstPage=self.add_page_number, onLaterPages=self.add_page_number)
        # self.pdf.build(self.elements, onFirstPage=self.add_page_number_and_line_count, onLaterPages=self.add_page_number_and_line_count)
        
pdf=PDFGenerator()
pdf.convert_json_to_pdf_buffer(data)


      

  

# # importing third-party modules  for pdf ===============================================
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak,Image
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER
# from reportlab.lib.units import inch
# from io import BytesIO
# import json,requests

# def json_data(filename):
#     with open (filename,'r') as file:
#         return json.load(file)
# data=json_data("./eP-pdf/ep.json")
 

# class PDFGenerator:
#     def __init__(self):

#         self.pdf = SimpleDocTemplate("ep-pdf.pdf", pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=40)
#         self.elements = []
#         self.style_sheet = getSampleStyleSheet()        
#         # Define styles      
#         self.heading2_style = ParagraphStyle(
#             'Heading2',
#             parent=self.style_sheet['Heading2'],
#             fontSize=12,    
#             fontName='Times-Bold',       
#         )
#         self.title_style = ParagraphStyle(
#             'Heading2',
#             parent=self.style_sheet['Heading2'],
#             fontSize=12,    
#             fontName='Times-Bold', 
#             alignment=TA_CENTER      
#         ) 
#     def estimate_paragraph_lines(self, text, style):
#         line_height = style.leading
#         width, height = letter[0] - 144, letter[1] - 112  # Page size minus margins (left+right and top+bottom)
        
#         # Create a temporary Paragraph to measure text height
#         para = Paragraph(text, style)
#         text_height = para.wrap(width, height)[1]  # Get the height the text will occupy
        
#         num_lines = text_height // line_height  # Estimate number of lines
#         print(f"Estimating lines for text: '{text[:50]}...' - Estimated Height: {text_height}, Line Height: {line_height}, Estimated Lines: {num_lines}")
#         return int(num_lines)
#     # Function to add justified paragraphs with numbering
#     def add_justified_paragraph_with_numbering(self,text,first_Line_Indent=0):
        
#         modified_style = ParagraphStyle(
#         'Justified',
#         parent=self.style_sheet['BodyText'],
#         fontName='Times-Roman',
#         fontSize=12,
#         leading=20,
#         alignment=TA_JUSTIFY,
#         firstLineIndent=first_Line_Indent)                                  
#         self.elements.append(Paragraph(text, modified_style))
#         self.elements.append(Spacer(1, 12))  
       
        
#     def download_image(self,img_url):
#         """Downloads an image from a URL and returns it as a BytesIO object."""
#         try:
#             response = requests.get(img_url)
#             if response.status_code == 200:
#                 return BytesIO(response.content)
#             else:
#                 print(f"Failed to download the image from {img_url}")
#         except Exception as e:
#             print(f"Error downloading image: {e}")
#         return None
 
        
#     def convert_json_to_pdf_buffer(self,Data: dict)-> BytesIO:
      
#         # Add title
#         title_text = Data['title']['text'].upper()
#         self.elements.append(Paragraph(title_text,self.title_style))
#         self.elements.append(Spacer(1, 12)) 
            
#         # Technical field text with numbering
#         self.elements.append(Paragraph("Technical field", self.heading2_style))

#         counter = self.add_justified_paragraph_with_numbering(Data["technical_field"]["text"])
#         self.elements.append(Paragraph("Background Art", self.heading2_style))
#         # Background text
#         background_text = Data["background"]["text"]
#         sections = background_text.split('\n\n')
#         for section in sections:
#             counter = self.add_justified_paragraph_with_numbering(section)

#         # Brief summary text
#         self.elements.append(Paragraph("Summary of the invention", self.heading2_style))
#         self.elements.append(Spacer(1, 12))
#         summary_text = Data["summary"]["text"]
#         sections = summary_text.split('\n\n')
#         for section in sections:
#             counter = self.add_justified_paragraph_with_numbering(section)
            
#         #FIGIURES LIST
#         self.elements.append(Paragraph("Brief description of the drawings",self.heading2_style))
#         self.elements.append(Spacer(1, 12))
#         figure_list=Data["list_of_figures"]
#         for figure in figure_list:
#             counter=self.add_justified_paragraph_with_numbering(figure)
        
#         #Detailed Description   
#         self.elements.append(Paragraph("Detailed description",self.heading2_style))
#         self.elements.append(Spacer(1,12))
#         # Method description
#         method_desc_text = Data["description"]["method_desc"]["text"]
#         method_desc_sections = method_desc_text.split('\n\n')
#         for section in method_desc_sections:
#             counter =  self.add_justified_paragraph_with_numbering(section)

#         # System description
#         system_desc_text_list = Data["description"]["system_desc"]["text_list"]
#         for section in system_desc_text_list:
#             counter = self.add_justified_paragraph_with_numbering(section)

#         # Invention Description
#         invention_desc_text = Data["description"]["invention_desc"]["text"]
#         invention_desc_sections = invention_desc_text.split('\n\n')
#         for section in invention_desc_sections:
#             counter =  self.add_justified_paragraph_with_numbering(section)
        
#         claims_style = ParagraphStyle(
#         'Claims',
#         parent=self.style_sheet['BodyText'],
#         fontName='Times-Roman',
#         fontSize=12,
#         leading=20,
#         alignment=TA_JUSTIFY,
#     )   
        
#         # Claims section
#         self.elements.append(PageBreak())
#         self.elements.append(Paragraph("Claims", self.heading2_style))
#         self.elements.append(Spacer(1, 12))
#         for index, claim in enumerate(Data['claims'], start=1):
#             claim_text = f"{index}. {claim['text']}"
#             claim_text = f"{index}.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{claim['text']}"
#             claim_parts = claim_text.split("\n")
#             for part in claim_parts:
#                 self.elements.append(Paragraph(part,claims_style))

#         # Abstract section
#         self.elements.append(PageBreak())
#         self.elements.append(Paragraph("Abstract", self.heading2_style))
#         self.elements.append(Spacer(1, 12))
#         abstract_text = Data["abstract"]["text"]
#         abstract_sections = abstract_text.split('\n\n')
#         for section in abstract_sections:
#             counter =  self.add_justified_paragraph_with_numbering(section)
            
#         #image section
#         self.elements.append(PageBreak())
#         self.elements.append(Paragraph("Figures", self.heading2_style))
#         sorted_claims = sorted(Data["claims"], key=lambda x: x.get("claim_type") == "system")
#         for claim in sorted_claims:
#             if claim.get("generated_figures_data") and claim["generated_figures_data"].get("latex_details"):
#                 for latex_detail in claim["generated_figures_data"]["latex_details"]:
#                     if "images_urls" in latex_detail:
#                         for img_url in latex_detail["images_urls"]:
#                             print("**************generating pdf*********")
#                             img_stream = self.download_image(img_url)
#                             if img_stream:
#                                 img = Image(img_stream)
#                                 img_width = img.drawWidth
#                                 img_height = img.drawHeight 
#                                 max_width = 5 * inch   
#                                 max_height = 5 * inch  
#                                 scale_factor = min(max_width / img_width, max_height / img_height)
#                                 if scale_factor < 1:
#                                     img.drawWidth = img_width * scale_factor
#                                     img.drawHeight = img_height * scale_factor
#                                 self.elements.append(img) 
#                             else:
#                                 print(f"Could not download image from {img_url}")
#         self.pdf.build(self.elements)
       
# pdf=PDFGenerator()
# pdf.convert_json_to_pdf_buffer(data)


      

  
 