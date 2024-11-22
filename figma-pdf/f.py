# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.platypus import Paragraph
# from reportlab.lib.utils import simpleSplit

# def create_pdf_with_text_in_box(file_path):
#     # Create a canvas
#     c = canvas.Canvas(file_path, pagesize=letter)
#     width, height = letter

#     # Define the margins and box dimensions
#     margin = 50
#     box_top = height - 100  # Starting 100 points below the top
#     box_bottom = 100        # Ending 100 points above the bottom
#     box_left = margin
#     box_right = width - margin
#     box_width = box_right - box_left
#     box_height = box_top - box_bottom

#     # Draw the outer box
#     c.rect(box_left, box_bottom, box_width, box_height, stroke=1, fill=0)

#     # Add a headline
#     headline = "This is the Headline"
#     c.setFont("Helvetica-Bold", 14)
#     headline_y = box_top - 20  # 20 points below the top of the box
#     c.drawString(box_left + 10, headline_y, headline)

#     # Add a paragraph
#     text = (
#         "This is a sample paragraph that fits inside the box. "
#         "You can include multiple lines of text, and they will be "
#         "wrapped automatically if you calculate the space correctly."
#     )
#     c.setFont("Helvetica", 12)
#     text_start_y = headline_y - 20  # 20 points below the headline
#     text_margin = 10  # Margin inside the box for the text

#     # Wrap text into lines
#     lines = simpleSplit(text, "Helvetica", 12, box_width - 2 * text_margin)
#     for line in lines:
#         c.drawString(box_left + text_margin, text_start_y, line)
#         text_start_y -= 15  # Line spacing

#     # Save the canvas
#     c.save()

# # Generate the PDF
# create_pdf_with_text_in_box("box_with_text.pdf")


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame

def create_pdf_with_box_and_text(file_path):
    # Create a document template
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []  # Collect all elements here
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading2']
    body_style = styles['BodyText']

    # Add a title
    elements.append(Paragraph("Sample PDF with Box and Text", title_style))
    elements.append(Spacer(1, 20))

    # Add content for the box
    box_content = []
    box_content.append(Paragraph("This is a headline", heading_style))
    box_content.append(Spacer(1, 12))
    box_content.append(Paragraph(
        "This paragraph is inside the box. You can include longer text here, "
        "and it will wrap automatically based on the width of the box.",
        body_style
    ))

    # Define box coordinates
    width, height = letter
    margin = 50
    box_top = height - 100
    box_bottom = 100
    box_left = margin
    box_right = width - margin
    box_width = box_right - box_left
    box_height = box_top - box_bottom

    # Add box with content using Frame
    frame = Frame(box_left, box_bottom, box_width, box_height, showBoundary=1)
    frame.addFromList(box_content, canvas.Canvas(file_path))

    # Finalize the document
    doc.build(elements)

# Generate the PDF
create_pdf_with_box_and_text("box_with_text_and_paragraphs.pdf")
