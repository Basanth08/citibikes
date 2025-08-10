#!/usr/bin/env python3
"""Create a manual table with basic schema for log files"""

import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv('aws_config.env')

def create_manual_table():
    """Create a table with basic schema for log files"""
    try:
        glue_client = boto3.client('glue')
        database_name = os.getenv('GLUE_DATABASE_NAME', 'citibikes_analytics')
        table_name = 'logs_manual'
        
        print(f"Creating manual table: {table_name}")
        
        # Create table with basic schema
        table_input = {
            'Name': table_name,
            'StorageDescriptor': {
                'Columns': [
                    {'Name': 'log_line', 'Type': 'string'},
                    {'Name': 'timestamp', 'Type': 'string'},
                    {'Name': 'level', 'Type': 'string'},
                    {'Name': 'message', 'Type': 'string'}
                ],
                'Location': 's3://citibikes-logs-2024/logs/',
                'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
                'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
                'SerdeInfo': {
                    'SerializationLibrary': 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe',
                    'Parameters': {
                        'field.delim': ' ',
                        'line.delim': '\n'
                    }
                }
            },
            'PartitionKeys': [
                {'Name': 'year', 'Type': 'string'},
                {'Name': 'month', 'Type': 'string'},
                {'Name': 'day', 'Type': 'string'},
                {'Name': 'hour', 'Type': 'string'}
            ]
        }
        
        # Create the table
        glue_client.create_table(DatabaseName=database_name, TableInput=table_input)
        print(f"Table {table_name} created successfully")
        
        return True
        
    except Exception as e:
        print(f"Error creating table: {e}")
        return False

if __name__ == "__main__":
    import os
    success = create_manual_table()
    if success:
        print("Manual table creation completed!")
    else:
        print("Manual table creation failed") 