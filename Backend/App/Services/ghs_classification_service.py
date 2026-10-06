from sqlalchemy.orm import Session

from App.Models.chemical import ChemicalModel
from App.Services.ghs_rule_engine import (
    GHSRuleEngine,
    GHSRuleResult,
)


class GHSClassificationService:
    """
    Service layer connecting chemical database data
    with the deterministic GHS rule engine.
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

        result = self.classify(
            flash_point=chemical.flash_point,
            boiling_point=chemical.boiling_point,
        )

        return chemical, result