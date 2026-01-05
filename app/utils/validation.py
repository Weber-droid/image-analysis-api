from pathlib import Path
from fastapi import UploadFile, HTTPException, status

from app.config import MAX_FILE_SIZE, ALLOWED_EXTENSIONS, ALLOWED_CONTENT_TYPES


def validate_file_extension(filename: str) -> str:
    extension = Path(filename).suffix.lower()
    
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "invalid_file_type",
                "message": f"File type '{extension}' is not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            }
        )
    
    return extension


def validate_content_type(content_type: str | None) -> None:
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "invalid_content_type",
                "message": f"Content type '{content_type}' is not allowed. Allowed types: {', '.join(ALLOWED_CONTENT_TYPES)}"
            }
        )


async def validate_file_size(file: UploadFile) -> bytes:
    contents = await file.read()
    size = len(contents)
    
    if size > MAX_FILE_SIZE:
        max_mb = MAX_FILE_SIZE / (1024 * 1024)
        actual_mb = size / (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "error": "file_too_large",
                "message": f"File size ({actual_mb:.2f}MB) exceeds maximum allowed size ({max_mb}MB)"
            }
        )
    
    if size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "empty_file",
                "message": "Uploaded file is empty"
            }
        )
    
    return contents


async def validate_image_file(file: UploadFile) -> tuple[bytes, str]:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "missing_filename",
                "message": "Uploaded file must have a filename"
            }
        )
    
    extension = validate_file_extension(file.filename)
    
    validate_content_type(file.content_type)
    
    contents = await validate_file_size(file)
    
    return contents, extension