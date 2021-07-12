"""
Materias, CRUD: the four basic operations (create, read, update, and delete) of data storage
"""
from sqlalchemy.orm import Session

from plataforma_web.materias.models import Materia


def get_materias(db: Session):
    """Consultar materias activas (excepto el id 1 que es NO DEFINIDO)"""
    return db.query(Materia).filter(Materia.estatus == "A").filter(Materia.id != 1).order_by(Materia.nombre).all()


def get_materia(db: Session, materia_id: int):
    """Consultar un materia"""
    return db.query(Materia).get(materia_id)
