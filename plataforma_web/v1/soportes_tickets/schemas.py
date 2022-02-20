"""
Soportes Tickets v1, esquemas de pydantic
"""
from datetime import datetime
from pydantic import BaseModel


class SoporteTicketOut(BaseModel):
    """Esquema para entregar soporte ticket"""

    id: int
    soporte_categoria_id: int
    soporte_categoria_nombre: str
    usuario_id: int
    usuario_nombre: str
    descripcion: str
    estado: str
    soluciones: str
    creado: datetime

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
