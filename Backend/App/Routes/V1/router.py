from fastapi import APIRouter
from App.Routes.V1.chemical import router as chemical_router

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


router.include_router(chemical_router)