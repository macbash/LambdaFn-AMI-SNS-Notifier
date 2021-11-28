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
