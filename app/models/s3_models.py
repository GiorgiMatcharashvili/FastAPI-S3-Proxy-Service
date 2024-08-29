from pydantic import BaseModel, Field, field_validator


class S3RequestModel(BaseModel):
    bucket_name: str = Field(..., min_length=1, description="The name of the S3 bucket")
    object_name: str = Field(
        ..., min_length=1, description="The name of the object in S3"
    )

    @field_validator("bucket_name", "object_name")
    def validate_non_empty_string(cls, value: str) -> str:
        """
        Validate that the field is a non-empty string.

        Args:
        - value: The value to be validated.

        Returns:
        - The validated value.

        Raises:
        - ValueError: If the value is an empty or whitespace-only string.
        """
        if not value.strip():
            raise ValueError("Field must be a non-empty string")
        return value
