# AWS S3 Proxy Service

## Introduction

The AWS S3 Proxy Service is a FastAPI-based application designed to interface with AWS S3 or any S3-compatible storage solution. It provides endpoints to upload files to a specified bucket and object in S3, as well as to download files from S3. This service is suitable for basic file management tasks and is built to handle both small and large files efficiently.

## Usage

To get started with this project, follow these steps:

### Clone the Repository

First, clone the repository to your local machine using the following command:

```bash
git clone https://github.com/GiorgiMatcharashvili/FastAPI-S3-Proxy-Service.git
```

### Install Docker and Docker-Compose

Ensure [Docker](https://docs.docker.com/get-started/get-docker/) and [Docker-Compose](https://docs.docker.com/compose/install/) are installed on your system.

### Configure Environment Variables

Rename the example environment file to `.env`:

```bash
cp env.example .env
```

Optionally, update the `.env` file with your specific AWS credentials and other configuration details.

### Build and Run the Application

Use Docker Compose to build and start the application:

```bash
docker-compose up --build
```

## Tests

### Unit Tests

This project includes unit tests located in the `tests` package in the `test_s3_proxy.py` file. To run the tests with coverage, use the following command:

```bash
pytest --cov=app tests/
```

### Manual Testing

For manual testing or to test the upload and download endpoints with large files, you can use the Postman collection and the sample large text file (8.6 MB) provided in the `postman` directory. Import the Postman collection into Postman to test the endpoints interactively.

## Efficiency

**FastAPI** and **Pydantic** are particularly efficient for this task due to their design and capabilities. FastAPI’s asynchronous capabilities and support for streaming responses are perfect for handling large file uploads and downloads, as it minimizes memory usage and maximizes performance. The use of `StreamingResponse` allows for efficient file handling, enabling the service to process large files without loading them entirely into memory.

Pydantic provides powerful data validation and settings management, ensuring that incoming data is validated against the expected schema. This helps prevent errors and ensures data integrity, which is crucial for maintaining a reliable file proxy service.

In combination with **boto3's** `TransferConfig`, which is used for managing multipart uploads and downloads, the service can handle large files efficiently by dividing them into smaller chunks and processing them in parallel.

By leveraging these technologies, the AWS S3 Proxy Service offers a high-performance, reliable, and scalable solution for managing files in S3.


## Technology Choices

### **FastAPI**:
Chosen for its performance and ease of use in building modern web APIs. FastAPI is designed to handle asynchronous operations and is highly efficient in managing I/O-bound tasks, making it ideal for a file proxy service.

### **Uvicorn**:
A lightning-fast ASGI server for serving FastAPI applications. It provides high performance and supports asynchronous operations, which is essential for handling large file transfers efficiently.

### **Boto3**:
The AWS SDK for Python, used for interacting with AWS S3. Boto3 provides a robust API for managing S3 buckets and objects, essential for file upload and download functionalities.

### **Pydantic**:
Used for data validation and settings management. Pydantic ensures that the input data conforms to the expected schema, providing a clear structure and validation rules for incoming requests.

### **Logging**:
Integrated for tracking and debugging. Logging helps capture important events and errors during the application’s execution, which is critical for maintaining and troubleshooting the service.

### **Docker & Docker-Compose**:
Used for containerization and environment management. Docker ensures that the application runs consistently across different environments, while Docker-Compose simplifies the setup and management of multi-container applications.

### **MinIO**:
An S3-compatible storage solution used for local development and testing. MinIO provides a lightweight alternative to AWS S3, allowing for easy local testing.

### **Pytest**:
Chosen for its powerful testing capabilities. Pytest supports fixtures and coverage reporting, making it an excellent choice for writing and running unit tests.

### **Pre-commit**:
Used to manage pre-commit hooks for code quality and consistency. Pre-commit ensures that code meets specified standards before committing, improving overall code quality.
