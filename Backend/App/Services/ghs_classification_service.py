from App.Services.ghs_rule_engine import (
    GHSRuleEngine,
    GHSRuleResult,
)


class GHSClassificationService:
    """
    Service layer connecting application data
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