from pydantic import BaseModel, Field, field_validator


class Chemical(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        description="Chemical name"
    )

    cas_number: str | None = Field(
        default=None,
        description="CAS Registry Number"
    )

    molecular_formula: str | None = Field(
        default=None,
        description="Molecular formula"
    )

    molecular_weight: float | None = Field(
        default=None,
        gt=0,
        description="Molecular weight in g/mol"
    )

    hazard_class: str | None = Field(
        default=None,
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

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Chemical name cannot be empty")

        return value


class ChemicalResponse(BaseModel):
    message: str
    chemical_id: str
    chemical: Chemical


class ChemicalListItem(BaseModel):
    chemical_id: str
    chemical: Chemical


class ChemicalListResponse(BaseModel):
    count: int
    chemicals: list[ChemicalListItem]