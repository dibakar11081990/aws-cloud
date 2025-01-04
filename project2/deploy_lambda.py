import boto3
import logging
import os
import zipfile
from templates.utils import load_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_lambda_deployment_package():
    """Create a Lambda deployment package"""
    try:
        # Create a temporary deployment package
        zip_path = '/tmp/lambda_function.zip'
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.write('lambda_function.py')
            
        with open(zip_path, 'rb') as zip_file:
            zip_contents = zip_file.read()
            
        return zip_contents
    except Exception as e:
        logger.error(f"Error creating deployment package: {e}")
        raise

def create_lambda_function(config):
    """Create Lambda function and configure S3 trigger"""
    try:
        # Create Lambda client
        lambda_client = boto3.client('lambda')
        s3_client = boto3.client('s3')
        
        # Get configurations
        lambda_config = config['lambda']
        input_bucket = config['s3']['buckets']['input']['name']
        
        # Get role ARN
        iam_client = boto3.client('iam')
        role_arn = iam_client.get_role(RoleName=config['iam']['lambda_role']['name'])['Role']['Arn']
        
        # Create deployment package
        deployment_package = create_lambda_deployment_package()
        
        # Create Lambda function
        response = lambda_client.create_function(
            FunctionName=lambda_config['function_name'],
            Runtime=lambda_config['runtime'],
            Role=role_arn,
            Handler=lambda_config['handler'],
            Code={
                'ZipFile': deployment_package
            },
            Timeout=lambda_config['timeout'],
            MemorySize=lambda_config['memory_size'],
            Description='Triggers Glue job when CSV file is uploaded to S3'
        )
        
        logger.info(f"Created Lambda function: {lambda_config['function_name']}")
        
        # Add permission for S3 to invoke Lambda
        lambda_client.add_permission(
            FunctionName=lambda_config['function_name'],
            StatementId='AllowS3Invoke',
            Action='lambda:InvokeFunction',
            Principal='s3.amazonaws.com',
            SourceArn=f'arn:aws:s3:::{input_bucket}'
        )
        
        # Configure S3 trigger
        s3_client.put_bucket_notification_configuration(
            Bucket=input_bucket,
            NotificationConfiguration={
                'LambdaFunctionConfigurations': [
                    {
                        'LambdaFunctionArn': response['FunctionArn'],
                        'Events': [lambda_config['trigger']['event_type']],
                        'Filter': {
                            'Key': {
                                'FilterRules': [
                                    {
                                        'Name': 'suffix',
                                        'Value': lambda_config['trigger']['suffix']
                                    }
                                ]
                            }
                        }
                    }
                ]
            }
        )
        
        logger.info(f"Configured S3 trigger for bucket: {input_bucket}")
        return response
        
    except Exception as e:
        logger.error(f"Error creating Lambda function: {e}")
        raise

def main():
    try:
        # Load configuration
        config = load_config()
        
        response = create_lambda_function(config)
        print(f"Successfully created and configured Lambda function. Response: {response}")
    except Exception as e:
        print(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
