from sqlalchemy.orm import Session

from App.Models.chemical import ChemicalModel
from App.Services.ghs_rule_engine import (
    GHSRuleEngine,
    GHSRuleResult,
)
from App.Services.regulatory_matching_service import (
    find_matching_regulatory_rules,
    get_validated_matching_rules,
)


class GHSClassificationService:
    """
    Connects chemical data, the prototype GHS rule engine,
    and regulatory rule traceability.

    The prototype engine does not independently establish
    regulatory compliance.
    """

    def __init__(self):
        self.rule_engine = GHSRuleEngine()

    def classify(
        self,
        flash_point: float | None = None,
        boiling_point: float | None = None,
    ) -> GHSRuleResult | None:
        return self.rule_engine.classify(
            flash_point=flash_point,
            boiling_point=boiling_point,
        )

    def get_regulatory_traceability(
        self,
        db: Session,
        classification: GHSRuleResult | None,
        jurisdiction: str | None = None,
    ) -> dict:
        if classification is None:
            return {
                "status": "not_classified",
                "matched_rule_count": 0,
                "validated_rule_count": 0,
                "rule_codes": [],
                "regulation_names": [],
                "regulation_versions": [],
                "jurisdictions": [],
                "sources": [],
                "message": (
                    "No prototype classification was generated. "
                    "Regulatory traceability could not be established."
                ),
            }

        matching_rules = find_matching_regulatory_rules(
            db=db,
            hazard_class=classification.hazard_class,
            hazard_category=classification.hazard_category,
            jurisdiction=jurisdiction,
        )

        validated_rules = get_validated_matching_rules(
            db=db,
            hazard_class=classification.hazard_class,
            hazard_category=classification.hazard_category,
            jurisdiction=jurisdiction,
        )

        if not matching_rules:
            traceability_status = "no_matching_rule"
            message = (
                "No matching regulatory rule record was found. "
                "The prototype classification is unverified."
            )

        elif not validated_rules:
            traceability_status = "matching_rules_unverified"
            message = (
                "Matching regulatory rule records exist, but none "
                "are marked validated. The prototype classification "
                "must not be treated as regulatory-approved."
            )

        else:
            traceability_status = "validated_rule_record_found"
            message = (
                "At least one matching rule record is marked validated. "
                "This status does not independently prove that the "
                "prototype classification is correct or compliant."
            )

        return {
            "status": traceability_status,
            "matched_rule_count": len(matching_rules),
            "validated_rule_count": len(validated_rules),
            "rule_codes": [
                rule.rule_code for rule in matching_rules
            ],
            "regulation_names": list(
                dict.fromkeys(
                    rule.regulation_name for rule in matching_rules
                )
            ),
            "regulation_versions": list(
                dict.fromkeys(
                    rule.regulation_version for rule in matching_rules
                )
            ),
            "jurisdictions": list(
                dict.fromkeys(
                    rule.jurisdiction for rule in matching_rules
                )
            ),
            "sources": list(
                dict.fromkeys(
                    rule.source for rule in matching_rules
                )
            ),
            "message": message,
        }

    def classify_chemical(
        self,
        db: Session,
        chemical_id: int,
    ):
        chemical = (
            db.query(ChemicalModel)
            .filter(ChemicalModel.id == chemical_id)
            .first()
        )

        if chemical is None:
            return None

        classification = self.classify(
            flash_point=chemical.flash_point,
            boiling_point=chemical.boiling_point,
        )

        return chemical, classification