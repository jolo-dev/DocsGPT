import logging
import os
import boto3

logger = logging.getLogger(__name__)

def init():

    aws_profile = os.getenv("AWS_PROFILE")
    access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    assume_role_arn = os.getenv("AWS_ASSUME_ROLE_ARN")

    logger.info("Initialize boto3")
    # Setting up Sessions according to the AWS credentials provided otherwise using the default session 
    if aws_profile:
        boto3.setup_default_session(profile_name=aws_profile)
        logger.info(f"Init boto3 with AWS Profile {aws_profile}")
    elif access_key_id and secret_access_key:
        session_token = os.getenv("AWS_SESSION_TOKEN")
        region = os.getenv("AWS_DEFAULT_REGION")
        boto3.setup_default_session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            aws_session_token=session_token,
            region_name=region
        )
        logger.info("Init boto3 with ACCESS_KEY and SECRET KEY")
    elif assume_role_arn:
        sts_client = boto3.client('sts')
        session_token = sts_client.assume_role(
            RoleArn=assume_role_arn,
            RoleSessionName="langchain-docs"
        )
        boto3.setup_default_session(
            aws_access_key_id=session_token['Credentials']['AccessKeyId'],
            aws_secret_access_key=session_token['Credentials']['SecretAccessKey'],
            aws_session_token=session_token['Credentials']['SessionToken']
        )
        logger.info("Init boto3 with Assume role arn")