"""
Sentencias v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from plataforma_web.v1.autoridades.crud import get_autoridad
from plataforma_web.v1.materias_tipos_juicios.crud import get_materia_tipo_juicio
from plataforma_web.v1.sentencias.models import Sentencia


def get_sentencias(
    db: Session,
    autoridad_id: int = None,
    materia_tipo_juicio_id: int = None,
) -> Any:
    """Consultar los sentencias activos"""
    consulta = db.query(Sentencia)
    if autoridad_id:
        autoridad = get_autoridad(db, autoridad_id)
        consulta = consulta.filter(Sentencia.autoridad == autoridad)
    if materia_tipo_juicio_id:
        materia_tipo_juicio = get_materia_tipo_juicio(db, materia_tipo_juicio_id)
        consulta = consulta.filter(Sentencia.materia_tipo_juicio == materia_tipo_juicio)
    return consulta.filter_by(estatus="A").order_by(Sentencia.fecha.desc())


def get_sentencia(db: Session, sentencia_id: int) -> Sentencia:
    """Consultar un sentencia por su id"""
    sentencia = db.query(Sentencia).get(sentencia_id)
    if sentencia is None:
        raise IndexError("No existe esa sentencia")
    if sentencia.estatus != "A":
        raise IndexError("No es activa esa sentencia, está eliminada")
    return sentencia
