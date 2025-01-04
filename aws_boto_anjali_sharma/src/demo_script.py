# Steps:
# 1. login into management console
# 2. go to services like S3, EC2 etc.
# 3. once move into perticular service, lets say IAM, I can create group, user, policies etc.

# Session noting but AWS mangement console


import boto3
import os
from pprint import pprint


os.system('clear')

## Create AWS management console object. Also known as "Session".
aws_management_console = boto3.session.Session(profile_name='boto3_user')
# print(dir(aws_management_console))
# print(aws_management_console.get_available_resources())

# for ele in dir(aws_management_console):
#     try:
#         cmd = f"aws_management_console.{ele}()"
#         print(cmd, exec(cmd))
#     except:
#         continue


## Resource is available for few services, which is limited to few services, alternatively we can use client 
# iam_console_resource = aws_management_console.resource('iam')

## list all IAM users
# for each_user in iam_console_resource.users.all():
#     print(each_user.name)
#     print(each_user)

## We can alternatively use client for same, which is more generic in nature
iam_console_client = aws_management_console.client('iam', region_name='ap-south-1')

pprint(iam_console_client.list_users())
pprint(iam_console_client.list_users()['Users'][0]['UserName'])
# pprint(dir(iam_console_client))

# for ele in dir(iam_console_client):
#     print(ele, end='\n')

# for each_user in iam_console_client.list_users()['Users']:
#     print(each_user['UserName'])