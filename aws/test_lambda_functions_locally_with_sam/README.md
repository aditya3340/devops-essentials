# Test AWS Lambda Locally Using AWS SAM

## 🧩 What Is AWS Lambda?

AWS Lambda is a **serverless computing service** that lets you run code without provisioning or managing servers. Your code runs in response to events such as HTTP requests, S3 uploads, or scheduled triggers, and AWS automatically manages scaling, availability, and resource allocation.

---

## ⚙️ What Is AWS SAM (Serverless Application Model)?

**AWS SAM** is an open-source framework built on top of **AWS CloudFormation** that simplifies the process of defining, building, and deploying serverless applications.
It allows you to:

* Define Lambda functions, APIs, and permissions in a single YAML template.
* Build and test applications locally.
* Deploy them easily to AWS.

---

## 🧰 SAM CLI Overview

The **AWS SAM CLI** is a developer tool for:

* Building serverless applications.
* Running and debugging Lambda functions locally.
* Packaging and deploying to AWS.

---

## 📦 Prerequisites

Make sure you have the following installed:

1. **AWS CLI**
   Used to configure your AWS credentials and access resources.

   ```bash
   aws configure
   ```

2. **Docker**
   Required because SAM uses Docker containers to emulate Lambda runtimes locally.

3. **AWS SAM CLI**
   Follow the official installation guide:
   [https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

---

## 🚀 Step-by-Step: Running Lambda Locally

### 1. Initialize a New SAM Application

Run:

```bash
sam init
```

You’ll be prompted to select:

* A template (e.g., Hello World example)
* Runtime (e.g., Python 3.12)
* Application name (e.g., sam-app)

---

### 2. Build the Application

Navigate to your project folder and build it:

```bash
cd sam-app
sam build
```

This compiles your source code and installs dependencies listed in `requirements.txt`.
The built artifacts are stored under:

```
.aws-sam/build/<function-name>/
```

---

### 3. Create a Test Event

Create an event file to simulate input to your Lambda:

```bash
echo '{ "key": "value" }' > event.json
```

---

### 4. Invoke the Lambda Locally

Run the following command:

```bash
sam local invoke "LambdaFunction" -e event.json --docker-network host
```

**Explanation:**

* `sam local invoke` — Runs the Lambda inside a local Docker container.
* `-e event.json` — Passes test input data.
* `--docker-network host` — Shares your local network, allowing the container to use **AWS credentials** from your host machine to access services like S3 or DynamoDB.

Sample Output:

```
Invoking lambda_function.lambda_handler (python3.12)
Using local image: public.ecr.aws/lambda/python:3.12-rapid-x86_64.
Mounting /home/kumar/sam-demo/sam-app/.aws-sam/build/LambdaFunction as /var/task inside container
START RequestId: ...
demo-aditya3340-bucket
END RequestId: ...
REPORT RequestId: ... Duration: 1908 ms Memory Size: 128 MB
"Hello from Drift Detector"
```

---

### 5. Testing Different Projects

To test another project:

1. Run `sam init` in that project’s root directory.
2. Adjust the `template.yaml` according to your Lambda handler.

**Example `template.yaml`:**

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  MyLambdaFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: lambda/
      Handler: lambda_function.lambda_handler
      Runtime: python3.12
      Architectures:
        - x86_64
      Events:
        HelloWorld:
          Type: Api
          Properties:
            Path: /hello
            Method: get
```

---

## 💡 Notes

* You can include additional libraries not preinstalled in the Lambda Docker image by adding them to `requirements.txt` before running `sam build`.
* The `--docker-network host` flag is crucial when your Lambda needs access to AWS services using your local credentials.

---

**✅ You can now build, test, and debug your AWS Lambda functions locally using SAM before deploying to AWS.**

