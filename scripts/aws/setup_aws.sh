#!/bin/bash
"""
AWS Setup Script for Citibikes Cloud Analytics

This script sets up the complete AWS infrastructure for the
Citibikes data pipeline cloud analytics.
"""

set -e

echo "☁️ Setting up AWS Cloud Analytics for Citibikes..."

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS CLI is not configured."
    echo "Please run 'aws configure' and set up your credentials."
    exit 1
fi

# Load environment variables
echo "📋 Loading AWS configuration..."
source config/aws_config.env

# Create S3 bucket
echo "🪣 Creating S3 bucket..."
python src/aws/create_s3_bucket.py

# Create IAM role
echo "🔐 Creating IAM role for Glue..."
python src/aws/create_glue_role.py

# Setup Glue infrastructure
echo "🕷️ Setting up Glue database and crawler..."
python src/aws/setup_glue.py

# Upload initial logs
echo "📤 Uploading initial logs to S3..."
python src/aws/aws_upload.py

echo "✅ AWS setup complete!"
echo ""
echo "Next steps:"
echo "1. Check S3 bucket: python src/aws/list_s3_contents.py"
echo "2. List Glue tables: python src/aws/list_tables.py"
echo "3. Run Athena queries: python src/aws/query_athena.py"
echo "4. Monitor crawler: python src/aws/check_crawler_status.py" 