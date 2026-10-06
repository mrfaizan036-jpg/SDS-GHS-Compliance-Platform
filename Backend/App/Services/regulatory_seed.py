from sqlalchemy.orm import Session

from App.Models.regulatory import RegulatoryReferenceModel


REGULATORY_REFERENCES = [
    {
        "jurisdiction": "International",
        "regulation_name": "UN GHS",
        "regulation_version": "Rev.11 (2025)",
        "hazard_class": "Flammable liquids",
        "hazard_category": None,
        "signal_word": None,
        "pictograms": None,
        "hazard_statements": None,
        "precautionary_statements": None,
        "source": "UNECE",
    },
]


def seed_regulatory_references(db: Session):
    for reference in REGULATORY_REFERENCES:

        existing = (
            db.query(RegulatoryReferenceModel)
            .filter(
                RegulatoryReferenceModel.regulation_name
                == reference["regulation_name"],
                RegulatoryReferenceModel.regulation_version
                == reference["regulation_version"],
                RegulatoryReferenceModel.hazard_class
                == reference["hazard_class"],
            )
            .first()
        )

        if existing is None:
            db.add(
                RegulatoryReferenceModel(
                    **reference
                )
            )

    db.commit()