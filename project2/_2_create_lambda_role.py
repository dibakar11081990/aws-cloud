import boto3
import json
import logging
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_lambda_role():
    """
    Create IAM role for AWS Lambda with necessary permissions
    """
    try:
        # Create IAM client
        iam_client = boto3.client('iam')
        
        # Define role name
        role_name = 'AWS_Custom_Lambda_Role_Policies'
        
        # Define trust relationship policy for Lambda
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        
        # Create the IAM role
        response = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Role for AWS Lambda with extended permissions'
        )
        
        logger.info(f"Created IAM role: {role_name}")
        
        # List of policies to attach
        policy_arns = [
            'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole',
            'arn:aws:iam::aws:policy/AmazonS3FullAccess',
            'arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole',
            'arn:aws:iam::aws:policy/AWSGlueConsoleFullAccess',
            'arn:aws:iam::aws:policy/service-role/AWSLambda_FullAccess'
        ]
        
        # Attach each policy to the role
        for policy_arn in policy_arns:
            try:
                iam_client.attach_role_policy(
                    RoleName=role_name,
                    PolicyArn=policy_arn
                )
                logger.info(f"Attached policy {policy_arn} to role {role_name}")
            except ClientError as e:
                logger.error(f"Error attaching policy {policy_arn}: {e}")
                raise
        
        # Wait for role to be available
        waiter = iam_client.get_waiter('role_exists')
        waiter.wait(RoleName=role_name)
        
        return response['Role']['Arn']
    
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            logger.warning(f"Role {role_name} already exists")
            return iam_client.get_role(RoleName=role_name)['Role']['Arn']
        else:
            logger.error(f"Error creating IAM role: {e}")
            raise

def main():
    try:
        role_arn = create_lambda_role()
        print(f"Successfully created/retrieved Lambda role. ARN: {role_arn}")
    except Exception as e:
        print(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
