#!/usr/bin/env python3
"""Start Glue crawler manually"""

import boto3
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv('aws_config.env')

def start_crawler():
    """Start the crawler and monitor its progress"""
    try:
        glue_client = boto3.client('glue')
        crawler_name = os.getenv('GLUE_CRAWLER_NAME', 'citibikes-logs-crawler')
        
        print(f"Starting crawler: {crawler_name}")
        
        # Start the crawler
        glue_client.start_crawler(Name=crawler_name)
        print("Crawler started successfully")
        
        # Monitor progress
        print("Monitoring crawler progress...")
        for i in range(20):  # Wait up to 10 minutes
            response = glue_client.get_crawler(Name=crawler_name)
            state = response['Crawler']['State']
            print(f"State: {state}")
            
            if state == 'READY':
                print("Crawler completed successfully!")
                return True
            elif state in ['STOPPING', 'STOPPED']:
                print("Crawler stopped unexpectedly")
                return False
            
            time.sleep(30)  # Wait 30 seconds
        
        print("Crawler is taking longer than expected")
        return False
        
    except Exception as e:
        print(f"Error starting crawler: {e}")
        return False

if __name__ == "__main__":
    import os
    success = start_crawler()
    if success:
        print("Crawler operation completed successfully!")
    else:
        print("Crawler operation failed") 