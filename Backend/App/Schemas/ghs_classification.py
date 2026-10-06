from pydantic import BaseModel, Field


class GHSClassificationRequest(BaseModel):
    flash_point: float | None = Field(
        default=None,
        description="Flash point in degrees Celsius"
    )

    boiling_point: float | None = Field(
        default=None,
        description="Boiling point in degrees Celsius"
    )


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