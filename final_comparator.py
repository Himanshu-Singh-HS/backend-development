import re
from  datetime import datetime
class GetPatentdata: 
    
    def merge_bibliographys_and_summaries(self,bibliographys: List[Dict], summaries: List[Dict]) -> List[Dict]:
        bibliography_lookup = {b.patent_number: b for b in bibliographys}
        merged_data = []

        for summary in summaries:
            each={}
            ucid = summary.ucid
            if ucid in bibliography_lookup:
                each.update(bibliography_lookup[ucid].dict())
                each.update(summary.dict())
                merged_data.append(each)
        return merged_data

    def get_patent_details(self,ucids):
        """
        Retrieves the bibliography and generates a summary for a given patent UCID.
        Returns both outputs in a structured Pydantic model.

        :param ucid: Unique Case Identifier for the patent
        :return: PatentDetailsResponse containing bibliography and summary
        """
        try:
            bibliographies = fetch_patent_bibliography(ucids)
            # Generate the patent summary
            summaries = generate_patent_summary(ucids)
            merged_data = self.merge_bibliographys_and_summaries(bibliographies, summaries)
            return merged_data
        except Exception as e:
            print("fetchoing error")
            raise Exception(str(e))
        
class patentdetails1:
    def __init__(self,ucids):
        self.datas = GetPatentdata().get_patent_details(ucids) 
        self.pdf_buffer = BytesIO()
        self.content = []
        self.styles = getSampleStyleSheet()
        self.ucids=ucids 
        self.pdf = SimpleDocTemplate(self.pdf_buffer, pagesize=letter)
    
    def create_styled_pdf(self):
        normal_style = self.styles['Normal']
        normal_style.fontSize = 10
        normal_style.fontName = 'Times-Roman'
        heading4_style = self.styles['Heading4']
        heading5_style = self.styles['Heading5']
        non_eng_styles = getSampleStyleSheet()
        non_eng_style = non_eng_styles['Normal']
        non_eng_style.fontSize = 10
        non_eng_style.fontName = 'SimHei'
        heading_title= "INVENTION DISCLOSURE ANALYZER REPORT -US PATENT "
        heading_title = [
            [Paragraph(heading_title, heading4_style)]   
        ]
        heading_title = Table(heading_title, colWidths=[6.5 * inch])
        heading_title.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#006400'),  # Background color for the header
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Text color for the header
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align the text
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),  # Bold font for the title
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding below the title
            ('BACKGROUND', (0, 1), (-1, -1), '#F5F5F5'),  # Background for content rows
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),   # Outer border only with 1px thickness
        ]))
        self.content.append(heading_title)
        self.content.append(Spacer(1, 12))  
        heading_content= "PRIOR ART - "
        heading_table_data = [
            [Paragraph(heading_content, heading4_style)]   
        ]
        heading_content_card = Table(heading_table_data, colWidths=[6.5 * inch])
        heading_content_card.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#E3EEEC'),  # Background color for the header
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Text color for the header
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align the text
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),  # Bold font for the title
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding below the title
            ('BACKGROUND', (0, 1), (-1, -1), '#F5F5F5'),  # Background for content rows
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),   # Outer border only with 1px thickness
        ]))
        self.content.append(heading_content_card)
        ucids_members_row = []
        for index, ucid in enumerate(self.ucids, start=1):
            ucids_members_row.append(f"{index}. {ucid}")
            
        heading_table_data = [
            [Paragraph("\n".join(ucids_members_row), normal_style)],        
        ]

        heading_content_card1 = Table(heading_table_data, colWidths=[6.5 * inch])
        heading_content_card1.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Text color for the header
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align the text
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),  # Bold font for the title
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding below the title
            ('BACKGROUND', (0, 1), (-1, -1), '#F5F5F5'),  # Background for content rows
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),   # Outer border only with 1px thickness
        ]))
        
        self.content.append(heading_content_card1)
        self.content.append(PageBreak())

        for ind, data in enumerate(self.datas,start=1):
            # pprint(data,width=150)
            
            # Title Section
            title = f"DOCUMENT - {ind}"
            title_table_data = [
                [Paragraph(title, heading4_style)]  # Add the Patent Title in the table
            ]
            patent_title_card = Table(title_table_data, colWidths=[6.5 * inch])
            patent_title_card.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), '#E3EEEC'),  # Background color for the header
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Text color for the header
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align the text
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),  # Bold font for the title
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding below the title
                ('BACKGROUND', (0, 1), (-1, -1), '#F5F5F5'),  # Background for content rows
                ('BOX', (0, 0), (-1, -1), 0.5, colors.black),   # Outer border only with 1px thickness
            ]))
            patent_title = f"Patent: <font color='#01AD68'>{data['patent_number']} </font>"
            
            table_data = [
                [Paragraph(patent_title, heading4_style)]  # Add the Patent Title in the table
            ]

            # Create the table for the Patent Title
            patent_table = Table(table_data, colWidths=[6.5 * inch])

            # Apply TableStyle
            patent_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), '#F5F5F5'),  # Background color for the header
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Text color for the header
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align the text
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),  # Bold font for the title
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding below the title
                ('BACKGROUND', (0, 1), (-1, -1), '#F5F5F5'),  # Background for content rows
                ('BOX', (0, 0), (-1, -1), 0.5, colors.black),   # Outer border only with 1px thickness
            ]))

            self.content.append(patent_title_card)

            self.content.append(patent_table)
            def is_valid_text(text, allowed_special_chars=".,/?;:'[{()}]\|=+-_*&^%$#@!~`"):
                # Create a regex pattern to allow letters, numbers, spaces, and specified special characters
                pattern = rf"^[a-zA-Z0-9{re.escape(allowed_special_chars)} ]*$"
                return bool(re.match(pattern, text)),text
            
            def separate_text_by_language(names_list, validation_function):
                english_texts = []
                non_english_texts = []
                try:
                    for name in names_list:
                        is_valid, processed_text = validation_function(name)
                        if is_valid:
                            english_texts.append(processed_text)
                        else:
                            non_english_texts.append(processed_text)
                except Exception as e:
                    print("error in seprate text by language ",e)
                return english_texts, non_english_texts

            eng_assignees,noneng_assignees = separate_text_by_language(join_names(data['assignees']), is_valid_text)
            eng_assignees = "\n, ".join(eng_assignees)
            noneng_assignees = "\n, ".join(noneng_assignees)
            
            eng_inventors,noneng_inventors = separate_text_by_language(join_names(data['inventors']), is_valid_text)
            eng_inventors = "\n, ".join(eng_inventors)
            noneng_inventors = "\n, ".join(noneng_inventors)
            

            names_data_with_paragraphs = [
                [
                Paragraph('Assignees',normal_style),
                Paragraph('Inventors',normal_style)],
                [
                [Paragraph(f'<b>{eng_assignees}</b>', normal_style) ,Paragraph(f'<b>{noneng_assignees}</b>', non_eng_style)],
                [Paragraph(f'<b>{eng_inventors}</b>', normal_style) ,Paragraph(f'<b>{noneng_inventors}</b>', non_eng_style)]
                ]
            ]

            # Set column widths (no increase)
            names_table = Table(names_data_with_paragraphs, colWidths=[4 * inch, 2.5 * inch, 2.5 * inch])

            names_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), '#F5F5F5'),  # Header row background
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header row text color
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Align text to the left
            # ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),  # Bold font for the header
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding below the header
                ('BACKGROUND', (0, 1), (-1, -1), '#F5F5F5'),  # Background for content rows
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Add grid lines
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Top-align the text
                ('LEFTPADDING', (0, 0), (-1, -1), 5),  # Padding for left side
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),  # Padding for right side
                ('BOX', (0, 0), (-1, -1), 0.5, colors.black),   # Outer border only with 1px thickness
            ]))
            self.content.append(names_table)

            # Dates Section in Table
            from datetime import datetime,date
       

            def safe_paragraph(key, default="N/A"):
                try:
                    value = data.get(key, default)
                    if value is None:
                        value = default
                    elif isinstance(value, str):  # Dates might be in ISO string already
                        return Paragraph(f'<b>{value}</b>', normal_style)
                    elif isinstance(value, date):
                        return Paragraph(f'<b>{value.isoformat()}</b>', normal_style)
                    else:
                        print(key,data[key],type(data[key]))
                except Exception as e:
                    # Log the error and return a default paragraph
                    print(f"Error processing {key}: {e}")
                    return Paragraph(f'<b>{default}</b>', normal_style)


            dates_data_with_paragraphs = [
                [
                    Paragraph('Legal Status', normal_style),
                    Paragraph('Priority Date', normal_style),
                    Paragraph('Application Date', normal_style),
                    Paragraph('Publication Date', normal_style)
                ],
                [
                    safe_paragraph("legal_status"),
                    safe_paragraph("priority_date"),
                    safe_paragraph("application_date"),
                    safe_paragraph("publication_date")
                ]
            ]

            dates_table = Table(dates_data_with_paragraphs, colWidths=[2.6 * inch, 1.3 * inch, 1.3 * inch])
            dates_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), '#F5F5F5'),  # Header row background
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header row text color
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Align text to the left
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),  # Bold font for the header
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding below the header
                ('BACKGROUND', (0, 1), (-1, -1), '#F5F5F5'),  # Background for content rows
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Add grid lines
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Top-align the text
                ('LEFTPADDING', (0, 0), (-1, -1), 5),  # Padding for left side
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),  # Padding for right side
                ('BOX', (0, 0), (-1, -1), 0.5, colors.black),   # Outer border only with 1px thickness
            ]))
            self.content.append(dates_table)

            # Family Members Section
            family_members_row = f"{', '.join([fm['ucid'] for fm in data['family_members']])}"

            # Start preparing the table content
            table_data = [
                # Header row
                [Paragraph("Family Members:", heading4_style)],
                [Paragraph(family_members_row, normal_style)],        
                # Classification Section
                [Paragraph("Classifications", heading4_style)],
            ]

            # Add classification sections dynamically from the `keys` list
            keys = ['ipc_classes', 'locarno_classes', 'ipcr_classes', 'national_classes', 'ecla_classes', 'cpc_classes']
            for item in keys:
                if data[item]:
                    table_data.append([Paragraph(item.replace('_', ' ').title(), heading5_style)])  # Heading for each classification type
                    classifications = process_classifications(data[item])
                    table_data.append([Paragraph(classifications, normal_style)])  # The classification content
                    table_data.append([Spacer(1, 0.005 * inch)])  # Spacer after each section

            # Create the table
            table = Table(table_data, colWidths=[6.5 * inch])

            # Apply TableStyle
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), '#F5F5F5'),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), '#F5F5F5'),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.black),   
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),   
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ]))

            self.content.append(table)

            summary_data = [
                [Paragraph("Summary:", heading4_style)],   
                [Paragraph(data['summary'], normal_style)],  
            ]
            # Create the table for the Summary section
            summary_table = Table(summary_data, colWidths=[6.5 * inch])

            # Apply TableStyle to format the table
            summary_table.setStyle(TableStyle([
                
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header row text color
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Align text to the left
                ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),  # Bold font for the header
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding below the header
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Top-align the text
                ('LEFTPADDING', (0, 0), (-1, -1), 5),  # Padding for left side
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),  # Padding for right side
                ('BOX', (0, 0), (-1, -1), 0.5, colors.black),   # Outer border only with 1px thickness
            ]))
            self.content.append(summary_table)
            self.content.append(PageBreak())
        self.pdf.build(self.content)
        self.pdf_buffer.seek(0) 
        return self.pdf_buffer

 
    # Add specific styles for title row
        if "BACKGROUND" in section["style"]:
            table_style.append(('BACKGROUND', (0, 0), (-1, 0), section["style"]['BACKGROUND']))
        if "TEXTCOLOR" in section["style"]:
            table_style.append(('TEXTCOLOR', (0, 0), (-1, 0), section["style"]['TEXTCOLOR']))
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.units import inch

