
# AWS S3 Proxy Service - FastAPI

## Overview

This project is a basic proxy service built with **FastAPI** to interact with **AWS S3**. It provides two main functionalities:
- **Upload a File**: Uploads a file to a specified S3 bucket and object.
- **Download a File**: Retrieves a file from a specified S3 bucket and object.

The service interacts directly with AWS S3.

---

## Requirements

### Prerequisites

Ensure you have the following installed:
- Python 3.12+
- AWS Account (with an S3 bucket created)
- Docker (optional, for containerized deployment)

### Python Dependencies

Install the necessary Python dependencies using `pip`:

```bash
pip install -r requirements.txt
```

Key dependencies include:
- `FastAPI`: Web framework for building APIs.
- `Boto3`: AWS SDK for Python.
- `Uvicorn`: ASGI server for running FastAPI.
- `Python-dotenv`: To manage environment variables.
---

## Environment Setup

### AWS Configuration

You will need to set up your AWS credentials to allow access to S3. Use a `.env` file to store these securely.

1. Create a `.env` file in the root directory:

```bash
touch .env
```

2. Add the following content to the `.env` file with your AWS credentials and region:

```
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_REGION=us-east-1  # Replace with your preferred AWS region
```

Alternatively, you can configure AWS credentials using the AWS CLI:

```bash
aws configure
```

---

## Running the Service Locally

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_name>
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the FastAPI Service

```bash
uvicorn app.main:app --port 8000 --reload
```

The service will be available at `http://127.0.0.1:8000`.

---

## API Endpoints

### 1. Upload a File to S3

- **URL**: `/api/v1/upload/`
- **Method**: `POST`
- **Parameters**:
  - `bucket_name`: The S3 bucket name (query parameter).
  - `object_name`: The desired object name in S3 (query parameter).
- **File**: Passed as form data (multipart/form-data).

#### Example cURL Request:

```bash
curl -X 'POST'   'http://127.0.0.1:8000/api/v1/upload/?bucket_name=my-bucket&object_name=myfile.txt'   -H 'accept: application/json'   -F 'file=@path_to_your_file'
```

### 2. Download a File from S3

- **URL**: `/api/v1/download/`
- **Method**: `POST`
- **Body**: JSON object with the following keys:
  - `bucket_name`: The S3 bucket name.
  - `object_name`: The object name in the S3 bucket.

#### Example cURL Request:

```bash
curl -X 'POST'   'http://127.0.0.1:8000/api/v1/download/'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "bucket_name": "my-bucket",
  "object_name": "myfile.txt"
}'
```

---

## Running Unit Tests

Tests use **pytest** and mock AWS interactions. Ensure that tests are run in an isolated environment without interacting with real AWS resources.

1. **Install Testing Dependencies**:

Make sure you have installed `pytest` for testing:

```bash
pip install pytest
```

2. **Run Tests**:

Run tests using the following command:

```bash
pytest tests/
```

Tests are located in the `tests/` folder. These will mock S3 services to avoid actual AWS calls during testing.

---

## Docker Instructions

If you'd like to run the service in Docker:

### 1. Build the Docker Image

```bash
docker build -t s3-fastapi-proxy .
```

### 2. Run the Docker Container

```bash
docker run -p 8000:8000 s3-fastapi-proxy
```

The service will be available at `http://127.0.0.1:8000`.

---