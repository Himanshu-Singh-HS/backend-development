# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from io import BytesIO

# # Example: Load binary data for a valid PNG image
# # Replace this with the actual binary data
# binary_image_data = (
#     b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\x00\x00\x00'
#     b'\x00\x00\x90wS\xde\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReadyq\xc9e<\x00\x00\x00xIDAT'
#     b'\x08\xd7c\xf8\x0f\x04\x0c\x00\xb2\xc1m\x80\xf5\xff\xc8\xf4\x00\xd1\xd5F\xab\xd5\x0e\xe3'
#     b'\x00\x00\x00\x00IEND\xaeB`\x82'
# )
 
# # Wrap binary data in a BytesIO object
# image_stream = BytesIO(binary_image_data)

# # Create a PDF
# output_pdf_path = "drafting-new-changes/output_fixed.pdf"
# c = canvas.Canvas(output_pdf_path, pagesize=letter)

# try:
#     # Draw the binary image in the PDF
#     c.drawImage(image_stream, x=100, y=50, width=20, height=20)
#     print("Image added to PDF successfully.")
# except Exception as e:
#     print(f"Error adding image: {e}")

# # Save the PDF
# c.save()
# print(f"PDF created successfully: {output_pdf_path}")
# # with open("test_image.png", "wb") as f:
# #     f.write(binary_image_data)
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO

# Example: Load binary data for a valid PNG image
binary_image_data = (
    b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\x00\x00\x00'
    b'\x00\x00\x90wS\xde\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReadyq\xc9e<\x00\x00\x00xIDAT'
    b'\x08\xd7c\xf8\x0f\x04\x0c\x00\xb2\xc1m\x80\xf5\xff\xc8\xf4\x00\xd1\xd5F\xab\xd5\x0e\xe3'
    b'\x00\x00\x00\x00IEND\xaeB`\x82'
)
# Save binary data to a file for debugging
with open("test_image.png", "wb") as f:
    f.write(binary_image_data)

print("Saved test_image.png for verification.")


# # Wrap binary data in a BytesIO object
# image_stream = BytesIO(binary_image_data)

# # Use ImageReader to read the binary image data
# image_reader = ImageReader(image_stream)

# # Create a PDF
# output_pdf_path = "output_fixed.pdf"
# c = canvas.Canvas(output_pdf_path, pagesize=letter)

# try:
#     # Draw the binary image in the PDF using ImageReader
#     c.drawImage(image_reader, x=100, y=500, width=200, height=200)
#     print("Image added to PDF successfully.")
# except Exception as e:
#     print(f"Error adding image: {e}")

# # Save the PDF
# c.save()
# print(f"PDF created successfully: {output_pdf_path}")
