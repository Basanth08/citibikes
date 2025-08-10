#!/usr/bin/env python3
"""Update Glue crawler configuration for better log file handling"""

import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv('aws_config.env')

def update_crawler():
    """Update crawler configuration for log files"""
    try:
        glue_client = boto3.client('glue')
        crawler_name = os.getenv('GLUE_CRAWLER_NAME', 'citibikes-logs-crawler')
        
        print(f"Updating crawler: {crawler_name}")
        
        # Update crawler with better configuration for log files
        response = glue_client.update_crawler(
            Name=crawler_name,
            Targets={
                'S3Targets': [
                    {
                        'Path': 's3://citibikes-logs-2024/logs/',
                        'Exclusions': ['**/athena-output/**']
                    }
                ]
            },
            SchemaChangePolicy={
                'UpdateBehavior': 'UPDATE_IN_DATABASE',
                'DeleteBehavior': 'LOG'
            }
        )
        
        print("Crawler updated successfully")
        
        # Start the crawler
        print("Starting updated crawler...")
        glue_client.start_crawler(Name=crawler_name)
        
        return True
        
    except Exception as e:
        print(f"Error updating crawler: {e}")
        return False

if __name__ == "__main__":
    import os
    success = update_crawler()
    if success:
        print("Crawler update and restart completed!")
    else:
        print("Crawler update failed") 