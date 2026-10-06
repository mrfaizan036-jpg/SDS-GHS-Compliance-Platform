from sqlalchemy import Column, Float, Integer, String

from App.Database.database import Base


class ChemicalModel(Base):
    __tablename__ = "chemicals"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

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