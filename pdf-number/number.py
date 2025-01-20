# import fitz  # PyMuPDF

# def print_lines_with_numbers(pdf_path):
#     with fitz.open(pdf_path) as pdf:
#         for page_number, page in enumerate(pdf, start=1):
#             text = page.get_text("text")
#             lines = text.splitlines()
#             for line_number, line in enumerate(lines, start=1):
#                 print(f"Page {page_number}, Line {line_number}: {line}")

# pdf_path = "pdf (5).pdf"
# print_lines_with_numbers(pdf_path)

import fitz  # PyMuPDF
def count_lines_excluding_numbers(pdf_path):
    line_count = 0
    with fitz.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text("text")  # Extract text
            lines = text.splitlines()  # Split into lines
            for line_number, line in enumerate(lines, start=1):
                # Check and remove left-side numbers if they exist
                if line.strip().isdigit() or (line.strip()[:-1].isdigit() and line.strip()[-1] in [" ", "\n"]):
                    continue  # Skip the line number
                line_count += 1
                print(f"Page {page_number}, Line {line_count}: {line}")
    return line_count

# pdf_path = "/mnt/data/pdf (5).pdf"
pdf_path = "pdf (5).pdf"
total_lines = count_lines_excluding_numbers(pdf_path)
print(f"Total meaningful lines in PDF: {total_lines}")


# line_text = " ".join([span['text'] for span in line['spans']]).strip()  
                        # if line_text.isdigit() or (line_text[:-1].isdigit() and line_text[-1] in [" ", "\n"]):
                        #     continue  # Skip lines that are just numbers
