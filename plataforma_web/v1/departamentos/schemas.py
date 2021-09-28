"""
Departamentos v1.0, esquemas
"""
from pydantic import BaseModel


class DepartamentoOut(BaseModel):
    """Esquema para entregar departamento"""

    id: int
    nombre: str
    nombre_corto: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
