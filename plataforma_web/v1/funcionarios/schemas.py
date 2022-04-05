"""
Funcionarios v1, esquemas de pydantic
"""
from datetime import date
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
    en_soportes: bool
    telefono: Optional[str] = ""
    extension: Optional[str] = ""
    domicilio_oficial: Optional[str] = ""
    ingreso_fecha: Optional[date]
    puesto_clave: Optional[str] = ""
    fotografia_url: Optional[str] = ""

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
