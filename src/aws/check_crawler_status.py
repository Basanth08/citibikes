#!/usr/bin/env python3
"""Check Glue crawler status and logs"""

import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv('aws_config.env')

def check_crawler():
    """Check crawler status and recent runs"""
    try:
        glue_client = boto3.client('glue')
        crawler_name = os.getenv('GLUE_CRAWLER_NAME', 'citibikes-logs-crawler')
        
        print(f"Checking crawler: {crawler_name}")
        
        # Get crawler details
        response = glue_client.get_crawler(Name=crawler_name)
        crawler = response['Crawler']
        
        print(f"State: {crawler['State']}")
        print(f"Last Run: {crawler.get('LastRun', 'Never')}")
        print(f"Last Updated: {crawler['LastUpdated']}")
        
        # Get recent runs
        try:
            runs_response = glue_client.get_crawler_runs(Name=crawler_name, MaxResults=5)
            
            print("\nRecent runs:")
            for run in runs_response['CrawlerRuns']:
                print(f"  Run ID: {run['Id']}")
                print(f"  Status: {run['Status']}")
                print(f"  Started: {run['StartedOn']}")
                if 'CompletedOn' in run:
                    print(f"  Completed: {run['CompletedOn']}")
                if 'ErrorMessage' in run:
                    print(f"  Error: {run['ErrorMessage']}")
                print("  ---")
        except Exception as e:
            print(f"Could not get crawler runs: {e}")
        
        return True
        
    except Exception as e:
        print(f"Error checking crawler: {e}")
        return False

if __name__ == "__main__":
    import os
    check_crawler() 