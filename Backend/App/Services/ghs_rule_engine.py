from dataclasses import dataclass


@dataclass
class GHSRuleResult:
    hazard_class: str
    hazard_category: str | None
    signal_word: str | None
    pictograms: str | None
    hazard_statements: str | None
    precautionary_statements: str | None


class GHSRuleEngine:
    """
    Deterministic rule engine for GHS hazard classification.

    Regulatory rules are explicit and deterministic.
    AI must not override the classification produced here.
    """

    def classify(
        self,
        flash_point: float | None = None,
        boiling_point: float | None = None,
    ) -> GHSRuleResult | None:

        if flash_point is None:
            return None

        if flash_point < 23:
            return GHSRuleResult(
                hazard_class="Flammable liquids",
                hazard_category="Category 2",
                signal_word="Danger",
                pictograms="GHS02",
                hazard_statements="Flammable liquid and vapour",
                precautionary_statements=(
                    "Keep away from heat, hot surfaces, sparks, "
                    "open flames and other ignition sources. No smoking."
                ),
            )

        if flash_point <= 60:
            return GHSRuleResult(
                hazard_class="Flammable liquids",
                hazard_category="Category 3",
                signal_word="Warning",
                pictograms="GHS02",
                hazard_statements="Flammable liquid and vapour",
                precautionary_statements=(
                    "Keep away from heat, hot surfaces, sparks, "
                    "open flames and other ignition sources. No smoking."
                ),
            )

        return None