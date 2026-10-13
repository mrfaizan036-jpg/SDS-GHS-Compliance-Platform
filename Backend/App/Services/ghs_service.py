from sqlalchemy.orm import Session

from App.Models.chemical import ChemicalModel
from App.Models.ghs import GHSClassificationModel
from App.Services.ghs_classification_service import (
    GHSClassificationService,
)
from App.Schemas.ghs import GHSClassification


def create_ghs_classification(
    db: Session,
    classification: GHSClassification,
):
    chemical = (
        db.query(ChemicalModel)
        .filter(
            ChemicalModel.id == classification.chemical_id
        )
        .first()
    )

    if chemical is None:
        return None

    db_classification = GHSClassificationModel(
        chemical_id=classification.chemical_id,
        hazard_class=classification.hazard_class,
        hazard_category=classification.hazard_category,
        signal_word=classification.signal_word,
        pictograms=classification.pictograms,
        hazard_statements=classification.hazard_statements,
        precautionary_statements=(
            classification.precautionary_statements
        ),
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


def get_classifications_for_chemical(
    db: Session,
    chemical_id: int,
):
    chemical = (
        db.query(ChemicalModel)
        .filter(
            ChemicalModel.id == chemical_id
        )
        .first()
    )

    if chemical is None:
        return None

    return (
        db.query(GHSClassificationModel)
        .filter(
            GHSClassificationModel.chemical_id == chemical_id
        )
        .all()
    )


def save_generated_classification(
    db: Session,
    chemical_id: int,
):
    classification_service = GHSClassificationService()

    result = classification_service.classify_chemical(
        db,
        chemical_id,
    )

    if result is None:
        return None

    chemical, classification = result

    if classification is None:
        return {
            "chemical": chemical,
            "classification": None,
        }

    db_classification = GHSClassificationModel(
        chemical_id=chemical.id,
        hazard_class=classification.hazard_class,
        hazard_category=classification.hazard_category,
        signal_word=classification.signal_word,
        pictograms=classification.pictograms,
        hazard_statements=classification.hazard_statements,
        precautionary_statements=(
            classification.precautionary_statements
        ),
    )

    db.add(db_classification)
    db.commit()
    db.refresh(db_classification)

    return {
        "chemical": chemical,
        "classification": db_classification,
    }


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