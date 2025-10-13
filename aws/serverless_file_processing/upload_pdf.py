import boto3
import hashlib

s3_client = boto3.client('s3')

def upload_pdf():
    
    response = s3_client.list_buckets()

    all_buckets = response['Buckets']

    bucket_name = f"{all_buckets[0]['Name']}"
    file_path = 'pass.pdf'
    s3_key = 'remote_file.pdf'

    local_md5 = md5(file_path)

    # upload file

    try:
        head = s3_client.head_object(Bucket=bucket_name, Key=s3_key)

        if head["ETag"].strip('"') == local_md5:
            print("File is already exists with the same content. Skipping upload.")

        else:
            s3_client.upload_file(file_path, bucket_name, s3_key)
            print(f"File '{file_path}' is uploaded to '{bucket_name}/{s3_key}' sucessfully...")

    except s3_client.exceptions.ClientError:
        # Object doesn’t exist
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"File '{file_path}' is uploaded to '{bucket_name}/{s3_key}' sucessfully...")


def md5(file_path):
    with open(file_path, "rb") as file:
        return hashlib.md5(file.read()).hexdigest()
    

upload_pdf()
