from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from App.Database.database import get_db
from App.Schemas.regulatory import (
    RegulatoryReference,
    RegulatoryReferenceResponse,
)
from App.Services.regulatory_service import (
    create_regulatory_reference,
    get_regulatory_reference,
    list_regulatory_references,
    delete_regulatory_reference,
)


router = APIRouter(
    prefix="/regulatory",
    tags=["Regulatory"],
)


@router.post(
    "/",
    response_model=RegulatoryReferenceResponse,
)
def create_regulatory_reference_route(
    reference: RegulatoryReference,
    db: Session = Depends(get_db),
):
    regulatory_reference = create_regulatory_reference(
        db,
        reference,
    )

    return {
        "message": "Regulatory reference created successfully",
        "reference_id": str(regulatory_reference.id),
        "reference": regulatory_reference,
    }


@router.get(
    "/{reference_id}",
    response_model=RegulatoryReferenceResponse,
)
def get_regulatory_reference_route(
    reference_id: int,
    db: Session = Depends(get_db),
):
    reference = get_regulatory_reference(
        db,
        reference_id,
    )

    if reference is None:
        raise HTTPException(
            status_code=404,
            detail="Regulatory reference not found",
        )

    return {
        "message": "Regulatory reference retrieved successfully",
        "reference_id": str(reference.id),
        "reference": reference,
    }


@router.get("/")
def list_regulatory_references_route(
    db: Session = Depends(get_db),
):
    references = list_regulatory_references(db)

    return {
        "count": len(references),
        "references": references,
    }


@router.delete(
    "/{reference_id}",
    response_model=RegulatoryReferenceResponse,
)
def delete_regulatory_reference_route(
    reference_id: int,
    db: Session = Depends(get_db),
):
    reference = delete_regulatory_reference(
        db,
        reference_id,
    )

    if reference is None:
        raise HTTPException(
            status_code=404,
            detail="Regulatory reference not found",
        )

    return {
        "message": "Regulatory reference deleted successfully",
        "reference_id": str(reference.id),
        "reference": reference,
    }