from fastapi import APIRouter, HTTPException

from app.models.schemas import HumanizeRequest, HumanizeResponse
from app.services.humanizer import humanize_text
from app.services.humanizer_rules import humanize_rules

router = APIRouter()


@router.post("/humanize", response_model=HumanizeResponse)
async def humanize(request: HumanizeRequest) -> HumanizeResponse:
    try:
        if request.mode == "rules":
            return humanize_rules(request.text, request.intensity)
        return humanize_text(request.text, request.intensity)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
