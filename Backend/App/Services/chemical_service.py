from sqlalchemy.orm import Session

from App.Models.chemical import ChemicalModel
from App.Schemas.chemical import Chemical


def create_chemical(db: Session, chemical: Chemical):
    db_chemical = ChemicalModel(
        name=chemical.name,
        cas_number=chemical.cas_number,
        molecular_formula=chemical.molecular_formula,
        molecular_weight=chemical.molecular_weight,
    )

    db.add(db_chemical)
    db.commit()
    db.refresh(db_chemical)

    return db_chemical


def get_chemical(db: Session, chemical_id: int):
    return (
        db.query(ChemicalModel)
        .filter(ChemicalModel.id == chemical_id)
        .first()
    )


def list_chemicals(db: Session):
    return db.query(ChemicalModel).all()


def update_chemical(
    db: Session,
    chemical_id: int,
    chemical: Chemical,
):
    db_chemical = get_chemical(db, chemical_id)

    if db_chemical is None:
        return None

    db_chemical.name = chemical.name
    db_chemical.cas_number = chemical.cas_number
    db_chemical.molecular_formula = chemical.molecular_formula
    db_chemical.molecular_weight = chemical.molecular_weight

    db.commit()
    db.refresh(db_chemical)

    return db_chemical


def delete_chemical(db: Session, chemical_id: int):
    db_chemical = get_chemical(db, chemical_id)

    if db_chemical is None:
        return None

    db.delete(db_chemical)
    db.commit()

    return db_chemical


def service_health(db: Session):
    chemical_count = db.query(ChemicalModel).count()

    return {
        "service": "chemical_service",
        "status": "operational",
        "chemical_count": chemical_count,
    }