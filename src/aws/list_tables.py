#!/usr/bin/env python3
"""List Glue tables created by the crawler"""

import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv('aws_config.env')

def list_tables():
    """List all tables in the Glue database"""
    try:
        glue_client = boto3.client('glue')
        database_name = os.getenv('GLUE_DATABASE_NAME', 'citibikes_analytics')
        
        print(f"Listing tables in database: {database_name}")
        
        # Get tables
        response = glue_client.get_tables(DatabaseName=database_name)
        
        if response['TableList']:
            print(f"\nFound {len(response['TableList'])} tables:")
            for table in response['TableList']:
                print(f"\nTable: {table['Name']}")
                print(f"  Location: {table['StorageDescriptor']['Location']}")
                print(f"  Created: {table['CreateTime']}")
                print(f"  Columns: {len(table['StorageDescriptor']['Columns'])}")
                
                # Show column details
                for col in table['StorageDescriptor']['Columns'][:5]:  # Show first 5 columns
                    print(f"    - {col['Name']}: {col['Type']}")
                if len(table['StorageDescriptor']['Columns']) > 5:
                    print(f"    ... and {len(table['StorageDescriptor']['Columns']) - 5} more columns")
        else:
            print("No tables found in the database")
        
        return True
        
    except Exception as e:
        print(f"Error listing tables: {e}")
        return False

if __name__ == "__main__":
    import os
    list_tables() 