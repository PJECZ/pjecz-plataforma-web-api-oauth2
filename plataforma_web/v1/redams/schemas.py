"""
REDAM (Registro Estatal de Deudores Alimentarios) v1, esquemas de pydantic
"""
from datetime import date
from pydantic import BaseModel


class RedamOut(BaseModel):
    """Esquema para entregar deudores"""

    id: int
    distrito_id: int
    distrito_nombre: str
    distrito_nombre_corto: str
    autoridad_descripcion: str
    autoridad_descripcion_corta: str
    autoridad_clave: str
    nombre: str
    expediente: str
    fecha: date
    observaciones: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
