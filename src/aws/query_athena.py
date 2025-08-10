#!/usr/bin/env python3
"""Minimal Athena queries for Citibikes analytics"""

import boto3
import os
import time
from dotenv import load_dotenv

# Load environment variables from aws_config.env
load_dotenv('aws_config.env')

def query_athena():
    """Run sample queries on Glue tables"""
    try:
        athena_client = boto3.client('athena')
        s3_client = boto3.client('s3')
        
        database = os.getenv('GLUE_DATABASE_NAME', 'citibikes_analytics')
        output_location = os.getenv('ATHENA_OUTPUT_LOCATION', 's3://citibikes-logs-2024/athena-output/')
        
        # Sample queries
        queries = {
            'total_logs': 'SELECT COUNT(*) as total_logs FROM logs_manual',
            'sample_data': 'SELECT * FROM logs_manual LIMIT 10',
            'log_structure': 'DESCRIBE logs_manual'
        }
        
        for query_name, query in queries.items():
            print(f"Running query: {query_name}")
            print(f"SQL: {query}")
            
            # Start query execution
            response = athena_client.start_query_execution(
                QueryString=query,
                QueryExecutionContext={'Database': database},
                ResultConfiguration={'OutputLocation': output_location}
            )
            
            query_execution_id = response['QueryExecutionId']
            print(f"Query ID: {query_execution_id}")
            
            # Wait for completion
            while True:
                query_status = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
                state = query_status['QueryExecution']['Status']['State']
                
                if state == 'SUCCEEDED':
                    print(f"Query {query_name} completed successfully!")
                    break
                elif state in ['FAILED', 'CANCELLED']:
                    print(f"Query {query_name} failed: {state}")
                    break
                
                time.sleep(2)
            
            print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"Error querying Athena: {e}")
        return False

if __name__ == "__main__":
    print("Running Athena queries...")
    success = query_athena()
    if success:
        print("All queries completed!")
    else:
        print("Some queries failed") 