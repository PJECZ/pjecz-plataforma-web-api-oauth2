"""
Domicilios v1, esquemas de pydantic
"""
from pydantic import BaseModel


class DomicilioOut(BaseModel):
    """Esquema para entregar domicilios"""

    id: int
    estado: str
    municipio: str
    calle: str
    num_ext: str
    num_int: str
    colonia: str
    cp: int
    completo: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
