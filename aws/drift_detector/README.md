A system that automatically detects “drift” — when your actual AWS infrastructure doesn’t match your Terraform configuration — and notifies you (or your team) via Slack or email.


🎯 Goals

✅ Detect real-time or scheduled drift between Terraform and AWS
✅ Report drift to a Slack channel or SNS topic
✅ Optionally auto-correct minor drifts (e.g., tags, missing policies)
✅ Use IaC (Terraform) + automation (Lambda/GitHub Actions)