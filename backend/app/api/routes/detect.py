from fastapi import APIRouter, HTTPException

from app.models.schemas import DetectRequest, DetectResponse
from app.services.detector import detect_ai

router = APIRouter()


@router.post("/detect", response_model=DetectResponse)
async def detect(request: DetectRequest) -> DetectResponse:
    try:
        return detect_ai(request.text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
