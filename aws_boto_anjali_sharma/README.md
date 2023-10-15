commands for aws profile creation:
----------------------------------------
1. aws configure --profile boto3_user:
   ask for AWS Access key ID and AWS Secret Access key and region name and Default output format -> <json>

2. put following in file ~/.aws/config
    [profile boto3_user]
    region = ap-south-1
    output = json

-------------------------------------------------------------

To create an EMR cluster with Admin access for EC2 and full access to S3, you can follow these steps:

    1. Create an IAM role for the cluster. This role will need to have the following permissions:
        ec2:DescribeInstances
        ec2:StartInstances
        ec2:StopInstances
        ec2:TerminateInstances
        s3:ListBucket
        s3:GetObject
        s3:PutObject
        s3:DeleteObject

You can create the IAM role using the AWS Management Console, the AWS CLI, or the AWS SDK.

    2. Create an EMR cluster. When creating the cluster, specify the IAM role that you created in step 1 as the cluster's role.

You can create the EMR cluster using the AWS Management Console, the AWS CLI, or the AWS SDK.

    3. Configure the EMR cluster's security groups. You will need to create two security groups: one for the master instance and one for the core instances.

The master instance security group should allow inbound traffic on TCP ports 22 (SSH) and 8088 (EMR web interface).

The core instance security group should allow inbound traffic on TCP ports 22 (SSH) and 8080 (Hadoop NameNode).

You can configure the security groups using the AWS Management Console, the AWS CLI, or the AWS SDK.

    4. Launch the EMR cluster. Once you have created the cluster and configured the security groups, you can launch the cluster.

You can launch the cluster using the AWS Management Console, the AWS CLI, or the AWS SDK.

Once the cluster is launched, you can access the master instance using SSH. You can then use the EMR web interface to manage the cluster and run jobs.

----------------------------------------------------------------------------------------------------------------

To create an EC2 instance profile for Amazon EMR, you can follow these steps:

    1. Open the AWS Management Console and go to the IAM console.
    2. In the left navigation pane, choose Roles.
    3. Choose Create role.
    4. Under Select role type, choose EC2.
    5. Choose Next: Permissions.
    6. Under Common policy types, choose Amazon EMR service roles.
    7. Choose EMR_EC2_DefaultRole and choose Next: Review.
    8. Under Role name, enter a name for your instance profile.
    9. Choose Create role.



---------------------------------------------------------------------------------------------
Cluster creation command with current configs
==================================================
aws emr create-cluster \
 --name "My cluster" \
 --log-uri "s3n://aws-logs-245491356924-ap-south-1/elasticmapreduce/" \
 --release-label "emr-6.12.0" \
 --service-role "arn:aws:iam::245491356924:role/emr_ec2_role" \
 --ec2-attributes '{"InstanceProfile":"emr_ec2_profile_role","EmrManagedMasterSecurityGroup":"sg-0d86e69a6375d7375","EmrManagedSlaveSecurityGroup":"sg-0712a2eac23dc46dd","KeyName":"emr_ec2_key_pair","AdditionalMasterSecurityGroups":[],"AdditionalSlaveSecurityGroups":[],"SubnetId":"subnet-019f49dbe5fff18fc"}' \
 --applications Name=Hadoop Name=Spark \
 --instance-groups '[{"InstanceCount":1,"InstanceGroupType":"TASK","Name":"Task - 1","InstanceType":"m5.xlarge","EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"VolumeType":"gp2","SizeInGB":32},"VolumesPerInstance":2}]}},{"InstanceCount":1,"InstanceGroupType":"CORE","Name":"Core","InstanceType":"m5.xlarge","EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"VolumeType":"gp2","SizeInGB":32},"VolumesPerInstance":2}]}},{"InstanceCount":1,"InstanceGroupType":"MASTER","Name":"Primary","InstanceType":"m5.xlarge","EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"VolumeType":"gp2","SizeInGB":32},"VolumesPerInstance":2}]}}]' \
 --scale-down-behavior "TERMINATE_AT_TASK_COMPLETION" \
 --ebs-root-volume-size "15" \
 --os-release-label "2.0.20230906.0" \
 --region "ap-south-1"



RunJobFlow Request Syntax
---------------------------------------

