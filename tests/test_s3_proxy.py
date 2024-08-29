import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock, ANY
from botocore.exceptions import NoCredentialsError, ClientError

client = TestClient(app)
PREFIX = "/api/v1"


@pytest.fixture(scope="module")
def mock_s3_client():
    """
    Fixture to mock the S3 client for testing purposes.

    Yields:
        MagicMock: Mocked S3 client instance.
    """
    with patch("app.utils.s3_utils.get_s3_client") as mock:
        mock_client = MagicMock()
        mock.return_value = mock_client
        yield mock_client


def test_upload_file(mock_s3_client):
    """
    Test the file upload endpoint with a successful upload scenario.
    """
    mock_s3_client.upload_fileobj.return_value = None

    response = client.post(
        PREFIX + "/upload/",
        files={"file": ("test.txt", b"test content")},
        data={"bucket_name": "test-bucket", "object_name": "test.txt"},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully"}


def test_upload_file_no_credentials(mock_s3_client):
    """
    Test the file upload endpoint when no AWS credentials are available.
    """
    mock_s3_client.upload_fileobj.side_effect = NoCredentialsError()

    response = client.post(
        PREFIX + "/upload/",
        files={"file": ("test.txt", b"test content")},
        data={"bucket_name": "test-bucket", "object_name": "test.txt"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Credentials not available"}


def test_download_file(mock_s3_client):
    """
    Test the file download endpoint with a successful download scenario.
    """
    mock_s3_client.get_object.return_value = {
        "Body": MagicMock(read=MagicMock(return_value=b"test content"))
    }

    response = client.get(
        PREFIX + "/download/",
        params={"bucket_name": "test-bucket", "object_name": "test.txt"},
    )

    assert response.status_code == 200
    assert response.content == b""
    mock_s3_client.get_object.assert_called_once_with(
        Bucket="test-bucket", Key="test.txt"
    )


def test_download_file_not_found(mock_s3_client):
    """
    Test the file download endpoint when the requested object is not found.
    """
    # Configure the mock to raise ClientError with NoSuchKey code
    mock_s3_client.get_object.side_effect = ClientError(
        {
            "Error": {
                "Code": "NoSuchKey",
                "Message": "The specified key does not exist.",
            }
        },
        "GetObject",
    )

    response = client.get(
        PREFIX + "/download/",
        params={"bucket_name": "test-bucket", "object_name": "non-existent.txt"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Object not found in the bucket"}


def test_create_bucket(mock_s3_client):
    """
    Test the create bucket endpoint with a successful bucket creation scenario.
    """
    response = client.post(
        PREFIX + "/create-bucket/", params={"bucket_name": "test-bucket"}
    )

    assert response.status_code == 200
    assert response.content == b'{"message":"Bucket created successfully"}'


def test_create_bucket_already_exist(mock_s3_client):
    """
    Test the create bucket endpoint when the bucket already exists.
    """
    # Simulate ClientError for BucketAlreadyExists
    mock_s3_client.create_bucket.side_effect = ClientError(
        {
            "Error": {
                "Code": "BucketAlreadyExists",
                "Message": "The requested bucket name is not available.",
            }
        },
        "CreateBucket",
    )

    # Make the request to create a bucket
    response = client.post(
        PREFIX + "/create-bucket/", params={"bucket_name": "existing-bucket"}
    )

    # Assert the response status and content
    assert response.status_code == 400
    assert response.json() == {
        "detail": "An error occurred (BucketAlreadyExists) when calling the CreateBucket "
        "operation: The requested bucket name is not available."
    }
