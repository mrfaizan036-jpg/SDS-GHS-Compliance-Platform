from fastapi import APIRouter, HTTPException

from App.Schemas.chemical import (
    Chemical,
    ChemicalResponse,
    ChemicalListResponse,
)
from App.Services.chemical_service import (
    create_chemical,
    get_chemical,
    list_chemicals,
    update_chemical,
    delete_chemical,
    service_health,
)


router = APIRouter(
    prefix="/chemicals",
    tags=["Chemicals"],
)


@router.post("/", response_model=ChemicalResponse)
def create_chemical_route(chemical: Chemical):
    chemical_id, chemical_data = create_chemical(chemical)

    return {
        "message": "Chemical created successfully",
        "chemical_id": chemical_id,
        "chemical": chemical_data,
    }


@router.get(
    "/{chemical_id}",
    response_model=ChemicalResponse,
)
def get_chemical_route(chemical_id: str):
    chemical = get_chemical(chemical_id)

    if chemical is None:
        raise HTTPException(
            status_code=404,
            detail="Chemical not found"
        )

    return {
        "message": "Chemical retrieved successfully",
        "chemical_id": chemical_id,
        "chemical": chemical,
    }


@router.get(
    "/",
    response_model=ChemicalListResponse,
)
def list_chemicals_route():
    chemicals = list_chemicals()

    return {
        "count": len(chemicals),
        "chemicals": chemicals,
    }


@router.put(
    "/{chemical_id}",
    response_model=ChemicalResponse,
)
def update_chemical_route(
    chemical_id: str,
    chemical: Chemical,
):
    if get_chemical(chemical_id) is None:
        raise HTTPException(
            status_code=404,
            detail="Chemical not found"
        )

    updated_chemical = update_chemical(
        chemical_id,
        chemical
    )

    return {
        "message": "Chemical updated successfully",
        "chemical_id": chemical_id,
        "chemical": updated_chemical,
    }


@router.delete(
    "/{chemical_id}",
    response_model=ChemicalResponse,
)
def delete_chemical_route(chemical_id: str):
    if get_chemical(chemical_id) is None:
        raise HTTPException(
            status_code=404,
            detail="Chemical not found"
        )

    deleted_chemical = delete_chemical(chemical_id)

    return {
        "message": "Chemical deleted successfully",
        "chemical_id": chemical_id,
        "chemical": deleted_chemical,
    }
@router.get("/service/health")
def chemical_service_health():
    return service_health()