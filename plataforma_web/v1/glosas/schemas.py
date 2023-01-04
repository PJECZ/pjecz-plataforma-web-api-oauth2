"""
Glosas v1, esquemas
"""
from datetime import date
from pydantic import BaseModel


class GlosaOut(BaseModel):
    """Esquema para entregar glosas"""

    id: int
    distrito_id: int | None
    distrito_nombre: str | None
    distrito_nombre_corto: str | None
    autoridad_id: int | None
    autoridad_descripcion: str | None
    autoridad_descripcion_corta: str | None
    autoridad_clave: str | None
    fecha: date
    tipo_juicio: str
    descripcion: str
    expediente: str
    archivo: str | None
    url: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
