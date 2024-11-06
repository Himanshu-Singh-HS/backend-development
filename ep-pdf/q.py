# # importing third-party modules  for pdf ===============================================
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak, Image
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
# from reportlab.lib.units import inch
# from io import BytesIO
# import json, requests
# import fitz   

# def json_data(filename):
#     with open(filename, 'r') as file:
#         return json.load(file)

# data = json_data("./eP-pdf/ep.json")

# class PDFGenerator:
#     def __init__(self):
#         self.pdf_file_path = "ans-ep123.pdf"
#         self.pdf = SimpleDocTemplate(self.pdf_file_path, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=40)
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
#             'Title',
#             parent=self.style_sheet['Heading1'],
#             fontSize=14,
#             fontName='Times-Bold', 
#             alignment=TA_CENTER      
#         ) 
        
#     def add_justified_paragraph_with_numbering(self, text, first_Line_Indent=0):
#         modified_style = ParagraphStyle(
#             'Justified',
#             parent=self.style_sheet['BodyText'],
#             fontName='Times-Roman',
#             fontSize=12,
#             leading=20,
#             alignment=TA_JUSTIFY,
#             firstLineIndent=first_Line_Indent)                                  
#         self.elements.append(Paragraph(text, modified_style))
#         self.elements.append(Spacer(1, 12))  
    
#     def download_image(self, img_url):
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

#     def add_page_number_and_line_count(self, canvas, doc):
#         page_num = canvas.getPageNumber()
#         text = f"Page {page_num}"
#         canvas.saveState()
#         canvas.setFont('Times-Roman', 12)
#         canvas.drawCentredString(4.25 * inch, 10.5 * inch, text)
        
#     def convert_json_to_pdf(self, Data):
#         # Add title
#         title_text = Data['title']['text'].upper()
#         self.elements.append(Paragraph(title_text, self.title_style))
#         self.elements.append(Spacer(1, 12))

#         # Technical field text with numbering
#         self.elements.append(Paragraph("Technical field", self.heading2_style))
#         self.add_justified_paragraph_with_numbering(Data["technical_field"]["text"])

#         # Background Art
#         self.elements.append(Paragraph("Background Art", self.heading2_style))
#         background_text = Data["background"]["text"]
#         for section in background_text.split('\n\n'):
#             self.add_justified_paragraph_with_numbering(section)

#         # Summary of the invention
#         self.elements.append(Paragraph("Summary of the invention", self.heading2_style))
#         summary_text = Data["summary"]["text"]
#         for section in summary_text.split('\n\n'):
#             self.add_justified_paragraph_with_numbering(section)

#         # Figures list
#         self.elements.append(Paragraph("Brief description of the drawings", self.heading2_style))
#         for figure in Data["list_of_figures"]:
#             self.add_justified_paragraph_with_numbering(figure)

#         # Detailed Description
#         self.elements.append(Paragraph("Detailed description", self.heading2_style))
#         for section in Data["description"]["method_desc"]["text"].split('\n\n'):
#             self.add_justified_paragraph_with_numbering(section)

#         for section in Data["description"]["system_desc"]["text_list"]:
#             self.add_justified_paragraph_with_numbering(section)

#         for section in Data["description"]["invention_desc"]["text"].split('\n\n'):
#             self.add_justified_paragraph_with_numbering(section)

#         # Claims
#         self.elements.append(PageBreak())
#         self.elements.append(Paragraph("Claims", self.heading2_style))
#         for index, claim in enumerate(Data['claims'], start=1):
#             claim_text = f"{index}. {claim['text']}"
#             for part in claim_text.split("\n"):
#                 self.elements.append(Paragraph(part, self.style_sheet['BodyText']))

#         # Abstract
#         self.elements.append(PageBreak())
#         self.elements.append(Paragraph("Abstract", self.heading2_style))
#         for section in Data["abstract"]["text"].split('\n\n'):
#             self.add_justified_paragraph_with_numbering(section)
        
#         # # Images
#         # self.elements.append(PageBreak())
#         # self.elements.append(Paragraph("Figures", self.heading2_style))
#         # sorted_claims = sorted(Data["claims"], key=lambda x: x.get("claim_type") == "system")
#         # for claim in sorted_claims:
#         #     if claim.get("generated_figures_data") and claim["generated_figures_data"].get("latex_details"):
#         #         for latex_detail in claim["generated_figures_data"]["latex_details"]:
#         #             if "images_urls" in latex_detail:
#         #                 for img_url in latex_detail["images_urls"]:
#         #                     img_stream = self.download_image(img_url)
#         #                     if img_stream:
#         #                         img = Image(img_stream)
#         #                         img.drawWidth = img.drawWidth * 0.5
#         #                         img.drawHeight = img.drawHeight * 0.5
#         #                         self.elements.append(img) 
        
