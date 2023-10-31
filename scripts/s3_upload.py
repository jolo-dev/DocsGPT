import logging
import boto3
from botocore.exceptions import ClientError
import os
from application.aws.boto import init

logger = logging.getLogger(__name__)

init()

# Create the S3 client after setting up the session
s3_client = boto3.client('s3')

def upload_file(file_name: str, bucket: str, object_name: str=None):
    """
    The function `upload_file` uploads a file to an S3 bucket using the specified S3 client.
    
    :param file_name: The name of the file that you want to upload to the S3 bucket
    :type file_name: str
    :param bucket: The `bucket` parameter is a string that represents the name of the S3 bucket where
    the file will be uploaded
    :type bucket: str
    :param object_name: The `object_name` parameter is an optional parameter that specifies the name of
    the object in the S3 bucket. If it is not specified, the function will use the base name of the
    `file_name` parameter as the object name
    :type object_name: str
    :return: the response from the S3 client's upload_file method if the upload is successful. If there
    is an error, it returns False.
    """
    

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        return response
    except ClientError as e:
        logging.error(e)
        return False