# Deploying a Python AWS Lambda Function Using a Container Image

This guide walks you through deploying a Python AWS Lambda function packaged as a Docker container image.

## Prerequisites

Ensure you have the following installed:

- **AWS CLI** (version 2 or later)
- **Docker** (version 25.0.0 or later)
- **Docker Buildx** plugin
- **Python** (version 3.8 or later)

## Steps

### 1. Set Up Your Project Directory

Create and navigate to your project directory:

```bash
mkdir my-lambda-function
cd my-lambda-function
```

### 2. Create the Lambda Function Code

Create a file named `lambda_function.py` with the following content:

```python
import sys

def handler(event, context):
    return f"Hello from AWS Lambda using Python {sys.version}!"
```

### 3. Define Dependencies

If your function has dependencies, list them in a `requirements.txt` file. For this example, leave it empty.

```bash
touch requirements.txt
```

### 4. Create the Dockerfile

Create a `Dockerfile` with the following content:

```dockerfile
# Use the AWS Lambda Python 3.12 base image
FROM public.ecr.aws/lambda/python:3.12

# Copy the requirements.txt and install dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

# Copy the Lambda function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD [ "lambda_function.handler" ]
```

### 5. Build the Docker Image

Build the Docker image:

```bash
docker buildx build --platform linux/amd64 -t my-lambda-image .
```

### 6. Push the Image to Amazon ECR

#### 6.1. Create an ECR Repository

```bash
aws ecr create-repository --repository-name my-lambda-repo --region us-east-1
```

#### 6.2. Authenticate Docker to ECR

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin account_id.dkr.ecr.us-east-1.amazonaws.com
```

#### 6.3. Tag and Push the Image

```bash
docker tag my-lambda-image:latest account_id.dkr.ecr.us-east-1.amazonaws.com/my-lambda-repo:latest
docker push account_id.dkr.ecr.us-east-1.amazonaws.com/my-lambda-repo:latest
```

### 7. Create an IAM Role for Lambda

Your Lambda function needs an **execution role** with the right permissions.

#### 7.1. Create a Trust Policy

Save the following JSON as `trust-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

#### 7.2. Create the IAM Role

```bash
aws iam create-role   --role-name my-lambda-execution-role   --assume-role-policy-document file://trust-policy.json
```

#### 7.3. Attach AWS Managed Policies

Attach the basic execution role and ECR read permissions:

```bash
aws iam attach-role-policy   --role-name my-lambda-execution-role   --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam attach-role-policy   --role-name my-lambda-execution-role   --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
```

### 8. Create the Lambda Function

```bash
aws lambda create-function   --function-name my-lambda-function   --package-type Image   --code ImageUri=account_id.dkr.ecr.us-east-1.amazonaws.com/my-lambda-repo:latest   --role arn:aws:iam::account_id:role/my-lambda-execution-role   --region us-east-1
```

### 9. Invoke the Lambda Function

```bash
aws lambda invoke   --function-name my-lambda-function   --payload '{}'   response.json
```

### 10. Update the Lambda Function Code

To update the function with a new image:

```bash
aws lambda update-function-code   --function-name my-lambda-function   --image-uri account_id.dkr.ecr.us-east-1.amazonaws.com/my-lambda-repo:latest   --publish
```

---

## Additional Resources

- [Deploy Python Lambda functions with container images](https://docs.aws.amazon.com/lambda/latest/dg/python-image.html)
- [AWS base images for Python](https://gallery.ecr.aws/lambda/python)
- [Using an alternative base image with the runtime interface client](https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-custom-runtime)
