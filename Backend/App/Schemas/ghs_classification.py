from pydantic import BaseModel, Field


class GHSClassificationRequest(BaseModel):
    flash_point: float | None = Field(
        default=None,
        description="Flash point in degrees Celsius",
    )

    boiling_point: float | None = Field(
        default=None,
        description="Boiling point in degrees Celsius",
    )

    jurisdiction: str | None = Field(
        default=None,
        description="Jurisdiction for regulatory rule matching",
    )


class RegulatoryTraceability(BaseModel):
    status: str = Field(
        description=(
            "Indicates whether matching regulatory records were found "
            "and whether any are marked validated."
        )
    )

    matched_rule_count: int = 0

    validated_rule_count: int = 0

    rule_codes: list[str] = Field(default_factory=list)

    regulation_names: list[str] = Field(default_factory=list)

    regulation_versions: list[str] = Field(default_factory=list)

    jurisdictions: list[str] = Field(default_factory=list)

    sources: list[str] = Field(default_factory=list)

    message: str


class GHSClassificationResult(BaseModel):
    classified: bool

    chemical_id: int | None = None

    chemical_name: str | None = None

    hazard_class: str | None = None

    hazard_category: str | None = None

    signal_word: str | None = None

    pictograms: str | None = None

    hazard_statements: str | None = None

    precautionary_statements: str | None = None

    classification_status: str = "prototype_unverified"

    regulatory_traceability: RegulatoryTraceability | None = None