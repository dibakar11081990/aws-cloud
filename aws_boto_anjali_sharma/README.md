commands for aws profile creation:
----------------------------------------
1. aws configure --profile boto3_user:
   ask for AWS Access key ID and AWS Secret Access key and region name and Default output format -> <json>

2. put following in file ~/.aws/config
    [profile boto3_user]
    region = ap-south-1
    output = json

3. 
