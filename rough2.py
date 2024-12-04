# import base64
# import boto3
# from botocore.exceptions import NoCredentialsError
# from io import BytesIO
# from PIL import Image




 
# def image_to_bytes(image_path: str) -> bytes:
    
#     image = Image.open(image_path)
    
    
#     img_byte_arr = BytesIO()
    
   
#     image.save(img_byte_arr, format='PNG')
    
#     img_byte_arr.seek(0)
#     return img_byte_arr.getvalue()

# img_bytes = image_to_bytes("wss.png")

# def upload_base64_to_s3(base64_string, bucket_name, s3_object_key, region='us-east-1'):
#     # Decode the base64 string to bytes
#     file_data = base64.b64decode(base64_string)
    
#     # Initialize S3 client
#     s3_client = boto3.client('s3', 
#                              aws_access_key_id=MONOLITH_AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=MONOLITH_AWS_SECRET_ACCESS_KEY,
#     region_name=MONOLITH_AWS_DEFAULT_REGION,
#     region_name=region)

#     try:
#         # Upload the file to S3
#         s3_client.put_object(Bucket=bucket_name, Key=s3_object_key, Body=file_data)
        
#         # Generate the S3 URL (public URL if the object is publicly accessible)
#         s3_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{s3_object_key}"
#         return s3_url
    
#     except NoCredentialsError:
#         return "Credentials not available."
#     except Exception as e:
#         return str(e)

# # Usage example
# base64_string = "your_base64_encoded_data_here"
# bucket_name = "your-s3-bucket-name"
# s3_object_key = "your/object/key/filename.ext"

# url = upload_base64_to_s3(base64_string, bucket_name, s3_object_key)
# print("S3 URL:", url)



import boto3
from botocore.exceptions import NoCredentialsError

from io import BytesIO
from PIL import Image


 
def get_s3_client():
    return s3_client


# method definitions ==========================================================
def get_s3_client():
    return s3_client


# Initialize the S3 client with your AWS credentials
 

# Convert image to bytes
def image_to_bytes(image_path: str) -> bytes:
    image = Image.open(image_path)
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()

# Function to upload image to S3 and return the URL
def upload_image_to_s3(img_bytes: bytes, bucket_name: str, object_key: str) -> str:
    try:
        # Initialize the S3 client
        # s3 = init_s3_client()
        s3 = get_s3_client()

        # Upload the image to S3
        s3.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=img_bytes,
            # ContentType='image/png',
            #  ContentDisposition='attachment; filename="wss.png"', 
            # ACL='public-read'  # Make the image publicly accessible
        )

        # Generate the S3 URL
        s3_url = f'https://{bucket_name}.s3.amazonaws.com/{object_key}'
        return s3_url
    except NoCredentialsError:
        print("Credentials not available")
        return None
    except Exception as e:
        print(f"Error uploading image to S3: {e}")
        return None

# Example usage
image_path = "wss.png"
bucket_name = "patentdraftingtest"  # Replace with your actual bucket name
object_key = "images/wss.png"  # You can customize the object path

# Convert the image to bytes
img_bytes = image_to_bytes(image_path)

# Upload the image to S3 and get the public URL
s3_url = upload_image_to_s3(img_bytes, bucket_name, object_key)

if s3_url:
    print(f"Image uploaded successfully. Access it here: {s3_url}")




#  for feature, url in zip(search_parameters.user_figure_features, s3_urls):
#         feature.fig_url.append(url)
#     # existing_report.save_changes()
#     existing_request.save_changes()