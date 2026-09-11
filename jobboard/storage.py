# import os

# STORAGE_DIR = os.environ.get('PDF_STORAGE_DIR', 'storage/applications')

# def save_pdf(filename, pdf_bytes):
#     os.makedirs(STORAGE_DIR, exist_ok=True)
#     file_path = os.path.join(STORAGE_DIR, filename)
#     with open(file_path, 'wb') as f:
#         f.write(pdf_bytes)
    
#     return file_path

import boto3
from flask import current_app

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=current_app.config['S3_ENDPOINT_URL'],
        aws_access_key_id=current_app.config['S3_ACCESS_KEY'],
        aws_secret_access_key=current_app.config['S3_SECRET_KEY'],
    )

def ensure_bucket_exists():
    s3 = get_s3_client()
    bucket = current_app.config['S3_BUCKET_NAME']
    existing_buckets = [b['Name'] for b in s3.list_buckets()['Buckets']]
    if bucket not in existing_buckets:
        s3.create_bucket(Bucket=bucket)

def save_pdf(filename, pdf_bytes):
    s3 = get_s3_client()
    bucket = current_app.config['S3_BUCKET_NAME']
    ensure_bucket_exists()

    s3.put_object(
        Bucket=bucket,
        Key=filename,
        Body=pdf_bytes,
        ContentType='application/pdf',
    )

    return f"{current_app.config['S3_ENDPOINT_URL']}/{bucket}/{filename}"