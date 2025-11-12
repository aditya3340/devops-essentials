#!/bin/bash

set -euo pipefail

BUCKET_NAME=${1:-} #name param for the user
BUCKET_REGION=${2:-"us-east-1"} #region for the bucket

#validations
if [[ -z "$BUCKET_NAME" ]];then
	echo "Error: Bucket name not provided."
	echo "Usage: $0 <bucket_name> [region]"
	exit 1
fi



#create bucket for terraform backend with object locking enabled
if [ "$BUCKET_REGION" = "us-east-1" ];then
	aws s3api create-bucket \
		--bucket "$BUCKET_NAME" \
		--region "$BUCKET_REGION" \
		--object-lock-enabled-for-bucket
else
	aws s3api create-bucket \
		--bucket "$BUCKET_NAME" \
		--region "$BUCKET_REGION" \
		--create-bucket-configuration LocationConstraint="$BUCKET_REGION" \
		--object-lock-enabled-for-bucket
fi

echo "Bucket created successfully."

#enable versioning for the bucket
aws s3api put-bucket-versioning \
	--bucket "$BUCKET_NAME" \
	--versioning-configuration Status=Enabled

echo "Bucket '$BUCKET_NAME' successfully created in region: '$BUCKET_REGION'"
