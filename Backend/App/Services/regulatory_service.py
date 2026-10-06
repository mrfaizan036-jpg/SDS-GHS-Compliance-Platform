from sqlalchemy.orm import Session

from App.Models.regulatory import RegulatoryReferenceModel
from App.Schemas.regulatory import RegulatoryReference


def create_regulatory_reference(
    db: Session,
    reference: RegulatoryReference,
):
    db_reference = RegulatoryReferenceModel(
        jurisdiction=reference.jurisdiction,
        regulation_name=reference.regulation_name,
        regulation_version=reference.regulation_version,
        hazard_class=reference.hazard_class,
        hazard_category=reference.hazard_category,
        signal_word=reference.signal_word,
        pictograms=reference.pictograms,
        hazard_statements=reference.hazard_statements,
        precautionary_statements=reference.precautionary_statements,
        source=reference.source,
    )

    db.add(db_reference)
    db.commit()
    db.refresh(db_reference)

    return db_reference


def get_regulatory_reference(
    db: Session,
    reference_id: int,
):
    return (
        db.query(RegulatoryReferenceModel)
        .filter(
            RegulatoryReferenceModel.id == reference_id
        )
        .first()
    )


def list_regulatory_references(
    db: Session,
):
    return db.query(RegulatoryReferenceModel).all()


def delete_regulatory_reference(
    db: Session,
    reference_id: int,
):
    db_reference = get_regulatory_reference(
        db,
        reference_id,
    )

    if db_reference is None:
        return None

    db.delete(db_reference)
    db.commit()

    return db_reference