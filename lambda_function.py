################################################
#Pre-Reqs
#--------
#
# Lambda IAM Role: SSM Parameter Read Access, EC2 Read Access, SNS Access for sending messages
#
# Environment Variables for Lambda like below,
#
## Key: AWS_AMI_PATH
## Value: /aws/service/eks/optimized-ami/1.21/amazon-linux-2/recommended/image_id
## Key: EC2_TAG_KEY
## Value: tag:project
## Key: EC2_TAG_KEY_VALUE
## Value: zook-z1-1aq12
## Key: SNS_ARN
## Value: arn:aws:sns:us-east-1:0000000000:zook-sns-arn
#
# Note: AWS_AMI_PATH - ssm public parameter for aws ami, EC2_TAG_KEY & EC2_TAG_KEY_VALUE - existing instance tag key and value, SNS_ARN - sns arn with email subscribed one.
# Author: macbash ( m_az@live.in )
# Date: 2021-11-28
#################################################

import boto3,os, json

client = boto3.client('ssm', region_name='us-east-1')
ec2 = boto3.client('ec2', region_name='us-east-1')
sns_client = boto3.client('sns', region_name='us-east-1')


def lambda_handler(event, context):
    aws_ami_path = os.environ['AWS_AMI_PATH']
    sns_arn_id = os.environ['SNS_ARN']
    EC2_TAG_NAME = os.environ['EC2_TAG_KEY']
    EC2_TAG_VALUE = os.environ['EC2_TAG_KEY_VALUE']
    param_details = client.get_parameter(Name=aws_ami_path, WithDecryption=True)
    latest_ami_id = param_details['Parameter']['Value']

    filters = [{
        'Name': EC2_TAG_NAME,
        'Values': [EC2_TAG_VALUE]
    }]
    reservations = ec2.describe_instances(Filters=filters)
    for reservation in reservations['Reservations']:
        for instance in reservation['Instances']:
            current_image_id = instance['ImageId']
    if current_image_id != latest_ami_id:
        print("NEW IMAGE:", latest_ami_id)
        message = {"NEW_IMAGE": latest_ami_id}
        response = sns_client.publish(TargetArn=sns_arn_id, Message=json.dumps({'default': json.dumps(message)}),
                                      Subject='AMI', MessageStructure='json')
