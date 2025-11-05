#!/bin/bash

set -euo pipefail

REGION="us-east-1"
TOPIC_NAME="terraform-drift"

echo "[INFO]: Looking for SNS Topic ARN for $TOPIC_NAME"
TOPIC_ARN=$(aws sns list-topics --region "$REGION" --query "Topics[?contains(TopicArn, '$TOPIC_NAME')].TopicArn" --output text)

if [ -z "$TOPIC_ARN" ]; then
	echo "[WARN]: No sns topic found with name '$TOPIC_NAME'."
	exit 0
fi

echo "[INFO]: Found SNS Topic ARN: $TOPIC_ARN"

#Deleting all subscription for the topic

SUBSCRIPTION_ARNS=$(aws sns list-subscriptions-by-topic \
	--topic-arn "$TOPIC_ARN" \
	--region "$REGION" \
	--query "Subscriptions[].SubscriptionArn" \
	--output text)

if [ -z "$SUBSCRIPTION_ARNS" ]; then
	echo "[INFO]: No subscriptions found for the topic '$TOPIC_NAME'"
else
	echo "[INFO]: Deleting Subscriptions..."
	for SUB_ARN in $SUBSCRIPTION_ARNS; do
		if [ "$SUB_ARN" != "PendingConfirmation" ]; then
			echo " - Deleting subscription: $SUB_ARN"
			aws sns unsubscribe --subscription-arn "$SUB_ARN" --region "$REGION" > /dev/null
		else
			echo " - Skipping 'PendingConfirmation' subscription."
		fi
	done
fi

echo "[INFO]: Deleting SNS Topic '$TOPIC_NAME'..."
aws sns delete-topic --topic-arn "$TOPIC_ARN" --region "$REGION"

echo "[INFO]: SNS Topic '$TOPIC_NAME' and its subscriptions have been deleted successfully."




