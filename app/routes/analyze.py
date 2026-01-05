import logging
from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel

from app.services.storage import storage_service
from app.services.analysis import analysis_service
from app.config import API_KEY

logger = logging.getLogger(__name__)
router = APIRouter()


class AnalyzeRequest(BaseModel):
    image_id: str
    detailed: bool = False  


class AnalysisMetadata(BaseModel):
    file_extension: str
    file_size_bytes: int
    analysis_version: str


class AnalyzeResponse(BaseModel):
    image_id: str
    skin_type: str
    issues: list[str]
    confidence: float
    metadata: AnalysisMetadata


class DetailedMetrics(BaseModel):
    hydration_level: float
    oil_index: float
    elasticity_score: float
    texture_score: float
    recommendations: list[str]


class DetailedAnalyzeResponse(AnalyzeResponse):
    detailed_metrics: DetailedMetrics


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
    "/analyze",
    response_model=AnalyzeResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Image not found"},
        401: {"model": ErrorResponse, "description": "Invalid API key"}
    },
    summary="Analyze an uploaded image",
    description="Perform skin analysis on a previously uploaded image"
)
async def analyze_image(
    request: AnalyzeRequest,
    api_key: str | None = Depends(verify_api_key)
):
    image_id = request.image_id
    logger.info(f"Analysis request received: image_id={image_id}, detailed={request.detailed}")
    
    image_path = storage_service.get_image_path(image_id)
    
    if image_path is None:
        logger.warning(f"Image not found: {image_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "image_not_found",
                "message": f"No image found with ID '{image_id}'. Please upload an image first using the /upload endpoint."
            }
        )
    
    if request.detailed:
        result = analysis_service.get_detailed_analysis(image_path, image_id)
        logger.info(f"Detailed analysis complete for {image_id}")
        return DetailedAnalyzeResponse(**result)
    else:
        result = analysis_service.analyze_image(image_path, image_id)
        logger.info(f"Analysis complete for {image_id}")
        return AnalyzeResponse(**result)


@router.get(
    "/image/{image_id}",
    responses={
        404: {"model": ErrorResponse, "description": "Image not found"}
    },
    summary="Get image info",
    description="Retrieve information about an uploaded image"
)
async def get_image_info(
    image_id: str,
    api_key: str | None = Depends(verify_api_key)
):
    info = storage_service.get_image_info(image_id)
    
    if info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "image_not_found",
                "message": f"No image found with ID '{image_id}'"
            }
        )
    
    return info