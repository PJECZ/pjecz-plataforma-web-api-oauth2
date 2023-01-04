"""
Ubicaciones Expedientes v1, esquemas
"""
from pydantic import BaseModel


class UbicacionExpedienteOut(BaseModel):
    """Esquema para entregar una ubicacion de expediente"""

    id: int | None
    distrito_id: int | None
    distrito_nombre: str | None
    distrito_nombre_corto: str | None
    autoridad_id: int | None
    autoridad_descripcion: str | None
    autoridad_descripcion_corta: str | None
    autoridad_clave: str | None
    expediente: str
    ubicacion: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
