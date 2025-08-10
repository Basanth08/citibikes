#!/usr/bin/env python3
"""Minimal S3 log uploader for Citibikes pipeline"""

import boto3
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from aws_config.env
load_dotenv('aws_config.env')

def upload_logs_to_s3():
    """Upload log files to S3 bucket"""
    try:
        s3_client = boto3.client('s3')
        bucket_name = os.getenv('S3_BUCKET_NAME', 'citibikes-logs-2024')
        
        log_files = ['citibikes_pipeline.log', 'citibikes_consumer.log']
        
        for log_file in log_files:
            if os.path.exists(log_file):
                timestamp = datetime.now().strftime('%Y/%m/%d/%H')
                s3_key = f"logs/{timestamp}/{log_file}"
                
                print(f"Uploading {log_file} to s3://{bucket_name}/{s3_key}")
                s3_client.upload_file(log_file, bucket_name, s3_key)
                print(f"Successfully uploaded {log_file}")
            else:
                print(f"Warning: Log file {log_file} not found")
                
        return True
        
    except Exception as e:
        print(f"Error uploading logs: {e}")
        return False

if __name__ == "__main__":
    print("Starting S3 log upload...")
    success = upload_logs_to_s3()
    if success:
        print("All logs uploaded successfully!")
    else:
        print("Log upload failed") 