from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def create_pdf_with_multilingual_text(output_path):
    c = canvas.Canvas(output_path, pagesize=A4)

    # Use CIDFont for CJK text
    c.setFont("HeiseiMin-W3", 12)

    # Draw Korean and Chinese text
    korean_text = "위르겐 헤레엠마누엘 하베츠 세바스찬 슐레흐트 알렉산더 아다미"
    chinese_text = "中国是一个拥有悠久历史的国家"
    combined_text = korean_text + " " + chinese_text

    # Write the text to the PDF
    c.drawString(100, 750, combined_text)

    # Save the PDF
    c.save()

# Generate PDF
create_pdf_with_multilingual_text("multilingual_text.pdf")
