#!/usr/bin/env python3
"""Create Glue service role for Citibikes analytics"""

import boto3
import json

def create_glue_role():
    """Create Glue service role with required permissions"""
    try:
        iam_client = boto3.client('iam')
        role_name = 'GlueServiceRole-Citibikes'
        
        print(f"Creating IAM role: {role_name}")
        
        # Trust policy for Glue
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "glue.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        
        # Create role
        try:
            response = iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description='Service role for Glue to access S3 and create tables'
            )
            print(f"Role {role_name} created successfully")
        except iam_client.exceptions.EntityAlreadyExistsException:
            print(f"Role {role_name} already exists")
        
        # Attach required policies
        policies = [
            'arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole',
            'arn:aws:iam::aws:policy/AmazonS3FullAccess'
        ]
        
        for policy in policies:
            try:
                iam_client.attach_role_policy(RoleName=role_name, PolicyArn=policy)
                print(f"Attached policy: {policy}")
            except Exception as e:
                print(f"Policy {policy} already attached or error: {e}")
        
        # Get role ARN
        response = iam_client.get_role(RoleName=role_name)
        role_arn = response['Role']['Arn']
        
        print(f"\nRole ARN: {role_arn}")
        print("\nIMPORTANT: Update your aws_config.env file with this role ARN:")
        print(f"GLUE_ROLE_ARN={role_arn}")
        
        return role_arn
        
    except Exception as e:
        print(f"Error creating role: {e}")
        return None

if __name__ == "__main__":
    print("Setting up Glue service role...")
    role_arn = create_glue_role()
    if role_arn:
        print("Glue service role setup completed!")
    else:
        print("Glue service role setup failed") 