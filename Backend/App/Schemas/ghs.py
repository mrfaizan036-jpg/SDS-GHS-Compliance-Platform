from pydantic import BaseModel, Field


class GHSClassification(BaseModel):
    chemical_id: int = Field(
        ...,
        gt=0,
        description="ID of the chemical"
    )

    hazard_class: str = Field(
        ...,
        min_length=1,
        description="GHS hazard class"
    )

    hazard_category: str | None = Field(
        default=None,
        description="GHS hazard category"
    )

    signal_word: str | None = Field(
        default=None,
        description="GHS signal word"
    )

    pictograms: str | None = Field(
        default=None,
        description="GHS pictograms"
    )

    hazard_statements: str | None = Field(
        default=None,
        description="GHS hazard statements"
    )

    precautionary_statements: str | None = Field(
        default=None,
        description="GHS precautionary statements"
    )


class GHSClassificationResponse(BaseModel):
    message: str
    classification_id: str
    classification: GHSClassification