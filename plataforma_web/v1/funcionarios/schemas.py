"""
Funcionarios v1, esquemas de pydantic
"""
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

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
