import base64
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


# Encode image as Base64 string
def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

 
def decode_base64_to_binary(base64_string: str) -> BytesIO:
    binary_data = base64.b64decode(base64_string)
    return BytesIO(binary_data)


 
def generate_pdf_with_base64_image(base64_string: str, output_pdf_path: str):
   
    image_stream = decode_base64_to_binary(base64_string)

 
    img_reader = ImageReader(image_stream)

 
    pdf_canvas = canvas.Canvas(output_pdf_path, pagesize=letter)

    
    try:
        pdf_canvas.drawImage(img_reader, x=100, y=500, width=200, height=200)
        print("Image added to PDF successfully.")
    except Exception as e:
        print(f"Error adding image to PDF: {e}")
    
    # Save the PDF
    pdf_canvas.save()
    print(f"PDF saved as: {output_pdf_path}")



base64_image = encode_image_to_base64("wss.png")
print("base64_image->-.>",base64_image)

 
generate_pdf_with_base64_image(base64_image, "output_with_base64_image.pdf")
