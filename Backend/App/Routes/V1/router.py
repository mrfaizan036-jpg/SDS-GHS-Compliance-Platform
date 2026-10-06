from fastapi import APIRouter

from App.Routes.V1.chemical import router as chemical_router
from App.Routes.V1.ghs import router as ghs_router
from App.Routes.V1.regulatory import router as regulatory_router


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
router.include_router(ghs_router)
router.include_router(regulatory_router)