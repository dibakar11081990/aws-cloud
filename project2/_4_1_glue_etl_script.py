###########################################################
# Move this file along with config.yml to a S3 bucket
###########################################################

import sys
import yaml
import boto3
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

def load_config_from_s3(script_bucket):
    """Load configuration from YAML file in S3"""
    try:
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=script_bucket, Key='config.yml')
        config_content = response['Body'].read().decode('utf-8')
        return yaml.safe_load(config_content)
    except Exception as e:
        print(f"Error loading config from S3: {e}")
        raise

# Get job parameters
args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    'input_path',
    'output_path',
    'SCRIPT_BUCKET'  # This will be automatically available as the bucket containing the script
])

# Initialize contexts and job
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

try:
    # Load configuration from S3
    script_bucket = args['SCRIPT_BUCKET']
    config = load_config_from_s3(script_bucket)
    etl_settings = config['glue']['etl_settings']
    
    print(f"Processing input path: {args['input_path']}")
    
    # Create dynamic frame from input path
    datasource = glueContext.create_dynamic_frame.from_options(
        "s3",
        {
            "paths": [args['input_path']],
            "recurse": True,
            "groupFiles": "inPartition",
            "groupSize": str(etl_settings['spark_settings']['group_size'])
        },
        format="csv",
        format_options={
            "withHeader": etl_settings['csv_settings']['header'],
            "separator": etl_settings['csv_settings']['separator'],
            "encoding": etl_settings['csv_settings']['encoding']
        }
    )
    
    # Convert to DataFrame and apply transformations
    output_df = datasource.toDF()
    
    # Apply coalesce if specified
    if etl_settings['spark_settings'].get('coalesce_size'):
        output_df = output_df.coalesce(etl_settings['spark_settings']['coalesce_size'])
    
    # Configure the writer
    writer = output_df.write\
        .mode(etl_settings['json_settings']['write_mode'])\
        .format("json")
    
    # Set compression if specified
    if etl_settings['json_settings'].get('compression'):
        writer = writer.option("compression", etl_settings['json_settings']['compression'])
    
    # Add partitioning if specified
    if etl_settings['json_settings'].get('partition_cols'):
        writer = writer.partitionBy(*etl_settings['json_settings']['partition_cols'])
    
    # Write the data
    print(f"Writing output to: {args['output_path']}")
    writer.save(args['output_path'])
    
    print(f"Successfully processed file: {args['input_path']}")
    print(f"Output written to: {args['output_path']}")
    
except Exception as e:
    print(f"Error processing file: {e}")
    raise
finally:
    job.commit()
