from fastapi import APIRouter
from fastapi import File, UploadFile, HTTPException, Query

from app.services.storage.s3_storage import S3StorageService

router = APIRouter()


@router.post("/files/")
async def upload_file(
        bucket_name: str = Query(..., description="The S3 bucket to upload the file to"),
        file_name: str = Query(..., description="The file name to save as in S3"),
        file: UploadFile = File(...,)
        # @TODO : max_length=5 * 1024 * 1024 5 MB limit | If we want to store even larger files we have to change implementation to use streams
):
    try:
        storage_service = S3StorageService(bucket_name=bucket_name, )
        await storage_service.save(file.file, file_name)
        return {"is_file_uploaded": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files/")
async def download_file(
        bucket_name: str = Query(..., description="The S3 bucket where the file is stored"),
        file_name: str = Query(..., description="The file name to download from S3")
):
    try:
        file_url = await S3StorageService(bucket_name=bucket_name).retrieve(file_name)
        return {"file_url": file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
