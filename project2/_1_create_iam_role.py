import boto3
import json
import logging
from templates.utils import load_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_iam_role(role_name, trust_service, policies):
    """
    Create IAM role with specified trust relationship and policies
    """
    try:
        # Create IAM client
        iam_client = boto3.client('iam')
        
        # Define trust relationship policy
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": f"{trust_service}.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        
        # Create the IAM role
        response = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description=f'Role for AWS {trust_service}'
        )
        
        logger.info(f"Created IAM role: {role_name}")
        
        # Attach policies
        for policy in policies:
            policy_arn = f'arn:aws:iam::aws:policy/{policy}'
            try:
                iam_client.attach_role_policy(
                    RoleName=role_name,
                    PolicyArn=policy_arn
                )
                logger.info(f"Attached policy {policy} to role {role_name}")
            except Exception as e:
                logger.error(f"Error attaching policy {policy}: {e}")
                raise
        
        return response['Role']['Arn']
    
    except Exception as e:
        if 'EntityAlreadyExists' in str(e):
            logger.warning(f"Role {role_name} already exists")
            return iam_client.get_role(RoleName=role_name)['Role']['Arn']
        else:
            logger.error(f"Error creating IAM role: {e}")
            raise

def main():
    # Load configuration
    config = load_config()
    
    try:
        # Create Glue role
        glue_role_config = config['iam']['glue_role']
        glue_role_arn = create_iam_role(
            glue_role_config['name'],
            'glue',
            glue_role_config['policies']
        )
        print(f"Successfully created/retrieved Glue role. ARN: {glue_role_arn}")
        
        # Create Lambda role
        lambda_role_config = config['iam']['lambda_role']
        lambda_role_arn = create_iam_role(
            lambda_role_config['name'],
            'lambda',
            lambda_role_config['policies']
        )
        print(f"Successfully created/retrieved Lambda role. ARN: {lambda_role_arn}")
        
    except Exception as e:
        print(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
