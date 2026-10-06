from pydantic import BaseModel, Field


class RegulatoryReference(BaseModel):
    jurisdiction: str = Field(
        ...,
        min_length=1,
        description="Regulatory jurisdiction"
    )

    regulation_name: str = Field(
        ...,
        min_length=1,
        description="Name of regulation or standard"
    )

    regulation_version: str = Field(
        ...,
        min_length=1,
        description="Version of the regulation or standard"
    )

    hazard_class: str = Field(
        ...,
        min_length=1,
        description="Hazard class"
    )

    hazard_category: str | None = Field(
        default=None,
        description="Hazard category"
    )

    signal_word: str | None = Field(
        default=None,
        description="Signal word"
    )

    pictograms: str | None = Field(
        default=None,
        description="GHS pictograms"
    )

    hazard_statements: str | None = Field(
        default=None,
        description="Hazard statements"
    )

    precautionary_statements: str | None = Field(
        default=None,
        description="Precautionary statements"
    )

    source: str = Field(
        ...,
        min_length=1,
        description="Authoritative regulatory source"
    )


class RegulatoryReferenceResponse(BaseModel):
    message: str
    reference_id: str
    reference: RegulatoryReference