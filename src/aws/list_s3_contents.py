#!/usr/bin/env python3
"""List contents of S3 bucket"""

import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv('aws_config.env')

def list_s3_contents():
    """List all objects in the S3 bucket"""
    try:
        s3_client = boto3.client('s3')
        bucket_name = os.getenv('S3_BUCKET_NAME', 'citibikes-logs-2024')
        
        print(f"Listing contents of bucket: {bucket_name}")
        
        # List objects
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name)
        
        total_files = 0
        total_size = 0
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    print(f"  {obj['Key']} ({obj['Size']} bytes)")
                    total_files += 1
                    total_size += obj['Size']
        
        print(f"\nTotal files: {total_files}")
        print(f"Total size: {total_size} bytes ({total_size / 1024 / 1024:.2f} MB)")
        
        return True
        
    except Exception as e:
        print(f"Error listing S3 contents: {e}")
        return False

if __name__ == "__main__":
    import os
    list_s3_contents() 