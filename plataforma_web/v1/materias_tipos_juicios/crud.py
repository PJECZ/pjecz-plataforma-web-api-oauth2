"""
Materias Tipos Juicios v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError

from ...core.materias_tipos_juicios.models import MateriaTipoJuicio
from ..materias.crud import get_materia


def get_materias_tipos_juicios(
    db: Session,
    estatus: str = None,
    materia_id: int = None,
) -> Any:
    """Consultar los tipos de juicios de una materia"""

    # Consultar
    consulta = db.query(MateriaTipoJuicio)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Filtrar por materia
    if materia_id is not None:
        materia = get_materia(db, materia_id)
        consulta = consulta.filter(MateriaTipoJuicio.materia == materia)

    # Entregar
    return consulta.order_by(MateriaTipoJuicio.descripcion)


def get_materia_tipo_juicio(
    db: Session,
    materia_tipo_juicio_id: int,
) -> MateriaTipoJuicio:
    """Consultar un tipo de juicio por su id"""
    materia_tipo_juicio = db.query(MateriaTipoJuicio).get(materia_tipo_juicio_id)
    if materia_tipo_juicio is None:
        raise PWNotExistsError("No existe ese tipo de juicio")
    if materia_tipo_juicio.estatus != "A":
        raise PWIsDeletedError("No es activa ese tipo de juicio, está eliminado")
    return materia_tipo_juicio
