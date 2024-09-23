# AWS S3 Proxy Service - FastAPI

## Overview

This project is a basic proxy service built with **FastAPI** to interact with **AWS S3**. It provides two main
functionalities:

- **Upload a File**: Uploads a file to a specified S3 bucket and object.
- **Download a File**: Retrieves a file from a specified S3 bucket and object.

### Limitations
- **File Size Limit**: The maximum file size for uploads is restricted to 5 GB. Files larger than this limit cannot be processed in memory, which may impact performance.
- **File Format Validation**: Currently supports a limited set of file formats: `.jpg`, `.jpeg`, `.png`, `.gif`, `.pdf`, and `.txt`. Other formats will be rejected during upload.
- **Debugging**: The OpenAPI documentation is hidden in non-debug modes, which may make it difficult to test the API without enabling debug mode.
- **In-Memory Storage**: For files under the defined memory size, the service uses in-memory storage. Large files will be streamed, which is not yet implemented in this version.
- **S3 Bucket Configuration**: The service is designed to work with a single S3 bucket specified during initialization. Multi-bucket support is not currently available.

### Future Enhancements
- **Streaming Uploads**: Implement support for streaming large files directly to S3 without holding them in memory.
- **Expanded File Format Support**: Add support for more file formats and types based on user feedback.
- **Multi-Bucket Management**: Allow configuration of multiple S3 buckets for file storage.
- *Antivirus Scanning**: Implement a feature to scan uploaded files for viruses or potential file attacks before they are stored in the S3 bucket.
- **File Compression and Email Notifications**: Implement functionality to zip large files before uploading and send email notifications when files have been compressed and uploaded successfully.
- **Dockerized and CI/CD**: Create Docker image and add CI/CD
---

## Requirements

### Prerequisites

Ensure you have the following installed:

- Python 3.12+
- AWS Account (with an S3 bucket created)
- Docker (optional, for containerized deployment) | Not implemented lack of time

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

- **URL**: `/api/v1/files/`
- **Method**: `POST`
- **Body**: JSON object with the following keys:
    - `bucket_name`: The S3 bucket name.
    - `object_name`: The object name in the S3 bucket.
- **File**: Passed as form data (multipart/form-data).

### 2. Download a File from S3

- **URL**: `/api/v1/files/`
- **Method**: `GET`
- **Parameters**:
    - `bucket_name`: The S3 bucket name (query parameter).
    - `object_name`: The desired object name in S3 (query parameter).

### More API doc

- **URL**: `localhost:port/docs`
- **URL**: `localhost:port/redoc`

---

## Running Unit Tests

Tests use **unittest** and mock AWS interactions. Ensure that tests are run in an isolated environment without
interacting with real AWS resources.

1. **Install Testing Dependencies**:

Make sure you have installed `unittest` for testing:

2. **Run Tests**:

Run tests using the following command:

```bash
python -m unittest discover
```

Tests are located in the `tests/` folder. These will mock S3 services to avoid actual AWS calls during testing.

---
