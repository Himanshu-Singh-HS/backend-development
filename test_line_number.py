from docx import Document
from docx.shared import Pt, Cm

def add_line_numbers(doc_path, output_path, line_spacing=1.5):
    # Load the document
    doc = Document(doc_path)

    line_number = 1

    # Iterate over each paragraph
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():  # Skip empty paragraphs
            # Add line number to the paragraph
            paragraph.text = f"{line_number}. {paragraph.text}"

            # Set font and style for line numbers
            for run in paragraph.runs:
                run.font.size = Pt(11)  # Adjust font size as needed

            # Increase line number
            line_number += 1

            # Set left indentation to simulate the line number in margin
            paragraph.paragraph_format.left_indent = Cm(1.5)  # Adjust as needed for margin

            # Set line spacing
            paragraph.paragraph_format.line_spacing = line_spacing

    # Save the modified document
    doc.save(output_path)
    print(f"Document saved with line numbers at {output_path}")

# Example usage
add_line_numbers("EPdoc.doc", "output_with_line_numbers.docx")
