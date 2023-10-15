import os
import boto3
import json_operations 
import json
from time import sleep
from pprint import pprint

os.system('clear')

#demo loading config data from json
config_data = json_operations.loadJsonData("./python-for-cloud-main/ep3/configs/config.json")
key_path = config_data["key_path"]
key_name = config_data["key_name"]
ami_id = config_data["ami_id"]            # Amazon Machine Image ID
instance_type = config_data["instance_type"]
region_name = config_data["region_name"]
ec2_json_data_path = config_data["ec2_data_path"]

# print(ec2_json_data_path)
ec2_data = json_operations.loadJsonData(ec2_json_data_path)

# Create AWS management console object 
aws_management_console = boto3.session.Session(profile_name='boto3_user')

# Create boto3 client for ec2
ec2_client = aws_management_console.client("ec2", region_name=region_name)

def create_key_pair():
    if not os.path.exists(key_path):
        key_pair = ec2_client.create_key_pair(KeyName=key_name)
        private_key = key_pair["KeyMaterial"]
        print(private_key)
        # write private key to file with 400 permissions
        with os.fdopen(os.open(key_path, os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
            handle.write(private_key)

# Delete exising key-pairs 
def delete_key_pairs(KeyName):
    response = ec2_client.delete_key_pair(KeyName=KeyName,)
    print(response)

# Create aws ec2 instance
def create_ec2_instance():
    # ami_id is amazon provided image id, go to EC2 console chose your region(important) 
    # and choose type of image we want to use and use that image id 
    instances = ec2_client.run_instances(
        ImageId=ami_id,
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        KeyName=key_name
    )
    instance_id = instances["Instances"][0]["InstanceId"]
    pprint(f'Instances: {instances["Instances"]}')

    pprint(f"ec2 instance id: {instance_id}")

    if "ec2_instance_ids" in ec2_data:
        ec2_data["ec2_instance_ids"].append(instance_id)
    else:
        ec2_data["ec2_instance_ids"] = [instance_id]


# get ip
def get_public_ip(instance_id_list:list):
  
    reservations = ec2_client.describe_instances(InstanceIds=instance_id_list).get("Reservations")

    for reservation in reservations:
        for instance in reservation['Instances']:
            # pprint(reservation['Instances'])
            pprint(f'public IP address for {instance.get("InstanceId")}: {instance.get("PublicIpAddress")}')

# get list of all running instances
def get_running_instances():
    sleep(5)

    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["running"],
        }
    ]).get("Reservations")

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            public_ip = instance["PublicIpAddress"]
            private_ip = instance["PrivateIpAddress"]

            pprint(f"{instance_id}, {instance_type}, {public_ip}, {private_ip}")
            
            if "ec2_instance_ids" in ec2_data:
                if instance_id not in ec2_data["ec2_instance_ids"]: 
                 ec2_data["ec2_instance_ids"].append(instance_id)
            else:
                ec2_data["ec2_instance_ids"] = [instance_id]
            
# reboot instance
def reboot_instance(instance_id):
    response = ec2_client.reboot_instances(InstanceIds=[instance_id])
    print(response)


# stop instance
def stop_ec2_instance(instance_id):
    response = ec2_client.stop_instances(InstanceIds=[instance_id])
    print(response)

# Terminate ec2 Instance
def terminate_ec2_instance(instance_id):
    response = ec2_client.terminate_instances(InstanceIds = instance_id,)
    print(response)

# start instance
def start_instance(instance_id):
    response = ec2_client.start_instances(InstanceIds=[instance_id])
    print(response)

# terminate a single instance
def terminate_single_instance(instance_id):
    response = ec2_client.terminate_instances(InstanceIds=[instance_id])
    print(response)
    ec2_data["ec2_instance_ids"].remove(instance_id)

# terminate multiple ec2 instances
def terminate_multiple_instances(instance_ids):
    response = ec2_client.terminate_instances(InstanceIds=instance_ids)
    print(response)
    final_instances_list = list(filter(lambda item: (item not in instance_ids) , ec2_data["ec2_instance_ids"]))
    ec2_data["ec2_instance_ids"] = final_instances_list
    print(json.dumps(ec2_data["ec2_instance_ids"]))


# create_key_pair()
# delete_key_pairs(key_name)
# create_ec2_instance()

# for x in range(3):
#   create_ec2_instance()

# get_public_ip(ec2_data["ec2_instance_ids"])
# reboot_instance("i-05e86d021b1d57851")
# stop_ec2_instance("i-03dc7c65d2116f49c")
# terminate_ec2_instance(["i-03dc7c65d2116f49c"])
# start_instance("i-0e13256538e6b7e19")
# terminate_single_instance(ec2_data["ec2_instance_ids"][0])
# get_running_instances()
# terminate_multiple_instances(ec2_data["ec2_instance_ids"])

# saving final ec2 instances data in json
savedEc2data = json_operations.saveJsonData(ec2_json_data_path, ec2_data)
if savedEc2data:
    print("Updated EC2 instances data saved saved")