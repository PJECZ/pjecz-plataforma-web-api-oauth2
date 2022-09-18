"""
Sentencias v1, esquemas de pydantic
"""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class SentenciaOut(BaseModel):
    """Esquema para entregar sentencia"""

    id: int
    distrito_id: int
    distrito_nombre: str
    distrito_nombre_corto: str
    autoridad_id: int
    autoridad_descripcion: str
    autoridad_descripcion_corta: str
    autoridad_clave: str
    materia_id: int
    materia_nombre: str
    materia_tipo_juicio_id: int
    materia_tipo_juicio_descripcion: str
    sentencia: str
    sentencia_fecha: date
    expediente: str
    fecha: date
    descripcion: str
    es_perspectiva_genero: bool
    archivo: Optional[str] = ""
    url: Optional[str] = ""
    creado: datetime

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneSentenciaOut(SentenciaOut, OneBaseOut):
    """Esquema para entregar una sentencia"""
