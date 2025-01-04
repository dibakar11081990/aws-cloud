import json
import boto3
from botocore.exceptions import ClientError
from pprint import pprint

'''
https://hands-on.cloud/boto3-iam-tutorial/#How-to-create-IAM-role
'''

class iamService:

    def __init__(self) -> None:
        self.aws_management_console = boto3.session.Session(profile_name='boto3_user')
        self.iam_client = self.aws_management_console.client('iam')
        self.sts = self.aws_management_console.client('sts')

    # Create IAM User
    def create_iam_user(self, user_name):
        try:
            response = self.iam_client.create_user(UserName=user_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("Object already exists")
                return False
            else:
                print("Unexpected error: %s" % e)
                return False
        return response


    def list_iam_users(self):
        try:
            paginator = self.iam_client.get_paginator('list_users')
            for response in paginator.paginate():
                #print(response["Users"])
                for user in response["Users"]:
                    print("User name: ",user["UserName"])
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("Object already exists")
            else:
                print("Unexpected error: %s" % e)
        

    def update_iam_user(self, existing_user_name, new_user_name):
        try:
            self.iam_client.update_user(UserName=existing_user_name,
                                NewUserName=new_user_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("Object already exists")
            else:
                print("Unexpected error: %s" % e)


    def delete_iam_user(self, existing_user_name):
        try:
            self.iam_client.delete_user(UserName=existing_user_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("Object already exists")
            else:
                print("Unexpected error: %s" % e)


    def create_iam_policy(self, policy_name, policy_json):
        try:
            self.iam_client.create_policy(
                PolicyName=policy_name,
                PolicyDocument=json.dumps(policy_json)
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("Object already exists")
                return False
            else:
                print("Unexpected error: %s" % e)
                return False
        return True


    def attach_custom_iam_policy_with_user(self,policy_name, user_name):
        try:
            account_id = self.sts.get_caller_identity()['Account']
            policy_arn = f'arn:aws:iam::{account_id}:policy/{policy_name}'
            self.iam_client.attach_user_policy(
                UserName=user_name,
                PolicyArn=policy_arn
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("Object already exists")
            else:
                print("Unexpected error: %s" % e)


    def attach_managed_iam_policy_with_user(self, policy_name, user_name):
        try:
            policy_arn = f'arn:aws:iam::aws:policy/{policy_name}'
            
            self.iam_client.attach_user_policy(
                UserName=user_name,
                PolicyArn=policy_arn
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("Object already exists")
            else:
                print("Unexpected error: %s" % e)


    def detach_custom_iam_policy_with_user(self, policy_name, user_name):
        try:
            account_id = self.sts.get_caller_identity()['Account']
            policy_arn = f'arn:aws:iam::{account_id}:policy/{policy_name}'
            
            self.iam_client.detach_user_policy(
                UserName=user_name,
                PolicyArn=policy_arn
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("Object already exists")
            else:
                print("Unexpected error: %s" % e)


    def detach_managed_iam_policy_with_user(self, policy_name, user_name):
        try:
            policy_arn = f'arn:aws:iam::aws:policy/{policy_name}'

            self.iam_client.detach_user_policy(
                UserName=user_name,
                PolicyArn=policy_arn
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("Object already exists")
            else:
                print("Unexpected error: %s" % e)

    def create_role(self, role_nm, role_policy):
        try:
            self.iam_client.create_role(
                RoleName=role_nm,
                AssumeRolePolicyDocument=json.dumps(role_policy)
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("Object already exists")
                return False
            else:
                print("Unexpected error: %s" % e)
                return False
        return True

    def add_policy_to_role(self,role_name, policy_name):
        try:
            account_id = self.sts.get_caller_identity()['Account']
            policy_arn = f'arn:aws:iam::{account_id}:policy/{policy_name}'

            self.iam_client.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("Object already exists")
            else:
                print("Unexpected error: %s" % e)


    def attach_custom_iam_policy_with_role(self, policy_name, role_name):
        try:
            
            account_id = self.sts.get_caller_identity()['Account']
            policy_arn = f'arn:aws:iam::{account_id}:policy/{policy_name}'
 
            self.iam_client.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("Object already exists")
            else:
                print("Unexpected error: %s" % e)

    

if __name__ == '__main__':

    custom_policy_json = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": [
                "ec2:*"
            ],
            "Resource": "*"
        }]
    }

    assume_role_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                    "AWS": "arn:aws:iam::245491356924:user/boto3_user2"
                },
            "Action": "sts:AssumeRole"
        }]
    }

    iams = iamService()
    # responseObject = iams.create_iam_user("boto3_user2")
    # pprint(f"\n{responseObject}")

    # iams.list_iam_users()

    # iams.update_iam_user("boto3_user2", "boto3_user3")
    # iams.list_iam_users()

    # iams.delete_iam_user("boto3_user3")
    # iams.list_iam_users()

    # iams.create_iam_policy("boto3_user2_policy", custom_policy_json)

    # iams.create_iam_user("boto3_user3")
    # iams.attach_custom_iam_policy_with_user("boto3_user2_policy", "boto3_user2")

    # iams.attach_managed_iam_policy_with_user("AdministratorAccess", "boto3_user2")

    # iams.detach_custom_iam_policy_with_user("boto3_user2_policy","boto3_user2")

    # iams.detach_managed_iam_policy_with_user("AdministratorAccess", "boto3_user2")
    
    # iams.create_role('boto3_user2_role', assume_role_policy)
    # iams.add_policy_to_role('boto3_user2_role', 'boto3_user2_policy')
    # iams.attach_custom_iam_policy_with_role('boto3_user2_policy', 'boto3_user2_role')
