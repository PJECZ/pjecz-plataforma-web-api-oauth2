"""
Soportes Tickets v1, esquemas de pydantic
"""
from pydantic import BaseModel


class SoporteTicketOut(BaseModel):
    """Esquema para entregar Soporte Ticket"""

    id: int
    soporte_categoria_id: int
    soporte_categoria_nombre: str
    usuario_id: int
    usuario_nombre: str
    descripcion: str
    estado: str
    resolucion: str
    soluciones: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
