"""
REPSVM Delitos v1, esquemas de pydantic
"""
from pydantic import BaseModel


class REPSVMDelitoOut(BaseModel):
    """Esquema para entregar delitos"""

    id: int
    nombre: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
