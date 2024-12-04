import time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak,Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER
import json
import os,requests
from io import BytesIO
from reportlab.lib.units import inch


def download_image(img_url):
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

def load_json_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

data_file = os.path.join(os.path.dirname(__file__), 'patent.json')
json_data = load_json_data(data_file)

# Create a custom paragraph style for justified alignment
style_sheet = getSampleStyleSheet()
justified_style = ParagraphStyle(
    'Justified',
    parent=style_sheet['BodyText'],
    fontName='Times-Roman',
    fontSize=12,
    leading=20,
    alignment=TA_JUSTIFY
)
centered_heading_style = ParagraphStyle(
    'CenteredHeading1',
    parent=style_sheet['Heading1'],
    alignment=TA_CENTER,
    fontSize=12,
    fontName='Times-Bold',  
)
heading2_style = ParagraphStyle(
    'Heading2',
    parent=style_sheet['Heading2'],
    # fontName='Times-Roman',  
    fontSize=12,    
    fontName='Times-Bold',       
)
title_style = ParagraphStyle(
    'Heading2',
    parent=style_sheet['Heading2'],
    # fontName='Times-Roman',  
    fontSize=12,    
    fontName='Times-Bold', 
    alignment=TA_CENTER      
)

# Function to add page number and Attorney Docket No. on each page
def add_page_number_and_docket(canvas, doc, docket_number="Attorney Docket No. "):
    """This method is called to add the page number and docket number to each page."""
    page_num = canvas.getPageNumber()
    text = f"{page_num}"
    # Add the page number  
    canvas.saveState()
    canvas.setFont('Times-Roman', 12)
    canvas.drawCentredString(4.25 * inch, 0.5 * inch, text)
    # Add Attorney Docket No. 
    extra_space = 1 * inch   
    extra_space_down = 0.5 * inch
    canvas.setFont('Times-Roman', 12)
    canvas.drawRightString((7.5 * inch) - extra_space, (10.5 * inch-extra_space_down), docket_number)
    canvas.restoreState()
    

