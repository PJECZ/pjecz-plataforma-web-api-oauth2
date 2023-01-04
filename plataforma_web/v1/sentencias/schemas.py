"""
Sentencias v1, esquemas
"""
from datetime import date, datetime
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class SentenciaOut(BaseModel):
    """Esquema para entregar sentencia"""

    id: int | None
    distrito_id: int | None
    distrito_nombre: str | None
    distrito_nombre_corto: str | None
    autoridad_id: int | None
    autoridad_descripcion: str | None
    autoridad_descripcion_corta: str | None
    autoridad_clave: str | None
    materia_id: int | None
    materia_nombre: str | None
    materia_tipo_juicio_id: int | None
    materia_tipo_juicio_descripcion: str | None
    sentencia: str | None
    sentencia_fecha: date | None
    expediente: str | None
    fecha: date | None
    descripcion: str | None
    es_perspectiva_genero: bool | None
    archivo: str | None
    url: str | None
    creado: datetime | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneSentenciaOut(SentenciaOut, OneBaseOut):
    """Esquema para entregar una sentencia"""
