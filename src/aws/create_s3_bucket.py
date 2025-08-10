#!/usr/bin/env python3
"""Create S3 bucket for Citibikes logs"""

import boto3
import os

def create_s3_bucket():
    """Create S3 bucket if it doesn't exist"""
    try:
        s3_client = boto3.client('s3')
        bucket_name = os.getenv('S3_BUCKET_NAME', 'citibikes-logs-2024')
        region = os.getenv('AWS_REGION', 'us-east-1')
        
        print(f"Creating S3 bucket: {bucket_name}")
        
        # Create bucket
        if region == 'us-east-1':
            response = s3_client.create_bucket(Bucket=bucket_name)
        else:
            response = s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        
        print(f"Successfully created bucket: {bucket_name}")
        print(f"Bucket ARN: arn:aws:s3:::{bucket_name}")
        
        # Create athena-output folder
        s3_client.put_object(Bucket=bucket_name, Key='athena-output/')
        print("Created athena-output folder")
        
        return True
        
    except s3_client.exceptions.BucketAlreadyExists:
        print(f"Bucket {bucket_name} already exists")
        return True
    except Exception as e:
        print(f"Error creating bucket: {e}")
        return False

if __name__ == "__main__":
    print("Setting up S3 bucket for Citibikes logs...")
    success = create_s3_bucket()
    if success:
        print("S3 bucket setup completed!")
    else:
        print("S3 bucket setup failed") 