def convert_json_to_pdf(Data: dict, output_filename: str):
    start=time.time()
    pdf = SimpleDocTemplate(output_filename, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=40)
    elements = []
    
    # Add title
    title_text = Data['title']['text'].upper()
    elements.append(Paragraph(title_text,title_style))
    elements.append(Spacer(1, 12)) 

    # Function to add justified paragraphs with numbering
    def add_justified_paragraph_with_numbering(text, counter=0,  first_Line_Indent=0):
        modified_style = ParagraphStyle(
        'Justified',
        parent=style_sheet['BodyText'],
        fontName='Times-Roman',
        fontSize=12,
        leading=20,
        alignment=TA_JUSTIFY,
        firstLineIndent=first_Line_Indent
    )   
        numbered_text = f"<b>[{counter:04d}]</b> {text}"
        if counter==0:
            elements.append(Paragraph(text, modified_style))
        else:
            elements.append(Paragraph(numbered_text, modified_style))
            elements.append(Spacer(1, 12))  
            return counter + 1
    # Technical field text with numbering
    elements.append(Paragraph("BACKGROUND", heading2_style))
    counter = 1
    counter = add_justified_paragraph_with_numbering(Data["technical_field"]["text"], counter)

    # Background text
    background_text = Data["background"]["text"]
    sections = background_text.split('\n\n')
    for section in sections:
        counter = add_justified_paragraph_with_numbering(section, counter)

    # Brief summary text
    elements.append(Paragraph("BRIEF SUMMARY", heading2_style))
    elements.append(Spacer(1, 12))
    summary_text = Data["summary"]["text"]
    sections = summary_text.split('\n\n')
    for section in sections:
        counter = add_justified_paragraph_with_numbering(section, counter)
        
    #FIGIURES LIST
    elements.append(Paragraph("BRIEF DESCRIPTION OF THE SEVERAL VIEWS OF THE DRAWINGS",heading2_style))
    elements.append(Spacer(1, 12))
    figure_list=Data["list_of_figures"]
    for figure in figure_list:
        counter=add_justified_paragraph_with_numbering(figure,counter)
    
    #Detailed Description   
    
    elements.append(Paragraph("DETAILED DESCRIPTION",heading2_style))
    elements.append(Spacer(1,12))
     # Method description
    method_desc_text = Data["description"]["method_desc"]["text"]
    method_desc_sections = method_desc_text.split('\n\n')
    for section in method_desc_sections:
        counter =  add_justified_paragraph_with_numbering(section, counter)

    # System description
    system_desc_text_list = Data["description"]["system_desc"]["text_list"]
    for section in system_desc_text_list:
        counter = add_justified_paragraph_with_numbering(section, counter)

    # Invention Description
    invention_desc_text = Data["description"]["invention_desc"]["text"]
    invention_desc_sections = invention_desc_text.split('\n\n')
    for section in invention_desc_sections:
        counter =  add_justified_paragraph_with_numbering(section, counter)
    
    claims_style = ParagraphStyle(
    'Claims',
    parent=style_sheet['BodyText'],
    fontName='Times-Roman',
    fontSize=12,
    leading=20,
    firstLineIndent =40   
)
    # Claims section
    elements.append(PageBreak())
    elements.append(Paragraph("CLAIMS",centered_heading_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("What is claimed is:", ParagraphStyle("font", fontSize=12, fontName="Times-Roman")))
    elements.append(Spacer(1, 12))
    for index, claim in enumerate(Data['claims'], start=1):
        claim_text = f"{index}. {claim['text']}"
    
    # Split the claim text by semicolon
        claim_parts = claim_text.split("\n")
    
    # Add each part of the claim as a new paragraph
        # for part in claim_parts:
        #   elements.append(Paragraph(part, style=claims_style))  # Add ";" back after splitting
        #   elements.append(Spacer(1, 12))
        
        # for i, part in enumerate(claim_parts):
        #     if i < len(claim_parts) - 1:  
        #         elements.append(Paragraph(part.strip() + ";", style=claims_style))
        #     else: 
        #         elements.append(Paragraph(part.strip(), style=claims_style))
        #     elements.append(Spacer(1, 12))
        for part in claim_parts:
            elements.append(Paragraph(part,claims_style))

    # Abstract section
    elements.append(PageBreak())
    elements.append(Paragraph("ABSTRACT", centered_heading_style))
    elements.append(Spacer(1, 12))
    abstract_text = Data["abstract"]["text"]
    abstract_sections = abstract_text.split('\n\n')
    print(abstract_sections)
    for section in abstract_sections:
        counter =  add_justified_paragraph_with_numbering(section,first_Line_Indent=40)
        
    #image section
    elements.append(PageBreak())
    elements.append(Paragraph("FIGURES", heading2_style))
    sorted_claims = sorted(Data["claims"], key=lambda x: x.get("claim_type") == "system")
    for claim in sorted_claims:
        if claim.get("generated_figures_data") and claim["generated_figures_data"].get("latex_details"):
            for latex_detail in claim["generated_figures_data"]["latex_details"]:
                if "images_urls" in latex_detail:
                    for img_url in latex_detail["images_urls"]:
                        img_stream = download_image(img_url)
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
                            elements.append(img) 
                        else:
                            print(f"Could not download image from {img_url}")

    # i am here building the pdf 
    # pdf.build(elements)
    # Build the PDF with page numbering
    # pdf.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    pdf.build(elements, onFirstPage=lambda canvas, doc: add_page_number_and_docket(canvas, doc, "Attorney Docket No. "),
              onLaterPages=lambda canvas, doc: add_page_number_and_docket(canvas, doc, "Attorney Docket No. "))
    print(f"{time.time()-start}:sec")
convert_json_to_pdf(json_data, "himanshu.pdf")

 

 
