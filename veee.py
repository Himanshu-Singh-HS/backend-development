from io import BytesIO
from PIL import Image

 
def image_to_bytes(image_path: str) -> bytes:
    
    image = Image.open(image_path)
    
    
    img_byte_arr = BytesIO()
    
   
    image.save(img_byte_arr, format='PNG')
    
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()

 
def bytes_to_image(img_bytes: bytes, output_path: str) -> None:
   
    img_byte_arr = BytesIO(img_bytes)
    image = Image.open(img_byte_arr)
    
    
    image.save(output_path)

  
img_bytes = image_to_bytes("wss.png")
print("img_bytes",img_bytes)
# bytes_to_image(img_bytes,"ans.png")

# import boto3
# from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# def upload_to_s3(binary_data, bucket_name, file_name, region="us-east-1"):
#     try:
       
#         s3_client = boto3.client("s3", region_name=region)
        
#         # Upload the binary data to the specified S3 bucket
#         s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=binary_data) 

       
#         s3_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{file_name}"
        
#         return s3_url

#     except (NoCredentialsError, PartialCredentialsError) as e:
#         print("AWS credentials are not configured properly.")
#         return None
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None


# if __name__ == "__main__":
  
#     binary_data = b"example binary data here"  
    
#     bucket_name = "your-s3-bucket-name"
#     file_name = "example_file.bin"

#     # Upload and generate S3 link 
#     s3_link = upload_to_s3(binary_data, bucket_name, file_name)
#     if s3_link:
#         print(f"File uploaded successfully! Access it here: {s3_link}")
































# print("img_bytes",img_bytes)a
# bytes_to_image(img_bytes, "output_image.png")
# from io import BytesIO
# from PIL import Image
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from reportlab.lib.utils import ImageReader


# def image_to_bytes(image_path: str) -> bytes:
#     image = Image.open(image_path)
#     img_byte_arr = BytesIO()
#     image.save(img_byte_arr, format='PNG')
#     img_byte_arr.seek(0)
#     return img_byte_arr.getvalue()


# # Function to generate PDF using ReportLab
# def generate_pdf_with_image(image_bytes: bytes, output_pdf_path: str):
#     # Wrap bytes in a BytesIO object
#     img_stream = BytesIO(image_bytes)

#     # Create an ImageReader object
#     try:
#         img_reader = ImageReader(img_stream)
#     except Exception as e:
#         print(f"Error reading image: {e}")
#         return

#     # Create a PDF
#     c = canvas.Canvas(output_pdf_path, pagesize=letter)

#     try:
#         # Draw the image on the PDF
#         c.drawImage(img_reader, x=100, y=500, width=200, height=200)
#         print("Image added to PDF successfully.")
#     except Exception as e:
#         print(f"Error adding image to PDF: {e}")

#     c.save()
#     print(f"PDF created successfully: {output_pdf_path}")


# image_bytes = image_to_bytes("wss.png")
# generate_pdf_with_image(image_bytes, "output_with_image.pdf")

 
