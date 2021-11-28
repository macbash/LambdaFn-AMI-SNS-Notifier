# LambdaFn-AMI-SNS-Notifier
Lambda function will notify latest AMI using SNS

## Pre-Reqs

Lambda IAM Role: SSM Parameter Read Access, EC2 Read Access, SNS Access for sending messages

## Environment Variables for Lambda like below,

Key: AWS_AMI_PATH

Value: /aws/service/eks/optimized-ami/1.21/amazon-linux-2/recommended/image_id

Key: EC2_TAG_KEY

Value: tag:project

Key: EC2_TAG_KEY_VALUE

Value: zook-z1-1aq12

Key: SNS_ARN

Value: arn:aws:sns:us-east-1:0000000000:zook-sns-arn

### Note:

AWS_AMI_PATH - ssm public parameter for aws ami, EC2_TAG_KEY & EC2_TAG_KEY_VALUE - existing instance tag key and value, SNS_ARN - sns arn with email subscribed one.

Author: macbash ( m_az@live.in )

Date: 2021-11-28
