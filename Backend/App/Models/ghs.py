from sqlalchemy import Column, Integer, String

from App.Database.database import Base


class GHSClassificationModel(Base):
    __tablename__ = "ghs_classifications"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    chemical_id = Column(
        Integer,
        nullable=False,
        index=True,
    )

    hazard_class = Column(
        String,
        nullable=False,
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