import json
import boto3
import os
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambda function handler that triggers Glue job when CSV file is uploaded to S3
    """
    try:
        # Get the S3 bucket and key from the event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        logger.info(f"Processing new file: s3://{bucket}/{key}")
        
        # Get Glue job name from environment variable
        glue_job_name = os.environ['GLUE_JOB_NAME']
        
        # Create Glue client
        glue_client = boto3.client('glue')
        
        # Start Glue job
        response = glue_client.start_job_run(
            JobName=glue_job_name,
            Arguments={
                '--input_path': f"s3://{bucket}/{key}",
                '--output_path': f"s3://{bucket.replace('input', 'output')}/{key.replace('.csv', '')}"
            }
        )
        
        logger.info(f"Started Glue job: {glue_job_name}")
        logger.info(f"Job run ID: {response['JobRunId']}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Successfully triggered Glue job',
                'jobRunId': response['JobRunId']
            })
        }
        
    except Exception as e:
        logger.error(f"Error processing S3 event: {e}")
        raise
