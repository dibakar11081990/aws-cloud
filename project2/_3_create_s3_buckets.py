import boto3
import logging
from utils import load_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_bucket(bucket_name, region='us-east-1'):
    """
    Create an S3 bucket in a specified region
    
    :param bucket_name: Bucket name to create
    :param region: String region to create bucket in, e.g., 'us-east-1'
    :return: True if bucket created, else False
    """
    try:
        s3_client = boto3.client('s3', region_name=region)
        
        # Different create_bucket configuration for regions other than 'us-east-1'
        if region == 'us-east-1':
            response = s3_client.create_bucket(
                Bucket=bucket_name
            )
        else:
            location = {'LocationConstraint': region}
            response = s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration=location
            )
            
        logger.info(f"Successfully created bucket: {bucket_name}")
        
        # Enable versioning for the bucket
        versioning = s3_client.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={'Status': 'Enabled'}
        )
        logger.info(f"Enabled versioning for bucket: {bucket_name}")
        
        return True
    
    except Exception as e:
        logger.error(f"Error creating bucket {bucket_name}: {e}")
        return False

def main():
    # Load configuration
    config = load_config()
    
    # Get region and bucket configurations
    region = config['aws']['region']
    buckets = [
        config['s3']['buckets']['input']['name'],
        config['s3']['buckets']['output']['name'],
        config['s3']['buckets']['glue_script']['name']
    ]
    
    # Create each bucket
    for bucket_name in buckets:
        if create_bucket(bucket_name, region):
            print(f"Successfully created and configured bucket: {bucket_name}")
        else:
            print(f"Failed to create bucket: {bucket_name}")

if __name__ == "__main__":
    main()
