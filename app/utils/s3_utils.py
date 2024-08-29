import logging
from typing import Union
import boto3
from botocore.exceptions import NoCredentialsError, ClientError, ParamValidationError
from boto3.s3.transfer import TransferConfig
from app.core.config import settings


# Configure logging to capture significant events and errors
logger = logging.getLogger(__name__)


def get_s3_client():
    """
    Creates and returns an S3 client using the configuration from settings.

    Returns:
        boto3.client: An S3 client instance configured with AWS credentials and settings.
    """
    return boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
        endpoint_url=settings.S3_ENDPOINT_URL,
    )


def upload_file_to_s3(file, bucket_name: str, object_name: str) -> dict:
    """
    Uploads a file to the specified S3 bucket and object name.

    Args:
        file: The file-like object to upload.
        bucket_name: The name of the S3 bucket.
        object_name: The key (object name) under which to store the file.

    Returns:
        dict: A dictionary with a success message or an error message.
    """
    s3_client = get_s3_client()
    config = TransferConfig(multipart_threshold=1024 * 25, max_concurrency=4)
    try:
        # Upload the file to S3
        s3_client.upload_fileobj(file, bucket_name, object_name, Config=config)
        return {"message": "File uploaded successfully"}
    except ClientError as e:
        # Handle various client errors based on the error code
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchBucket":
            logger.error(f"The specified bucket '{bucket_name}' does not exist")
            return {"error": "The specified bucket does not exist"}
        else:
            logger.error(f"Client error: {e}")
            return {"error": str(e)}
    except ParamValidationError as e:
        # Handle parameter validation errors
        logger.error(f"Parameter validation error: {e}")
        return {"error": str(e)}
    except NoCredentialsError:
        # Handle cases where AWS credentials are not available
        logger.error("Credentials not available")
        return {"error": "Credentials not available"}
    except s3_client.exceptions.NoSuchBucket:
        # Handle cases where the specified bucket does not exist
        logger.error(f"The specified bucket '{bucket_name}' does not exist")
        return {"error": "The specified bucket does not exist"}


def download_file_from_s3(bucket_name: str, object_name: str) -> Union[dict, bytes]:
    """
    Downloads a file from the specified S3 bucket and object name.

    Args:
        bucket_name: The name of the S3 bucket.
        object_name: The key (object name) of the file to download.

    Returns:
        Union[dict, bytes]: The file content if successful, or an error dictionary.
    """
    s3_client = get_s3_client()
    try:
        # Retrieve the object from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
        return response["Body"]
    except ClientError as e:
        # Handle various client errors based on the error code
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchBucket":
            logger.error(f"The specified bucket '{bucket_name}' does not exist")
            return {"error": "The specified bucket does not exist"}
        elif error_code == "NoSuchKey":
            logger.error(f"Object '{object_name}' not found in bucket '{bucket_name}'")
            return {"error": "Object not found in the bucket"}
        else:
            logger.error(f"Client error: {e}")
            return {"error": str(e)}
    except ParamValidationError as e:
        # Handle parameter validation errors
        logger.error(f"Parameter validation error: {e}")
        return {"error": str(e)}
    except NoCredentialsError:
        # Handle cases where AWS credentials are not available
        logger.error("Credentials not available")
        return {"error": "Credentials not available"}


def create_bucket(bucket_name: str) -> dict:
    """
    Creates a new S3 bucket with the specified name.

    Args:
        bucket_name: The name of the S3 bucket to create.

    Returns:
        dict: A dictionary with a success message or an error message.
    """
    s3_client = get_s3_client()
    try:
        # Create the bucket in S3
        s3_client.create_bucket(Bucket=bucket_name)
        return {"message": "Bucket created successfully"}
    except ClientError as e:
        # Handle errors that occur while creating the bucket
        logger.error(f"Client error while creating bucket '{bucket_name}': {e}")
        return {"error": str(e)}
    except ParamValidationError as e:
        # Handle parameter validation errors
        logger.error(f"Parameter validation error: {e}")
        return {"error": str(e)}
    except NoCredentialsError:
        # Handle cases where AWS credentials are not available
        logger.error("Credentials not available")
        return {"error": "Credentials not available"}