#         # Build and save the initial PDF
#         self.pdf.build(self.elements, onFirstPage=self.add_page_number_and_line_count, onLaterPages=self.add_page_number_and_line_count)

#         # Add line numbers and save the final PDF
#         self.add_line_numbers()

#     def add_line_numbers(self):
#         """Add line numbers to the generated PDF using PyMuPDF."""
#         pdf_document = fitz.open(self.pdf_file_path)
#         for page_num in range(pdf_document.page_count):
#             page = pdf_document[page_num]
#             text_dict = page.get_text("dict")
#             line_index = 0
#             for block in text_dict['blocks']:
#                 if block['type'] == 0:
#                     for line in block['lines']:
#                         for span in line['spans']:
#                             bbox = span['bbox']
#                             y_position = bbox[1]
#                             x_offset = bbox[0] - 30
#                             if line_index % 5 == 0 and line_index != 0:
#                                 page.insert_text((x_offset, y_position), f"{line_index}", fontsize=10, color=(0, 0, 0))
#                         line_index += 1  
#         pdf_document.save(self.pdf_file_path.replace('.pdf', '-numbered.pdf'))
#         pdf_document.close()
#         print("Document generation with line numbering completed successfully.")

# pdf = PDFGenerator()
# pdf.convert_json_to_pdf(data)



from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.units import inch
from io import BytesIO
import json, requests
import fitz

def json_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

data = json_data("./eP-pdf/ep.json")

class PDFGenerator:
    def __init__(self):
        self.pdf_file_path = "pdff.pdf"  # Only one final output PDF file
        self.buffer = BytesIO()  # Use an in-memory buffer for the initial PDF
        self.pdf = SimpleDocTemplate(self.buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=40)
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

    def add_page_number_and_line_count(self, canvas, doc, start_line=1):
        """This method adds the page number and draws the line numbers in sets of five on the left side."""
        page_num = canvas.getPageNumber()
        text = f" {page_num}"
        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
        canvas.drawCentredString(4.25 * inch, 10.5 * inch, text)
        canvas.restoreState()

    def convert_json_to_pdf_buffer(self, Data: dict) -> BytesIO:
        # Add title and other content sections here...
        title_text = Data['title']['text'].upper()
        self.elements.append(Paragraph(title_text, self.title_style))
        self.elements.append(Spacer(1, 12))

        # Technical field, background, summary, etc. sections added to `self.elements`...
        # Example for adding claims section:
        self.elements.append(PageBreak())
        self.elements.append(Paragraph("Claims", self.heading2_style))
        self.elements.append(Spacer(1, 12))
        claims_style = ParagraphStyle(
            'Claims',
            parent=self.style_sheet['BodyText'],
            fontName='Times-Roman',
            fontSize=12,
            leading=20,
            alignment=TA_JUSTIFY,
        )
        for index, claim in enumerate(Data['claims'], start=1):
            claim_text = f"{index}. {claim['text']}"
            claim_parts = claim_text.split("\n")
            for part in claim_parts:
                self.elements.append(Paragraph(part, claims_style))

        # Generate PDF in memory buffer
        self.pdf.build(self.elements, onFirstPage=self.add_page_number_and_line_count, onLaterPages=self.add_page_number_and_line_count)
        return self.buffer

    def add_line_numbers(self):
        """Add line numbers to the generated PDF in the buffer using PyMuPDF."""
        self.buffer.seek(0)  # Reset buffer pointer to start
        pdf_document = fitz.open(stream=self.buffer, filetype="pdf")

        # Loop through each page
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            # Get text as a dictionary to retrieve details about each line
            text_dict = page.get_text("dict")
            line_index = 0
            # Loop through each block of text
            for block in text_dict['blocks']:
                if block['type'] == 0:  # Ensure it's a text block
                    for line in block['lines']:
                        for span in line['spans']:
                            # Calculate the y position for the line number
                            bbox = span['bbox']
                            y_position = bbox[1]  # Top of the bounding box
                            x_offset = bbox[0] - 30  # Positioning to the left

                            if line_index % 5 == 0 and line_index != 0:
                                page.insert_text((x_offset, y_position), f"{line_index} ", fontsize=10, color=(0, 0, 0))

                        line_index += 1

        # Save the final PDF with line numbers to disk
        pdf_document.save(self.pdf_file_path)
        pdf_document.close()
        print("Document completed successfully.")

pdf = PDFGenerator()
pdf_buffer = pdf.convert_json_to_pdf_buffer(data)  # Generate PDF in buffer
pdf.add_line_numbers()  # Add line numbers to buffer content
