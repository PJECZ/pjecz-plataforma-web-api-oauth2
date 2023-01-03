"""
REPSVM Agresores-Delitos v1, esquemas
"""
from pydantic import BaseModel


class REPSVMAgresorDelitoOut(BaseModel):
    """Esquema para entregar agresores-delitos"""

    id: int
    repsvm_agresor_id: int
    repsvm_agresor_nombre: str
    repsvm_delito_id: int
    repsvm_delito_nombre: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
