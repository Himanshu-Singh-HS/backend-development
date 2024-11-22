from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# doc = SimpleDocTemplate("test_report_lab.pdf", pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
# doc.pagesize = landscape(A4)
# elements = []

# data = [
# ["Letter", "Number", "Stuff", "Long stuff that should be wrapped"],
# ["A", "01", "ABCD", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"],
# ["B", "02", "CDEF", "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"],
# ["C", "03", "SDFSDF", "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"],
# ["D", "04", "SDFSDF", "DDDDDDDDDDDDDDDDDDDDDDDD DDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"],
# ["E", "05", "GHJGHJGHJ", "EEEEEEEEEEEEEE EEEEEEEEEEEEEEEEE EEEEEEEEEEEEEEEEEEEE EEEEEEEEEEEEEE EEEEEEEEEEEEEEEEE EEEEEEEEEEEEEEEEEEEE EEEEEEEEEEEEEE EEEEEEEEEEEEEEEEE EEEEEEEEEEEEEEEEEEEE EEEEEEEEEEEEEE EEEEEEEEEEEEEEEEE EEEEEEEEEEEEEEEEEEEE "],
# ]

# style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
#                        ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
#                        ('VALIGN',(0,0),(0,-1),'TOP'),
#                        ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
#                        ('ALIGN',(0,-1),(-1,-1),'CENTER'),
#                        ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
#                        ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
#                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
#                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
#                        ])

# #Configure style and word wrap
# s = getSampleStyleSheet()
# s = s["BodyText"]
# s.wordWrap = 'CJK'
# data2 = [[Paragraph(cell, s) for cell in row] for row in data]
# t=Table(data2)
# t.setStyle(style)

# #Send the data and build the file
# elements.append(t)
# doc.build(elements)


 

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

    def add_table(self):
        # Define the table data (empty cells for the horizontal lines)
        data = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ]

        # Define the table style (adding borders and horizontal lines)
        style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),  # Border for all cells
            ('LINEBELOW', (0, 0), (-1, 0), 1, (0, 0, 0)),  # Horizontal line for row 1
            ('LINEBELOW', (0, 1), (-1, 1), 1, (0, 0, 0)),  # Horizontal line for row 2
            ('LINEBELOW', (0, 2), (-1, 2), 1, (0, 0, 0)),  # Horizontal line for row 3
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center the text inside the cells
            ('FONTSIZE', (0, 0), (-1, -1), 12),  # Set font size for all cells
        ])

        # Create the table object
        table = Table(data, colWidths=[doc.width / 3] * 3)  # Divide the width into 3 equal parts
        table.setStyle(style)

        # Add the table to the elements list (it will appear on the first page)
        self.elements.append(table)
        self.elements.append(Spacer(1, 12))  # Add some space after the table

    def convert_json_to_pdf_buffer(self, Data: dict) -> BytesIO:
        # Add table to the first page
        self.add_table()

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

        # (The rest of your code continues...)

        # Build the PDF document
        self.pdf.build(self.elements)

# Example usage:
pdf = pdfgenerator()
pdf.convert_json_to_pdf_buffer(data)
