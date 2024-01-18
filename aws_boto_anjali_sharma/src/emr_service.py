import boto3
from datetime import datetime
import json

class boto3_EMR:

    def __init__(self, **cluster_config) -> None:
        self.aws_management_console = boto3.session.Session(profile_name='boto3_user')
        self.emr_client = self.aws_management_console.client('emr')
        self.cluster_config = cluster_config
        


    # Create the EMR client
    def createEMRCluster(self):
        response = self.emr_client.run_job_flow(**cluster_config)

        cluster_id = response['JobFlowId']

        # Print the cluster ID
        print(cluster_id)

        # Wait for the cluster to be created
        self.emr_client.get_waiter("cluster_running").wait(ClusterId=cluster_id)

        
    # # 1. Describe Clusters: list and describe existing EMR clusters
    def describe_clusters(self, cluster_id):

        # List all EMR clusters
        response = self.emr_client.list_clusters(ClusterStates=['RUNNING', 'WAITING', 'TERMINATING', 'TERMINATED'])
        clusters = response.get('Clusters', [])
        print(f"all EMR Clusters: ", clusters)

        # Describe a specific cluster
        cluster_id = cluster_id
        response = self.emr_client.describe_cluster(ClusterId=cluster_id)
        cluster_info = response.get('Cluster')
        print(f"cluster info for cluster_id {cluster_id}: \n {cluster_info}")


    # 2. Terminate Clusters: use Boto3 to terminate an existing EMR cluster:
    def terminate_cluster(self, cluster_id):
        cluster_id = cluster_id
        self.emr_client.terminate_job_flows(JobFlowIds=[cluster_id])
        print(f"Cluster {cluster_id} terminated")


    # 3. Submit EMR Steps: submit custom steps to run on an EMR cluster. Steps can include running Hive, Spark, or custom scripts:
    def submitEMRSteps(self, cluster_id):
        # Specify your cluster and step details
        cluster_id = cluster_id
        step_name = 'My EMR Step'
        script_location = 's3://your-bucket/your-script.py'

        # Submit a custom step
        response = self.emr_client.add_job_flow_steps(
            JobFlowId=cluster_id,
            Steps=[
                {
                    'Name': step_name,
                    'ActionOnFailure': 'CONTINUE',  # Change this to 'TERMINATE_CLUSTER' or 'CANCEL_AND_WAIT' as needed.
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': ['spark-submit', script_location]
                    }
                }
            ]
        )


    # 4. List Bootstrap Actions: list the bootstrap actions that are associated with your cluster:
    def listBootstrapActions(self, cluster_id):
        
        cluster_id = cluster_id #'your-cluster-id'
        # List bootstrap actions
        response = self.emr_client.list_bootstrap_actions(ClusterId=cluster_id)
        bootstrap_actions = response.get('BootstrapActions', [])


    # 5. Modify Cluster Configuration: modify the configuration of an existing EMR cluster:
    def modifyClusterConfiguration(self, cluster_id):
        # Specify your cluster ID and desired configurations
        cluster_id =  cluster_id #'your-cluster-id'
        new_instance_count = 5  # New number of core nodes
        new_instance_type = 'm5.4xlarge'  # New instance type

        # Modify the cluster configuration
        response = self.emr_client.modify_instance_fleet(
            ClusterId=cluster_id,
            InstanceFleet={
                'InstanceFleetId': 'CORE',  # Specify 'CORE' for core nodes or 'MASTER' for the master node.
                'TargetOnDemandCapacity': new_instance_count,
                'TargetSpotCapacity': 0,
                'InstanceTypeConfigs': [{'InstanceType': new_instance_type}]
            }
        )

    # 6. Attach managed scaling policy to the EMR cluster
    """
    There are two ways of managing auto-scaling for your EMR cluster:

    1. Regular auto-scaling policy – this approach is similar to setting up an auto-scaling policy for your EC2 instances. You choose CloudWatch metrics you’d like to monitor and scale based on.

    2. Managed auto-scaling policy – this approach was introduced by the AWS in Jul 2020. Managed scaling lets you automatically increase or decrease the number of instances or units in your cluster based on workload.
      EMR continuously evaluates cluster metrics to make scaling decisions that optimize your clusters for cost and speed. Managed scaling is available for clusters with either instance groups or instance fleets.
    """

    def managed_scaling_policy(self, managed_scaling_policy):
        response = self.emr_client.list_clusters(
            CreatedAfter=datetime(2023, 9, 1),
            CreatedBefore=datetime(2060, 9, 30),
            ClusterStates=['RUNNING']
        )
        
        cluster_id = response['Clusters'][0]['Id']
        response = self.emr_client.put_managed_scaling_policy(
            ClusterId=cluster_id,
            ManagedScalingPolicy=managed_scaling_policy
        )

        print (json.dumps(response, indent=4, sort_keys=True, default=str))


    # 7. Describe EMR cluster managed scaling policy
    def desc_managed_scaling_policy(self):
        response = self.emr_client.list_clusters(
            CreatedAfter=datetime(2021, 9, 1),
            CreatedBefore=datetime(2021, 9, 30),
            ClusterStates=[
                'WAITING'
            ]
        )

        cluster_id = response['Clusters'][0]['Id']
        response = self.emr_client.get_managed_scaling_policy(
            ClusterId=cluster_id
        )

        print (json.dumps(response, indent=4, sort_keys=True, default=str))


    # 8. RemoveEMR cluster managed scaling policy
    def remove_managed_scaling_policy(self):
        response = self.emr_client.list_clusters(
            CreatedAfter=datetime(2021, 9, 1),
            CreatedBefore=datetime(2021, 9, 30),
            ClusterStates=[
                'RUNNING'
            ]
        )
        cluster_id = response['Clusters'][0]['Id']
        response = self.emr_client.remove_managed_scaling_policy(
            ClusterId=cluster_id
        )
        print (json.dumps(response, indent=4, sort_keys=True, default=str))
            
    # 9. Attach auto-scaling policy to the EMR cluster
    def attach_auto_scaling_policy(self):
        response = self.emr_client.list_clusters(
            CreatedAfter=datetime(2021, 9, 1),
            CreatedBefore=datetime(2021, 9, 30),
            ClusterStates=[
                'WAITING'
            ]
        )
        cluster_id = response['Clusters'][0]['Id']
        response = self.emr_client.list_instances(
            ClusterId=cluster_id
        )
        instancegroup_id = response['Instances'][0]['InstanceGroupId']
        response = self.emr_client.put_auto_scaling_policy(
            ClusterId=cluster_id,
            InstanceGroupId=instancegroup_id,
            AutoScalingPolicy={
                'Constraints': {
                    'MinCapacity': 1,
                    'MaxCapacity': 2
                },
                'Rules': [
                    {
                        'Name': 'Scale Up',
                        'Description': 'string',
                        'Action': {
                            'SimpleScalingPolicyConfiguration': {
                                'AdjustmentType': 'CHANGE_IN_CAPACITY',
                                'ScalingAdjustment': 1,
                                'CoolDown': 120
                            }
                        },
                        'Trigger': {
                            'CloudWatchAlarmDefinition': {
                                'ComparisonOperator': 'GREATER_THAN_OR_EQUAL',
                                'EvaluationPeriods': 1,
                                'MetricName': 'Scale Up',
                                'Period': 300,
                                'Statistic': 'AVERAGE',
                                'Threshold': 75
                            }
                        }
                    },
                ]
            }
        )
        print (json.dumps(response, indent=4, sort_keys=True, default=str))


    # 10. Remove auto-scaling policy from the EMR cluster
    def remove_auto_scaling_policy(self):
        response = self.emr_client.list_clusters(
            CreatedAfter=datetime(2021, 9, 1),
            CreatedBefore=datetime(2021, 9, 30),
            ClusterStates=[
                'RUNNING'
            ]
        )
        cluster_id = response['Clusters'][0]['Id']
        response = self.emr_client.list_instances(
            ClusterId=cluster_id
        )
        instancegroup_id = response['Instances'][0]['InstanceGroupId']
        response = self.emr_client.remove_auto_scaling_policy(
            ClusterId=cluster_id,
            InstanceGroupId=instancegroup_id
        )
        print (json.dumps(response, indent=4, sort_keys=True, default=str))



        

