"""
REPSVM Agresores v2, esquemas de pydantic
"""
from pydantic import BaseModel


class REPSVMAgresorOut(BaseModel):
    """Esquema para entregar agresores"""

    id: int
    distrito_id: int
    distrito_nombre: str
    distrito_nombre_corto: str
    consecutivo: int
    delito_generico: str
    delito_especifico: str
    nombre: str
    numero_causa: str
    pena_impuesta: str
    observaciones: str
    sentencia_url: str
    tipo_juzgado: str
    tipo_sentencia: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
