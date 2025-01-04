import boto3
import logging
from botocore.exceptions import ClientError
from templates.utils import load_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_files_to_s3(s3_client, script_bucket):
    """Upload necessary files to S3"""
    try:
        # Upload Glue ETL script
        s3_client.upload_file(
            'glue_etl_script.py',
            script_bucket,
            'glue_etl_script.py'
        )
        logger.info(f"Uploaded glue_etl_script.py to s3://{script_bucket}/")

        # Upload config file
        s3_client.upload_file(
            'config.yml',
            script_bucket,
            'config.yml'
        )
        logger.info(f"Uploaded config.yml to s3://{script_bucket}/")

    except Exception as e:
        logger.error(f"Error uploading files to S3: {e}")
        raise

def create_glue_job(config):
    """
    Create AWS Glue ETL job
    """
    try:
        # Create Glue client
        glue_client = boto3.client('glue')
        s3_client = boto3.client('s3')
        
        # Get Glue configuration
        glue_config = config['glue']
        
        # Job parameters
        input_bucket = config['s3']['buckets']['input']['name']
        output_bucket = config['s3']['buckets']['output']['name']
        script_bucket = config['s3']['buckets']['glue_script']['name']
        
        # Upload necessary files to S3
        upload_files_to_s3(s3_client, script_bucket)
        
        # Create Glue job
        response = glue_client.create_job(
            Name=glue_config['job_name'],
            Role=config['iam']['glue_role']['name'],
            Command={
                'Name': 'glueetl',
                'ScriptLocation': f"s3://{script_bucket}/glue_etl_script.py",
                'PythonVersion': glue_config['python_version']
            },
            DefaultArguments={
                '--job-language': 'python',
                '--continuous-log-logGroup': f"/aws-glue/jobs/{glue_config['job_name']}",
                '--enable-continuous-cloudwatch-log': 'true',
                '--enable-metrics': 'true',
                '--job-bookmark-option': glue_config['bookmark_option'],
                '--input_path': f"s3://{input_bucket}/",
                '--output_path': f"s3://{output_bucket}/",
                '--TempDir': f"s3://{script_bucket}/temporary/",
                '--SCRIPT_BUCKET': script_bucket  # Pass the script bucket name to the job
            },
            MaxRetries=0,
            WorkerType=glue_config['worker_type'],
            NumberOfWorkers=glue_config['number_of_workers'],
            GlueVersion=glue_config['glue_version'],
            Timeout=glue_config['timeout_minutes'],
            ExecutionProperty={
                'MaxConcurrentRuns': glue_config['max_concurrent_runs']
            }
        )
        
        logger.info(f"Successfully created Glue job: {glue_config['job_name']}")
        return response
        
    except ClientError as e:
        logger.error(f"Error creating Glue job: {e}")
        raise

def main():
    try:
        # Load configuration
        config = load_config()
        
        response = create_glue_job(config)
        print(f"Successfully created Glue job. Response: {response}")
    except Exception as e:
        print(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
