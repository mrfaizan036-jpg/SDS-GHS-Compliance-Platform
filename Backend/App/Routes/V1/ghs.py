from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from App.Database.database import get_db
from App.Schemas.ghs import (
    GHSClassification,
    GHSClassificationResponse,
)
from App.Services.ghs_service import (
    create_ghs_classification,
    get_ghs_classification,
    list_ghs_classifications,
    delete_ghs_classification,
)


router = APIRouter(
    prefix="/ghs",
    tags=["GHS"],
)


@router.post(
    "/",
    response_model=GHSClassificationResponse,
)
def create_ghs_classification_route(
    classification: GHSClassification,
    db: Session = Depends(get_db),
):
    ghs_classification = create_ghs_classification(
        db,
        classification,
    )

    return {
        "message": "GHS classification created successfully",
        "classification_id": str(ghs_classification.id),
        "classification": ghs_classification,
    }


@router.get(
    "/{classification_id}",
    response_model=GHSClassificationResponse,
)
def get_ghs_classification_route(
    classification_id: int,
    db: Session = Depends(get_db),
):
    classification = get_ghs_classification(
        db,
        classification_id,
    )

    if classification is None:
        raise HTTPException(
            status_code=404,
            detail="GHS classification not found",
        )

    return {
        "message": "GHS classification retrieved successfully",
        "classification_id": str(classification.id),
        "classification": classification,
    }


@router.get("/")
def list_ghs_classifications_route(
    db: Session = Depends(get_db),
):
    classifications = list_ghs_classifications(db)

    return {
        "count": len(classifications),
        "classifications": classifications,
    }


@router.delete(
    "/{classification_id}",
    response_model=GHSClassificationResponse,
)
def delete_ghs_classification_route(
    classification_id: int,
    db: Session = Depends(get_db),
):
    classification = delete_ghs_classification(
        db,
        classification_id,
    )

    if classification is None:
        raise HTTPException(
            status_code=404,
            detail="GHS classification not found",
        )

    return {
        "message": "GHS classification deleted successfully",
        "classification_id": str(classification.id),
        "classification": classification,
    }