"""
Distritos, esquemas de pydantic
"""
from pydantic import BaseModel


class Distrito(BaseModel):
    """Esquema para distritos"""

    id: int
    distrito: str
    distrito_corto: str
