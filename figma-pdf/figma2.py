# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph
# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors

# class pdfgenerator:
#     def __init__(self):
#         self.pdf = SimpleDocTemplate("ep_ans.pdf", pagesize=letter)
#         self.elements = []
#         self.style_sheet = getSampleStyleSheet()

#         # Define table cell style
#         self.table_style = TableStyle([
#             ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Black grid lines for all cells
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),          # Center alignment for all cells
#             ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),    # Set font
#             ('FONTSIZE', (0, 0), (-1, -1), 10),             # Set font size
#         ])

#         # Define header style
#         self.heading_style = ParagraphStyle(
#             'Heading',
#             parent=self.style_sheet['Heading2'],
#             fontSize=12,    
#             fontName='Times-Bold',       
#         )

#     def create_table(self):
#         """ Create a table with text data """
#         data = [
#             ['Header 1', 'Header 2', 'Header 3'],  # Table header row
#             [Paragraph("Row 1, Cell 1,Row 1, Cell 1,Row 1, Cell 1Row 1, Cell 1Row 1, Cell 1", self.heading_style), 'Row 1, Cell 2', 'Row 1, Cell 3'],
#             ['Row 2, Cell 1', 'Row 2, Cell 2', 'Row 2, Cell 3'],
#             ['Row 3, Cell 1', 'Row 3, Cell 2', 'Row 3, Cell 3']
#         ]

#         # Create table and apply style
#         table = Table(data)
#         table.setStyle(self.table_style)

#         # Add the table to the elements list
#         self.elements.append(table)

#     def generate_pdf(self):
#         # Add the table to the PDF document
#         self.create_table()
#         self.pdf.build(self.elements)

# # Example usage:
# pdf = pdfgenerator()
# pdf.generate_pdf()


#    # Define the table style (adding borders and horizontal lines)
#         # style = TableStyle([
#         #     ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),  # Border for all cells
#         #     ('LINEBELOW', (0, 0), (-1, 0), 1, (0, 0, 0)),  # Horizontal line for row 1
#         #     ('LINEBELOW', (0, 1), (-1, 1), 1, (0, 0, 0)),  # Horizontal line for row 2
#         #     ('LINEBELOW', (0, 2), (-1, 2), 1, (0, 0, 0)),  # Horizontal line for row 3
#         #     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center the text inside the cells
#         #     ('FONTSIZE', (0, 0), (-1, -1), 12),  # Set font size for all cells
#         # ])


from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
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

data = json_data("/Users/patdelanalytics/backend-development/figma-pdf/ep.json")
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


from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer,PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from io import BytesIO
import json

def json_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

data = json_data("/Users/patdelanalytics/backend-development/figma-pdf/ep.json")

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

    def add_table(self,data):
        # Define the table data (empty cells for the horizontal lines)
        table_data = [
            [ f"{data["summaries"][0]}" 'Header 2'],
            [],
            [],
            [],
           
        ] 

      
        style = TableStyle([
            ('LINEBELOW', (0, 0), (-1, 0), 1, (0, 0, 0)),  
            ('LINEBELOW', (0, 1), (-1, 1), 1, (0, 0, 0)),  
            ('LINEBELOW', (0, 2), (-1, 2), 1, (0, 0, 0)),  
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  
            ('FONTSIZE', (0, 0), (-1, -1), 12),  
            ('BOX', (0, 0), (-1, -1), 0.5, (0, 0, 0)),  # Border around the whole table (box)
        ])

        # Define margins
        left_margin = 72   
        right_margin = 72  
        available_width = self.pdf.pagesize[0] - left_margin - right_margin  # Available width after margins
        column_width = available_width / 3  # Divide available width into 3 equal parts
        

        # table = Table(data, colWidths=[self.pdf.pagesize[0] / 3] * 3)  # Divide the width into 3 equal parts
        table = Table(table_data, colWidths=[column_width] * 3) 
        table.setStyle(style)

        self.elements.append(table)
        self.elements.append(Spacer(1, 12))  

    def convert_json_to_pdf_buffer(self, Data: dict) -> BytesIO:
        self.add_table(Data)
        self.pdf.build(self.elements)

pdf = pdfgenerator()
pdf.convert_json_to_pdf_buffer(data)
