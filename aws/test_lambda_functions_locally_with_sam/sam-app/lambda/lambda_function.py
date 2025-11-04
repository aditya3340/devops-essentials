import boto3, botocore


def lambda_handler(event, handler):
    
    s3 = boto3.resource('s3')
    
    for bucket in s3.buckets.all():
        print(bucket.name)
    
    return 'Hello from drift Detector'