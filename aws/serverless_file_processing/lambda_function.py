import boto3
import uuid
from urllib.parse import unquote_plus
from pypdf import PdfReader, PdfWriter


s3_client = boto3.client('s3')

def lambda_handler(event, context):

    #iterate over the s3 event object and get the key for all uploaded files
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        download_path = f'/tmp/{uuid.uuid4()}.pdf'
        upload_path = f'/tmp/converted-{uuid.uuid4}.pdf'


        if key.lower().endswith('.pdf'):
            s3_client.download_file(bucket, key, download_path)
            encrypt_pdf(download_path, upload_path)
            encrypted_key = add_encrypted_suffix(key)
            #upload to the encrypted bucket
            s3_client.upload_file(upload_path, f'amzn-encrypted-pdf-s3-bucket', encrypted_key)


def encrypt_pdf(file_path, encrypted_file_path):

    reader = PdfReader(file_path)

    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    #add password to the new pdf
    writer.encrypt("my-secret-password")

    #save the new pdf to a file
    with open(encrypted_file_path, "wb") as file:
        writer.write(file)


def add_encrypted_suffix(orignal_key):
    filename, extension = orignal_key.rsplit('.', 1)

    return f'{filename}_encrypted.{extension}'





# arn:aws:iam::682033480771:role/LambdaS3Role