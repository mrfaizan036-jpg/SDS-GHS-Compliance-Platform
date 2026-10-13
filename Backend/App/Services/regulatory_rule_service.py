from sqlalchemy.orm import Session

from App.Models.regulatory import RegulatoryReferenceModel
from App.Models.regulatory_rule import RegulatoryRuleModel
from App.Schemas.regulatory_rule import RegulatoryRuleCreate


def create_regulatory_rule(
    db: Session,
    rule: RegulatoryRuleCreate,
):
    existing_rule = (
        db.query(RegulatoryRuleModel)
        .filter(RegulatoryRuleModel.rule_code == rule.rule_code)
        .first()
    )

    if existing_rule is not None:
        raise ValueError(
            f"Rule code '{rule.rule_code}' already exists."
        )

    if rule.reference_id is not None:
        reference = (
            db.query(RegulatoryReferenceModel)
            .filter(
                RegulatoryReferenceModel.id == rule.reference_id
            )
            .first()
        )

        if reference is None:
            raise ValueError(
                f"Regulatory reference {rule.reference_id} does not exist."
            )

    rule_data = rule.model_dump(mode="json")

    if rule_data.get("source_url") is not None:
        rule_data["source_url"] = str(rule_data["source_url"])

    db_rule = RegulatoryRuleModel(**rule_data)

    db.add(db_rule)

    try:
        db.commit()
        db.refresh(db_rule)
    except Exception:
        db.rollback()
        raise

    return db_rule


def get_regulatory_rule(
    db: Session,
    rule_id: int,
):
    return (
        db.query(RegulatoryRuleModel)
        .filter(RegulatoryRuleModel.id == rule_id)
        .first()
    )


def get_regulatory_rule_by_code(
    db: Session,
    rule_code: str,
):
    return (
        db.query(RegulatoryRuleModel)
        .filter(RegulatoryRuleModel.rule_code == rule_code)
        .first()
    )


def list_regulatory_rules(
    db: Session,
    validation_status: str | None = None,
    jurisdiction: str | None = None,
):
    query = db.query(RegulatoryRuleModel)

    if validation_status is not None:
        query = query.filter(
            RegulatoryRuleModel.validation_status == validation_status
        )

    if jurisdiction is not None:
        query = query.filter(
            RegulatoryRuleModel.jurisdiction == jurisdiction
        )

    return query.order_by(RegulatoryRuleModel.id.asc()).all()


def list_validated_rules(
    db: Session,
    jurisdiction: str | None = None,
):
    query = db.query(RegulatoryRuleModel).filter(
        RegulatoryRuleModel.validation_status == "validated"
    )

    if jurisdiction is not None:
        query = query.filter(
            RegulatoryRuleModel.jurisdiction == jurisdiction
        )

    return query.order_by(RegulatoryRuleModel.id.asc()).all()


def update_regulatory_rule_status(
    db: Session,
    rule_id: int,
    validation_status: str,
    reviewed_by: str | None = None,
    reviewed_at=None,
):
    allowed_statuses = {
        "draft",
        "under_review",
        "validated",
        "deprecated",
    }

    if validation_status not in allowed_statuses:
        raise ValueError("Invalid regulatory rule validation status.")

    db_rule = get_regulatory_rule(db, rule_id)

    if db_rule is None:
        return None

    if validation_status == "validated":
        if not reviewed_by or not reviewed_by.strip():
            raise ValueError(
                "A reviewer must be recorded before a rule can be validated."
            )

        if not db_rule.source.strip():
            raise ValueError(
                "A source must be recorded before a rule can be validated."
            )

    db_rule.validation_status = validation_status

    if reviewed_by is not None:
        db_rule.reviewed_by = reviewed_by

    if reviewed_at is not None:
        db_rule.reviewed_at = reviewed_at

    try:
        db.commit()
        db.refresh(db_rule)
    except Exception:
        db.rollback()
        raise

    return db_rule


def delete_regulatory_rule(
    db: Session,
    rule_id: int,
):
    db_rule = get_regulatory_rule(db, rule_id)

    if db_rule is None:
        return None

    db.delete(db_rule)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return db_rule