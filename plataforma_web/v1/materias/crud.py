"""
Materias v1.0, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from plataforma_web.v1.materias.models import Materia


def get_materias(db: Session) -> Any:
    """Consultar las materias activas (excepto el id 1 que es NO DEFINIDO)"""
    return db.query(Materia).filter_by(estatus="A").filter(Materia.id != 1).order_by(Materia.nombre.asc())


def get_materia(db: Session, materia_id: int) -> Materia:
    """Consultar un materia por su id"""
    materia = db.query(Materia).get(materia_id)
    if materia is None:
        raise IndexError("No existe esa materia")
    if materia.estatus != "A":
        raise ValueError("No es activa la materia, está eliminada")
    return materia
