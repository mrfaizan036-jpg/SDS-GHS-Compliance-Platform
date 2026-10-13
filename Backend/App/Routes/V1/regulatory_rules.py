from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from App.Database.database import get_db
from App.Schemas.regulatory_rule import (
    RegulatoryRuleCreate,
    RegulatoryRuleResponse,
)
from App.Services.regulatory_rule_service import (
    create_regulatory_rule,
    delete_regulatory_rule,
    get_regulatory_rule,
    list_regulatory_rules,
    update_regulatory_rule_status,
)


router = APIRouter(
    prefix="/regulatory-rules",
    tags=["Regulatory Rules"],
)


@router.post(
    "/",
    response_model=RegulatoryRuleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_rule(
    rule: RegulatoryRuleCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_regulatory_rule(db, rule)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/",
    response_model=list[RegulatoryRuleResponse],
)
def get_rules(
    validation_status: str | None = Query(default=None),
    jurisdiction: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    allowed_statuses = {
        "draft",
        "under_review",
        "validated",
        "deprecated",
    }

    if (
        validation_status is not None
        and validation_status not in allowed_statuses
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid validation_status filter.",
        )

    return list_regulatory_rules(
        db,
        validation_status=validation_status,
        jurisdiction=jurisdiction,
    )


@router.get(
    "/{rule_id}",
    response_model=RegulatoryRuleResponse,
)
def get_rule(
    rule_id: int,
    db: Session = Depends(get_db),
):
    rule = get_regulatory_rule(db, rule_id)

    if rule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Regulatory rule not found.",
        )

    return rule


@router.patch(
    "/{rule_id}/status",
    response_model=RegulatoryRuleResponse,
)
def change_rule_status(
    rule_id: int,
    validation_status: str = Query(...),
    reviewed_by: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    if validation_status not in {
        "draft",
        "under_review",
        "validated",
        "deprecated",
    }:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid validation status.",
        )

    reviewed_at = (
        datetime.now(timezone.utc)
        if validation_status == "validated"
        else None
    )

    try:
        rule = update_regulatory_rule_status(
            db=db,
            rule_id=rule_id,
            validation_status=validation_status,
            reviewed_by=reviewed_by,
            reviewed_at=reviewed_at,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if rule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Regulatory rule not found.",
        )

    return rule


@router.delete(
    "/{rule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_rule(
    rule_id: int,
    db: Session = Depends(get_db),
):
    rule = delete_regulatory_rule(db, rule_id)

    if rule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Regulatory rule not found.",
        )

    return None