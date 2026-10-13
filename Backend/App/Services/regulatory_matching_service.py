from sqlalchemy.orm import Session

from App.Models.regulatory_rule import RegulatoryRuleModel


def find_matching_regulatory_rules(
    db: Session,
    hazard_class: str,
    hazard_category: str | None = None,
    jurisdiction: str | None = None,
):
    """
    Find regulatory rule records matching a hazard class.

    Only exact hazard-class matches are returned.
    If a category or jurisdiction is provided, it must also match.

    Matching records are not automatically considered
    scientifically or legally correct.
    """

    query = db.query(RegulatoryRuleModel).filter(
        RegulatoryRuleModel.hazard_class == hazard_class
    )

    if hazard_category is not None:
        query = query.filter(
            RegulatoryRuleModel.hazard_category == hazard_category
        )

    if jurisdiction is not None:
        query = query.filter(
            RegulatoryRuleModel.jurisdiction == jurisdiction
        )

    return query.order_by(RegulatoryRuleModel.id.asc()).all()


def get_validated_matching_rules(
    db: Session,
    hazard_class: str,
    hazard_category: str | None = None,
    jurisdiction: str | None = None,
):
    """
    Find matching records whose stored validation status is validated.

    This checks the database status only. It does not independently
    verify the underlying regulatory criteria.
    """

    query = db.query(RegulatoryRuleModel).filter(
        RegulatoryRuleModel.hazard_class == hazard_class,
        RegulatoryRuleModel.validation_status == "validated",
    )

    if hazard_category is not None:
        query = query.filter(
            RegulatoryRuleModel.hazard_category == hazard_category
        )

    if jurisdiction is not None:
        query = query.filter(
            RegulatoryRuleModel.jurisdiction == jurisdiction
        )

    return query.order_by(RegulatoryRuleModel.id.asc()).all()