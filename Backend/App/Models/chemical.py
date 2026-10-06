from sqlalchemy import Column, Float, Integer, String

from App.Database.database import Base


class ChemicalModel(Base):
    __tablename__ = "chemicals"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String,
        nullable=False,
    )

    cas_number = Column(
        String,
        nullable=True,
        index=True,
    )

    molecular_formula = Column(
        String,
        nullable=True,
    )

    molecular_weight = Column(
        Float,
        nullable=True,
    )

    hazard_class = Column(
        String,
        nullable=True,
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
        String,
        nullable=True,
    )

    precautionary_statements = Column(
        String,
        nullable=True,
    )
    
    flash_point = Column(
        Float,
        nullable=True,
    )

    boiling_point = Column(
        Float,
        nullable=True,
    )