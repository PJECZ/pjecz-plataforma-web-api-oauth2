"""
Materias Tipos Juicios v1, esquemas de pydantic
"""
from pydantic import BaseModel


class MateriaTipoJuicioOut(BaseModel):
    """Esquema para entregar tipo de juicio"""

    id: int
    descripcion: str
    materia_id: int
    materia_nombre: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
