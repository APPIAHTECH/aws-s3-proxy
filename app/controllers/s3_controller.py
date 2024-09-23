from fastapi import APIRouter
from fastapi import Depends
from fastapi import File, UploadFile, Query

from app.services.s3_service import S3Service
from settings.config import Config

router = APIRouter(prefix=Config.API_PREFIX)


async def get_storage_service(bucket_name: str = Query(...)) -> S3Service:
    return S3Service(bucket_name=bucket_name)


@router.post("/files/")
async def upload_file(
        object_name: str = Query(..., description="The file name with extension to save as in S3"),
        file: UploadFile = File(..., ),
        s3_service: S3Service = Depends(get_storage_service)
):
    return await s3_service.upload_file(spooled_temp_file=file, object_name=object_name)


@router.get("/files/")
async def download_file(
        object_name: str = Query(..., description="The file name to download from S3"),
        s3_service: S3Service = Depends(get_storage_service)
):
    return await s3_service.download_file(object_name=object_name)
