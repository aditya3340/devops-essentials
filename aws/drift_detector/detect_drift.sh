#!/bin/bash
set -euo pipefail

# --- Config ---
WORKDIR="/app"
TMP_DIR="/tmp"
PLAN_FILE="$TMP_DIR/plan_output.txt"
CACHE_DIR="$TMP_DIR/plugin-cache"
STATE_FILE="$TMP_DIR/terraform.tfstate"
S3_STATE_BUCKET="<terraform-backend-s3-bucket-name>"
S3_STATE_KEY="dev/terraform.tfstate"
SNS_TOPIC_ARN="<your-sns-topic-arn>"

DATE_TAG=$(date +%F-%H%M%S)

# --- Environment setup ---
export TF_PLUGIN_CACHE_DIR="$CACHE_DIR"
mkdir -p "$CACHE_DIR"
cd "$WORKDIR"

echo "[INFO] Starting Terraform drift detection at $DATE_TAG"

# --- Step 1: Fetch remote state (optional for speed) ---
echo "[INFO] Fetching remote state..."
aws s3 cp "s3://$S3_STATE_BUCKET/$S3_STATE_KEY" "$STATE_FILE" > /dev/null 2>&1 || true

# --- Step 2: Ensure backend initialized ---
echo "[INFO] Initializing Terraform backend..."
if [ -d "/tmp/.terraform"]; then
	echo "[INFO] Using cached Terraform init"
	cp -r /tmp/.terraform ./
else
	terraform init -backend=true -input=false -reconfigure > /dev/null
	cp -r .terraform /tmp/.terraform
fi

# --- Step 3: Run Terraform plan ---
echo "[INFO] Running Terraform plan..."
set +e
terraform plan \
  -detailed-exitcode \
  -no-color \
  -input=false 2>&1 | tee "$PLAN_FILE"
EXIT_CODE=${PIPESTATUS[0]}
set -e

# --- Step 4: Handle results ---
case $EXIT_CODE in
  0)
    echo "[RESULT] No drift detected"
    ;;
  2)
    echo "[RESULT] Drift detected!"
    echo "[INFO] Sending drift details to SNS..."

    DRIFT_LOG=$(tail -c 250000 "$PLAN_FILE" | sed 's/"/\\"/g')
    aws sns publish \
      --topic-arn "$SNS_TOPIC_ARN" \
      --subject "Terraform Drift Detected - $DATE_TAG" \
      --message "$DRIFT_LOG" \
      > /dev/null
    ;;
  *)
    echo "[ERROR]: Terraform plan failed (exit code: $EXIT_CODE)"
    ;;
esac

echo "[INFO] Drift check completed at $(date +%T)"
