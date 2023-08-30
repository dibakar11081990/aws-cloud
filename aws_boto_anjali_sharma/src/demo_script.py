# Steps:
# 1. login into management console
# 2. go to services like S3, EC2 etc.
# 3. once move into perticular service, lets say IAM, I can create group, user, policies etc.

# Session noting but AWS mangement console


import boto3
import os


os.system('clear')

## Create AWS console object 
aws_mg_con = boto3.session.Session(profile_name='boto3_user')
# print(dir(aws_mg_con))
# print(aws_mg_con.get_available_resources())

# for ele in dir(aws_mg_con):
#     try:
#         cmd = f"aws_mg_con.{ele}()"
#         print(cmd, exec(cmd))
#     except:
#         continue


## Resource is available for few services, which is limited to few services, alternatively we can use client
# iam_con = aws_mg_con.resource('iam')

## list all IAM users
# for each_user in iam_con.users.all():
#     print(each_user.name)
#     print(each_user)

## We can alternatively use client for same, which is more generic in nature
iam_con_client = aws_mg_con.client('iam', region_name='ap-south-1')

# for ele in dir(iam_con_client):
#     print(ele, end='\n')

for each_user in iam_con_client.list_users()['Users']:
    print(each_user['UserName'])