"""
Materias Tipos Juicios v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from plataforma_web.v1.materias.crud import get_materia
from plataforma_web.v1.materias_tipos_juicios.models import MateriaTipoJuicio


def get_materias_tipos_juicios(db: Session, materia_id: int) -> Any:
    """Consultar los tipos de juicios activos de una materia"""
    materia = get_materia(db, materia_id)
    consulta = db.query(MateriaTipoJuicio).filter(MateriaTipoJuicio.materia == materia)
    return consulta.filter_by(estatus="A").order_by(MateriaTipoJuicio.id.desc())


def get_materia_tipo_juicio(db: Session, materia_tipo_juicio_id: int) -> MateriaTipoJuicio:
    """Consultar un tipo de juicio por su id"""
    materia_tipo_juicio = db.query(MateriaTipoJuicio).get(materia_tipo_juicio_id)
    if materia_tipo_juicio is None:
        raise IndexError("No existe ese tipo de juicio")
    if materia_tipo_juicio.estatus != "A":
        raise ValueError("No es activa ese tipo de juicio, está eliminado")
    return materia_tipo_juicio
