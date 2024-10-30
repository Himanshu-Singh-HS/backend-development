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

    def estimate_paragraph_lines(self, text, style):
        # Estimate the number of lines for the paragraph by dividing its height by line height
        line_height = style.leading
        width, height = letter[0] - 144, letter[1] - 112  # Page size minus margins (left+right and top+bottom)
        
        # Create a temporary Paragraph to measure text height
        para = Paragraph(text, style)
        text_height = para.wrap(width, height)[1]  # Get the height the text will occupy
        
        num_lines = text_height // line_height  # Estimate number of lines
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
        print(f"Added {lines} lines for paragraph: {text[:50]}...")  # Print number of lines added
    
    def convert_json_to_pdf_buffer(self, Data: dict) -> BytesIO:
        # Add title
        title_text = Data['title']['text'].upper()
        self.elements.append(Paragraph(title_text, self.title_style))
        self.elements.append(Spacer(1, 12)) 
        self.total_lines += self.estimate_paragraph_lines(title_text, self.title_style)  # Estimate title lines
        
        # Technical field text with numbering
        self.elements.append(Paragraph("Technical field", self.heading2_style))
        self.total_lines += self.estimate_paragraph_lines("Technical field", self.heading2_style)  # Estimate heading lines
        
        self.add_justified_paragraph_with_numbering(Data["technical_field"]["text"])
        
        self.elements.append(Paragraph("Background Art", self.heading2_style))
        self.total_lines += self.estimate_paragraph_lines("Background Art", self.heading2_style)  # Estimate heading lines
        
        # Background text
        background_text = Data["background"]["text"]
        sections = background_text.split('\n\n')
        for section in sections:
            self.add_justified_paragraph_with_numbering(section)
                
        self.pdf.build(self.elements)
        print(f"Total number of lines in the document: {self.total_lines}")
      
pdf=pdfgenerator()
pdf.convert_json_to_pdf_buffer(data)