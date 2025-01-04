import boto3
import json
import logging
from templates.utils import load_config
import os
import zipfile
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_lambda_zip():
    """Create a ZIP file containing the Lambda function code"""
    try:
        with zipfile.ZipFile('lambda_function.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write('lambda_function.py')
        logger.info("Created lambda_function.zip successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating ZIP file: {e}")
        raise

def get_lambda_arn(lambda_client, function_name):
    """Get the ARN of the Lambda function"""
    try:
        response = lambda_client.get_function(FunctionName=function_name)
        return response['Configuration']['FunctionArn']
    except Exception as e:
        logger.error(f"Error getting Lambda ARN: {e}")
        raise

def create_s3_trigger(lambda_client, function_name, bucket_name):
    """Create S3 trigger for Lambda function"""
    try:
        # Get Lambda ARN
        lambda_arn = get_lambda_arn(lambda_client, function_name)
        
        # Add S3 permission to Lambda
        try:
            lambda_client.add_permission(
                FunctionName=function_name,
                StatementId='S3TriggerPermission',
                Action='lambda:InvokeFunction',
                Principal='s3.amazonaws.com',
                SourceArn=f'arn:aws:s3:::{bucket_name}'
            )
            logger.info("Added S3 permission to Lambda function")
        except lambda_client.exceptions.ResourceConflictException:
            logger.info("S3 permission already exists")
        
        # Create S3 trigger
        s3_client = boto3.client('s3')
        bucket_notification = {
            'LambdaFunctionConfigurations': [
                {
                    'LambdaFunctionArn': lambda_arn,
                    'Events': ['s3:ObjectCreated:Put'],
                    'Filter': {
                        'Key': {
                            'FilterRules': [
                                {
                                    'Name': 'suffix',
                                    'Value': '.csv'
                                }
                            ]
                        }
                    }
                }
            ]
        }
        
        s3_client.put_bucket_notification_configuration(
            Bucket=bucket_name,
            NotificationConfiguration=bucket_notification
        )
        logger.info(f"Successfully created S3 trigger for bucket {bucket_name}")
        
    except Exception as e:
        logger.error(f"Error creating S3 trigger: {e}")
        raise

def create_lambda_function(config):
    """Create AWS Lambda function"""
    try:
        # Create Lambda client
        lambda_client = boto3.client('lambda')
        
        # Get Lambda configuration
        lambda_config = config['lambda']
        input_bucket = config['s3']['buckets']['input']['name']
        
        # Create ZIP file
        create_lambda_zip()
        
        # Read the ZIP file
        with open('lambda_function.zip', 'rb') as zip_file:
            zip_bytes = zip_file.read()
        
        try:
            # Try to create the Lambda function
            response = lambda_client.create_function(
                FunctionName=lambda_config['function_name'],
                Runtime=lambda_config['runtime'],
                Role=config['iam']['lambda_role']['arn'],
                Handler=lambda_config['handler'],
                Code={
                    'ZipFile': zip_bytes
                },
                Timeout=lambda_config['timeout'],
                Environment={
                    'Variables': {
                        'GLUE_JOB_NAME': config['glue']['job_name']
                    }
                }
            )
            logger.info(f"Successfully created Lambda function: {lambda_config['function_name']}")
            
            # Wait for the function to be fully created
            logger.info("Waiting for Lambda function to be ready...")
            time.sleep(10)
            
        except lambda_client.exceptions.ResourceConflictException:
            logger.info(f"Lambda function {lambda_config['function_name']} already exists")
            
            # Update the existing function code
            lambda_client.update_function_code(
                FunctionName=lambda_config['function_name'],
                ZipFile=zip_bytes
            )
            logger.info(f"Updated Lambda function code: {lambda_config['function_name']}")
        
        # Create S3 trigger
        create_s3_trigger(
            lambda_client,
            lambda_config['function_name'],
            input_bucket
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error creating Lambda function: {e}")
        raise

def main():
    try:
        # Load configuration
        config = load_config()
        
        # Create Lambda function
        response = create_lambda_function(config)
        print(f"Successfully created/updated Lambda function and S3 trigger")
        
    except Exception as e:
        print(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
