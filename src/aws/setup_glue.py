#!/usr/bin/env python3
"""Minimal Glue setup for Citibikes analytics"""

import boto3
import os
import time
from dotenv import load_dotenv

# Load environment variables from aws_config.env
load_dotenv('aws_config.env')

def setup_glue():
    """Setup Glue database and crawler"""
    try:
        glue_client = boto3.client('glue')
        
        database_name = os.getenv('GLUE_DATABASE_NAME', 'citibikes_analytics')
        crawler_name = os.getenv('GLUE_CRAWLER_NAME', 'citibikes-logs-crawler')
        role_arn = os.getenv('GLUE_ROLE_ARN')
        bucket_name = os.getenv('S3_BUCKET_NAME', 'citibikes-logs-2024')
        
        if not role_arn:
            print("GLUE_ROLE_ARN environment variable not set")
            return False
        
        # Create database
        print(f"Creating Glue database: {database_name}")
        try:
            glue_client.create_database(DatabaseInput={'Name': database_name})
            print(f"Database {database_name} created")
        except glue_client.exceptions.AlreadyExistsException:
            print(f"Database {database_name} already exists")
        
        # Create crawler
        print(f"Creating Glue crawler: {crawler_name}")
        try:
            glue_client.create_crawler(
                Name=crawler_name,
                Role=role_arn,
                Targets={'S3Targets': [{'Path': f's3://{bucket_name}/logs/'}]},
                DatabaseName=database_name,
                Schedule='cron(0 */6 * * ? *)'
            )
            print(f"Crawler {crawler_name} created")
        except glue_client.exceptions.AlreadyExistsException:
            print(f"Crawler {crawler_name} already exists")
        
        # Start crawler
        print(f"Starting crawler: {crawler_name}")
        glue_client.start_crawler(Name=crawler_name)
        
        # Wait for completion
        print("Waiting for crawler to complete...")
        while True:
            response = glue_client.get_crawler(Name=crawler_name)
            state = response['Crawler']['State']
            print(f"Crawler state: {state}")
            
            if state == 'READY':
                print("Crawler completed successfully!")
                break
            elif state in ['STOPPING', 'STOPPED']:
                print("Crawler stopped unexpectedly")
                return False
            
            time.sleep(30)
        
        return True
        
    except Exception as e:
        print(f"Error setting up Glue: {e}")
        return False

if __name__ == "__main__":
    print("Setting up Glue infrastructure...")
    success = setup_glue()
    if success:
        print("Glue setup completed!")
    else:
        print("Glue setup failed") 