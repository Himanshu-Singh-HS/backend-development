# import base64
# import boto3
# from botocore.exceptions import NoCredentialsError



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


import requests

url = 'http://localhost:8000/api/v1/drafting/test_create_draft'

headers = {
    'accept': 'application/json',
    'Content-Type': 'multipart/form-data'
}

# Data to be sent in the search_parameters field
search_parameters = {
    "novelty": "string",
    "jurisdiction": "US",
    "abstract": "",
    "user_figure_features": [],
    "uploaded_classes": [],
    "component_start_number": 0,
    "uploaded_ucids": [],
    "problem_statement": "string",
    "project_title": "",
    "drafting_type": "DRAFTING",
    "user_figures": [
        {
            "figure_number": 0,
            "binary_data": "string"
        }
    ],
    "keyfeatures": "",
    "invention_disclosure": "string"
}

# Files to be uploaded
files = {
    'files': ('a84145d2-bba6-11ef-b1a2-0a58a9feac02_Fig1_page_0.png', open('a84145d2-bba6-11ef-b1a2-0a58a9feac02_Fig1_page_0.png', 'rb'), 'image/png'),
}

# Sending the POST request
response = requests.post(url, headers=headers, data={'search_parameters': str(search_parameters)}, files=files)

# Print response status and content
print(f'Status Code: {response.status_code}')
print(f'Response: {response.text}')
