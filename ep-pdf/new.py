# import fitz  # PyMuPDF

# # Open the existing PDF in update mode
# pdf_document = fitz.open("/Users/patdelanalytics/backend-development/ep-pdf.pdf")

# # Loop through each page
# for page_num in range(pdf_document.page_count):
#     page = pdf_document[page_num]
#     print(f"--- Page {page_num + 1} ---")

#     # Get text as a dictionary to retrieve details about each line
#     text_dict = page.get_text("dict")
    
#     # Initialize the line index
#     line_index = 1

#     # Loop through each block of text
#     for block in text_dict['blocks']:
#         if block['type'] == 0:  # Ensure it's a text block
#             for line in block['lines']:
#                 # Loop through each span (segment) in the line
#                 for span in line['spans']:
#                     # Calculate the y position for the line number
#                     # Span has 'bbox' which gives (x0, y0, x1, y1)
#                     bbox = span['bbox']
#                     y_position = bbox[1]  # Use the top of the bounding box for positioning
#                     x_offset = bbox[0] - 30  # Positioning to the left of the text

#                     # Insert the line number at the calculated position
#                     if line_index%5==0:
#                         page.insert_text((x_offset, y_position), f"{line_index} ", fontsize=14, color=(0, 0, 0))

#                 line_index += 1  # Increment line index after each line

# # Save the modified PDF
# pdf_document.save("/Users/patdelanalytics/backend-development/ep-pdf-numbered.pdf")
# pdf_document.close()


import fitz  # PyMuPDF

# Open the existing PDF in update mode
pdf_document = fitz.open("/Users/patdelanalytics/backend-development/ep-pdf.pdf")

# Loop through each page
for page_num in range(pdf_document.page_count):
    page = pdf_document[page_num]
    print(f"--- Page {page_num + 1} ---")

    # Get text as a dictionary to retrieve details about each line
    text_dict = page.get_text("dict")

    # Initialize the line index for the current page
    line_index = 1

    # Loop through each block of text
    for block in text_dict['blocks']:
        if block['type'] == 0:  # Ensure it's a text block
            for line in block['lines']:
                # Loop through each span (segment) in the line
                for span in line['spans']:
                    # Calculate the y position for the line number
                    # Span has 'bbox' which gives (x0, y0, x1, y1)
                    bbox = span['bbox']
                    y_position = bbox[1]  # Use the top of the bounding box for positioning
                    x_offset = bbox[0] - 30  # Positioning to the left of the text

                    # Insert the line number at the calculated position
                    if line_index%5==0:
                      page.insert_text((x_offset, y_position), f"{line_index} ", fontsize=14, color=(0, 0, 0))

                line_index += 1  # Increment line index after each line

# Save the modified PDF
pdf_document.save("/Users/patdelanalytics/backend-development/ep-pdf-numbered.pdf")
pdf_document.close()

