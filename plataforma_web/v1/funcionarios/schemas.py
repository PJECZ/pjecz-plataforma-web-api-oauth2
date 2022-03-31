"""
Funcionarios v1, esquemas de pydantic
"""
from typing import Optional
from pydantic import BaseModel


class FuncionarioOut(BaseModel):
    """Esquema para entregar funcionario"""

    id: int
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    curp: str
    email: str
    puesto: str
    en_funciones: bool
    en_sentencias: bool
    en_soportes: bool
    en_tesis_jurisprudencias: bool
    telefono: Optional[str]
    extension: Optional[str]

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
