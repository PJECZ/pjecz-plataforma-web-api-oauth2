"""
Soportes Tickets v1, esquemas de pydantic
"""
from datetime import datetime
from pydantic import BaseModel


class SoporteTicketOut(BaseModel):
    """Esquema para entregar soporte ticket"""

    id: int
    funcionario_id: int
    funcionario_nombre: str
    soporte_categoria_id: int
    soporte_categoria_nombre: str
    usuario_id: int
    usuario_email: str
    usuario_nombre: str
    usuario_oficina_id: int
    usuario_oficina_clave: str
    descripcion: str
    estado: str
    soluciones: str
    creado: datetime

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
