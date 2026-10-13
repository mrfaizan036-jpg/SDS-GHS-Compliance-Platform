from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.sql import func

from App.Database.database import Base


class RegulatoryRuleModel(Base):
    __tablename__ = "regulatory_rules"

    id = Column(Integer, primary_key=True, index=True)

    rule_code = Column(String, unique=True, nullable=False, index=True)

    jurisdiction = Column(String, nullable=False, index=True)

    regulation_name = Column(String, nullable=False)

    regulation_version = Column(String, nullable=False)

    hazard_class = Column(String, nullable=False, index=True)

    hazard_category = Column(String, nullable=True)

    criteria_summary = Column(Text, nullable=False)

    source = Column(String, nullable=False)

    source_url = Column(String, nullable=True)

    validation_status = Column(
        String,
        nullable=False,
        default="draft",
        index=True,
    )

    reviewed_by = Column(String, nullable=True)

    reviewed_at = Column(DateTime(timezone=True), nullable=True)

    effective_date = Column(Date, nullable=True)

    reference_id = Column(
        Integer,
        ForeignKey("regulatory_references.id"),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )