from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1",
    tags=["API V1"],
)
@router.get("/status")
def api_status():
    return {
        "api": "v1",
        "status": "operational"
    }