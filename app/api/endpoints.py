import logging
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import StreamingResponse
from app.utils.s3_utils import upload_file_to_s3, download_file_from_s3, create_bucket
from app.models.s3_models import S3RequestModel

# Configure logging for this module
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/upload/")
async def upload_file(
    bucket_name: str = Form(...),
    object_name: str = Form(...),
    file: UploadFile = File(...),
):
    """
    Uploads a file to the specified S3 bucket and object name.

    Args:
    - bucket_name: The name of the S3 bucket.
    - object_name: The name of the object in S3.
    - file: The file to be uploaded.

    Returns:
    - JSON with success or error message.
    """
    logger.info(
        f"Received upload request for bucket '{bucket_name}' and object '{object_name}'"
    )
    try:
        S3RequestModel(bucket_name=bucket_name, object_name=object_name)
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    result = upload_file_to_s3(file.file, bucket_name, object_name)

    if "error" in result:
        logger.error(f"Upload error: {result['error']}")
        raise HTTPException(status_code=400, detail=result["error"])

    logger.info(
        f"File uploaded successfully to bucket '{bucket_name}' and object '{object_name}'"
    )
    return result


@router.get("/download/")
async def download_file(bucket_name: str, object_name: str):
    """
    Downloads a file from the specified S3 bucket and object name.

    Args:
    - bucket_name: The name of the S3 bucket.
    - object_name: The name of the object in S3.

    Returns:
    - File content or an error message.
    """
    logger.info(
        f"Received download request for bucket '{bucket_name}' and object '{object_name}'"
    )
    try:
        S3RequestModel(bucket_name=bucket_name, object_name=object_name)
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    file_stream = download_file_from_s3(bucket_name, object_name)

    if isinstance(file_stream, dict) and "error" in file_stream:
        logger.error(f"Download error: {file_stream['error']}")
        raise HTTPException(status_code=404, detail=file_stream["error"])

    logger.info(
        f"File downloaded successfully from bucket '{bucket_name}' and object '{object_name}'"
    )
    return StreamingResponse(file_stream, media_type="application/octet-stream")


@router.post("/create-bucket/")
async def create_bucket_endpoint(bucket_name: str):
    """
    Creates a new S3 bucket with the specified name.

    Args:
    - bucket_name: The name of the S3 bucket to create.

    Returns:
    - JSON with success or error message.
    """
    logger.info(f"Received create bucket request for bucket '{bucket_name}'")
    try:
        S3RequestModel(bucket_name=bucket_name, object_name="dummy")
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    result = create_bucket(bucket_name)

    if "error" in result:
        logger.error(f"Create bucket error: {result['error']}")
        raise HTTPException(status_code=400, detail=result["error"])

    logger.info(f"Bucket '{bucket_name}' created successfully")
    return result
