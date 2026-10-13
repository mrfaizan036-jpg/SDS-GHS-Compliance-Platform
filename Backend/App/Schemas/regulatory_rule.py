from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


ValidationStatus = Literal[
    "draft",
    "under_review",
    "validated",
    "deprecated",
]


class RegulatoryRuleBase(BaseModel):
    rule_code: str = Field(min_length=1, max_length=100)

    jurisdiction: str = Field(min_length=1, max_length=100)

    regulation_name: str = Field(min_length=1, max_length=255)

    regulation_version: str = Field(min_length=1, max_length=100)

    hazard_class: str = Field(min_length=1, max_length=255)

    hazard_category: str | None = None

    criteria_summary: str = Field(min_length=1)

    source: str = Field(min_length=1, max_length=500)

    source_url: HttpUrl | None = None

    validation_status: ValidationStatus = "draft"

    reviewed_by: str | None = None

    reviewed_at: datetime | None = None

    effective_date: date | None = None

    reference_id: int | None = Field(default=None, gt=0)


class RegulatoryRuleCreate(RegulatoryRuleBase):
    pass


class RegulatoryRuleResponse(RegulatoryRuleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)