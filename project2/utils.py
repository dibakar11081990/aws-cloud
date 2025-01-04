import yaml
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(config_file='config.yml'):
    """Load configuration from YAML file"""
    try:
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Error loading config file: {e}")
        raise

def get_account_id():
    """Get AWS account ID"""
    import boto3
    try:
        sts = boto3.client('sts')
        return sts.get_caller_identity()['Account']
    except Exception as e:
        logger.error(f"Error getting AWS account ID: {e}")
        raise
