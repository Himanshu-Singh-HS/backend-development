import boto3

def update_content_disposition(bucket_name, object_key):
    s3 = boto3.client('s3', 
                      aws_access_key_id=MONOLITH_AWS_ACCESS_KEY_ID, 
                      aws_secret_access_key=MONOLITH_AWS_SECRET_ACCESS_KEY, 
                      region_name=MONOLITH_AWS_DEFAULT_REGION)

    try:
        # Copy the object with new metadata (Content-Disposition)
        s3.copy_object(
            Bucket=bucket_name,
            Key=object_key,
            CopySource={'Bucket': bucket_name, 'Key': object_key},
            MetadataDirective='REPLACE',  # This tells S3 to replace metadata
            ContentDisposition='attachment; filename="wss.png"'  # Forces download
        )
        print(f"Successfully updated Content-Disposition for {object_key}")
    except Exception as e:
        print(f"Error updating metadata: {e}")

# Example usage
bucket_name = 'patentdraftingtest'
object_key = 'images/wss.png'

update_content_disposition(bucket_name, object_key)
