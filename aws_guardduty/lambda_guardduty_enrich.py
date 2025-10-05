"""
Lambda: GuardDuty Custom Finding Enrichment
Author: Elhadji Fallou Ndiaye
Description:
Receives GuardDuty findings from EventBridge, enriches data, stores to S3, and publishes to SNS.
Safe for demo and non-destructive.
"""

import json
import boto3
import datetime
import os

s3_client = boto3.client("s3")
sns_client = boto3.client("sns")

BUCKET = os.environ.get("EVIDENCE_BUCKET", "my-guardduty-evidence-bucket")
SNS_TOPIC = os.environ.get("SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:guardduty-alerts")

def lambda_handler(event, context):
    print("[INFO] Event received at", datetime.datetime.utcnow().isoformat())
    findings = event.get("detail", {})

    finding_id = findings.get("id", "unknown")
    severity = findings.get("severity", 0)
    title = findings.get("title", "No title")
    resource = findings.get("resource", {}).get("resourceType", "N/A")

    # Create summary
    summary = {
        "finding_id": finding_id,
        "title": title,
        "severity": severity,
        "resource": resource,
        "time": datetime.datetime.utcnow().isoformat()
    }

    # Store evidence in S3
    file_key = f"guardduty/findings/{finding_id}_{datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%S')}.json"
    s3_client.put_object(Bucket=BUCKET, Key=file_key, Body=json.dumps(event))
    print(f"[INFO] Stored finding evidence to s3://{BUCKET}/{file_key}")

    # Publish summary to SNS
    sns_client.publish(
        TopicArn=SNS_TOPIC,
        Message=json.dumps(summary),
        Subject=f"GuardDuty Finding - Severity {severity}"
    )
    print("[INFO] Published alert summary to SNS")

    return {"status": "processed", "finding_id": finding_id, "severity": severity}
