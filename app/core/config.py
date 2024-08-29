from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field, root_validator


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    AWS_ACCESS_KEY_ID: str = Field(..., env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = Field(..., env="AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = Field(default="us-east-1", env="AWS_REGION")
    S3_ENDPOINT_URL: str = Field(default=None, env="S3_ENDPOINT_URL")
    MINIO_ROOT_USER: str = Field(..., env="MINIO_ROOT_USER")
    MINIO_ROOT_PASSWORD: str = Field(..., env="MINIO_ROOT_PASSWORD")
    CORS_ALLOW_ORIGINS: str = Field(default="*", env="CORS_ALLOW_ORIGINS")

    @root_validator(pre=True)
    def check_required_vars(cls, values):
        """Ensure required environment variables are set."""
        required_vars = [
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "MINIO_ROOT_USER",
            "MINIO_ROOT_PASSWORD",
        ]
        for var in required_vars:
            if not values.get(var):
                raise ValueError(f"Environment variable {var} is required.")
        return values


settings = Settings()
