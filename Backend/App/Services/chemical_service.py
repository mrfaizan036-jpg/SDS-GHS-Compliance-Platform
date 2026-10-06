from uuid import uuid4

from App.Schemas.chemical import Chemical


chemicals_db = {}


def create_chemical(chemical: Chemical):
    chemical_id = str(uuid4())

    chemicals_db[chemical_id] = chemical

    return chemical_id, chemical


def get_chemical(chemical_id: str):
    return chemicals_db.get(chemical_id)


def list_chemicals():
    return [
        {
            "chemical_id": chemical_id,
            "chemical": chemical,
        }
        for chemical_id, chemical in chemicals_db.items()
    ]


def update_chemical(chemical_id: str, chemical: Chemical):
    chemicals_db[chemical_id] = chemical

    return chemical


def delete_chemical(chemical_id: str):
    return chemicals_db.pop(chemical_id)

def service_health():
    return {
        "service": "chemical_service",
        "status": "operational",
        "chemical_count": len(chemicals_db),
    }