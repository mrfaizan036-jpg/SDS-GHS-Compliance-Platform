from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from App.Database.database import get_db
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
def create_chemical_route(
    chemical: Chemical,
    db: Session = Depends(get_db),
):
    chemical_data = create_chemical(db, chemical)

    return {
        "message": "Chemical created successfully",
        "chemical_id": str(chemical_data.id),
        "chemical": chemical_data,
    }


@router.get(
    "/{chemical_id}",
    response_model=ChemicalResponse,
)
def get_chemical_route(
    chemical_id: int,
    db: Session = Depends(get_db),
):
    chemical = get_chemical(db, chemical_id)

    if chemical is None:
        raise HTTPException(
            status_code=404,
            detail="Chemical not found",
        )

    return {
        "message": "Chemical retrieved successfully",
        "chemical_id": str(chemical.id),
        "chemical": chemical,
    }


@router.get(
    "/",
    response_model=ChemicalListResponse,
)
def list_chemicals_route(
    db: Session = Depends(get_db),
):
    chemicals = list_chemicals(db)

    return {
        "count": len(chemicals),
        "chemicals": [
            {
                "chemical_id": str(chemical.id),
                "chemical": chemical,
            }
            for chemical in chemicals
        ],
    }


@router.put(
    "/{chemical_id}",
    response_model=ChemicalResponse,
)
def update_chemical_route(
    chemical_id: int,
    chemical: Chemical,
    db: Session = Depends(get_db),
):
    updated_chemical = update_chemical(
        db,
        chemical_id,
        chemical,
    )

    if updated_chemical is None:
        raise HTTPException(
            status_code=404,
            detail="Chemical not found",
        )

    return {
        "message": "Chemical updated successfully",
        "chemical_id": str(updated_chemical.id),
        "chemical": updated_chemical,
    }


@router.delete(
    "/{chemical_id}",
    response_model=ChemicalResponse,
)
def delete_chemical_route(
    chemical_id: int,
    db: Session = Depends(get_db),
):
    deleted_chemical = delete_chemical(
        db,
        chemical_id,
    )

    if deleted_chemical is None:
        raise HTTPException(
            status_code=404,
            detail="Chemical not found",
        )

    return {
        "message": "Chemical deleted successfully",
        "chemical_id": str(deleted_chemical.id),
        "chemical": deleted_chemical,
    }


@router.get("/service/health")
def chemical_service_health(
    db: Session = Depends(get_db),
):
    return service_health(db)