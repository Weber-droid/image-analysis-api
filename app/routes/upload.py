import logging
from fastapi import APIRouter, UploadFile, File, Depends, Header, HTTPException, status
from pydantic import BaseModel

from app.utils.validation import validate_image_file
from app.services.storage import storage_service
from app.config import API_KEY

logger = logging.getLogger(__name__)
router = APIRouter()


class UploadResponse(BaseModel):
    image_id: str
    message: str = "Image uploaded successfully"


class ErrorResponse(BaseModel):
    error: str
    message: str


async def verify_api_key(x_api_key: str | None = Header(default=None)):
    if x_api_key is not None and x_api_key != API_KEY:
        logger.warning(f"Invalid API key attempt")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "invalid_api_key",
                "message": "Invalid API key provided"
            }
        )
    return x_api_key


@router.post(
    "/upload",
    response_model=UploadResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid file"},
        401: {"model": ErrorResponse, "description": "Invalid API key"},
        413: {"model": ErrorResponse, "description": "File too large"}
    },
    summary="Upload an image",
    description="Upload a JPEG or PNG image (max 5MB) for analysis"
)
async def upload_image(
    file: UploadFile = File(..., description="Image file to upload (JPEG or PNG, max 5MB)"),
    api_key: str | None = Depends(verify_api_key)
):
    logger.info(f"Upload request received: filename={file.filename}, content_type={file.content_type}")
    
    contents, extension = await validate_image_file(file)
    
    image_id = storage_service.generate_image_id()
    storage_service.save_image(image_id, contents, extension)
    
    logger.info(f"Image uploaded successfully: image_id={image_id}")
    
    return UploadResponse(image_id=image_id)