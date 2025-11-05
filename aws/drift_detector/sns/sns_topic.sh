#!/bin/bash

EMAIL_ID="kumar.aditya3340@gmail.com"
REGION="us-east-1"

echo "[INFO]: Creating SNS Topic..."
aws sns create-topic \
	--name terraform-drift \
	--region $REGION \
	--output json > topic_arn.json

if [ $? -ne 0 ]; then
	echo "[ERROR]: Unable to create SNS Topic Error: ($?)"
	exit 1
fi


ARN=$(jq -r '.TopicArn' topic_arn.json)
echo "[INFO]: SNS Topic is Created with ARN: $ARN"

echo "[INFO]: Creating Test Subscription for EMAIL: $EMAIL_ID"

aws sns subscribe \
	--topic-arn "$ARN" \
	--protocol email \
	--region $REGION \
	--notification-endpoint "$EMAIL_ID" > /dev/null
if [ $? -ne 0 ]; then
	echo "[ERROR]: Unable to create Subscription for $EMAIL_ID in SNS TOPIC $ARN."
	exit 1
fi

echo "[INFO]: Subscription for $EMAIL_ID have been successfully created. Please Check your email-id for confirmation!"

