"""
Departamentos v1.0, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from plataforma_web.v1.departamentos.models import Departamento


def get_departamentos(db: Session) -> Any:
    """Consultar los departamentos activos"""
    return db.query(Departamento).filter_by(estatus="A").order_by(Departamento.nombre)


def get_departamento(db: Session, departamento_id: int) -> Departamento:
    """Consultar un departamento por su id"""
    departamento = db.query(Departamento).get(departamento_id)
    if departamento is None:
        raise IndexError("No existe ese departamento")
    if departamento.estatus != "A":
        raise ValueError("No es activo el departamento, está eliminado")
    return departamento
