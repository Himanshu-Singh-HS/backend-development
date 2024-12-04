# # Inventor위르겐 헤레엠마누엘 하베츠세바스찬 슐레흐트알렉산더 아다미


# from reportlab.pdfgen import canvas
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.lib.pagesizes import A4

# # Step 1: Register Korean font
# try:
#  pdfmetrics.registerFont(TTFont('NotoSansKR', 'korea/NotoSansKR.ttf'))
# except Exception as e:
#     print("error here ",e)

# # Step 2: Create a PDF
# def create_pdf_with_korean_text(output_path):
#     c = canvas.Canvas(output_path, pagesize=A4)

#     # Use the registered Korean font
#     c.setFont('NotoSansKR', 12)

#     # Draw Korean text
#     korean_text = "Th 대한민국, 中国, 日本, and Россия   대한민국 (Korea) is celebrated for its innovative technology and vibrant K-culture. भारत (India) mesmerizes the world with its rich history, spirituality, and vibrant festivals. 中国 (China), with its deep-rooted traditions, is a powerhouse of innovation and resilience. 日本 (Japan) blends ancient wisdom with futuristic ideas, creating a harmonious balance of tradition and modernity. Россия (Russia) enchants with its vast landscapes, classical art, and enduring spirit. Together, these nations shape a world full of diversity and unity. "
    
#     c.drawString(100, 750, korean_text)

#     # Save the PDF
#     c.save()

# # Generate PDF
# create_pdf_with_korean_text("korean_text.pdf")
# print("sucessfully created pdf ")


from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

# Step 1: Register a font that supports both Korean and Chinese characters
# pdfmetrics.registerFont(TTFont('NotoSansCJK', 'NotoSansCJK-Regular.ttf'))

# Step 1: Register Korean font
try:
#  pdfmetrics.registerFont(TTFont('NotoSansKR', 'korea/NotoSansKR.ttf'))
   pdfmetrics.registerFont(TTFont('NotoSansCJK', 'korea/NotoSansCJKsc-Regular.ttf'))  
except Exception as e:
    print("error here ",e)
# Step 2: Create a PDF
def create_pdf_with_multilingual_text(output_path):
    c = canvas.Canvas(output_path, pagesize=A4)

    # Use the registered font
    c.setFont('NotoSansCJK', 12)

    # Draw Korean and Chinese text
    korean_text = "위르겐 헤레엠마누엘 himanhsu singh"
    chinese_text = "中国是一个拥有悠久历史的国家"
    combined_text = korean_text + " " + chinese_text

    # Write the text to the PDF
    c.drawString(100, 750, combined_text)

    # Save the PDF
    c.save()

# Generate PDF
create_pdf_with_multilingual_text("multilingual_text.pdf")
