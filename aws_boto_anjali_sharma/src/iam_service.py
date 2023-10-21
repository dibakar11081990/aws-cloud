import json
import boto3
from botocore.exceptions import ClientError

class iamService:

    def __init__(self) -> None:
        self.aws_management_console = boto3.session.Session(profile_name='boto3_user')
        self.emr_client = self.aws_management_console.client('emr')

    # Create IAM User
    def create_iam_user(self, user_name):
        try:
            iam_client = self.emr_client.client('iam')
            response = iam_client.create_user(UserName=user_name)
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
            iam_client = self.emr_client.client('iam')
            paginator = iam_client.get_paginator('list_users')
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
            iam_client = self.emr_client.client('iam')
            iam_client.update_user(UserName=existing_user_name,
                                NewUserName=new_user_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("Object already exists")
            else:
                print("Unexpected error: %s" % e)


    def delete_iam_user(self, existing_user_name):
        try:
            iam_client = self.emr_client.client('iam')
            iam_client.delete_user(UserName=existing_user_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("Object already exists")
            else:
                print("Unexpected error: %s" % e)


    def create_iam_policy(self, policy_name, policy_json):
        try:
            iam_client = self.emr_client.client('iam')
            iam_client.create_policy(
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
            sts = self.emr_client.client('sts')
            account_id = sts.get_caller_identity()['Account']
            policy_arn = f'arn:aws:iam::{account_id}:policy/{policy_name}'
            iam_client = boto3.client('iam')
            iam_client.attach_user_policy(
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
            sts = self.emr_client.client('sts')
            policy_arn = f'arn:aws:iam::aws:policy/{policy_name}'
            iam_client = self.emr_client.client('iam')
            iam_client.attach_user_policy(
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
            sts = self.emr_client.client('sts')
            account_id = sts.get_caller_identity()['Account']
            policy_arn = f'arn:aws:iam::{account_id}:policy/{policy_name}'
            iam_client = self.emr_client.client('iam')
            iam_client.detach_user_policy(
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
            sts = self.emr_client.client('sts')
            policy_arn = f'arn:aws:iam::aws:policy/{policy_name}'
            iam_client = self.emr_client.client('iam')
            iam_client.detach_user_policy(
                UserName=user_name,
                PolicyArn=policy_arn
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("Object already exists")
            else:
                print("Unexpected error: %s" % e)


    def add_policy_to_role(self,role_name, policy_arn):
        try:
            iam_client = self.emr_client.client('iam')
            iam_client.attach_role_policy(
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
            sts = self.emr_client.client('sts')
            account_id = sts.get_caller_identity()['Account']
            policy_arn = f'arn:aws:iam::{account_id}:policy/{policy_name}'
            iam_client = self.emr_client.client('iam')
            iam_client.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("Object already exists")
            else:
                print("Unexpected error: %s" % e)


    def create_role(self, role_name, trust_document):
        try:
            iam_client = self.emr_client.client('iam')
            iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_document)
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("Object already exists")
            else:
                print("Unexpected error: %s" % e)
    

if __name__ == '__main__':

    # custom_policy_json = {
    #     "Version": "2012-10-17",
    #     "Statement": [{
    #         "Effect": "Allow",
    #         "Action": [
    #             "ec2:*"
    #         ],
    #         "Resource": "*"
    #     }]
    # }

    # responseObject = create_iam_user("SandipSimpleTest1")
    # print(responseObject)

    # list_iam_users()

    # update_iam_user("SandipTest1", "SandipTest1Renamed")
    # list_iam_users()

    # delete_iam_user("SandipTest1Renamed")
    # list_iam_users()

    # create_iam_policy("test_policy_1_by_sandip", custom_policy_json)

    # create_iam_user("sandip_poilcy_test_user_1")
    # attach_custom_iam_policy_with_user("test_policy_1_by_sandip", "sandip_poilcy_test_user_1")

    # attach_managed_iam_policy_with_user("AdministratorAccess", "sandip_poilcy_test_user_1")

    # detach_custom_iam_policy_with_user("test_policy_1_by_sandip","sandip_poilcy_test_user_1")

    # detach_managed_iam_policy_with_user("AdministratorAccess", "sandip_poilcy_test_user_1")