def create_table(data, style, col_width=6.5 * inch):
    """
    Create a styled table with the given data and style.
    
    Args:
        data (list): Table data.
        style (list): List of TableStyle properties.
        col_width (float): Column width for the table.
    
    Returns:
        Table: A styled table.
    """
    table = Table(data, colWidths=[col_width])
    table.setStyle(TableStyle(style))
    return table

# Styles for tables
default_table_style = [
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header row text color
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Align text to the left
    ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),  # Bold font for the header
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding below the header
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Top-align the text
    ('LEFTPADDING', (0, 0), (-1, -1), 5),  # Padding for left side
    ('RIGHTPADDING', (0, 0), (-1, -1), 5),  # Padding for right side
    ('BOX', (0, 0), (-1, -1), 0.5, colors.black),  # Outer border with 1px thickness
]

# Example data
summary_data = [
    [Paragraph("Summary:", heading4_style)],  # Header for Summary
    [Paragraph(data['summary'], normal_style)],  # Content of the Summary
]
similarity_data = [[Paragraph("\n".join(data['similarity']), normal_style)]]
differences_data = [[Paragraph("\n".join(data['differences']), normal_style)]]

# Creating tables using the function
content.append(create_table(summary_data, default_table_style))
content.append(create_table(similarity_data, default_table_style))
content.append(create_table(differences_data, default_table_style))