if __name__ == "__main__":

#     # Set the cluster configuration
    cluster_config = {
        "Name":'test_emr_job_boto3',
        "LogUri":"s3n://aws-logs-245491356924-ap-south-1/elasticmapreduce/",
        "ReleaseLabel":"emr-6.12.0",
        "ScaleDownBehavior" : "TERMINATE_AT_TASK_COMPLETION",
        "EbsRootVolumeSize" : 15,
        "OSReleaseLabel":"2.0.20230906.0",
        "JobFlowRole": "emr_ec2_profile_role",
        "ServiceRole": "arn:aws:iam::245491356924:role/emr_ec2_role",
        "Applications":[
                { 'Name' : 'Hadoop' },
                { 'Name': 'Spark' },
            ],
        "Instances":{ 
            "EmrManagedMasterSecurityGroup":"sg-0d86e69a6375d7375",
            "EmrManagedSlaveSecurityGroup":"sg-0712a2eac23dc46dd",
            "Ec2KeyName":"emr_ec2_key_pair",
            "AdditionalMasterSecurityGroups":[],
            "AdditionalSlaveSecurityGroups":[],
            "Ec2SubnetId":"subnet-019f49dbe5fff18fc",
            "TerminationProtected": False,
            "KeepJobFlowAliveWhenNoSteps": False,
            'InstanceGroups': [
                {
                    "InstanceCount":1,
                    "Name":"Task - 1",
                    "Market": "ON_DEMAND",
                    "InstanceRole": "TASK",
                    "InstanceType":"m5.xlarge",
                    "EbsConfiguration":
                        {"EbsBlockDeviceConfigs":
                            [
                                {
                                    "VolumeSpecification":
                                        {
                                            "VolumeType":"gp2",
                                            "SizeInGB":32
                                        },
                                    "VolumesPerInstance":2
                                }
                            ]
                        }
                },
                {
                    "InstanceCount":1,
                    "Market": "ON_DEMAND",
                    "InstanceRole": "CORE",
                    "Name":"Core",
                    "InstanceType":"m5.xlarge",
                    "EbsConfiguration":
                        {"EbsBlockDeviceConfigs":
                            [
                                {
                                    "VolumeSpecification":
                                        {
                                            "VolumeType":"gp2",
                                            "SizeInGB":32
                                        },
                                    "VolumesPerInstance":2
                                }
                            ]
                        }
                },
                {
                    "InstanceCount":1,
                    "Market": "ON_DEMAND",
                    "InstanceRole": "MASTER",
                    "Name":"Primary",
                    "InstanceType":"m5.xlarge",
                    "EbsConfiguration":
                        {"EbsBlockDeviceConfigs":
                            [
                                {"VolumeSpecification":
                                    {
                                        "VolumeType":"gp2",
                                        "SizeInGB":32
                                    },
                                "VolumesPerInstance":2
                                }
                            ]
                        }
                }
            ]}            
        }


    emr_cluster_obj = boto3_EMR(**cluster_config)
    emr_cluster_obj.createEMRCluster()
    # emr_cluster_obj.describe_clusters('j-LKKGNIBIBKKH')

    managed_scaling_policy={
        'ComputeLimits': {
            'UnitType': 'Instances',
            'MinimumCapacityUnits': 1,
            'MaximumCapacityUnits': 3
        }
    }



