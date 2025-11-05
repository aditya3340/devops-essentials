#!/bin/bash

set -euo pipefail


BUCKET_NAME=${1:-}

# --- Validation ---
if [[ -z "$BUCKET_NAME" ]]; then
  echo "Error: Bucket name not provided."
  echo "Usage: $0 <bucket-name>"
  exit 1
fi

echo "Cleaning up S3 bucket: $BUCKET_NAME ..."

# Delete all object versions
aws s3api list-object-versions \
  --bucket "$BUCKET_NAME" \
  --output text \
  --query 'Versions[].{Key:Key,VersionId:VersionId}' |
  grep -v '^$' |
while read -r Key VersionId; do
  if [[ -n "$VersionId" && -n "$Key" ]]; then
    aws s3api delete-object --bucket "$BUCKET_NAME" --key "$Key" --version-id "$VersionId"
  fi
done


# Delete all delete markers
aws s3api list-object-versions \
  --bucket "$BUCKET_NAME" \
  --output text \
  --query 'DeleteMarkers[].{Key:Key,VersionId:VersionId}' |
  grep -v '^$' |
while read -r Key VersionId; do
  if [[ -n "$VersionId" && -n "$Key" ]]; then
    aws s3api delete-object --bucket "$BUCKET_NAME" --key "$Key" --version-id "$VersionId"
  fi
done

aws s3 rb "s3://$BUCKET_NAME"