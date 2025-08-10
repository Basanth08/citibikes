#!/usr/bin/env python3
"""Get detailed table schema from Glue"""

import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv('aws_config.env')

def get_table_schema():
    """Get detailed schema of the logs table"""
    try:
        glue_client = boto3.client('glue')
        database_name = os.getenv('GLUE_DATABASE_NAME', 'citibikes_analytics')
        table_name = 'logs'
        
        print(f"Getting schema for table: {table_name}")
        
        # Get table details
        response = glue_client.get_table(
            DatabaseName=database_name,
            Name=table_name
        )
        
        table = response['Table']
        
        print(f"\nTable: {table['Name']}")
        print(f"Location: {table['StorageDescriptor']['Location']}")
        
        # Handle optional fields
        if 'InputFormat' in table['StorageDescriptor']:
            print(f"Input Format: {table['StorageDescriptor']['InputFormat']}")
        if 'OutputFormat' in table['StorageDescriptor']:
            print(f"Output Format: {table['StorageDescriptor']['OutputFormat']}")
        
        print(f"\nColumns ({len(table['StorageDescriptor']['Columns'])}):")
        for col in table['StorageDescriptor']['Columns']:
            print(f"  - {col['Name']}: {col['Type']}")
        
        print(f"\nPartition Keys ({len(table.get('PartitionKeys', []))}):")
        for part in table.get('PartitionKeys', []):
            print(f"  - {part['Name']}: {part['Type']}")
        
        return True
        
    except Exception as e:
        print(f"Error getting table schema: {e}")
        return False

if __name__ == "__main__":
    import os
    get_table_schema() 