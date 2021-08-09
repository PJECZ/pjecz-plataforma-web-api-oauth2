"""
Roles v1.0, esquemas
"""
from pydantic import BaseModel


class RolOut(BaseModel):
    """Esquema para entregar rol"""

    id: int
    nombre: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
