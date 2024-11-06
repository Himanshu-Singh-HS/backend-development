

# importing third-party modules  for pdf ===============================================
import time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak,Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER
from reportlab.lib.units import inch
from io import BytesIO
import json,requests
import fitz   

def json_data(filename):
    with open (filename,'r') as file:
        return json.load(file)
data=json_data("./eP-pdf/ep.json")

class PDFGenerator:
    def __init__(self):
        self.pdf_file_path = "himanshu1.pdf" 
        self.buffer = BytesIO()
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
        
    # Add page numbering and handle line numbering
    def add_page_number_and_line_count(self, canvas, doc, start_line=1):
        """This method adds the page number and draws the line numbers in sets of five on the left side."""
        page_num = canvas.getPageNumber()
        text = f" {page_num}"
        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
        canvas.drawCentredString(4.25 * inch, 10.5 * inch, text)


        
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
                            # print(img_url)
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
        # self.pdf.build(self.elements, onFirstPage=self.add_page_number, onLaterPages=self.add_page_number)
        self.pdf.build(self.elements, onFirstPage=self.add_page_number_and_line_count, onLaterPages=self.add_page_number_and_line_count)
        pdf.add_line_numbers()
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
                            y_position = bbox[1]+13# Top of the bounding box
                            x_offset = bbox[0] - 30  # Positioning to the left

                            if line_index % 5 == 0 and line_index != 0:
                              page.insert_text((x_offset, y_position), f"{line_index} ", fontsize=10, color=(0, 0, 0))

                        line_index += 1

        # Save the final PDF with line numbers to disk
        pdf_document.save(self.pdf_file_path)
        pdf_document.close()
        print("total time taken by pdf -> ",time.time()-start)
        print("Document completed successfully.")
        
pdf=PDFGenerator()
start=time.time()
pdf.convert_json_to_pdf_buffer(data)
 