{
    "AdditionalInfo": "string",
    "AmiVersion": "string",
    "Applications": [ 
       { 
          "AdditionalInfo": { 
             "string" : "string" 
          },
          "Args": [ "string" ],
          "Name": "string",
          "Version": "string"
       }
    ],
    "AutoScalingRole": "string",
    "AutoTerminationPolicy": { 
       "IdleTimeout": number
    },
    "BootstrapActions": [ 
       { 
          "Name": "string",
          "ScriptBootstrapAction": { 
             "Args": [ "string" ],
             "Path": "string"
          }
       }
    ],
    "Configurations": [ 
       { 
          "Classification": "string",
          "Configurations": [ 
             "Configuration"
          ],
          "Properties": { 
             "string" : "string" 
          }
       }
    ],
    "CustomAmiId": "string",
    "EbsRootVolumeSize": number,
    "Instances": { 
       "AdditionalMasterSecurityGroups": [ "string" ],
       "AdditionalSlaveSecurityGroups": [ "string" ],
       "Ec2KeyName": "string",
       "Ec2SubnetId": "string",
       "Ec2SubnetIds": [ "string" ],
       "EmrManagedMasterSecurityGroup": "string",
       "EmrManagedSlaveSecurityGroup": "string",
       "HadoopVersion": "string",
       "InstanceCount": number,
       "InstanceFleets": [ 
          { 
             "InstanceFleetType": "string",
             "InstanceTypeConfigs": [ 
                { 
                   "BidPrice": "string",
                   "BidPriceAsPercentageOfOnDemandPrice": number,
                   "Configurations": [ 
                      { 
                         "Classification": "string",
                         "Configurations": [ 
                            "Configuration"
                         ],
                         "Properties": { 
                            "string" : "string" 
                         }
                      }
                   ],
                   "CustomAmiId": "string",
                   "EbsConfiguration": { 
                      "EbsBlockDeviceConfigs": [ 
                         { 
                            "VolumeSpecification": { 
                               "Iops": number,
                               "SizeInGB": number,
                               "Throughput": number,
                               "VolumeType": "string"
                            },
                            "VolumesPerInstance": number
                         }
                      ],
                      "EbsOptimized": boolean
                   },
                   "InstanceType": "string",
                   "WeightedCapacity": number
                }
             ],
             "LaunchSpecifications": { 
                "OnDemandSpecification": { 
                   "AllocationStrategy": "string",
                   "CapacityReservationOptions": { 
                      "CapacityReservationPreference": "string",
                      "CapacityReservationResourceGroupArn": "string",
                      "UsageStrategy": "string"
                   }
                },
                "SpotSpecification": { 
                   "AllocationStrategy": "string",
                   "BlockDurationMinutes": number,
                   "TimeoutAction": "string",
                   "TimeoutDurationMinutes": number
                }
             },
             "Name": "string",
             "ResizeSpecifications": { 
                "OnDemandResizeSpecification": { 
                   "TimeoutDurationMinutes": number
                },
                "SpotResizeSpecification": { 
                   "TimeoutDurationMinutes": number
                }
             },
             "TargetOnDemandCapacity": number,
             "TargetSpotCapacity": number
          }
       ],
       "InstanceGroups": [ 
          { 
             "AutoScalingPolicy": { 
                "Constraints": { 
                   "MaxCapacity": number,
                   "MinCapacity": number
                },
                "Rules": [ 
                   { 
                      "Action": { 
                         "Market": "string",
                         "SimpleScalingPolicyConfiguration": { 
                            "AdjustmentType": "string",
                            "CoolDown": number,
                            "ScalingAdjustment": number
                         }
                      },
                      "Description": "string",
                      "Name": "string",
                      "Trigger": { 
                         "CloudWatchAlarmDefinition": { 
                            "ComparisonOperator": "string",
                            "Dimensions": [ 
                               { 
                                  "Key": "string",
                                  "Value": "string"
                               }
                            ],
                            "EvaluationPeriods": number,
                            "MetricName": "string",
                            "Namespace": "string",
                            "Period": number,
                            "Statistic": "string",
                            "Threshold": number,
                            "Unit": "string"
                         }
                      }
                   }
                ]
             },
             "BidPrice": "string",
             "Configurations": [ 
                { 
                   "Classification": "string",
                   "Configurations": [ 
                      "Configuration"
                   ],
                   "Properties": { 
                      "string" : "string" 
                   }
                }
             ],
             "CustomAmiId": "string",
             "EbsConfiguration": { 
                "EbsBlockDeviceConfigs": [ 
                   { 
                      "VolumeSpecification": { 
                         "Iops": number,
                         "SizeInGB": number,
                         "Throughput": number,
                         "VolumeType": "string"
                      },
                      "VolumesPerInstance": number
                   }
                ],
                "EbsOptimized": boolean
             },
             "InstanceCount": number,
             "InstanceRole": "string",
             "InstanceType": "string",
             "Market": "string",
             "Name": "string"
          }
       ],
       "KeepJobFlowAliveWhenNoSteps": boolean,
       "MasterInstanceType": "string",
       "Placement": { 
          "AvailabilityZone": "string",
          "AvailabilityZones": [ "string" ]
       },
       "ServiceAccessSecurityGroup": "string",
       "SlaveInstanceType": "string",
       "TerminationProtected": boolean
    },
    "JobFlowRole": "string",
    "KerberosAttributes": { 
       "ADDomainJoinPassword": "string",
       "ADDomainJoinUser": "string",
       "CrossRealmTrustPrincipalPassword": "string",
       "KdcAdminPassword": "string",
       "Realm": "string"
    },
    "LogEncryptionKmsKeyId": "string",
    "LogUri": "string",
    "ManagedScalingPolicy": { 
       "ComputeLimits": { 
          "MaximumCapacityUnits": number,
          "MaximumCoreCapacityUnits": number,
          "MaximumOnDemandCapacityUnits": number,
          "MinimumCapacityUnits": number,
          "UnitType": "string"
       }
    },
    "Name": "string",
    "NewSupportedProducts": [ 
       { 
          "Args": [ "string" ],
          "Name": "string"
       }
    ],
    "OSReleaseLabel": "string",
    "PlacementGroupConfigs": [ 
       { 
          "InstanceRole": "string",
          "PlacementStrategy": "string"
       }
    ],
    "ReleaseLabel": "string",
    "RepoUpgradeOnBoot": "string",
    "ScaleDownBehavior": "string",
    "SecurityConfiguration": "string",
    "ServiceRole": "string",
    "StepConcurrencyLevel": number,
    "Steps": [ 
       { 
          "ActionOnFailure": "string",
          "HadoopJarStep": { 
             "Args": [ "string" ],
             "Jar": "string",
             "MainClass": "string",
             "Properties": [ 
                { 
                   "Key": "string",
                   "Value": "string"
                }
             ]
          },
          "Name": "string"
       }
    ],
    "SupportedProducts": [ "string" ],
    "Tags": [ 
       { 
          "Key": "string",
          "Value": "string"
       }
    ],
    "VisibleToAllUsers": boolean
 }