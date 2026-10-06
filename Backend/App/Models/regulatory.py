from sqlalchemy import Column, Integer, String, Text

from App.Database.database import Base


class RegulatoryReferenceModel(Base):
    __tablename__ = "regulatory_references"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    jurisdiction = Column(
        String,
        nullable=False,
        index=True,
    )

    regulation_name = Column(
        String,
        nullable=False,
    )

    regulation_version = Column(
        String,
        nullable=False,
    )

    hazard_class = Column(
        String,
        nullable=False,
        index=True,
    )

    hazard_category = Column(
        String,
        nullable=True,
    )

    signal_word = Column(
        String,
        nullable=True,
    )

    pictograms = Column(
        String,
        nullable=True,
    )

    hazard_statements = Column(
        Text,
        nullable=True,
    )

    precautionary_statements = Column(
        Text,
        nullable=True,
    )

    source = Column(
        String,
        nullable=False,
    )