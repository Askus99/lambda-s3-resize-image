import boto3
import urllib
from PIL import Image
import io
import json

s3_client = boto3.client('s3')

def resize_image(image_data, max_size=(300, 300)):
    with Image.open(io.BytesIO(image_data)) as img:
        img.thumbnail(max_size)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img.format)
        return img_byte_arr.getvalue()
        
def lambda_handler(event, context):
    # Get the object from the event and show its content type
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    destination_bucket = 'result-image-bucket-1'
    
    # Download the image from S3
    response = s3_client.get_object(Bucket=source_bucket, Key=source_key)
    image_data = response['Body'].read()
    
    # Resize the image
    try:
        resized_image_data = resize_image(image_data)
        # Upload the resized image to the destination bucket
        s3_client.put_object(Bucket=destination_bucket, Key=source_key, Body=resized_image_data, ContentType='image/jpeg')
    except Exception as e:
        return f"error : {e}"
    
    
    return {
        'statusCode': 200,
        'body': 'all good'
    }

