from sqlalchemy.orm import Session

from App.Models.ghs import GHSClassificationModel
from App.Schemas.ghs import GHSClassification


def create_ghs_classification(
    db: Session,
    classification: GHSClassification,
):
    db_classification = GHSClassificationModel(
        chemical_id=classification.chemical_id,
        hazard_class=classification.hazard_class,
        hazard_category=classification.hazard_category,
        signal_word=classification.signal_word,
        pictograms=classification.pictograms,
        hazard_statements=classification.hazard_statements,
        precautionary_statements=classification.precautionary_statements,
    )

    db.add(db_classification)
    db.commit()
    db.refresh(db_classification)

    return db_classification


def get_ghs_classification(
    db: Session,
    classification_id: int,
):
    return (
        db.query(GHSClassificationModel)
        .filter(
            GHSClassificationModel.id == classification_id
        )
        .first()
    )


def list_ghs_classifications(
    db: Session,
):
    return db.query(GHSClassificationModel).all()


def delete_ghs_classification(
    db: Session,
    classification_id: int,
):
    db_classification = get_ghs_classification(
        db,
        classification_id,
    )

    if db_classification is None:
        return None

    db.delete(db_classification)
    db.commit()

    return db_classification