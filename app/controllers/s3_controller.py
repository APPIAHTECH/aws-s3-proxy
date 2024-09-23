from fastapi import APIRouter
from fastapi import Depends
from fastapi import File, UploadFile, Query

from app.services.storage.s3_storage import S3StorageService
from utils.exceptions import FileFormatError
from utils.file_manager import FileManager

router = APIRouter()


async def get_storage_service(bucket_name: str = Query(...)) -> S3StorageService:
    return S3StorageService(bucket_name=bucket_name)


@router.post("/files/")
async def upload_file(
        object_name: str = Query(..., description="The file name with extention to save as in S3"),
        file: UploadFile = File(..., ),
        storage_service: S3StorageService = Depends(get_storage_service)
):
    if not FileManager.is_valid_file_format(spooled_temp_file=file):
        raise FileFormatError("File format is not valid")

    unique_filename = FileManager.generate_unique_filename(object_name)

    await storage_service.save(file.file, unique_filename)

    return {"filename": unique_filename}


@router.get("/files/")
async def download_file(
        object_name: str = Query(..., description="The file name to download from S3"),
        storage_service: S3StorageService = Depends(get_storage_service)
):
    file_path = await storage_service.retrieve(object_name)
    return {"file_url": file_path}
